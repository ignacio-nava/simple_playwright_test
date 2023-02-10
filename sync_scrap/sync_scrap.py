from playwright.sync_api import sync_playwright

import time

def sync_scrap(url):
    base_url = '/'.join(url.split('/')[:3])

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        
        page.goto(url)

        categories_container = page.query_selector_all('.acsUxWidget')
        _, *categories_rows = categories_container[1].query_selector_all('.bxc-grid__row')
            
        categories = {}
        for row in categories_rows:
            columns = row.query_selector_all('.bxc-grid__column')
            for column in columns:
                data = column.query_selector('div > a')
                key = data.get_attribute('aria-label').replace('Unique ', '')
                value = data.get_attribute('href')
                categories[key] = categories.get(key, f'{base_url}{value}')

        return categories