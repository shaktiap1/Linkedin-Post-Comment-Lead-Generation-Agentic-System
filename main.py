import asyncio

from scraper.browser import BrowserManager
from scraper.linkedin_login import LinkedInLogin
from scraper.comment_scroller import CommentScroller
from scraper.comment_extractor import CommentExtractor
from scraper.lead_processor import LeadProcessor

from utils.logger import get_logger
from config.settings import LINKEDIN_EMAIL, LINKEDIN_PASSWORD, POST_URL


logger = get_logger(__name__)


async def run():

    browser_manager = BrowserManager()

    browser, page = await browser_manager.start()

    try:

        # -------------------------------
        # STEP 1: LOGIN
        # -------------------------------

        login = LinkedInLogin(page)

        await login.login(LINKEDIN_EMAIL, LINKEDIN_PASSWORD)


        # -------------------------------
        # STEP 2: OPEN POST + SCROLL
        # -------------------------------

        scroller = CommentScroller(page)

        await scroller.open_post(POST_URL)

        await scroller.scroll_comments()


        # -------------------------------
        # STEP 3: EXTRACT COMMENTS
        # -------------------------------

        extractor = CommentExtractor(page)

        comments = await extractor.extract_comments()

        logger.info(f"Total raw comments extracted: {len(comments)}")

        print(comments)


        # -------------------------------
        # STEP 4: PROCESS LEADS
        # -------------------------------

        processor = LeadProcessor(comments)

        unique_leads = processor.remove_duplicates()

        logger.info(f"Unique leads found: {len(unique_leads)}")


        # -------------------------------
        # STEP 5: EXPORT CSV
        # -------------------------------

        processor.export_csv(unique_leads)

        logger.info("Lead extraction pipeline completed successfully")


    finally:

        await browser_manager.close()


if __name__ == "__main__":

    asyncio.run(run())