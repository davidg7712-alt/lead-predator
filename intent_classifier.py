import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class IntentClassifier:
    """
    Analyzes review text to determine the level of urgency and intent.
    """
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def classify_review(self, review_text, niche="HVAC"):
        """
        Classifies a review into RED, ORANGE, or YELLOW tiers.
        """
        prompt = f"""
        Act as an Expert Lead Qualifier. Analyze the following Google Review for a {niche} business.
        Determine if the customer is a "Lost Sale" lead for the business they are reviewing.
        
        REVIEW: "{review_text}"
        
        CRITICAL RULE:
        Only classify as RED (Lead de Oro) if:
        1. The customer expresses a NEED but the business FAILED to fulfill it (No-show, didn't answer call, gave no quote, or was extremely late).
        2. The sale HAS NOT HAPPENED yet. If the customer complains about a service that WAS COMPLETED (e.g., "they fixed it but it was expensive" or "the technician was rude"), it is NOT a lead.
        
        TIER DEFINITIONS:
        - RED (Lead de Oro): High-intent. Customer is frustrated because they couldn't get the service. They are looking for someone else RIGHT NOW.
        - ORANGE: General inquiry or checking prices without immediate frustration.
        - YELLOW: Complaints AFTER a completed service. Not a lead for immediate sale.
        
        FORMAT: Return a JSON object with:
        {{
            "tier": "RED" | "ORANGE" | "YELLOW",
            "confidence": 0-100,
            "summary": "Short explanation of why this is a lost sale (or why it isn't)",
            "is_lead": boolean
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a lead generation intelligence engine. Be precise and conservative with 'RED' classifications."},
                    {"role": "user", "content": prompt}
                ],
                response_format={ "type": "json_object" }
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"{{\"error\": \"{str(e)}\"}}"

if __name__ == "__main__":
    classifier = IntentClassifier()
    # Test with a "No-show" example
    test_review = "Called them 3 hours ago for my AC emergency and they never showed up. Staying in a hotel tonight."
    print(classifier.classify_review(test_review))
