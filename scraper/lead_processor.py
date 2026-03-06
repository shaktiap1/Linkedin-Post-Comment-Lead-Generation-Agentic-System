from utils.logger import get_logger
import csv

logger = get_logger(__name__)


class LeadProcessor:

    def __init__(self, comments):
        self.comments = comments


    def remove_duplicates(self):

        logger.info("Removing duplicate commenters")

        unique = {}
        
        for comment in self.comments:

            profile = comment["commenter_profile_url"]

            if profile not in unique:
                unique[profile] = comment

        unique_comments = list(unique.values())

        logger.info(f"Unique commenters: {len(unique_comments)}")

        return unique_comments


    def export_csv(self, data, filename="linkedin_leads.csv"):

        logger.info("Exporting leads to CSV")

        keys = ["commenter_name", "commenter_profile_url", "comment_text"]

        with open(filename, "w", newline="", encoding="utf-8") as f:

            writer = csv.DictWriter(f, fieldnames=keys)

            writer.writeheader()

            for row in data:
                writer.writerow(row)

        logger.info(f"CSV exported: {filename}")