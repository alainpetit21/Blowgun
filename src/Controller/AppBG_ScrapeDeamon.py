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
        super().__init__("AppPythonCryptoFinanceUpdater")
        self.repoReport = BG_Report_Repository()


    def load(self):
        pass

    def ProcessDataSource(self, urlDataSource, elementDelimiter, subElementURL, subElementTitle, subElementDateReport):
        # Perform the requests
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
        response = requests.get(urlDataSource, headers=headers)

        # Lets test what headers are sent by sending a request to HTTPBin

        if (response.status_code != 200):
            print(urlDataSource + " is does not works; ignoring this source")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        summaries = soup.find_all(elementDelimiter)

        # Parse the result
        # URL, elementDelimiter, subElementURL, subElementTitle, subElementDateReport
        for summary in summaries:
            strWholeArticleHTML = ""
            for item in summary.contents:
                strWholeArticleHTML = strWholeArticleHTML + str(item)

            strWholeArticleHTML = strWholeArticleHTML.replace("\n", "")
            strWholeArticleHTML = strWholeArticleHTML.replace("\t", "")
            dom = etree.XML("<root>" + strWholeArticleHTML + "</root>")

            report = BG_Report()
            report.setURL(dom.xpath('//' + subElementURL + '/@href')[0])
            report.setTitle(dom.xpath('//' + subElementTitle)[0].text)
            report.setDate(dom.xpath('//' + subElementDateReport)[0].text)
            report.setClassification("UNCLASSIFIED")

            if self.repoReport.exist(report):
                print(".", end="")
                continue

            print("Adding article : " + report.getTitle() + ". date: " + report.getDate())
            self.repoReport.save(report)

    def onManageSpecialBackFillAvast(self):
        # Special backfil krebsonsecurity.com/page/[2-213]
        for i in range(2, 8):
            # https://decoded.avast.io/page/2/,article,div[2]/div[1]/h2/a,div[2]/div[1]/h2/a,div[2]/div[1]/div[2]/span[2]/span
            try:
                self.ProcessDataSource("https://decoded.avast.io/page/" + str(i) + "/", "article", "div[2]/div[1]/h2/a", "div[2]/div[1]/h2/a", "div[2]/div[1]/div[2]/span[2]/span")
            except Exception as err:
                print("Something went wrong with " + str(err) + ", ignoring this report")
                continue


    def onManageSpecialBackFillKrebOnSecurity(self):
        # Special backfil krebsonsecurity.com/page/[2-213]
        for i in range(2, 213):
            # https://krebsonsecurity.com/page/2/,article,header/h2/a,header/h2/a,header/div[2]/div/div[1]/span
            try:
                self.ProcessDataSource("https://krebsonsecurity.com/page/" + str(i) + "/", "article", "header/h2/a", "header/h2/a", "header/div[2]/div/div[1]/span")
            except Exception as err:
                print("Something went wrong with " + str(err) + ", ignoring this report")
                continue

    def onManageOrdinary(self):
        with open('./data/datasources.csv', newline='') as csvfile:
            dataSources = csv.reader(csvfile, delimiter=',', quotechar='"')

            for row in dataSources:
                #Get the datasource from the csv
                urlDataSource = row[0]
                elementDelimiter = row[1]
                subElementURL = row[2]
                subElementTitle = row[3]
                subElementDateReport = row[4]
                self.ProcessDataSource(row[0], row[1], row[2], row[3], row[4])


#        time.sleep(1*60*60) #every 1 hours
        time.sleep(10)

    def onManage(self):
        #self.onManageSpecialBackFillKrebOnSecurity()
        #self.onManageSpecialBackFillAvast()
        self.onManageOrdinary()
