import asyncio

from scraper.browser import BrowserManager
from scraper.linkedin_login import LinkedInLogin
from scraper.comment_scroller import CommentScroller


POST_URL = "https://www.linkedin.com/posts/shaktesh-pandey-3a2936245_most-transformed-students-award-goes-to-activity-7434753641732939776-P5bp?utm_source=share&utm_medium=member_desktop&rcm=ACoAADzUGaoBsNWoHsC-PjTuvyq3zhztiMg0GB4"


async def run():

    browser = BrowserManager()

    page = await browser.start()

    login = LinkedInLogin(page)

    await login.login()

    scroller = CommentScroller(page)

    await scroller.open_post(POST_URL)

    await scroller.scroll_comments()

    await asyncio.sleep(10)

    await browser.close()


asyncio.run(run())