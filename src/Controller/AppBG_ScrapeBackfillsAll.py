from src.Controller.AppBG_ScrapeDeamon import AppBG_ScrapeDeamon
from src.Repository.BG_Report_Repository import BG_Report_Repository
from datetime import date, timedelta


class AppBG_ScrapeBackfillsAll(AppBG_ScrapeDeamon):
    def __init__(self):
        super().__init__()
        self.repoReport = BG_Report_Repository()

    def load(self):
        pass

    def onManageSpecialBackFill_PaloAltoUnit42(self):
        print("Backfill Unit42")

        with open('./data/Unit42_BackFill.html', newline='') as file:
            lines = file.readlines()
            text = "".join(lines)

            self._processHTML("https://unit42.paloaltonetworks.com/", text, "article", {}, "div[2]/h3/a", "div[2]/h3/a", "div[2]/ul/li[2]/time")

    def onManageSpecialBackFill_Avast(self):
        print("Backfill Avast")

        # Special backfil krebsonsecurity.com/page/[2-213]
        for i in range(2, 8):
            print("Page " + str(i) + "of 8")

            try:
                self._processDataSource("https://decoded.avast.io/page/" + str(i) + "/", "article", {}, "div[2]/div[1]/h2/a", "div[2]/div[1]/h2/a", "div[2]/div[1]/div[2]/span[2]/span")
            except Exception as err:
                print("Something went wrong with " + str(err) + ", ignoring this report")
                continue

    def onManageSpecialBackFill_KrebOnSecurity(self):
        print("Backfill KrebOnSecurity")

        for i in range(2, 213):
            print("Page " + str(i) + "of 213")

            # https://krebsonsecurity.com/page/2/,article,header/h2/a,header/h2/a,header/div[2]/div/div[1]/span
            try:
                self._processDataSource("https://krebsonsecurity.com/page/" + str(i) + "/", "article", {}, "header/h2/a", "header/h2/a", "header/div[2]/div/div[1]/span")
            except Exception as err:
                print("Something went wrong with " + str(err) + ", ignoring this report")
                continue

    def onManageSpecialBackFill_darkreading(self):
        print("Backfill darkreading")
        for i in range(2, 377):
            print("Page " + str(i) + "of 377")

            # https://www.darkreading.com/threat-intelligence?page=377,div,class:topic-content-article,div[2]/div/div/div[1]/div[2]/a,div[2]/div/div/div[1]/div[2]/a,div[2]/div/div/div[2]/div[2]/div[2]
            try:
                self._processDataSource("https://www.darkreading.com/threat-intelligence?page=" + str(i), "div", {'class': 'topic-content-article'}, "div[2]/div/div/div[1]/div[2]/a", "div[2]/div/div/div[1]/div[2]/a", "div[2]/div/div/div[2]/div[2]/div[2]")
            except Exception as err:
                print("Something went wrong with " + str(err) + ", ignoring this report")
                continue

    def onManageSpecialBackFill_threatpost(self):
        print("Backfill threatpost")

        with open('./data/Threatpost_Backfill.html', newline='') as file:
            lines = file.readlines()
            text = "".join(lines)

            self._processHTML("https://threatpost.com/", text, "article", {}, "div/div[2]/h2/a", "div/div[2]/h2/a", "div/div[2]/div/div[2]/time")


    def onManageSpecialBackFill_schneier(self):
        print("Backfill schneier")
        for i in range(2, 811):
            print("Page " + str(i) + "of 811")

            try:
                self._processDataSource("https://www.schneier.com/page/" + str(i) + "/", "div", {'class': 'article'}, "h2/a", "h2/a", "p[last()]/a[1]")
            except Exception as err:
                print("Something went wrong with " + str(err) + ", ignoring this report")
                continue


    def onManageSpecialBackFill_securityaffairs(self):
        print("Backfill securityaffairs")
        for i in range(2, 1284):
            print("Page " + str(i) + "of 1284")

            try:
                self._processDataSource("https://securityaffairs.co/wordpress/page/" + str(i) + "/", "div", {'class': 'post'}, "div/div/div[2]/div/h3/a", "div/div/div[2]/div/h3/a", "div/div/div[4]/a[1]")
            except Exception as err:
                print("Something went wrong with " + str(err) + ", ignoring this report")
                continue

    def onManageSpecialBackFill_cybergeeks(self):
        print("Backfill cybergeeks")
        for i in range(2, 3):
            print("Page " + str(i) + "of 2")

            try:
                self._processDataSource("https://cybergeeks.tech/page/" + str(i) + "/", "article", {}, "div/div/header/h2/a", "div/div/header/h2/a", "div/div/header/div/span[3]/span[1]")
            except Exception as err:
                print("Something went wrong with " + str(err) + ", ignoring this report")
                continue

    def onManageSpecialBackFill_hackernews(self):
        dataStart = date.today()
        print("Backfill cybergeeks")
        for i in range(1, 4300):
            print("Page " + str(i) + "of 4300")
            url = f"https://thehackernews.com/search?updated-max={dataStart.strftime('%Y-%m-%d')}T00:00:00-00:00&max-results=25"
            try:
                self._processDataSource(url, "div", {'class': 'body-post'}, "a", "a/div/div[2]/h2", "a/div/div[2]/div[1]")
            except Exception as err:
                print("Something went wrong with " + str(err) + ", ignoring this report")

            dataStart = dataStart - timedelta(days=1.0)

    def onManageSpecialBackFill_rapid7(self):
        print("Backfill rapid7")
        for i in range(2, 302):
            print("Page " + str(i) + "of 302")

            try:
                self._processDataSource("https://www.rapid7.com/blog/posts/?page=" + str(i), "a", {'class': 'blog-all-posts__wrapper--item'}, "", "div[1]/h3", " ")
            except Exception as err:
                print("Something went wrong with " + str(err) + ", ignoring this report")
                continue

    def onManageSpecialBackFill_alienvault(self):
        print("Backfill Alienvault")
        for i in range(2, 1583):
            print("Page " + str(i) + "of 1583")

            try:
                self._processDataSource("https://cybersecurity.att.com/blogs/P" + str(i), "div", {'class': 'blog-card'}, "div/div[2]/a", "div/div[2]/a", "div/div[3]")
            except Exception as err:
                print("Something went wrong with " + str(err) + ", ignoring this report")
                continue

    def onManageSpecialBackFill_welivesecurity(self):
        print("Backfill welivesecurity")
        for i in range(2, 284):
            print("Page " + str(i) + "of 284")

            try:
                self._processDataSource("https://www.welivesecurity.com/page/" + str(i) + "/", "article", {}, "div[2]/h2/a", "div[2]/h2/a", "div[2]/span/time")
            except Exception as err:
                print("Something went wrong with " + str(err) + ", ignoring this report")
                continue

    def onManageSpecialBackFill_nakedsecurity(self):
        print("Backfill nakedsecurity")
        for i in range(2, 1628):
            print("Page " + str(i) + "of 1628")

            try:
                self._processDataSource("https://nakedsecurity.sophos.com/page/" + str(i) + "/", "article", {}, "div[2]/h3/a", "div[2]/h3/a", "")
            except Exception as err:
                print("Something went wrong with " + str(err) + ", ignoring this report")
                continue

    def onManage(self):
        self.onManageSpecialBackFill_nakedsecurity()
        self.onManageSpecialBackFill_welivesecurity()
        self.onManageSpecialBackFill_alienvault()
        self.onManageSpecialBackFill_rapid7()
        self.onManageSpecialBackFill_hackernews()
        self.onManageSpecialBackFill_cybergeeks()
        self.onManageSpecialBackFill_securityaffairs()
        self.onManageSpecialBackFill_schneier()
        self.onManageSpecialBackFill_threatpost()
        self.onManageSpecialBackFill_KrebOnSecurity()
        self.onManageSpecialBackFill_Avast()
        self.onManageSpecialBackFill_PaloAltoUnit42()
        self.onManageSpecialBackFill_darkreading()
