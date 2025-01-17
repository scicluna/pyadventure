from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict
if TYPE_CHECKING:
    from classes.Player.player import Player

class Spell(TypedDict):
    name: str
    description: str
    mana_cost: int
    rank: int  # Used to track the spell's level or effectiveness

class SpellManager:
    def __init__(self, player:Player):
        """Initialize the SpellManager with an empty spell list."""
        self.spells: list[Spell] = []
        self.player = player

    def add_spell(self, spell: Spell) -> None:
        """
        Add a spell to the player's collection. Replace with a higher rank if it already exists.
        :param spell: The spell to add.
        """
        for i, existing_spell in enumerate(self.spells):
            if existing_spell["name"] == spell["name"]:
                if spell["rank"] > existing_spell["rank"]:
                    self.spells[i] = spell
                    print(f"Upgraded {spell['name']} to rank {spell['rank']}.")
                else:
                    print(f"{spell['name']} is already at an equal or higher rank.")
                return
        self.spells.append(spell)
        print(f"Added new spell: {spell['name']}.")

    def has_spell(self, spell_name: str) -> bool:
        """
        Check if the player has a specific spell.
        :param spell_name: The name of the spell to check.
        :return: True if the spell exists, False otherwise.
        """
        return any(spell["name"] == spell_name for spell in self.spells)

    def use_spell(self, spell_name: str, player: "Player") -> None:
        """
        Attempt to cast a spell, consuming mana if the player has enough.
        :param spell_name: The name of the spell to cast.
        :param player: The player object to check and consume mana.
        """
        for spell in self.spells:
            if spell["name"] == spell_name:
                if player.stats.resources["mp"] >= spell["mana_cost"]:
                    # Consume mana and cast the spell
                    player.stats.modify_mp(-spell["mana_cost"])
                    print(f"Casted {spell_name}. (-{spell['mana_cost']} MP)")

                    # Placeholder for visual/special effect
                    # e.g., play_animation(spell["name"])
                    return
                else:
                    print(f"Not enough mana to cast {spell_name}. Required: {spell['mana_cost']}, Available: {player.stats.resources['mp']}.")
                    return
        print(f"Spell {spell_name} not found.")

    def list_spells(self) -> list[str]:
        """
        List all spells for display or choice options.
        :return: A list of spell names.
        """
        return [f"{spell['name']} (Rank {spell['rank']}) - {spell['mana_cost']} MP" for spell in self.spells]

    