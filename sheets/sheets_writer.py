import csv
from typing import List, Dict

import gspread
from google.oauth2.service_account import Credentials

from utils.logger import get_logger


logger = get_logger(__name__)


class SheetsWriter:

    def __init__(self, service_account_file: str, sheet_name: str):

        self.service_account_file = service_account_file
        self.sheet_name = sheet_name

    def write(self, leads: List[Dict]):

        if not leads:
            logger.warning("No leads to write")
            return

        try:
            self._write_to_sheets(leads)
        except Exception as e:

            logger.error("Google Sheets write failed")
            logger.error(str(e))

        # Always write CSV backup
        self._write_csv(leads)

    def _write_to_sheets(self, leads: List[Dict]):

        logger.info("Writing leads to Google Sheets")

        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        credentials = Credentials.from_service_account_file(
            self.service_account_file,
            scopes=scope
        )

        client = gspread.authorize(credentials)

        sheet = client.open(self.sheet_name).sheet1

        rows = []

        for lead in leads:

            rows.append([
                lead.get("extracted_at"),
                lead.get("post_url"),
                lead.get("commenter_name"),
                lead.get("commenter_profile_url"),
                lead.get("comment_text"),
                lead.get("email")
            ])

        sheet.append_rows(rows)

        logger.info(f"{len(rows)} leads written to Google Sheets")

    def _write_csv(self, leads: List[Dict]):

        logger.info("Writing CSV backup")

        file_name = "leads_backup.csv"

        headers = [
            "extracted_at",
            "post_url",
            "commenter_name",
            "commenter_profile_url",
            "comment_text",
            "email"
        ]

        with open(file_name, "w", newline="", encoding="utf-8") as file:

            writer = csv.DictWriter(file, fieldnames=headers)

            writer.writeheader()

            writer.writerows(leads)

        logger.info("CSV backup saved")