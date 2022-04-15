"""
Module for SingletonDecorator class. 1 classes in this module : SingletonDecorator
------------------------------------------------------------------------------------------------------------------------
"""


class Singleton:
    """
    Class SingletonDecorator Description :
        Decorator helper object that will manage the Singleton DesignPattern as a Python Decorator. Keep in mind That
        an instance of this call holds a class level object. Thus this keep of makes this a meta-class.

    Class Attributes (Static attributes):
        None

    Instance Attributes :
        objClass = a class-level object that contains the id for the instance
        objInstance = the only and only instance for this associated class.
    """

    # ==================================================================================================================
    def __init__(self, objClass):
        """ __init__ Description : (public visibility) :
            Constructor for the SingletonDecorator object. Technically speaking, this is created as we decorated another
            class (noting the objClass as argument)
        """
        self.objClass = objClass
        self.objInstance = None

    # ==================================================================================================================
    def __call__(self, *args, **kwds):
        """ __call__ Description : (public visibility) :
            Operator() method, this is called whenever our "decorated" class is called as a "method" with the
            parenthesis as such Class(). Instead of recreating an object, it will look return the objInstance if it was
            already created or create a new one if not.
        """
        if self.objInstance is None:
            self.objInstance = self.objClass(*args, **kwds)

        return self.objInstance

# ======================================================================================================================
# TUTORIAL ON SINGLETON
# ======================================================================================================================
# How to Define the Singleton Class
# ======================================================================================================================
# @SingletonDecorator
# class ClassToto(...):

# ======================================================================================================================
# How to use the  Singleton Class
# ======================================================================================================================
# print(ClassToto().something attribute or method in the class)
# print(ClassToto().something attribute or method in the class)
# ======================================================================================================================
# How does it do it?
# ======================================================================================================================
# The first call to ClassToto with parenthesis will get redirected into the decorator, who will then use the __call__
# function and since instance is None, it will create 1 instance of the object with the args and kwds.

# The second time it is called though instance will not be None and it will just return instance.
