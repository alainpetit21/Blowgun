import time
import csv
import requests

from bs4 import BeautifulSoup
from lxml import etree
from src.CCC.Thread import Thread
from src.Controller.AppBG_ScrapeDeamon import AppBG_ScrapeDeamon

from src.Repository.BG_Report_Repository import BG_Report_Repository
from src.Model.BG_Report import BG_Report


class AppBG_ScrapeBackfillsAll(AppBG_ScrapeDeamon):
    def __init__(self):
        super().__init__()
        self.repoReport = BG_Report_Repository()

    def load(self):
        pass

    def onManageSpecialBackFillPaloAltoUnit42(self):
        with open('./data/Unit42_BackFill.html', newline='') as file:
            lines = file.readlines()
            text = "".join(lines)

            self._processHTML(text, "article", {}, "div[2]/h3/a", "div[2]/h3/a", "div[2]/ul/li[2]/time")

    def onManageSpecialBackFillAvast(self):
        # Special backfil krebsonsecurity.com/page/[2-213]
        for i in range(2, 8):
            # https://decoded.avast.io/page/2/,article,div[2]/div[1]/h2/a,div[2]/div[1]/h2/a,div[2]/div[1]/div[2]/span[2]/span
            try:
                self._processDataSource("https://decoded.avast.io/page/" + str(i) + "/", "article", {}, "div[2]/div[1]/h2/a", "div[2]/div[1]/h2/a", "div[2]/div[1]/div[2]/span[2]/span")
            except Exception as err:
                print("Something went wrong with " + str(err) + ", ignoring this report")
                continue

    def onManageSpecialBackFillKrebOnSecurity(self):
        # Special backfil krebsonsecurity.com/page/[2-213]
        for i in range(2, 213):
            # https://krebsonsecurity.com/page/2/,article,header/h2/a,header/h2/a,header/div[2]/div/div[1]/span
            try:
                self._processDataSource("https://krebsonsecurity.com/page/" + str(i) + "/", "article", {}, "header/h2/a", "header/h2/a", "header/div[2]/div/div[1]/span")
            except Exception as err:
                print("Something went wrong with " + str(err) + ", ignoring this report")
                continue

    def onManageSpecialBackFilldarkreading(self):
        for i in range(2, 377):
            # https://www.darkreading.com/threat-intelligence?page=377,div,class:topic-content-article,div[2]/div/div/div[1]/div[2]/a,div[2]/div/div/div[1]/div[2]/a,div[2]/div/div/div[2]/div[2]/div[2]
            try:
                self._processDataSource("https://www.darkreading.com/threat-intelligence?page=" + str(i), "div", {'class': 'topic-content-article'}, "div[2]/div/div/div[1]/div[2]/a", "div[2]/div/div/div[1]/div[2]/a", "div[2]/div/div/div[2]/div[2]/div[2]")
            except Exception as err:
                print("Something went wrong with " + str(err) + ", ignoring this report")
                continue

    def onManage(self):
        self.onManageSpecialBackFillKrebOnSecurity()
        self.onManageSpecialBackFillAvast()
        self.onManageSpecialBackFillPaloAltoUnit42()
        self.onManageSpecialBackFilldarkreading()
