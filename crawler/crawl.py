import asyncio
import aiohttp
from aiohttp import ClientSession
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
import re

BASE_URL = "https://books.toscrape.com/"
LISTING_URL = urljoin(BASE_URL, "catalogue/page-{}.html")
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data/raw_html")
CONCURRENCY = 10
TOTAL_PRODUCTS_WANTED = 500

os.makedirs(DATA_DIR, exist_ok=True)
logging.basicConfig(level=logging.INFO)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; ProductIngestBot/1.0; +https://example.com/bot)'
}

async def fetch(session: ClientSession, url: str, retries=3):
    try:
        async with session.get(url, headers=HEADERS) as response:
            if response.status == 200:
                return await response.text()
            else:
                logging.warning(f"Non-200 for {url}: {response.status}")
    except Exception as e:
        if retries > 0:
            await asyncio.sleep(1)
            return await fetch(session, url, retries - 1)
        else:
            logging.error(f"Failed to fetch {url}: {e}")
    return None

async def fetch_product(session, url, product_id):
    fname = os.path.join(DATA_DIR, f"{product_id}.html")
    if os.path.exists(fname):
        logging.info(f"Already fetched {product_id}")
        return True
    html = await fetch(session, url)
    if html:
        with open(fname, "w", encoding="utf8") as f:
            f.write(html)
        logging.info(f"Saved product: {product_id}")
        return True
    else:
        logging.error(f"Failed product: {product_id}")
        return False

async def gather_tasks(tasks, concurrency=CONCURRENCY):
    semaphore = asyncio.Semaphore(concurrency)
    async def limited(task_func):
        async with semaphore:
            return await task_func
    return await asyncio.gather(*(limited(t) for t in tasks))

async def crawl_all_products():
    seen = set()
    product_tasks = []
    page = 1
    product_count = 0

    async with aiohttp.ClientSession() as session:
        while product_count < TOTAL_PRODUCTS_WANTED:
            url = LISTING_URL.format(page)
            html = await fetch(session, url)
            if html is None: break
            soup = BeautifulSoup(html, "lxml")
            prods = soup.select(".product_pod h3 a") # Links to product pages

            if not prods: break

            for prod in prods:
                href = prod.get("href")
                # Site uses relative links like "../../../", normalize to absolute
                abs_url = urljoin(BASE_URL + "catalogue/", href)
                slug = re.sub(r'[/\\]', '_', href.split('/')[-2])
                if slug in seen:
                    continue
                seen.add(slug)
                product_tasks.append((abs_url, slug))
                product_count += 1
                if product_count >= TOTAL_PRODUCTS_WANTED:
                    break
            if product_count >= TOTAL_PRODUCTS_WANTED:
                break
            page += 1

        logging.info(f"Collected {len(product_tasks)} to fetch; starting...")

        # Now fetch all product pages
        fetch_tasks = [
            fetch_product(session, prod_url, product_id)
            for prod_url, product_id in product_tasks
        ]
        # Don't overrun concurrency!
        results = []
        for i in range(0, len(fetch_tasks), CONCURRENCY):
            batch = fetch_tasks[i:i+CONCURRENCY]
            batch_results = await asyncio.gather(*batch)
            results.extend(batch_results)
        return results

if __name__ == "__main__":
    asyncio.run(crawl_all_products())