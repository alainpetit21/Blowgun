from src.Controller.AppBG_ScrapeBackfillsAll import AppBG_ScrapeBackfillsAll
from src.Controller.AppBG_ScrapeDeamon import AppBG_ScrapeDeamon
from src.Controller.WebAppBG_Engine import WebAppBG_Engine


def main():
    print("Welcome to Blowgun ScrapeDeamon")

    # Create the App object, load it, and run it (with main)
    obj_app = AppBG_ScrapeBackfillsAll()
    obj_app.load()
    obj_app.onManage()

    obj_app = AppBG_ScrapeDeamon()
    obj_app.load()
    obj_app.start()

    obj_webApp = WebAppBG_Engine()
    obj_webApp.load()
    obj_webApp.main()



if __name__ == '__main__':
    main()
