import asyncio
from playwright.async_api import async_playwright

async def find_dollar_tickets():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("https://us.megabus.com")

        # Fill in trip details
        await page.locator("#searchOriginInput").fill("Chicago, IL")
        await page.locator("#searchDestinationInput").fill("Omaha, NE")
        await page.locator("#search-departure-date").fill("05/01/2025")

        # Click the Search button
        await page.locator("button:has-text('Search')").click()

        # Wait for results to load
        await page.wait_for_selector(".travel-depart__content", timeout=15000)

        # Scrape prices
        journey_boxes = await page.locator(".travel-depart__content").all()
        for box in journey_boxes:
            text = await box.inner_text()
            if "$1.00" in text:
                print("\nFound a $1 ticket!\n")
                print(text)
                print("-" * 40)

        await browser.close()

asyncio.run(find_dollar_tickets())
