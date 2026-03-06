import asyncio
from utils.logger import get_logger

logger = get_logger(__name__)


class CommentScroller:

    def __init__(self, page):
        self.page = page

    async def open_post(self, post_url):

        logger.info(f"Opening LinkedIn post: {post_url}")

        await self.page.goto(post_url)

        await asyncio.sleep(5)

    async def scroll_comments(self, max_scroll=10):

        logger.info("Starting comment scrolling")

        for i in range(max_scroll):

            logger.info(f"Scroll iteration {i+1}")

            # scroll down
            await self.page.mouse.wheel(0, 2000)

            await asyncio.sleep(2)

            # click load more comments if visible
            try:

                load_more = await self.page.query_selector(
                    "button[aria-label*='Load more comments']"
                )

                if load_more:

                    logger.info("Clicking load more comments")

                    await load_more.click()

                    await asyncio.sleep(2)

            except Exception:

                logger.warning("Load more comments button not found")

        logger.info("Finished scrolling comments")