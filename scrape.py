from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  # Import Keys class for simulating keyboard keys
from selenium.common.exceptions import TimeoutException

from time import sleep
import pandas as pd

url_base = "https://www.nature.com/"
search_query = "enzymatic degradation plastic"

def calculate(string):
    return string + "abs"


def scrape_data():
    options = Options()
    options.add_argument("--start-maximized")  # Maximizing the window
    driver = webdriver.Chrome(options=options)  # Creating a Chrome WebDriver instance
    driver.get(url_base)

    # Waiting for the accept button to be clickable
    accept_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-cc-action="accept"]')))

    # Clicking the accept button
    accept_button.click()

    # Waiting for the search button to be clickable
    search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.c-header__link--search')))

    # Clicking on the search button to expand the search form
    search_button.click()

    # Finding the search input field
    search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.c-header__input')))

    # Entering the search query
    search_input.send_keys(search_query)

    # Simulate hitting the "Enter" key
    search_input.send_keys(Keys.RETURN)

    # Finding all links with class 'c-card__link'
    article_links = driver.find_elements(By.CSS_SELECTOR, 'a.c-card__link')

    urls = []
    titles = []
    authors_list = []
    dates = []
    abstracts = []

    # Extracting URLs and printing them
    for link in article_links:
        url = link.get_attribute('href')
        urls.append(url)

    for url in urls[:5]:  # This will iterate only over the first 10 URLs
        driver.get(url)
        sleep(0.5)

        # article titles
        article_title_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.c-article-title')))
        article_title = article_title_element.text
        titles.append(article_title)
        sleep(0.5)

        ## Finding the authors' list element
        authors_list_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.c-article-author-list')))
        author_name_elements = authors_list_element.find_elements(By.CSS_SELECTOR, 'a[data-test="author-name"]')
        authors = [author_name.text for author_name in author_name_elements]
        authors_list.append(authors)
        sleep(0.5)

        # article abstract
        try:
            # Article abstract
            abstract_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Abs1-content')))
            abstract = abstract_element.text
            abstracts.append(abstract)
        except TimeoutException:
            abstracts.append("None found")  # Append None if abstract not found

        # article publish date
        date_published_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//ul[@class="c-article-identifiers"]//li[contains(text(), "Published:")]/time')))
        date_published = date_published_element.get_attribute('datetime')
        dates.append(date_published)

    driver.quit()

    data = {
        'URL': urls[:5],
        'Title': titles,
        'Authors': authors_list,
        'Date': dates,
        'Abstract': abstracts
    }

    # Create a DataFrame
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    scrape_data()
