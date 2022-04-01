"""
Module for WebApp class. 2 vclasses in this module : WebApp and CherryPyExposure
------------------------------------------------------------------------------------------------------------------------
"""

# ======================================================================================================================
# importing external modules
import cherrypy
import os
import os.path
import time

# ======================================================================================================================
# importing internal modules
from src.CCC.App import App
from src.CCC.Thread import Thread


class CherryPyExposure(Thread):
    """
    Class CherryPyExposure Description :
        Derived from Thread (internal), this class serve as the Base class for application-side future derivation. it
        kinda encapslutae basic Cherrypy jo into simple way of using Cherrypy.

    Class Attributes (Static attributes):
        None

    Instance Attributes :
        None
    """

    # ==================================================================================================================
    def __init__(self, pObjRESTfulService=None):
        """ __init__ Description : (public visibility) :
            Constructor for a new CherryPyExposure object, basically redirecting to super classes the construction.
        """
        super().__init__("Thread-WebAppCherryPy")
        self.rest_service = pObjRESTfulService          #name must match the Exposure

    # ==================================================================================================================
    def load(self):
        """ load Description : (public visibility) :
            Preparing the Thread for running.
        """
        #cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 5000, 'request.show_tracebacks': False})
        cherrypy.config.update({'server.socket_host': '127.0.0.1', 'server.socket_port': 8080, 'request.show_tracebacks': False})

    # ==================================================================================================================
    def onManage(self, param1= None):
        """ onManage Description : (public visibility) :
            Event (callback) for one loop of execution. In this exemple, 1 loop is all we need since quickstart is
            blocking.
        """

        # A Python dictionary that contains several parameters especially for the http routes exposures
        dicConfigParams = {
            '/': {
                'tools.sessions.on': True,
                'tools.staticdir.root': os.path.abspath(os.getcwd() + "/Web")
            },
            '/rest_service': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.response_headers.on': True,
                'tools.sessions.on': True,
                'tools.response_headers.headers': [('Content-Type', 'text/plain'), ('Content-Type', 'text/xml')],
            },
            '/public': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': './public'
            }
        }

        # This call is blocking (e.g. when we go to the next line it mean that the server has ended).
        cherrypy.quickstart(self, '/', dicConfigParams)
        self.setRunning(False)


# ======================================================================================================================
class WebApp(App):
    """
    Class WebApp Description :
        Derived from App (internal), this class serve as the Base class for application-side future derivation. it
        kinda encapslutae basic Cherrypy jo into simple way of using Cherrypy.

    Class Attributes (Static attributes):
        None

    Instance Attributes :
        objThreadWebExposure :  Received as dependy injection. It is the Èxposure side of the application that will
                                manage the presentation layer(View) of the WebApp.
    """

    # ==================================================================================================================
    def __init__(self, strThreadName: str, objWebappExposure: CherryPyExposure):
        """ __init__ Description : (public visibility) :
            Constructor if the WebApp. it basically overload the base constructor and start the Presentation exposure
            (View).
        """
        super().__init__(strThreadName)

        self.objThreadWebExposure = objWebappExposure
        self.objThreadWebExposure.start()
        time.sleep(0.1)
