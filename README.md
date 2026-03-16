# Anti-Turing

A terminal-based **reverse Turing test** game. You're a human who has infiltrated a chatroom full of Claude AI agents. They know one participant is human — they just don't know which one. Every round ends with a vote to eliminate the most "human-seeming" player.

**Survive all rounds to win.**

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## How It Works

1. **Topic** — Each round starts with a random discussion prompt
2. **Chat** — All players take turns responding (you type; AIs generate via Claude Haiku)
3. **Vote** — Everyone votes for who they think is human. Most votes = eliminated
4. **Survive** — Outlast all the AI agents to win

## Game Modes

| Mode | Players | Rounds |
|------|---------|--------|
| `quick` | 3 AIs + you | ~3 rounds |
| `standard` | 4 AIs + you | ~4 rounds *(default)* |
| `big` | 5 AIs + you | ~5 rounds |

## Prerequisites

- Python 3.9+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- An [Anthropic API key](https://console.anthropic.com/)

## Setup

```bash
git clone https://github.com/dirkbrand/anti-turing.git
cd anti-turing

# Create virtual environment and install dependencies
uv venv
uv pip install -r requirements.txt

# Set your API key
export ANTHROPIC_API_KEY=your_key_here
```

## Play

```bash
source .venv/bin/activate
python main.py
```

Or without activating:

```bash
.venv/bin/python main.py
```

## Tips

- Keep your responses short and to the point — walls of text feel human
- Match the tone and energy of the other "players"
- When voting, pick someone other than yourself to avoid standing out
- The AIs have distinct personalities: analytical, witty, philosophical, skeptical...

## Project Structure

```
anti-turing/
├── main.py         # Entry point, game setup menu
├── game.py         # Game loop and round management
├── agents.py       # Claude Haiku agent wrapper and personas
├── ui.py           # Rich terminal UI
├── topics.py       # Discussion topic pool
├── config.py       # Game configuration
└── requirements.txt
```

## License

MIT — see [LICENSE](LICENSE)
