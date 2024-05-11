from seleniumbase import BaseCase
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

class MyTestClass(BaseCase):
    def setUp(self):
        super().setUp()  # Call the setUp() method of the BaseCase class

    def test_scrape_data(self):
        url_base = "https://www.nature.com/"
        search_query = "enzymatic degradation plastic"
        self.open(url_base)
        self.maximize_window()  # Maximizing the window
        
        # Waiting for the accept button to be clickable
        self.wait_for_element_to_be_clickable('button[data-cc-action="accept"]')

        # Clicking the accept button
        self.click('button[data-cc-action="accept"]')

        # Waiting for the search button to be clickable
        self.wait_for_element_to_be_clickable('a.c-header__link--search')

        # Clicking on the search button to expand the search form
        self.click('a.c-header__link--search')

        # Finding the search input field
        search_input = self.wait_for_element_present('input.c-header__input')

        # Entering the search query
        search_input.send_keys(search_query)

        # Simulate hitting the "Enter" key
        search_input.send_keys(Keys.RETURN)

        # Finding all links with class 'c-card__link'
        article_links = self.find_elements('a.c-card__link')

        urls = []
        titles = []
        authors_list = []
        dates = []
        abstracts = []

        # Extracting URLs and printing them
        for link in article_links:
            url = link.get_attribute('href')
            urls.append(url)

        for url in urls[:2]:  # This will iterate only over the first 2 URLs
            self.open(url)
            self.wait(0.5)

            # article titles
            article_title_element = self.wait_for_element_present('h1.c-article-title')
            article_title = article_title_element.text
            titles.append(article_title)
            self.wait(0.5)

            ## Finding the authors' list element
            authors_list_element = self.wait_for_element_present('ul.c-article-author-list')
            author_name_elements = self.find_elements('a[data-test="author-name"]')
            authors = [author_name.text for author_name in author_name_elements]
            authors_list.append(authors)
            self.wait(0.5)

            # article abstract
            try:
                # Article abstract
                abstract_element = self.wait_for_element_present('#Abs1-content')
                abstract = abstract_element.text
                abstracts.append(abstract)
            except TimeoutException:
                abstracts.append("None found")  # Append None if abstract not found

            # article publish date
            date_published_element = self.wait_for_element_present('//ul[@class="c-article-identifiers"]//li[contains(text(), "Published:")]/time')
            date_published = date_published_element.get_attribute('datetime')
            dates.append(date_published)

        data = {
            'URL': urls[:2],
            'Title': titles,
            'Authors': authors_list,
            'Date': dates,
            'Abstract': abstracts
        }

        # Create a DataFrame
        df = pd.DataFrame(data)
        print(df)
        
if __name__ == "__main__":
    MyTestClass(methodName='test_scrape_data').test_scrape_data()