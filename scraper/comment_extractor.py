from utils.logger import get_logger

logger = get_logger(__name__)


COMMENT_CONTAINER_SELECTORS = [
    "article.comments-comment-entity",
    ".comments-comment-entity",
    ".comments-comment-item",
]


NAME_SELECTORS = [
    "span.comments-comment-meta__description-title"
]


COMMENT_SELECTORS = [
    "span.break-words",
    ".comments-comment-item__main-content",
    ".feed-shared-comment__text",
]


PROFILE_SELECTORS = [
    'a[href*="/in/"]'
]


class CommentExtractor:

    def __init__(self, page):
        self.page = page

    async def extract_comments(self):

        logger.info("Extracting comments from page")

        try:
            await self.page.wait_for_selector(
                "article.comments-comment-entity",
                timeout=10000
            )
        except Exception:
            logger.warning("Comment containers not immediately found")

        containers = []

        for selector in COMMENT_CONTAINER_SELECTORS:

            containers = await self.page.query_selector_all(selector)

            if containers:
                logger.info(f"Found containers using selector: {selector}")
                break

        logger.info(f"Total comment containers: {len(containers)}")

        comments_data = []

        for container in containers:

            name = await self._extract_name(container)
            text = await self._extract_comment(container)
            profile = await self._extract_profile(container)

            if text:

                comments_data.append({
                    "commenter_name": name,
                    "commenter_profile_url": profile,
                    "comment_text": text
                })

        logger.info(f"Extracted {len(comments_data)} comments")

        return comments_data


    async def _extract_name(self, container):

        # PRIMARY selector (correct LinkedIn name location)
        element = await container.query_selector(
            "span.comments-comment-meta__description-title"
        )

        if element:

            try:
                name = (await element.inner_text()).strip()

                if name:
                    return name

            except Exception:
                pass

        # FALLBACK (in case LinkedIn changes DOM)
        anchor = await container.query_selector('a[href*="/in/"]')

        if anchor:

            try:
                aria = await anchor.get_attribute("aria-label")

                if aria and "View" in aria:
                    name = aria.replace("View", "").split("’")[0].strip()
                    return name

            except Exception:
                pass

        return None


    async def _extract_comment(self, container):

        for selector in COMMENT_SELECTORS:

            element = await container.query_selector(selector)

            if element:

                try:
                    text = (await element.inner_text()).strip()

                    if text:
                        return text

                except Exception:
                    continue

        return None


    async def _extract_profile(self, container):

        for selector in PROFILE_SELECTORS:

            element = await container.query_selector(selector)

            if element:

                try:
                    return await element.get_attribute("href")

                except Exception:
                    continue

        return None
'''
Why We Used Multiple Selectors

LinkedIn DOM frequently change karta hai.

Isliye fallback selector strategy use ki gayi:

selector 1 try
↓
selector 2 try
↓
selector 3 try

Yeh scraper ko self-healing behaviour deta hai.
'''