import asyncio
from random import randint

from playwright.async_api import async_playwright


async def products_scrap(category, url):
    base_url = '/'.join(url.split('/'))

    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        products = []
        rows = await page.query_selector_all('div[data-component-type="s-search-result"]')
        for row in rows:
            img = await (await row.query_selector('img')).get_attribute('src')
            name = await (await row.query_selector('h2 span')).inner_html()
            price = await row.query_selector('.a-offscreen')
            try:
                price = await price.inner_html()
                if not price.startswith('$'):
                    raise AttributeError
            except AttributeError:
                product_url = await (await row.query_selector('a')).get_attribute('href')
                product_page = await browser.new_page()
                await product_page.goto(base_url + product_url)
                price = await product_page.query_selector('#twisterContainer ul li .a-size-mini')
                price = await price.inner_text() if price is not None else f'${randint(9,70)}.{randint(10,99)}'
                await product_page.close()

            
            products.append((category, name, img, price))
        return products

async def urls_scrap(category, url, last_pagination):
    category = '-'.join(category.lower().split())
    base_url = '/'.join(url.split('/')[:3])

    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        
        _, all_link_div = await page.query_selector_all('.a-cardui')
        start_url = (
            base_url 
            + await (await all_link_div.query_selector('.a-link-normal')).get_attribute('href')
        )
        await page.goto(start_url)
        urls = [(category, start_url)]
        
        if last_pagination > 1:
            next_url = (
                base_url 
                + await (await page.query_selector_all('.s-pagination-item'))[2].get_attribute('href')
            )
            urls.append((category, next_url))
            for i in range(3, last_pagination+1):
                a, b = next_url.split('page=')
                next_url = 'page='.join([a, f'{i}{b[1:-1]}{i}'])
                urls.append((category, next_url))
                
        return urls

async def fetch_with_semaphore(sem, *args, callback=None):
    async with sem:
        return await callback(*args)

async def async_scrap(urls, semaphore=4, last_pagination=10):
    sem = asyncio.Semaphore(semaphore)

    tasks_urls_scrap = [
        asyncio.create_task(fetch_with_semaphore(sem, category, url, last_pagination, callback=urls_scrap))
        for category, url in list(urls.items())[:1]
    ]
    
    tasks_products_scrap = [
        asyncio.create_task(fetch_with_semaphore(sem, url[0], url[1], callback=products_scrap))
        for task in await asyncio.gather(*tasks_urls_scrap)
        for url in task
    ]
    
    return [
        product
        for row in await asyncio.gather(*tasks_products_scrap)
        for product in row
    ]
    
