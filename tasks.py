# tasks.py
from seleniumbase import SB
from celery import Celery

import os
from celery import Celery

# Read the Redis URL from the environment variables
redis_url = os.environ.get('REDIS_URL')

# Create the Celery instance
app = Celery('tasks', broker=redis_url)

@app.task
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