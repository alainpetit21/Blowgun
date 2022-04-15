from datetime import date

import cherrypy

from src.CCC.WebApp import WebApp, CherryPyExposure
from src.Model.BG_QueryResults import BG_QueryResults
from src.Repository.BG_Report_Repository import BG_Report_Repository


# ======================================================================================================================
class MyCherryPyThread(CherryPyExposure):
    def __init__(self, pObjRESTfulService):
        super().__init__(pObjRESTfulService)
        self.repoReport = BG_Report_Repository()

    @cherrypy.expose
    def index(self, keyword="", tail=""):
        with open('./Web/public/header.html') as file:
            header = file.read()
        with open('./Web/public/footer.html') as file:
            footer = file.read()

        objQueryResults: BG_QueryResults
        if tail == "":
            objQueryResults = self.repoReport.searchInTitle(keyword)
        else:
            objQueryResults = self.repoReport.searchInTitleLatest(keyword, int(tail))

        return header + objQueryResults.buildSimpleHTML() + footer


# ======================================================================================================================
@cherrypy.expose
class MyCherryPyRestService:
    def __init__(self):
        self.repoReport = BG_Report_Repository()

    @cherrypy.tools.accept(media='text/plain')
    def POST(self):
        return "POST"

    @cherrypy.tools.accept(media='text/plain')
    def GET(self, keyword="", tail=""):
        if tail == "":
            objQueryResults = self.repoReport.searchInTitle(keyword)
            return str(objQueryResults)
        else:
            objQueryResults = self.repoReport.searchInTitleLatest(keyword, int(tail))
            return str(objQueryResults)

    def PUT(self):
        return "PUT"

    def DELETE(self):
        return "DELETE"


# ======================================================================================================================
class WebAppBG_Engine(WebApp):
    # Class attributes
    idx_my_model = None

    def __init__(self):
        super().__init__(strThreadName="AppMyCherryPyTest", objWebappExposure=MyCherryPyThread(MyCherryPyRestService()))

    def load(self):
        print("Welcome to Web Blowgun Engine")

    def on_manage(self, param1=None):
        self.is_running = False
