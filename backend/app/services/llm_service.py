"""
LLM Service - Gemini Integration with Fallback
Handle all LLM interactions with automatic failover
"""
import google.generativeai as genai
from openai import OpenAI
from anthropic import Anthropic
from typing import Dict, Any, Optional, List
import json

from app.config import settings


class LLMService:
    """Manage LLM interactions with fallback mechanism"""
    
    def __init__(self):
        # Configure Gemini (primary)
        genai.configure(api_key=settings.gemini_api_key)
        self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Configure fallbacks
        self.openai_client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
        self.claude_client = Anthropic(api_key=settings.claude_api_key) if settings.claude_api_key else None
    
    def _call_gemini(self, prompt: str, temperature: float = 0.7) -> str:
        """Call Gemini API"""
        response = self.gemini_model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
            )
        )
        return response.text
    
    def _call_openai(self, prompt: str, temperature: float = 0.7) -> str:
        """Call OpenAI API as fallback"""
        if not self.openai_client:
            raise Exception("OpenAI API key not configured")
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return response.choices[0].message.content
    
    def _call_claude(self, prompt: str, temperature: float = 0.7) -> str:
        """Call Claude API as fallback"""
        if not self.claude_client:
            raise Exception("Claude API key not configured")
        
        response = self.claude_client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return response.content[0].text
    
    def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """
        Generate text with automatic fallback
        Tries: Gemini → OpenAI → Claude
        """
        try:
            return self._call_gemini(prompt, temperature)
        except Exception as e:
            print(f"⚠️ Gemini failed: {e}. Trying OpenAI...")
            try:
                return self._call_openai(prompt, temperature)
            except Exception as e2:
                print(f"⚠️ OpenAI failed: {e2}. Trying Claude...")
                return self._call_claude(prompt, temperature)
    
    def extract_structured_data(self, raw_text: str) -> Dict[str, Any]:
        """
        Extract structured data from daily log text
        Returns: concepts, activities, assignments, mood, difficulty
        """
        prompt = f"""Extract structured information from this internship daily log:

TEXT:
{raw_text}

Extract and return ONLY a valid JSON object with this structure:
{{
  "concepts": ["concept1", "concept2", ...],
  "activities": [
    {{"type": "coding/debugging/learning/meeting", "description": "...", "duration_minutes": 60}}
  ],
  "assignments": [
    {{"title": "...", "description": "...", "due_date": "YYYY-MM-DD or null"}}
  ],
  "mood": "positive/neutral/negative/frustrated/excited",
  "difficulty_level": "easy/medium/hard",
  "key_learnings": ["learning1", "learning2", ...]
}}

Be precise and extract only what's clearly mentioned. Return ONLY the JSON, no other text."""

        response = self.generate(prompt, temperature=0.3)
        
        # Parse JSON response
        try:
            # Extract JSON from response (in case there's extra text)
            start = response.find('{')
            end = response.rfind('}') + 1
            json_str = response[start:end]
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"⚠️ Failed to parse JSON: {e}")
            # Return default structure
            return {
                "concepts": [],
                "activities": [],
                "assignments": [],
                "mood": "neutral",
                "difficulty_level": "medium",
                "key_learnings": []
            }
    
    def generate_summary(self, data: Dict[str, Any], mode: str = "daily") -> str:
        """
        Generate summaries for VTU diary
        Modes: daily, weekly, monthly
        """
        if mode == "weekly":
            prompt = f"""Generate a professional weekly internship diary entry for VTU submission.

DATA:
{json.dumps(data, indent=2)}

Write in first-person, past tense, formal academic tone. Include:
- Overview of the week
- Key concepts learned
- Projects/tasks completed
- Challenges faced and solutions
- Skills developed

Length: 300-400 words. Make it sound human-written, not AI-generated."""
        
        elif mode == "daily":
            prompt = f"""Generate a professional daily internship diary entry for VTU submission.

DATA:
{json.dumps(data, indent=2)}

Write in first-person, past tense, formal tone. Include:
- What I worked on
- What I learned
- Challenges and solutions

Length: 150-200 words."""
        
        else:  # monthly
            prompt = f"""Generate a professional monthly internship report for VTU submission.

DATA:
{json.dumps(data, indent=2)}

Write in first-person, formal academic tone. Include:
- Monthly overview
- Major achievements
- Technical skills acquired
- Projects completed
- Future goals

Length: 500-600 words."""
        
        return self.generate(prompt, temperature=0.7)
    
    def explain_concept(self, concept_name: str, user_context: Dict[str, Any]) -> str:
        """
        Explain a concept with identity-aware personalization
        user_context: {learned_concepts: [], past_mistakes: [], current_level: ""}
        """
        learned = user_context.get("learned_concepts", [])
        mistakes = user_context.get("past_mistakes", [])
        
        prompt = f"""Explain the concept "{concept_name}" to an intern learning it.

IMPORTANT CONTEXT:
- They already know: {', '.join(learned) if learned else 'basic programming'}
- Common mistakes they make: {', '.join(mistakes) if mistakes else 'none recorded'}

Provide:
1. Clear definition
2. How it relates to what they already know
3. Practical example
4. Common pitfalls (especially relevant to their past mistakes)

Keep it conversational, encouraging, and practical. Maximum 250 words."""
        
        return self.generate(prompt, temperature=0.7)
    
    def generate_guidance(self, user_history: Dict[str, Any]) -> str:
        """
        Generate learning guidance and next steps
        """
        prompt = f"""Based on this learner's internship history, suggest what they should learn next.

HISTORY:
{json.dumps(user_history, indent=2)}

Provide:
1. Assessment of current progress
2. Recommended next topics to learn
3. Prioritization and reasoning
4. Specific resources or practice suggestions

Be encouraging and specific. Maximum 200 words."""
        
        return self.generate(prompt, temperature=0.7)


# Global instance
llm_service = LLMService()
