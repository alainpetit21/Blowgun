import time
import csv

import datefinder as datefinder
import requests

from bs4 import BeautifulSoup
from lxml import etree
from src.CCC.Thread import Thread

from src.Repository.BG_Report_Repository import BG_Report_Repository
from src.Model.BG_Report import BG_Report


class AppBG_ScrapeDeamon(Thread):
    def __init__(self):
        super().__init__("AppBG_ScrapeDeamon")
        self.repoReport = BG_Report_Repository()

    def load(self):
        pass

    def _processHTML(self, htmlSource, elementDelimiter, dicAttribute, subElementURL, subElementTitle,
                     subElementDateReport):
        soup = BeautifulSoup(htmlSource, 'html.parser')

        if len(dicAttribute) == 0:
            summaries = soup.findAll(elementDelimiter)
        else:
            summaries = soup.findAll(elementDelimiter, attrs=dicAttribute)

        # Parse the result
        # URL, elementDelimiter, subElementURL, subElementTitle, subElementDateReport
        for summary in summaries:
            strWholeArticleHTML = str(summary)
            # for item in summary.contents:
            # strWholeArticleHTML = strWholeArticleHTML + str(item)

            strWholeArticleHTML = strWholeArticleHTML.replace("\n", "")
            strWholeArticleHTML = strWholeArticleHTML.replace("\t", "")

            try:
                dom = etree.XML("<root>" + strWholeArticleHTML + "</root>")
                # dom = etree.XML("<root>" + str(summary) + "</root>")

                report = BG_Report()
                report.setClassification("UNCLASSIFIED")
                report.setURL(dom.xpath('//' + subElementURL + '/@href')[0])
                report.setTitle(dom.xpath('//' + subElementTitle)[0].text)
                strDate = dom.xpath('//' + elementDelimiter + "/" + subElementDateReport)[0].text
                matches = datefinder.find_dates(strDate)
                for match in matches:
                    report.setDate(match.strftime("%Y/%m/%d"))
                    break

            except Exception as err:
                print("Something wrong happen parsing this report: " + str(err) + ", ignoring")
                continue

            if self.repoReport.exist(report):
                print(".", end="")
                continue

            print("Adding article : " + report.getTitle() + ". date: " + report.getDate())
            self.repoReport.save(report)

    def _processDataSource(self, urlDataSource, elementDelimiter, dicAttribute, subElementURL, subElementTitle,
                           subElementDateReport):
        # Perform the requests
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
        response = requests.get(urlDataSource, headers=headers)

        # Lets test what headers are sent by sending a request to HTTPBin

        if response.status_code != 200:
            print(urlDataSource + " is does not works; ignoring this source")
            return

        self._processHTML(response.text, elementDelimiter, dicAttribute, subElementURL, subElementTitle, subElementDateReport)

    def onManageTest(self):
        csvText = "https://www.darkreading.com/threat-intelligence,div,class:topic-content-article,div[2]/div/div/div[1]/div[2]/a,div[2]/div/div/div[1]/div[2]/a,div[2]/div/div/div[2]/div[2]/div[2]"
        lstRow = csvText.split(sep=",")

        elementDelimiterAttribute = {}
        urlDataSource = lstRow[0]
        elementDelimiter = lstRow[1]
        lstAttribute = lstRow[2].split(sep=":")
        elementDelimiterAttribute[lstAttribute[0]] = lstAttribute[1]
        subElementURL = lstRow[3]
        subElementTitle = lstRow[4]
        subElementDateReport = lstRow[5]
        self._processDataSource(urlDataSource, elementDelimiter, elementDelimiterAttribute, subElementURL, subElementTitle, subElementDateReport)

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

        print("Waiting for an hour to do another round of Horizontal search")
        time.sleep(1 * 60 * 60)  # every 1 hours
        # time.sleep(10)

    def onManage(self):
        self.onManageNormal()
