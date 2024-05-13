from bs4 import BeautifulSoup
import requests

def scrape_bs():
    # Send an HTTP request to the URL
    url = "https://www.nature.com/search?q=enzymes%20&order=relevance"
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the specific <a> tag by its text content
    link = soup.find('a', text="Natural diversity screening, assay development, and characterization of nylon-6 enzymatic depolymerization")

    # Extract the link if it exists
    if link:
        href = link.get('href')
        print("Link:", href)
    else:
        print("Link not found.")

    return href