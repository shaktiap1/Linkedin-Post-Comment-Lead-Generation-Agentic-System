import hashlib
from typing import List, Dict


class LeadDeduplicator:

    def __init__(self, comments: List[Dict], post_url: str):
        self.comments = comments
        self.post_url = post_url
        self.seen_hashes = set()

    def deduplicate(self) -> List[Dict]:

        unique_comments = []

        for comment in self.comments:

            hash_key = self._generate_hash(
                self.post_url,
                comment.get("commenter_profile_url"),
                comment.get("comment_text")
            )

            if hash_key not in self.seen_hashes:

                self.seen_hashes.add(hash_key)
                unique_comments.append(comment)

        return unique_comments

    def _generate_hash(self, post_url, profile_url, comment_text):

        raw_key = f"{post_url}|{profile_url}|{comment_text}"

        return hashlib.sha256(raw_key.encode()).hexdigest()
    


'''
How Deduplication Works

Example input:

[
 {"name": "Harpreet", "profile": "...", "comment": "Congrats"},
 {"name": "Harpreet", "profile": "...", "comment": "Congrats"},
 {"name": "Priyanshi", "profile": "...", "comment": "Amazing"}
]

Hash keys generated:

hash(post + harpreet + congrats)
hash(post + harpreet + congrats) ← duplicate
hash(post + priyanshi + amazing)

Output:

[
 {"name": "Harpreet", "profile": "...", "comment": "Congrats"},
 {"name": "Priyanshi", "profile": "...", "comment": "Amazing"}
]



Why Hashing Is Used

Hashing ensures:

O(1) duplicate detection

memory-efficient storage

fast lookups

Using:

SHA256

which is collision resistant.
'''