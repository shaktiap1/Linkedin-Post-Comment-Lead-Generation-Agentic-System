import asyncio
from scraper.browser import BrowserManager
from scraper.linkedin_login import LinkedInLogin


async def run():

    browser = BrowserManager()

    page = await browser.start()

    login = LinkedInLogin(page)

    await login.login()

    await asyncio.sleep(5)

    await browser.close()


asyncio.run(run())