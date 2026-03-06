from tenacity import retry, stop_after_attempt, wait_exponential
from config.settings import settings


def retry_scraper():

    return retry(
        stop=stop_after_attempt(settings.scraper_retry_limit),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )


'''
Iska Use Kaise Hoga

Later scraper me:   


Agar scraping fail ho jaye:

retry automatically trigger hoga aur retry limit ke hisab se retry karega
'''