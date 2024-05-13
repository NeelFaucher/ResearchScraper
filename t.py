# tasks.py
from seleniumbase import SB
from celery import Celery

def scrape_2():
    print("INSIDE SCRAPE_2")
    url_base = "https://www.nature.com/"

    with SB(uc=True, xvfb=True) as sb:
        print("HERE")
        sb.driver.uc_open_with_reconnect(url_base, 20)
        print("OPENED WEBSITE")
        # Get the title of the page
        title = sb.driver.title
        print("Title of the page:", title)

    return title