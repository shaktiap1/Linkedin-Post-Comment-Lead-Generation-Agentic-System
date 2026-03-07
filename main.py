import asyncio

from scraper.browser import BrowserManager
from scraper.linkedin_login import LinkedInLogin
from scraper.comment_scroller import CommentScroller
from scraper.comment_extractor import CommentExtractor

from processing.comment_normalizer import CommentNormalizer
from processing.email_extractor import EmailExtractor
from processing.deduplicator import LeadDeduplicator
from processing.lead_builder import LeadBuilder

from sheets.sheets_writer import SheetsWriter

from config.settings import settings
from utils.logger import get_logger


logger = get_logger(__name__)

POST_URL = "https://www.linkedin.com/posts/shaktesh-pandey-3a2936245_most-transformed-students-award-goes-to-activity-7434753641732939776-P5bp?utm_source=share&utm_medium=member_desktop&rcm=ACoAADzUGaoBsNWoHsC-PjTuvyq3zhztiMg0GB4"


async def run():

    logger.info("Starting LinkedIn Lead Extraction System")

    browser_manager = BrowserManager()

    page = await browser_manager.start()

    try:

        # LOGIN
        login = LinkedInLogin(page)
        await login.login()

        # OPEN POST
        scroller = CommentScroller(page)
        await scroller.open_post(POST_URL)
        await scroller.scroll_comments()

        # EXTRACT COMMENTS
        extractor = CommentExtractor(page)
        comments = await extractor.extract_comments()

        logger.info(f"Extracted {len(comments)} raw comments")

        # NORMALIZE
        normalizer = CommentNormalizer(comments)
        normalized_comments = normalizer.normalize()

        # EMAIL EXTRACTION
        email_extractor = EmailExtractor(normalized_comments)
        comments_with_email = email_extractor.extract()

        # DEDUPLICATION
        deduplicator = LeadDeduplicator(
            comments_with_email,
            POST_URL
        )

        unique_comments = deduplicator.deduplicate()

        logger.info(f"{len(unique_comments)} comments after deduplication")

        # BUILD LEADS
        builder = LeadBuilder(unique_comments, POST_URL)
        leads = builder.build()

        logger.info(f"{len(leads)} structured leads generated")

        # OUTPUT
        writer = SheetsWriter(
        settings.google_service_account_file,
        settings.google_sheet_name
)

        writer.write(leads)

        logger.info("Lead export completed")

    finally:

        await browser_manager.close()


if __name__ == "__main__":
    asyncio.run(run())