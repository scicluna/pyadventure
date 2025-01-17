from enum import Enum
from typing import TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from classes.Player.player import Player

class EffectAction(Enum):
    MODIFY_HP = "modify_hp"  # Increase the player's HP
    MODIFY_MP = "modify_mp"  # Increase the player's MP
    MARK_FLAG = "mark_flag"  # Mark a flag
    UNMARK_FLAG = "unmark_flag"  # Unmark a flag
    GAIN_ITEM = "gain_item"  # Add an item to the player's inventory
    CONSUME_ITEM = "consume_item"  # Remove an item from the player's inventory
    MODIFY_STAT = "modify_stat"  # Modify a specific stat
    SET_NEXT_EVENT = "set_next_event"  # Transition to a specific event
    LEARN_SPELL = "learn_spell"  # Teach the player a spell
    PLAY_ANIMATION = "play_animation"  # Play a specific animation or effect
    PLAY_SOUND = "play_sound"  # Play a specific sound
    CHANGE_LOCATION = "change_location"  # Update the player's location

class Requirement(Enum):
    STRENGTH = "strength"
    AGILITY = "agility"
    STAMINA = "stamina"
    WILLPOWER = "willpower"
    CHARISMA = "charisma"
    LEVEL = "level"
    ITEM = "item"
    FLAG = "flag"
    SPELL = "spell"

    @staticmethod
    def from_string(key: str):
        """Convert a string key to a Requirement enum."""
        try:
            return Requirement(key)
        except ValueError:
            raise ValueError(f"Invalid requirement key: {key}")

class Outcome(TypedDict):
    threshold: list[dict[str, str|int]]
    text: str
    effects: list[dict["action": EffectAction, "value": str|int]]

class Choice:
    def __init__(self, text: str, screen_fx: str, min_requirement: dict, outcomes: list):
        self.text: str = text
        self.screen_fx: str = screen_fx
        self.min_requirement: list[dict[Requirement,str|int]] = min_requirement
        self.outcomes: list[Outcome] = outcomes

    def is_available(self, player:Player) -> bool:
        """Check if the choice meets the minimum requirements."""
        for condition in self.min_requirement:
            if not self.evaluate_condition(condition, player):
                return False
        return True
    
    def evaluate_condition(self, condition: dict[str, str | int], player: Player) -> bool:
        """Evaluate a single condition."""
        key, value = next(iter(condition.items()))
        try:
            requirement = Requirement.from_string(key)
        except ValueError:
            print(f"Unknown requirement key '{key}' in condition: {condition}")
            return False

        if requirement in [
            Requirement.STRENGTH, Requirement.AGILITY, Requirement.STAMINA,
            Requirement.WILLPOWER, Requirement.CHARISMA, Requirement.LEVEL
        ]:
            return player.stats.explicit_stats.get(requirement.value, 0) >= value

        if requirement == Requirement.ITEM:
            return player.inventory.check_item(value)

        if requirement == Requirement.FLAG:
            return player.flags.check_flag(value)

        if requirement == Requirement.SPELL:
            return player.spell_manager.has_spell(value)

        print(f"Unhandled requirement: {key} in {condition}")
        return False


    def apply_outcome(self, outcome: Outcome, player: Player) -> None:
        """Apply the effects of a choice outcome."""
        for effect in outcome["effects"]:
            action = EffectAction(effect["action"])  # Validate against the enum
            value = effect["value"]

            if action == EffectAction.MODIFY_HP:
                player.stats.modify_hp(value)
            elif action == EffectAction.MARK_FLAG:
                player.flags.set_flag(value)
            elif action == EffectAction.UNMARK_FLAG:
                player.flags.clear_flag(value)
            elif action == EffectAction.GAIN_ITEM:
                player.inventory.add_item(value)
            elif action == EffectAction.CONSUME_ITEM:
                player.inventory.remove_item(value)
            elif action == EffectAction.MODIFY_STAT:
                player.stats.modify_stat(value)
            elif action == EffectAction.SET_NEXT_EVENT:
                player.event_manager.set_next_event(value)
            elif action == EffectAction.MODIFY_MP:
                player.stats.modify_mp(value)
            elif action == EffectAction.LEARN_SPELL:
                player.spell_manager.add_spell(value)
            elif action == EffectAction.PLAY_ANIMATION:
                # Future hook for animations
                pass
            elif action == EffectAction.PLAY_SOUND:
                # Future hook for sound effects
                pass
            elif action == EffectAction.CHANGE_LOCATION:
                player.stats.meta_info["location"] = value
            else:
                print(f"Invalid effect action: {action} -- {value} -- {self.text}")