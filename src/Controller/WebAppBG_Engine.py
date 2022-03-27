import cherrypy

# ======================================================================================================================
# importing library modules
from src.CCC.WebApp import WebApp, CherryPyExposure


class MyCherryPyThread(CherryPyExposure):
    def __init__(self, pObjRESTfulService):
        super().__init__(pObjRESTfulService)

    @cherrypy.expose
    def index(self):
        # return open('Web/index.html')
        return "Welcome to Web Blowgun Engine"


@cherrypy.expose
class MyCherryPyRestService:

    @cherrypy.tools.accept(media='text/plain')
    def POST(self):
        return "POST"

    def GET(self):
        return "GET"

    def PUT(self):
        return "PUT"

    def DELETE(self):
        return "DELETE"


# ======================================================================================================================
# class AppFastTinkerbell
class WebAppBG_Engine(WebApp):
    # ==================================================================================================================
    # Class attributes
    idx_my_model = None

    # ==================================================================================================================
    # Class Methods
    # ==================================================================================================================
    # __init__ : Constructor methods that will creat this object. I does not do a lot but, overload the BaseClass
    #               construction call
    def __init__(self):
        super().__init__(strThreadName="AppMyCherryPyTest", objWebappExposure=MyCherryPyThread(MyCherryPyRestService()))

    # ==================================================================================================================
    # load : Called a bit after the constructor. In this example we will use this time to initiate the string
    def load(self):
        print("Welcome to Web Blowgun Engine")


    # ==================================================================================================================
    # on_manage : Periodically called (one per loop) for performing client-side operations. In this examples we only
    #               print the string and exit
    def on_manage(self, param1= None):
        self.is_running = False
