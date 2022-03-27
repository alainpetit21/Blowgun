"""
Module for App class. 1 classes in this module : App
------------------------------------------------------------------------------------------------------------------------
"""
# ======================================================================================================================
# importing external modules
import time
import logging


# ======================================================================================================================
class App:
    """
    Class WebAppINF4018_Server Description :
        Implement generic method for a application object. The only thing that remains on client side are client specfic
        application logic / orchestration / etc.

    Class Attributes (Static attributes):
        None

    Instance Attributes :
        isRunning = a boolean that specify if the App is running or not
        strAppName = a string for the Name of the Application
        objDomain = a simple app should need a Domain (as per Domain-Derived Design by Robert C Martin) or Model
                    as per the MVC Design Standard
        lstSubThread = None
    """

    # ==================================================================================================================
    def __init__(self, p_str_name, debug_level=3):
        """ __init__ Description : (public visibility) :
            Constructor methode that manage the Singleton DP and generic constructor management for this object.
        """

        self.isRunning = False          # Generic attributes, used internally
        self.strAppName = p_str_name    # Generic attributes, used internally
        self.objDomain = None           # Domain Object of the App in DDD architecture or Model in MVC architecture
        self.lstSubThread = []          # Support for multi-threaded, list of launched Thread

        # Set basic logging output format
        if debug_level == 0:    logging.basicConfig(level=logging.NOTSET, format='[%(levelname)s] (%(threadName)-10s) %(message)s')
        if debug_level == 1:    logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')
        if debug_level == 2:    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] (%(threadName)-10s) %(message)s')
        if debug_level == 3:    logging.basicConfig(level=logging.WARNING, format='[%(levelname)s] (%(threadName)-10s) %(message)s')
        if debug_level == 4:    logging.basicConfig(level=logging.ERROR, format='[%(levelname)s] (%(threadName)-10s) %(message)s')
        if debug_level == 5:    logging.basicConfig(level=logging.CRITICAL, format='[%(levelname)s] (%(threadName)-10s) %(message)s')

    # ==================================================================================================================
    def setDomain(self, p_obj_model):
        """ setDomain Description : (public visibility) :
            Method for adding a Domain Object For the App. This follow the Domain as per DDD architecture or the Model
            in a standard Model View Controller architecture.
        """
        self.objDomain = p_obj_model

    # ==================================================================================================================
    def getDomain(self):
        """ getDomain Description : (public visibility) :
            Return the Domain (or the Model in MVC).
        """
        return self.objDomain

    # ==================================================================================================================
    def setRunning(self, pWillBeRunning=True):
        """ setRunning Description : (public visibility) :
            Set the internal running boolean to True (default) or the value in argument.
        """
        self.isRunning = pWillBeRunning

    # ==================================================================================================================
    def getRunningStatus(self):
        """ getRunningStatus Description : (public visibility) :
            return wheter this object is running or not.
        """
        return self.isRunning

    # ==================================================================================================================
    def launchThread(self, p_obj_thread):
        """ launchThread Description : (public visibility) :
            Allow the App the launch sub-Thread enabling multi-threading application. The app will keep that in memory
            to monitor their closure before exiting.
        """
        self.lstSubThread.append(p_obj_thread)
        p_obj_thread.start()

    # ==================================================================================================================
    def main(self, param1= None):
        """ launchThread Description : (public visibility) :
            Mostly for internal purposes only, shall contains the main loop.
        """
        self.isRunning = True

        # Main Loop
        while self.isRunning:
            logging.debug('Performing one loop')
            self.onManage()
            time.sleep(0.1)

        # Ensure that no other thread are running
        logging.debug('About to quit, but first check if any other threads are running')
        other_thread_is_running= True
        while other_thread_is_running:
            other_thread_is_running = False

            for obj_thread in self.lstSubThread:
                if obj_thread.is_running:
                    logging.debug('Found a thread : {}'.format(obj_thread.str_name))
                    other_thread_is_running = True

                logging.debug('Trying to join : {}'.format(obj_thread.str_name))
                obj_thread.join()
            time.sleep(1)

    # ==================================================================================================================
    def onManage(self):
        """ onManage Description : (public visibility) :
            Mostly for external client-side purposes only. Callback style that will be implemented beyond a level.
        """
        pass
