import anthropic
from typing import List, Dict
import os


class AIService:
    """Service for AI operations using Claude API"""

    def __init__(self):
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-20250514"

    def generate_tags_and_summary(self, title: str, content: str) -> Dict[str, any]:
        """
        Generate tags and summary for a document

        Returns:
            {
                'tags': ['tag1', 'tag2', ...],
                'summary': 'Brief summary text...'
            }
        """
        prompt = f"""Analyze this document and provide:
1. A list of 3-5 relevant tags (single words or short phrases, lowercase)
2. A brief summary (2-3 sentences)

Document Title: {title}

Document Content:
{content}

Respond in JSON format:
{{
    "tags": ["tag1", "tag2", "tag3"],
    "summary": "Brief summary here..."
}}"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract text from response
            response_text = message.content[0].text

            # Parse JSON from response
            import json
            # Remove markdown code blocks if present
            response_text = response_text.strip()
            if response_text.startswith('```'):
                # Remove first and last line (```json and ```)
                lines = response_text.split('\n')
                response_text = '\n'.join(lines[1:-1])

            result = json.loads(response_text)

            return {
                'tags': result.get('tags', []),
                'summary': result.get('summary', '')
            }

        except Exception as e:
            print(f"AI Service Error: {e}")
            # Return empty results on error (graceful degradation)
            return {
                'tags': [],
                'summary': ''
            }

    def generate_tags(self, title: str, content: str) -> List[str]:
        """Generate only tags (backward compatibility)"""
        result = self.generate_tags_and_summary(title, content)
        return result['tags']

    def generate_summary(self, content: str) -> str:
        """Generate only summary (backward compatibility)"""
        result = self.generate_tags_and_summary("", content)
        return result['summary']