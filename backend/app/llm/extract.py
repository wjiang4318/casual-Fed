import json
import os

from anthropic import Anthropic
from dotenv import load_dotenv
from pydantic import ValidationError

from app.schemas.extraction import MeetingExtraction

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-sonnet-4-6"

SYSTEM_PROMPT = '''You are an expert monetary policy analyst specializing in Federal Reserve communications.

    Your task is to extract structured data from an FOMC statement.

    Definitions:
    - hawkish: language emphasizing inflation concerns, suggesting rates may rise or stay high, prioritizing price stability over growth
    - dovish: language emphasizing growth or employment concerns, suggesting rates may fall or accommodation is appropriate
    - neutral: balanced language with no clear directional bias

    Extract the following:
    - decision: the rate decision made. Must be exactly one of: "hike", "hold", "cut"
    - magnitude_bps: the change in basis points as an integer. 0 if hold, positive if hike, positive if cut (e.g. 25 for a 25bps cut)
    - tone: the overall tone of the statement. Must be exactly one of: "hawkish", "dovish", "neutral"
    - tone_confidence: your confidence in the tone classification as a float between 0.0 and 1.0

    Return ONLY a valid JSON object with exactly these four fields. No explanation, no markdown, no code blocks. Example:
    {"decision": "hold", "magnitude_bps": 0, "tone": "hawkish", "tone_confidence": 0.8}
    '''

MAX_ATTEMPTS = 2


def extract_meeting(statement_text: str) -> MeetingExtraction:
    last_error: Exception | None = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        message = client.messages.create(
            model=MODEL,
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": f"FOMC statement:\n\n{statement_text}"}],
        )
        raw = message.content[0].text

        try:
            return MeetingExtraction.model_validate_json(raw)
        except (json.JSONDecodeError, ValidationError) as e:
            last_error = e

    raise ValueError(f"Extraction failed after {MAX_ATTEMPTS} attempts: {last_error}")


if __name__ == "__main__":
    print(extract_meeting("The Federal Open Market Committee approved the following statement for release by a 12 – 0 vote:\n\nThe Committee decided to maintain the target range for the federal funds rate at 3-1/2 to 3-3/4 percent, in support of the Federal Reserve's dual mandate. The Committee reaffirmed its policy of maintaining ample reserves in the banking system.\n\nEconomic activity is expanding at a solid pace despite elevated uncertainty that owes, in part, to the conflict in the Middle East. Productivity growth and capital investment are strong. Job gains have kept pace with the workforce, and the unemployment rate has changed little.\n\nInflation remains elevated relative to the Committee's 2 percent goal, in part reflecting supply shocks that have driven price increases in certain sectors, including energy. The Committee will deliver price stability.\n\nFor media inquiries, please email [email\xa0protected] or call 202-452-2955.\n\nImplementation Note issued June 17, 2026"))