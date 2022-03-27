"""
Module for Thread class. 1 classes in this module : Thread
------------------------------------------------------------------------------------------------------------------------
"""

# ======================================================================================================================
# importing external modules
from threading import Thread as BaseThread

# ======================================================================================================================
# importing internal modules
from src.CCC.App import App


# ======================================================================================================================
class Thread(App, BaseThread):
    """
    Class WebAppINF4018_Server Description :
        Derived from App and the Python internal Thread (as BasedThread alias here). Implement generic methods for a
        thread object. The only thing that remains on client side are client specfic application logic / orchestration
        / etc. Thread are actually derived from App object and should be conceptually treated by client side as mini
        sub-program, with their own mini sub-module..

    Class Attributes (Static attributes):
        None

    Instance Attributes :
        None
    """

    # ==================================================================================================================
    def __init__(self, pStrThreadName):
        """ __init__ Description : (public visibility) :
            Constructor for a new Thread object, basically redirecting to super classes the construction.
        """
        BaseThread.__init__(self, name=pStrThreadName, target=Thread._start, args=([self]))
        App.__init__(self, pStrThreadName)

    # ==================================================================================================================
    def load(self):
        """ load Description : (public visibility) :
            To be implemented client-side to perform all sort of loading and creating modules.
        """
        raise NotImplementedError("Subclass must implement abstract method")

    # ==================================================================================================================
    def _start(self):
        """ _start Description : (private visibility) :
            Our own private internal start that will be the hook for the Python BaseThread. Not to be confused with the
            start function that is to be call client side to initiated the thread
        """
        self.setRunning(True)
        self.load()
        self.main()
