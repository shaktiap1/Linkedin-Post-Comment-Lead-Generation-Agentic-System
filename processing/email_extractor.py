import re
from typing import List, Dict, Optional


class EmailExtractor:

    EMAIL_REGEX = re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    )

    def __init__(self, comments: List[Dict]):
        self.comments = comments

    def extract(self) -> List[Dict]:
        """
        Extract email addresses from comment text.
        """

        processed_comments = []

        for comment in self.comments:

            text = comment.get("comment_text", "")
            email = self._extract_email(text)

            processed_comment = {
                "commenter_name": comment.get("commenter_name"),
                "commenter_profile_url": comment.get("commenter_profile_url"),
                "comment_text": text,
                "email": email
            }

            processed_comments.append(processed_comment)

        return processed_comments

    def _extract_email(self, text: str) -> Optional[str]:
        """
        Return first email found in text.
        """

        if not text:
            return None

        match = self.EMAIL_REGEX.search(text)

        if match:
            return match.group(0)

        return None