#!/usr/bin/env python3
"""Anti-Turing: Reverse Turing Test Game — Entry Point"""

import os
import sys

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt

load_dotenv()

from .config import GAME_MODES, DEFAULT_MODE
from .game import run_game

console = Console()


def print_title() -> None:
    console.clear()
    title = Text()
    title.append("ANTI-TURING\n", style="bold bright_red")
    title.append("Reverse Turing Test\n\n", style="dim")
    title.append(
        "You're a human joining a chatroom full of AIs.\n"
        "They know one of them is human — but not who.\n"
        "Each round, they vote to eliminate the most 'human-seeming' participant.\n\n"
        "Survive all rounds to win.",
        style="italic white",
    )
    console.print(Panel(title, border_style="bright_red", expand=False))
    console.print()


def select_mode() -> str:
    console.print("[bold]Choose a game mode:[/]\n")
    for key, mode in GAME_MODES.items():
        default_marker = " [dim](default)[/]" if key == DEFAULT_MODE else ""
        console.print(f"  [bold cyan]{key}[/]  — {mode.description}{default_marker}")
    console.print()

    while True:
        choice = Prompt.ask("Mode", default=DEFAULT_MODE).strip().lower()
        if choice in GAME_MODES:
            return choice
        console.print(f"  [red]Invalid mode. Choose from: {', '.join(GAME_MODES.keys())}[/]")


_TECHY_NAMES = [
    "Glitch", "Qubit", "Nexus", "Vortex", "Cipher", "Phantom",
    "Static", "Kernel", "Proxy", "Vector", "Entropy", "Daemon",
]


def get_human_name() -> str:
    import random
    default = random.choice(_TECHY_NAMES)
    console.print()
    name = Prompt.ask("Enter your player name", default=default).strip()
    if not name:
        name = default
    return name


def play_again() -> bool:
    console.print()
    answer = Prompt.ask("Play again?", choices=["y", "n"], default="n")
    return answer.lower() == "y"


def _check_api_key() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        console.print()
        console.print(Panel(
            "[bold red]ANTHROPIC_API_KEY is not set[/]\n\n"
            "Anti-Turing uses Claude AI to power the agents and requires an Anthropic API key.\n\n"
            "[bold]To fix this:[/]\n"
            "  1. Get a key at [link=https://console.anthropic.com]console.anthropic.com[/link]\n"
            "  2. Set it in your shell:\n\n"
            "     [bold cyan]export ANTHROPIC_API_KEY=sk-ant-...[/]\n\n"
            "  Or add it to a [bold].env[/] file in your working directory:\n\n"
            "     [bold cyan]ANTHROPIC_API_KEY=sk-ant-...[/]",
            border_style="red",
            title="[bold red]Missing API Key[/]",
            expand=False,
        ))
        console.print()
        sys.exit(1)


def main() -> None:
    _check_api_key()
    while True:
        print_title()
        mode_key = select_mode()
        mode = GAME_MODES[mode_key]
        human_name = get_human_name()

        console.print()
        console.print(
            f"  [dim]Starting {mode.name} game: {mode.num_agents} agents + you = "
            f"{mode.total_players} players[/]"
        )
        console.print()
        input("  Press Enter to begin...")

        run_game(mode, human_name)

        if not play_again():
            console.print("\n  [dim]Thanks for playing Anti-Turing.[/]\n")
            break


if __name__ == "__main__":
    main()
