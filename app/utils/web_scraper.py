from playwright.sync_api import sync_playwright
from langchain.schema import Document
import logging

logger = logging.getLogger(__name__)

def get_rendered_webpage(url: str) -> Document:
    """
    Scrape and render the content of a webpage using Playwright.

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        Document: A Langchain Document object containing the rendered HTML content.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)
            page.wait_for_load_state("networkidle")
            html = page.content()
            browser.close()
            return Document(page_content=html, metadata={"source": url})
    except Exception as e:
        logger.error(f"Error during web scraping: {e}\n")
        raise
