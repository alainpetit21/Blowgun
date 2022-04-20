import os
import traceback

from cherrypy.lib.static import serve_file

from src.CCC.WebApp import WebApp, CherryPyExposure
from src.Model.BG_QueryResults import BG_QueryResults
from src.Repository.BG_Report_Repository import BG_Report_Repository
from datetime import date

import cherrypy
import pdfkit

# ======================================================================================================================
class MyCherryPyThread(CherryPyExposure):
    def __init__(self, pObjRESTfulService):
        super().__init__(pObjRESTfulService)
        self.repoReport = BG_Report_Repository()

    @cherrypy.expose
    def index(self):
        return "Welcome to Blowgun Engine"

    @cherrypy.expose
    def downloadPDF(self, url):
        baseName = url.replace("/", "")
        baseName = baseName.replace(".", "")
        baseName = baseName.replace(":", "")
        fileOutput = './output/' + baseName + '-' + str(date.today()) + '.pdf'

        try:
            pdfkit.from_url(url, fileOutput)
        except Exception as ex:
            print("Found error, but trying to ignore")
            traceback.print_exc()

        if os.path.exists(fileOutput):
            localDir = os.path.dirname(__file__)
            absDir = os.path.join(os.getcwd(), localDir)
            path = os.path.join(absDir, "pdf_file.pdf")
            path = os.getcwd() + "/" + fileOutput

            return serve_file(path, "application/x-download", "attachment", os.path.basename(path))
        else:
            return "Error in PDF Generation, please press back and try again"

    @cherrypy.expose
    def query(self, keyword="", tail=""):
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
