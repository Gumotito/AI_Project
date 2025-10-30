"""
Engagement Agent
Suggests follow-up prompts to deepen user engagement based on the initial prompt and (optionally) the first answer.
"""

import logging
from typing import Optional
from services.llm_service import get_llm_service
from services.guardrails import get_guardrails, GuardrailViolation

logger = logging.getLogger(__name__)


class EngagementAgent:
    """Agent focused on prompting continued interaction."""

    def __init__(self):
        self.name = "Engagement Agent"
        self.llm = get_llm_service()
        self.guardrails = get_guardrails()
        logger.info(f"{self.name} initialized")

    async def suggest_followup(self, prompt: str, answer: Optional[str] = None, prev: Optional[str] = None) -> str:
        """
        Suggest a single short, engaging follow-up prompt.
        Requirements:
        - One question only
        - Max ~120 characters
        - Build on the user's intent without repeating it verbatim
        - Encourage action, specificity, or comparison
        """
        system = (
            "You help keep a conversation going by proposing one smart follow-up question. "
            "Constraints: output ONLY the question (no preface), <= 120 characters, "
            "avoid repeating the user's exact wording, deepen or operationalize their intent. "
            + ("Do NOT repeat or paraphrase the previous suggestion; pick a different angle. " if prev else "")
            + "Favor variety across: measurement, comparison, next step, challenge, zoom-in, zoom-out."
        )
        user = (
            f"User prompt: {prompt}\n"
            + (f"Assistant answer: {answer}\n" if answer else "")
            + (f"Previous suggestion: {prev}\n" if prev else "")
            + "Return ONE short follow-up question only."
        )
        try:
            suggestion = await self.llm.generate(user, system_message=system, timeout=12.0)
            # Post-process: keep it to one line, trim quotes
            suggestion = suggestion.strip().splitlines()[0].strip()
            if suggestion.startswith(("- ", "• ", "* ")):
                suggestion = suggestion[2:].strip()
            if suggestion.startswith("\"") and suggestion.endswith("\"") and len(suggestion) > 1:
                suggestion = suggestion[1:-1].strip()
            # Hard cap length
            if len(suggestion) > 160:
                suggestion = suggestion[:157].rstrip() + "…"
            # Ensure it ends with a question mark for clarity
            if not suggestion.endswith("?"):
                suggestion = suggestion.rstrip(".!") + "?"
            
            # Validate follow-up
            is_valid, error = self.guardrails.validate_followup(suggestion)
            if not is_valid:
                logger.warning(f"Invalid follow-up generated: {error}")
                suggestion = f"What else would you like to know about {prompt[:50]}?"
            
            # Check for harmful content
            try:
                suggestion = self.guardrails.validate_output(suggestion, self.name)
            except GuardrailViolation:
                logger.error("Harmful follow-up generated, using safe fallback")
                suggestion = "What would you like to explore next?"
            
            return suggestion
        except Exception as e:
            logger.error(f"Follow-up suggestion failed: {e}")
            # Fallback heuristic if LLM unavailable
            base = prompt.strip().rstrip("?.!")
            return f"What would be the next concrete step to explore about '{base[:60]}…' ?"
