import time
import csv
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
        self.onManageSpecialBackFillKrebOnSecurity()
        self.onManageSpecialBackFillAvast()
        self.onManageSpecialBackFillPaloAltoUnit42()

    def _processHTML(self, htmlSource, elementDelimiter, subElementURL, subElementTitle, subElementDateReport):
        soup = BeautifulSoup(htmlSource, 'html.parser')
        summaries = soup.find_all(elementDelimiter)

        # Parse the result
        # URL, elementDelimiter, subElementURL, subElementTitle, subElementDateReport
        for summary in summaries:
            strWholeArticleHTML = str(summary)
            #for item in summary.contents:
                #strWholeArticleHTML = strWholeArticleHTML + str(item)

            strWholeArticleHTML = strWholeArticleHTML.replace("\n", "")
            strWholeArticleHTML = strWholeArticleHTML.replace("\t", "")

            try:
                dom = etree.XML("<root>" + strWholeArticleHTML + "</root>")
                #dom = etree.XML("<root>" + str(summary) + "</root>")

                report = BG_Report()
                report.setClassification("UNCLASSIFIED")
                report.setURL(dom.xpath('//' + subElementURL + '/@href')[0])
                report.setTitle(dom.xpath('//' + subElementTitle)[0].text)
                report.setDate(dom.xpath('//article/' + subElementDateReport)[0].text)
            except Exception as err:
                print("Something wrong happen parsing this report: " + str(err) + ", ignoring")
                continue

            if self.repoReport.exist(report):
                print(".", end="")
                continue

            print("Adding article : " + report.getTitle() + ". date: " + report.getDate())
            self.repoReport.save(report)


    def _processDataSource(self, urlDataSource, elementDelimiter, subElementURL, subElementTitle, subElementDateReport):
        # Perform the requests
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
        response = requests.get(urlDataSource, headers=headers)

        # Lets test what headers are sent by sending a request to HTTPBin

        if (response.status_code != 200):
            print(urlDataSource + " is does not works; ignoring this source")
            return

        self._processHTML(response.text, elementDelimiter, subElementURL, subElementTitle, subElementDateReport)


    def onManageSpecialBackFillPaloAltoUnit42(self):
        with open('./data/Unit42_BackFill.html', newline='') as file:
            lines = file.readlines()
            text = "".join(lines)

            self._processHTML(text, "article", "div[2]/h3/a", "div[2]/h3/a", "div[2]/ul/li[2]/time")


    def onManageSpecialBackFillAvast(self):
        # Special backfil krebsonsecurity.com/page/[2-213]
        for i in range(2, 8):
            # https://decoded.avast.io/page/2/,article,div[2]/div[1]/h2/a,div[2]/div[1]/h2/a,div[2]/div[1]/div[2]/span[2]/span
            try:
                self._processDataSource("https://decoded.avast.io/page/" + str(i) + "/", "article", "div[2]/div[1]/h2/a", "div[2]/div[1]/h2/a", "div[2]/div[1]/div[2]/span[2]/span")
            except Exception as err:
                print("Something went wrong with " + str(err) + ", ignoring this report")
                continue


    def onManageSpecialBackFillKrebOnSecurity(self):
        # Special backfil krebsonsecurity.com/page/[2-213]
        for i in range(2, 213):
            # https://krebsonsecurity.com/page/2/,article,header/h2/a,header/h2/a,header/div[2]/div/div[1]/span
            try:
                self._processDataSource("https://krebsonsecurity.com/page/" + str(i) + "/", "article", "header/h2/a", "header/h2/a", "header/div[2]/div/div[1]/span")
            except Exception as err:
                print("Something went wrong with " + str(err) + ", ignoring this report")
                continue

    def onManageNormal(self):
        with open('./data/datasources.csv', newline='') as csvfile:
            dataSources = csv.reader(csvfile, delimiter=',', quotechar='"')

            for row in dataSources:
                #Get the datasource from the csv
                urlDataSource = row[0]
                elementDelimiter = row[1]
                subElementURL = row[2]
                subElementTitle = row[3]
                subElementDateReport = row[4]
                self._processDataSource(row[0], row[1], row[2], row[3], row[4])


        time.sleep(1*60*60) #every 1 hours
        #time.sleep(10)

    def onManage(self):
        #self.onManageSpecialBackFillKrebOnSecurity()
        #self.onManageSpecialBackFillAvast()
        #self.onManageSpecialBackFillPaloAltoUnit42()
        self.onManageNormal()
