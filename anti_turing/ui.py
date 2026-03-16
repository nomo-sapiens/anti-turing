from __future__ import annotations

import time

from rich.console import Console
from rich.panel import Panel
from rich.padding import Padding
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


MAX_CHAT_LINES = 14


def clear() -> None:
    console.clear()


def print_room(players: list, round_num: int, topic: str) -> None:
    """Render the ASCII chatroom panel showing all players."""
    all_names = [p.name for p in players]

    cells: list[Text] = []
    for p in players:
        t = Text()
        if not p.alive:
            t.append("✗ ", style="dim red")
            t.append(p.name, style="dim strikethrough")
        elif p.is_human:
            t.append("★ ", style="bold bright_yellow")
            t.append(p.name, style=f"bold {HUMAN_COLOR}")
            t.append(" (you)", style="dim")
        else:
            color = _player_color(p.name, all_names)
            t.append("◎ ", style=f"bold {color}")
            t.append(p.name, style=f"bold {color}")
        cells.append(t)

    # Arrange in a 3-column grid
    grid = Table.grid(padding=(0, 3))
    for _ in range(3):
        grid.add_column(min_width=16)

    for i in range(0, len(cells), 3):
        row = list(cells[i : i + 3])
        while len(row) < 3:
            row.append(Text(""))
        grid.add_row(*row)

    alive_count = sum(1 for p in players if p.alive)

    console.print(
        Panel(
            Padding(grid, (1, 2)),
            title=f"[bold bright_red]ANTI-TURING[/]  [dim]·  Round {round_num}  ·  {alive_count} connected[/]",
            subtitle=f"[dim]▸[/] [italic white]{topic}[/]",
            border_style="bright_red",
        )
    )


def redraw_screen(
    players: list,
    round_num: int,
    topic: str,
    chat_history: list[dict],
    human_name: str,
    thinking_name: str | None = None,
) -> None:
    """Clear and redraw the room + recent chat messages."""
    clear()
    print_room(players, round_num, topic)
    print_section("DISCUSSION")

    all_names = [p.name for p in players]
    for msg in chat_history[-MAX_CHAT_LINES:]:
        is_human = msg["speaker"] == human_name
        print_chat_message(msg["speaker"], msg["text"], all_names, human_name, is_human=is_human)

    if thinking_name:
        console.print(f"\n  [dim]{thinking_name} is typing...[/]")


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


def prompt_human_vote(human_name: str, candidates: list[str]) -> tuple[str, str]:
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
        voted = None
        # Try number
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(candidates):
                voted = candidates[idx]
        # Try name (partial match)
        if voted is None:
            for name in candidates:
                if name.lower().startswith(choice.lower()):
                    voted = name
                    break
        if voted is not None:
            reason = Prompt.ask("  Your reason").strip()
            if not reason:
                reason = "gut feeling"
            return voted, reason
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


def prompt_continue() -> None:
    console.print()
    console.input("  [dim]Press Enter to continue...[/]")


def print_section(title: str) -> None:
    console.print()
    console.print(f"[bold dim]{'─' * 4} {title} {'─' * 4}[/]")
    console.print()


def print_info(msg: str) -> None:
    console.print(f"  [dim]{msg}[/]")


