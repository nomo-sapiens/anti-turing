# Anti-Turing

A terminal-based **reverse Turing test** game. You're a human who has infiltrated a chatroom full of Claude AI agents. They know one participant is human — they just don't know which one. Every round ends with a vote to eliminate the most "human-seeming" player.

**Survive all rounds to win.**

[![PyPI](https://img.shields.io/pypi/v/anti-turing)](https://pypi.org/project/anti-turing/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)

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

## Installation

```bash
pip install anti-turing
```

Or with [pipx](https://pipx.pypa.io/) (recommended for CLI tools — keeps it isolated):

```bash
pipx install anti-turing
```

## Requirements

**An Anthropic API key is required.** The agents are powered by Claude Haiku.

1. Get a key at [console.anthropic.com](https://console.anthropic.com/)
2. Set it in your environment before playing:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

Or create a `.env` file in your working directory:

```
ANTHROPIC_API_KEY=sk-ant-...
```

If the key is missing, the game will tell you exactly what to do.

## Play

```bash
anti-turing
```

## Tips

- Keep your responses short and to the point — walls of text feel human
- Match the tone and energy of the other "players"
- When voting, pick someone other than yourself to avoid standing out
- The AIs have distinct personalities: analytical, witty, philosophical, skeptical...

## Development Setup

```bash
git clone https://github.com/dirkbrand/anti-turing.git
cd anti-turing

uv venv
uv pip install -e ".[dev]"

# Set your API key
export ANTHROPIC_API_KEY=sk-ant-...

anti-turing
```

## Project Structure

```
anti-turing/
├── anti_turing/
│   ├── main.py         # Entry point, game setup menu
│   ├── game.py         # Game loop and round management
│   ├── agents.py       # Claude Haiku agent wrapper
│   ├── ui.py           # Rich terminal UI
│   ├── topics.py       # Discussion topic pool
│   └── config.py       # Game modes and personas
├── pyproject.toml
└── README.md
```

## License

MIT — see [LICENSE](LICENSE)
