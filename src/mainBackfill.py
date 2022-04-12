from src.Controller.AppBG_ScrapeBackfillsAll import AppBG_ScrapeBackfillsAll


def main():
    print("Welcome to Blowgun ScrapeDeamon")

    # Create the App object, load it, and run it (with main)
    obj_app = AppBG_ScrapeBackfillsAll()
    obj_app.load()
    obj_app.onManage()


if __name__ == '__main__':
    main()
