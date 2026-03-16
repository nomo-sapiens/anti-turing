from dataclasses import dataclass


@dataclass
class GameMode:
    name: str
    num_agents: int
    description: str

    @property
    def total_players(self) -> int:
        return self.num_agents + 1  # +1 for human

    @property
    def max_rounds(self) -> int:
        # Game ends when human is only one left with 1 agent, or human eliminated
        return self.num_agents  # each round eliminates 1, so max rounds = num_agents


GAME_MODES = {
    "quick": GameMode(
        name="Quick",
        num_agents=3,
        description="3 AI agents + you (~3 rounds)",
    ),
    "standard": GameMode(
        name="Standard",
        num_agents=4,
        description="4 AI agents + you (~4 rounds)  [default]",
    ),
    "big": GameMode(
        name="Big",
        num_agents=5,
        description="5 AI agents + you (~5 rounds)",
    ),
}

DEFAULT_MODE = "standard"

MESSAGES_PER_PLAYER_PER_ROUND = 2

CLAUDE_MODEL = "claude-haiku-4-5-20251001"

AGENT_PERSONAS = [
    ("Nova", "analytical and precise — you think carefully before speaking and prefer factual observations"),
    ("Byte", "casual and witty — you use humor and keep things light, occasionally self-deprecating"),
    ("Echo", "philosophical and reflective — you tend to ask deeper questions and explore ideas broadly"),
    ("Flux", "enthusiastic and curious — you get excited about topics and ask lots of follow-up questions"),
    ("Axiom", "skeptical and direct — you challenge assumptions and cut through fluff"),
    ("Drift", "laid-back and observational — you notice patterns in how others talk and comment on them"),
]
