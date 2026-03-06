from typing import List, Dict
from datetime import datetime


class LeadBuilder:

    def __init__(self, comments: List[Dict], post_url: str):
        self.comments = comments
        self.post_url = post_url

    def build(self) -> List[Dict]:

        leads = []

        for comment in self.comments:

            lead = {
                "extracted_at": self._timestamp(),
                "post_url": self.post_url,
                "commenter_name": comment.get("commenter_name"),
                "commenter_profile_url": comment.get("commenter_profile_url"),
                "comment_text": comment.get("comment_text"),
                "email": comment.get("email")
            }

            leads.append(lead)

        return leads

    def _timestamp(self):

        return datetime.utcnow().isoformat()