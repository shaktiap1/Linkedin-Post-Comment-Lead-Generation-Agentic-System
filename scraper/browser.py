from playwright.async_api import async_playwright
from utils.logger import get_logger

logger = get_logger(__name__)


class BrowserManager:

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    async def start(self):

        logger.info("Starting Playwright")

        self.playwright = await async_playwright().start()

        self.browser = await self.playwright.chromium.launch(
            headless=False
        )

        self.context = await self.browser.new_context()

        self.page = await self.context.new_page()

        logger.info("Browser launched successfully")

        return self.page

    async def close(self):

        logger.info("Closing browser")

        await self.browser.close()

        await self.playwright.stop()