import asyncio
from utils.logger import get_logger
from config.settings import settings

logger = get_logger(__name__)


class LinkedInLogin:

    def __init__(self, page):
        self.page = page

    async def login(self):

        logger.info("Navigating to LinkedIn login page")

        await self.page.goto("https://www.linkedin.com/login")

        await self.page.wait_for_selector("#username")

        logger.info("Entering credentials")

        await self.page.fill("#username", settings.linkedin_email)
        await self.page.fill("#password", settings.linkedin_password)

        await self.page.click("button[type='submit']")

        try:

            # Wait for LinkedIn feed search bar
            await self.page.wait_for_selector(
                "input[placeholder='Search']",
                timeout=10000
            )

            logger.info("LinkedIn login successful")

        except Exception:

            logger.error("Login verification failed")

        await asyncio.sleep(3)