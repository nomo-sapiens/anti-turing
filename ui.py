from __future__ import annotations

import time

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box
from rich.prompt import Prompt

console = Console()

# Color palette for player names (cycling)
PLAYER_COLORS = [
    "cyan", "yellow", "green", "magenta", "blue", "bright_red",
    "bright_cyan", "bright_yellow",
]

HUMAN_COLOR = "bright_white"


def _player_color(name: str, name_list: list[str]) -> str:
    try:
        idx = name_list.index(name)
        return PLAYER_COLORS[idx % len(PLAYER_COLORS)]
    except ValueError:
        return "white"


def clear() -> None:
    console.clear()


def print_header(round_num: int, total_rounds: int, topic: str, alive_players: list[str], human_name: str) -> None:
    title = Text()
    title.append("ANTI-TURING", style="bold bright_red")
    title.append("  |  Round ", style="dim")
    title.append(str(round_num), style="bold white")
    title.append(f" of {total_rounds}", style="dim")

    console.print()
    console.print(Panel(title, expand=False, border_style="bright_red"))

    # Topic
    topic_text = Text()
    topic_text.append("TOPIC: ", style="bold yellow")
    topic_text.append(topic, style="italic white")
    console.print(Panel(topic_text, expand=True, border_style="yellow"))

    # Players sidebar
    _print_players(alive_players, human_name)
    console.print()


def _print_players(alive_players: list[str], human_name: str) -> None:
    table = Table(box=box.SIMPLE, show_header=False, pad_edge=False)
    table.add_column("player", style="white")
    table.add_column("status", style="green")

    for name in alive_players:
        if name == human_name:
            table.add_row(f"[bold {HUMAN_COLOR}]{name}[/] (you)", "[green]alive[/]")
        else:
            color = _player_color(name, alive_players)
            table.add_row(f"[{color}]{name}[/]", "[green]alive[/]")

    console.print(Panel(table, title="Players", border_style="dim", expand=False))


def print_chat_message(speaker: str, text: str, all_names: list[str], human_name: str, is_human: bool = False) -> None:
    if is_human:
        color = HUMAN_COLOR
        label = f"[bold {color}]{speaker}[/] [dim](you)[/]"
    else:
        color = _player_color(speaker, all_names)
        label = f"[bold {color}]{speaker}[/]"

    console.print(f"  {label}: {text}")


def prompt_human_message(human_name: str) -> str:
    console.print()
    text = Prompt.ask(f"  [bold bright_white]{human_name}[/] [dim](you)[/]")
    return text.strip()


def prompt_human_vote(human_name: str, candidates: list[str]) -> str:
    console.print()
    console.print(Panel(
        "[bold yellow]VOTE TIME[/]\nWho do you think will get the most votes? Vote for someone to blend in.",
        border_style="yellow",
        expand=False,
    ))
    for i, name in enumerate(candidates, 1):
        console.print(f"  [dim]{i}.[/] {name}")
    console.print()

    while True:
        choice = Prompt.ask("  Your vote (name or number)")
        # Try number
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                return candidates[idx]
        # Try name (partial match)
        for name in candidates:
            if name.lower().startswith(choice.lower()):
                return name
        console.print("  [red]Invalid choice, try again.[/]")


def print_vote_reveal(votes: dict[str, str], reasons: dict[str, str], eliminated: str, human_name: str, all_names: list[str]) -> None:
    console.print()
    console.print(Panel("[bold red]VOTE RESULTS[/]", border_style="red", expand=False))
    time.sleep(0.5)

    # Tally
    tally: dict[str, int] = {}
    for voted in votes.values():
        tally[voted] = tally.get(voted, 0) + 1

    for voter, voted in sorted(votes.items()):
        color = _player_color(voter, all_names)
        voted_color = _player_color(voted, all_names) if voted != human_name else HUMAN_COLOR
        reason = reasons.get(voter, "")
        console.print(f"  [bold {color}]{voter}[/] voted for [bold {voted_color}]{voted}[/]  [dim]— {reason}[/]")
        time.sleep(0.3)

    console.print()
    time.sleep(0.4)

    elim_color = _player_color(eliminated, all_names) if eliminated != human_name else HUMAN_COLOR
    console.print(f"  [bold red]ELIMINATED:[/] [bold {elim_color}]{eliminated}[/]")
    console.print()


def print_round_separator() -> None:
    console.print()
    console.rule(style="dim")
    console.print()


def print_game_over_lose(round_num: int) -> None:
    console.print()
    console.print(Panel(
        "[bold red]GAME OVER — YOU WERE IDENTIFIED[/]\n\n"
        f"[dim]You survived {round_num - 1} round(s) before being voted out.[/]\n\n"
        "[italic]The AIs saw through you. Better luck next time.[/]",
        border_style="red",
        expand=False,
    ))
    console.print()


def print_game_over_win(rounds_survived: int) -> None:
    console.print()
    console.print(Panel(
        "[bold bright_green]YOU WIN — YOU FOOLED ALL THE AIs![/]\n\n"
        f"[dim]You survived {rounds_survived} round(s) and outlasted every agent.[/]\n\n"
        "[italic]Congratulations. You are the last one standing.[/]",
        border_style="bright_green",
        expand=False,
    ))
    console.print()


def print_section(title: str) -> None:
    console.print()
    console.print(f"[bold dim]{'─' * 4} {title} {'─' * 4}[/]")
    console.print()


def print_info(msg: str) -> None:
    console.print(f"  [dim]{msg}[/]")


def print_thinking(agent_name: str) -> None:
    console.print(f"  [dim]{agent_name} is typing...[/]", end="\r")
