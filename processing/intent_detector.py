from typing import List, Dict

from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


class IntentDetector:

    def __init__(self, comments: List[Dict]):
        self.comments = comments

        self.llm = ChatOpenAI(
            temperature=0,
            model="gpt-4o-mini"
        )

        self.prompt = PromptTemplate.from_template(
            """
Classify the intent of the following LinkedIn comment.

Possible labels:

Hiring
Collaboration
Product Interest
General
Spam

Return only one label.

Comment:
{comment}
"""
        )

    def detect(self) -> List[Dict]:

        processed = []

        for comment in self.comments:

            text = comment.get("comment_text", "")

            intent = self._detect_intent(text)

            processed.append({
                "commenter_name": comment.get("commenter_name"),
                "commenter_profile_url": comment.get("commenter_profile_url"),
                "comment_text": text,
                "email": comment.get("email"),
                "intent": intent
            })

        return processed

    def _detect_intent(self, text: str) -> str:

        if not text:
            return "General"

        chain = self.prompt | self.llm

        response = chain.invoke({"comment": text})

        return response.content.strip()
    

'''
How This Module Works

Pipeline flow:

Normalized comments
        ↓
Email extraction
        ↓
Intent detection
        ↓
Structured lead candidates
'''