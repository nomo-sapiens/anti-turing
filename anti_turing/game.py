from __future__ import annotations

import random
import time

import anthropic

from .config import GameMode, AGENT_PERSONAS, MESSAGES_PER_PLAYER_PER_ROUND
from .agents import Agent
from .topics import get_random_topic
from . import ui


class Player:
    def __init__(self, name: str, is_human: bool, agent: Agent | None = None):
        self.name = name
        self.is_human = is_human
        self.agent = agent
        self.alive = True


def run_game(mode: GameMode, human_name: str) -> None:
    client = anthropic.Anthropic()

    # Build players
    all_names = [human_name]
    selected_personas = random.sample(AGENT_PERSONAS, mode.num_agents)
    agents: list[Agent] = []
    for persona_name, persona_desc in selected_personas:
        agent = Agent(persona_name, persona_desc, client)
        agents.append(agent)
        all_names.append(persona_name)

    random.shuffle(all_names)

    players: list[Player] = []
    for name in all_names:
        if name == human_name:
            players.append(Player(name, is_human=True))
        else:
            agent = next(a for a in agents if a.name == name)
            players.append(Player(name, is_human=False, agent=agent))

    round_num = 0

    while True:
        alive = [p for p in players if p.alive]
        alive_names = [p.name for p in alive]
        human_player = next(p for p in alive if p.is_human)

        # Win condition: only 2 left and one of them is human
        if len(alive) <= 2:
            human_rounds = round_num
            ui.clear()
            ui.print_game_over_win(human_rounds)
            return

        round_num += 1
        topic = get_random_topic()

        # --- Chat phase ---
        chat_history: list[dict] = []

        # Each player speaks MESSAGES_PER_PLAYER_PER_ROUND times
        # Build a random order of turns
        turn_order: list[Player] = []
        for _ in range(MESSAGES_PER_PLAYER_PER_ROUND):
            shuffled = alive.copy()
            random.shuffle(shuffled)
            turn_order.extend(shuffled)

        ui.redraw_screen(players, round_num, topic, chat_history, human_name)

        for player in turn_order:
            if not player.alive:
                continue
            if player.is_human:
                msg = ui.prompt_human_message(human_name)
                if not msg:
                    msg = "..."
                chat_history.append({"speaker": player.name, "text": msg})
                ui.redraw_screen(players, round_num, topic, chat_history, human_name)
            else:
                ui.redraw_screen(players, round_num, topic, chat_history, human_name, thinking_name=player.name)
                msg = player.agent.generate_message(topic, chat_history, alive_names, human_name)
                time.sleep(0.4)
                chat_history.append({"speaker": player.name, "text": msg})
                ui.redraw_screen(players, round_num, topic, chat_history, human_name)
                ui.prompt_continue()

        # --- Vote phase ---
        ui.clear()
        ui.print_room(players, round_num, topic)
        ui.print_section("VOTE")

        votes: dict[str, str] = {}   # voter -> voted_for
        reasons: dict[str, str] = {}

        # Human votes
        candidates = [p.name for p in alive if p.name != human_name]
        human_vote, human_reason = ui.prompt_human_vote(human_name, candidates)
        votes[human_name] = human_vote
        reasons[human_name] = human_reason

        # Agents vote
        for player in alive:
            if player.is_human:
                continue
            agent_candidates = [p.name for p in alive if p.name != player.name]
            voted, reason = player.agent.vote(
                topic, chat_history, alive_names, agent_candidates, human_name
            )
            votes[player.name] = voted
            reasons[player.name] = reason

        # Tally votes
        tally: dict[str, int] = {}
        for voted in votes.values():
            tally[voted] = tally.get(voted, 0) + 1

        max_votes = max(tally.values())
        top_candidates = [name for name, count in tally.items() if count == max_votes]
        eliminated_name = random.choice(top_candidates)  # random tiebreak

        ui.print_vote_reveal(votes, reasons, eliminated_name, human_name, alive_names)
        ui.prompt_continue()

        # Mark eliminated
        for player in players:
            if player.name == eliminated_name:
                player.alive = False
                break

        # Check lose condition
        if eliminated_name == human_name:
            ui.clear()
            ui.print_game_over_lose(round_num)
            return

        # Show who was eliminated
        ui.print_info(f"{eliminated_name} has been eliminated. They were an AI agent.")
        time.sleep(2)
