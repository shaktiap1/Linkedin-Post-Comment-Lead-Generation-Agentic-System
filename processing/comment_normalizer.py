import re
from typing import List, Dict


class CommentNormalizer:

    def __init__(self, comments: List[Dict]):
        self.comments = comments

    def normalize(self) -> List[Dict]:
        """
        Normalize all comment texts.
        """

        normalized_comments = []

        for comment in self.comments:

            normalized_text = self._normalize_text(
                comment.get("comment_text", "")
            )

            normalized_comment = {
                "commenter_name": comment.get("commenter_name"),
                "commenter_profile_url": comment.get("commenter_profile_url"),
                "comment_text": normalized_text
            }

            normalized_comments.append(normalized_comment)

        return normalized_comments

    def _normalize_text(self, text: str) -> str:
        """
        Clean and normalize comment text.
        """

        if not text:
            return ""

        # Remove leading and trailing whitespace
        text = text.strip()

        # Replace multiple spaces with single space
        text = re.sub(r"\s+", " ", text)

        # Remove newlines and tabs
        text = text.replace("\n", " ").replace("\t", " ")

        return text