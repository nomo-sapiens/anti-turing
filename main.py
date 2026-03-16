#!/usr/bin/env python3
"""Anti-Turing: Reverse Turing Test Game — Entry Point"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt

from config import GAME_MODES, DEFAULT_MODE
from game import run_game

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


def get_human_name() -> str:
    console.print()
    name = Prompt.ask("Enter your player name", default="Human").strip()
    if not name:
        name = "Human"
    return name


def play_again() -> bool:
    console.print()
    answer = Prompt.ask("Play again?", choices=["y", "n"], default="n")
    return answer.lower() == "y"


def main() -> None:
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
