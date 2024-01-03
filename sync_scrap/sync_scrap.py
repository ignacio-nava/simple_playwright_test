from playwright.sync_api import sync_playwright

import time


def sync_scrap(url):
    base_url = '/'.join(url.split('/')[:3])

    with sync_playwright() as pw:
        #  Open browser
        browser = pw.chromium.launch()
        page = browser.new_page()
        #  Go to URL
        page.goto(url)
        #  Find element that contains all categories to scrap
        categories_container = page.query_selector(
            '.left_nav.browseBox').query_selector('ul')
        #  Make dictionary with this categories
        categories = {}
        for row in categories_container.query_selector_all('li'):
            data = row.query_selector('a')
            key = data.inner_html().replace('&amp;', 'and')
            value = data.get_attribute('href')
            categories[key] = categories.get(key, f'{base_url}{value}')

        return categories
