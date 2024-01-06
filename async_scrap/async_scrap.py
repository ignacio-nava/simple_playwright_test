import asyncio
from random import randint

from playwright.async_api import async_playwright


async def scrap_products(index, category, url, last_pagination):
    index += 1
    base_url = '/'.join(url.split('/')[:3])

    async with async_playwright() as pw:
        print(f'[{index}] Starting to scrap \033[1;46m{category}\033[0m', flush=True)
        browser = await pw.chromium.launch()
        page = await browser.new_page()
        products = []
        for i in range(1, last_pagination+1):
            if i == 1:
                await page.goto(url)
            elif i == 2:
                try:
                    await page.goto(base_url + next_page)
                except UnboundLocalError:
                    break
            else:
                base, paginator = next_page.split('page=')
                next_page = 'page='.join([base, f'{i}{paginator[1:-1]}{i}'])
                await page.goto(base_url + next_page)

            components = await page.query_selector_all('.s-search-results > div')
            for component in components:
                component_type = await component.get_attribute('data-component-type')
                if component_type == 's-search-result':
                    name = await (await component.query_selector('h2 span')).inner_html()
                    image = await (
                        await component.query_selector('.s-product-image-container img')
                    ).get_attribute('src')
                    price = await component.query_selector('.a-price > span.a-offscreen')
                    try:
                        price = await price.inner_html()
                        if not price.startswith('$'):
                            raise AttributeError
                    except AttributeError:
                        price = f'${randint(9,70)}.{randint(10,99)}'

                    products.append((category, name, image, price))
                else:
                    if i != 1:
                        continue
                    paginator = await component.query_selector('div[role="navigation"] a')
                    if paginator:
                        next_page = await paginator.get_attribute('href')

        scrap_len = len(products)
        scrap_len = f'{scrap_len} New Product' if scrap_len == 1 else f'{scrap_len} New Products'
        print(
            f'\033[1;42m[{index}]\033[0m Finish scrap \033[1;42m{category:40} -> {scrap_len} \033[0m')
        return products


async def fetch_with_semaphore(sem, *args, callback=None):
    async with sem:
        return await callback(*args)


async def async_scrap(urls, **kwargs):
    sem = asyncio.Semaphore(kwargs['semaphore'])

    print(f'\33[1m{len(urls.keys())} Categories founded\033[0m\n')

    tasks_products_scrap = [
        asyncio.create_task(
            fetch_with_semaphore(
                sem, index, category, url,
                kwargs['last_pagination'], callback=scrap_products
            )
        )
        for index, (category, url) in enumerate(urls.items())
    ]

    return [
        product
        for row in await asyncio.gather(*tasks_products_scrap)
        for product in row
    ]
