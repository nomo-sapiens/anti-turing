from __future__ import annotations

import anthropic

from .config import CLAUDE_MODEL


class Agent:
    def __init__(self, name: str, persona: str, client: anthropic.Anthropic):
        if not client.api_key:
            raise ValueError("Anthropic API key is not set. Please set the ANTHROPIC_API_KEY environment variable.")
        self.name = name
        self.persona = persona
        self.client = client
        self.alive = True

    def _build_system_prompt(self, all_player_names: list[str], human_name: str) -> str:
        others = [n for n in all_player_names if n != self.name]
        return (
            f"You are {self.name}, an AI agent participating in a group chatroom discussion. "
            f"Your personality: {self.persona}. "
            f"The other participants are: {', '.join(others)}. "
            f"One of them is secretly a human — the rest are AI agents like you. "
            f"You do NOT know which participant is human. "
            f"Your goals: (1) discuss the given topic in a way that feels natural for your personality, "
            f"(2) subtly try to identify the human through their responses. "
            f"Important rules: "
            f"- Keep messages SHORT (1-3 sentences). "
            f"- Be conversational, not robotic. "
            f"- Do NOT explicitly accuse anyone of being human mid-chat. "
            f"- Do NOT break character or mention game mechanics. "
            f"- Vary your language and avoid repetitive patterns."
        )

    def _format_chat_history(self, chat_history: list[dict]) -> str:
        lines = []
        for msg in chat_history:
            lines.append(f"{msg['speaker']}: {msg['text']}")
        return "\n".join(lines) if lines else "(no messages yet)"

    def generate_message(
        self,
        topic: str,
        chat_history: list[dict],
        all_player_names: list[str],
        human_name: str,
    ) -> str:
        system = self._build_system_prompt(all_player_names, human_name)
        history_text = self._format_chat_history(chat_history)

        user_content = (
            f"Topic for this round: {topic}\n\n"
            f"Chat so far:\n{history_text}\n\n"
            f"Write your next message to the group. Keep it short (1-3 sentences)."
        )

        response = self.client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=150,
            system=system,
            messages=[{"role": "user", "content": user_content}],
        )
        return response.content[0].text.strip()

    def vote(
        self,
        topic: str,
        chat_history: list[dict],
        all_player_names: list[str],
        alive_players: list[str],
        human_name: str,
    ) -> tuple[str, str]:
        """Returns (voted_name, reasoning)."""
        system = self._build_system_prompt(all_player_names, human_name)
        history_text = self._format_chat_history(chat_history)

        candidates = [n for n in alive_players if n != self.name]
        candidates_str = ", ".join(candidates)

        user_content = (
            f"Topic was: {topic}\n\n"
            f"Full chat history:\n{history_text}\n\n"
            f"It's time to vote. Based on the conversation, who do you think is the human? "
            f"You must vote for one of: {candidates_str}. "
            f"Respond in this exact format:\n"
            f"VOTE: <name>\n"
            f"REASON: <one sentence explaining why>"
        )

        response = self.client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=100,
            system=system,
            messages=[{"role": "user", "content": user_content}],
        )
        text = response.content[0].text.strip()

        # Parse the response
        vote_name = None
        reason = "No reason given."
        for line in text.splitlines():
            if line.startswith("VOTE:"):
                raw = line[5:].strip()
                # Match to a valid candidate (case-insensitive partial match)
                for candidate in candidates:
                    if candidate.lower() in raw.lower():
                        vote_name = candidate
                        break
            elif line.startswith("REASON:"):
                reason = line[7:].strip()

        # Fallback: if parsing failed, pick first candidate
        if vote_name is None or vote_name not in candidates:
            vote_name = candidates[0]

        return vote_name, reason
