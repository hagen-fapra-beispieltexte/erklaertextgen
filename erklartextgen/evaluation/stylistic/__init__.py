import openai
import json

DEFAULT_MODEL = "gpt-4o"
PROMPT = """
Evaluate the following text on the following dimensions on a scale from 1 to 5: 
1. Fluidity:
   1: Very choppy and disjointed.
   2: Choppy with noticeable interruptions.
   3: Fairly fluid with some minor disruptions.
   4: Mostly fluid with few interruptions.
   5: Very fluid and natural.
2. Liveliness:
   1: Very dry and boring.
   2: Quite dry with limited liveliness.
   3: Moderately lively, somewhat interesting.
   4: Mostly lively and engaging.
   5: Very lively and captivating.
3. Engagement Level:
   1: Very dull, not engaging.
   2: Quite dull, minimally engaging.
   3: Moderately engaging, somewhat captivating.
   4: Mostly engaging and captivating.
   5: Very engaging and captivating.
4. Suitability for Children:
   1: Not suitable for children, inappropriate content.
   2: Mostly unsuitable, with some inappropriate elements.
   3: Moderately suitable, generally acceptable from age 16 and up.
   4: Mostly suitable, appropriate for most children from age 12 and up.
   5: Very suitable for children, entirely appropriate vor children of every age.
Provide only the numerical scores in JSON format with the fields: 'fluidity_score', 'liveliness_score', 'engagement_score', 'suitability_score'.
"""


class GPT4StyleEvaluator:
    def __init__(self, api_key, model="gpt-4o"):
        self.model = model
        self.client = openai.OpenAI(api_key=api_key)

    def evaluate(self, text):
        """
        Evaluates the style of a text based on
        - fluidity
        - liveliness
        - engagement level
        - suitability for children

        Returns an empty dict if the response parsing failed.
        """

        messages = [{"role": "user", "content": f"{PROMPT}\n\n{text}"}]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=150,
            temperature=0.7,
            response_format={"type": "json_object"},
        )

        # Extracts and processes the response
        response_content = response.choices[0].message.content.strip()
        try:
            style_evaluation = json.loads(response_content)
        except (json.JSONDecodeError, AssertionError):
            style_evaluation = {}

        return style_evaluation
