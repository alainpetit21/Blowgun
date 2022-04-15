from bs4 import BeautifulSoup
from lxml import etree
from src.CCC.Thread import Thread
import datefinder as datefinder
import time
import csv
import re
import requests


from src.Repository.BG_Report_Repository import BG_Report_Repository
from src.Model.BG_Report import BG_Report


# ======================================================================================================================
class AppBG_ScrapeDeamon(Thread):
    def __init__(self):
        super().__init__("AppBG_ScrapeDeamon")
        self.repoReport = BG_Report_Repository()

    def load(self):
        pass

    def _processSpecificPatches(self, strHTML) -> str:
        strHTML = strHTML.replace("\n", "")
        strHTML = strHTML.replace("\t", "")
        strHTML = strHTML.replace('a "="" href', "a href")
        strHTML = strHTML.replace('<i class="icon-font icon-calendar"></i>', "") # Pathc for hackernews to remove specialcase of calender in index [0] for dates
        strHTML = strHTML.replace('<div id="detect_page_2"></div>', "") # Patch for darkreading to remove specialcase of being unable to read 50 % of the article

        return strHTML

    def _processDOMFindURL(self, dom, strRootWebsite, subElementURL) -> str:
        strURL = dom.xpath('//' + subElementURL + '/@href')[0]

        if not strURL[:4] == "http":
            return strRootWebsite + strURL[1:]
        else:
            return strURL

    def _processDOMFindTitle(self, dom, subElementTitle) -> str:
        strTitle = dom.xpath('//' + subElementTitle)[0].text
        strTitle = strTitle.replace('"', '')

        return strTitle

    def _processDOMFindDate(self, dom, report, elementDelimiter, subElementDateReport) -> str:
        strDate = ""
        domDateXPath = '//' + elementDelimiter + "/" + subElementDateReport

        try:
            strDate = dom.xpath(domDateXPath)[0].text
        except Exception as err:
            #if that doesn't work, try to read from URL.
            urlDataSource = re.findall(r"([0-9]{2,4}\/[0-9]{2}\/[0-9]{2})", report.getURL())
            matches = datefinder.find_dates(urlDataSource[0])
            for match in matches:
                strDate = match.strftime("%Y/%m/%d")
                break
            else:
                raise Exception()

        matches = datefinder.find_dates(strDate)
        for match in matches:
            return match.strftime("%Y/%m/%d")

    def _processHTML(self, htmlRoot, htmlSource, elementDelimiter, dicAttribute, subElementURL, subElementTitle, subElementDateReport):
        time.sleep(0.1)  # every 0.1 second, for some reason when it's writing too fast to stdin, it crashes
        soup = BeautifulSoup(htmlSource, 'html.parser')

        if len(dicAttribute) == 0:
            summaries = soup.findAll(elementDelimiter)
        else:
            summaries = soup.findAll(elementDelimiter, attrs=dicAttribute)

        # Parse the result
        # URL, elementDelimiter, subElementURL, subElementTitle, subElementDateReport
        for summary in summaries:
            strWholeArticleHTML = str(summary)
            strWholeArticleHTML = self._processSpecificPatches(strWholeArticleHTML)

            try:
                dom = etree.XML("<root>" + strWholeArticleHTML + "</root>")
                # dom = etree.XML("<root>" + str(summary) + "</root>")

                report = BG_Report()
                report.setClassification("UNCLASSIFIED")
                report.setURL(self._processDOMFindURL(dom, htmlRoot, subElementURL))
                report.setTitle(self._processDOMFindTitle(dom, subElementTitle))
                report.setDate(self._processDOMFindDate(dom, report, elementDelimiter, subElementDateReport))

            except Exception as err:
                # For some unknown reason, placing a breakpoint in here cause SIGSEGV during execution ... weird ...
                # This is often due to error in the actual html page. Unfortunately it is an acceptable risk to ignore.
                print("\nSomething wrong happen parsing this report: " + str(err) + ", ignoring report")
                # print("\nSomething wrong happen parsing this report: " + str(err) + ", ignoring report :" + strWholeArticleHTML + "\n" + elementDelimiter + "\n" + str(dicAttribute) + "\n" + subElementURL + "\n" + subElementTitle + "\n" + subElementDateReport)
                continue

            if self.repoReport.exists(report):
                print(".", end="")
                continue

            print("Adding article : " + report.getTitle() + ". date: " + report.getDate())
            self.repoReport.save(report)

    def _processDataSource(self, urlDataSource, elementDelimiter, dicAttribute, subElementURL, subElementTitle, subElementDateReport):
        # Perform the requests
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
        response = requests.get(urlDataSource, headers=headers)

        # Lets test what headers are sent by sending a request to HTTPBin

        if response.status_code != 200:
            print(urlDataSource + " is does not works; ignoring this source")
            return

        urlDataSource = re.findall(r"^https:..[\w+.]+.", urlDataSource)[0]

        self._processHTML(urlDataSource, response.text, elementDelimiter, dicAttribute, subElementURL, subElementTitle, subElementDateReport)

    def onManageNormal(self):
        with open('./data/datasources.csv', newline='') as csvfile:
            dataSources = csv.reader(csvfile, delimiter=',', quotechar='"')

            i = 0
            for row in dataSources:
                if i == 0:  # Skip the first header row
                    i = i + 1
                    continue

                # Get the datasource from the csv
                elementDelimiterAttribute = {}
                if not row[2] == "":
                    lstAttribute = row[2].split(sep=":")
                    elementDelimiterAttribute[lstAttribute[0]] = lstAttribute[1]

                urlDataSource = row[0]
                elementDelimiter = row[1]
                subElementURL = row[3]
                subElementTitle = row[4]
                subElementDateReport = row[5]
                self._processDataSource(urlDataSource, elementDelimiter, elementDelimiterAttribute, subElementURL, subElementTitle, subElementDateReport)
                i = i + 1

        print("\nWaiting for an hour to do another round of Horizontal search")
        time.sleep(1 * 60 * 60)  # every 1 hours
        # time.sleep(10)

    def onManage(self):
        self.onManageNormal()
