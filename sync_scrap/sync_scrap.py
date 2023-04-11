from playwright.sync_api import sync_playwright

import time

def sync_scrap(url):
    base_url = '/'.join(url.split('/')[:3])

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        
        page.goto(url)

        categories_container = page.query_selector('#s-refinements').query_selector_all('ul')[1]
       
        categories = {}
        for row in categories_container.query_selector_all('li'):
            data = row.query_selector('a')
            key = data.query_selector_all('span')[1].inner_html().replace('&amp;', 'and')
            value = data.get_attribute('href')
            categories[key] = categories.get(key, f'{base_url}{value}')

        return categories