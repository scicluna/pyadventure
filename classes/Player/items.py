from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classes.Player.player import Player
    from classes.Player.status_effects import StatusEffect


class Item:
    def __init__(self, ref:int, name:str, stackable=False, description="", gold_cost=0, count=1):
        """
        Base class for all items.
        :param name: Name of the item.
        :param stackable: Whether the item can be stacked.
        :param description: A brief description of the item.
        :param value: The item's monetary value.
        """
        self.ref = ref
        self.name = name
        self.count = count
        self.stackable = stackable
        self.description = description
        self.gold_cost = gold_cost

    @staticmethod
    def create_item(reference:int, data: dict) -> Item:
        """
        Factory method to create an item based on the data dictionary.
        :param data: A dictionary containing item properties.
        :return: An instance of Item or its subclasses.
        """
        print(reference)
        item = data[str(reference)]
        item_type = item["type"]
        if item_type == "Consumable":
            return Consumable(
                ref=reference,
                name=item["name"],
                stackable=item["stackable"],
                description=item["description"],
                gold_cost=item["gold_cost"],
                effect_type=item["effect_type"],
                effect_value=item.get("effect_value", 0),
                status_effect=item.get("status_effect", None),
            )
        elif item_type == "Equipment":
            return Equipment(
                ref=reference,
                name=item["name"],
                stackable=item["stackable"],
                description=item["description"],
                gold_cost=item["gold_cost"],
                slot=item["slot"],
                stats=item["stats"],
                required_stats=item.get("required_stats", {}),
            )
        elif item_type == "PlotItem":
            return PlotItem(
                ref=reference,
                name=item["name"],
                stackable=item["stackable"],
                description=item["description"],
                gold_cost=item["gold_cost"],
                quest_name=item["quest_name"],
            )
        else:
            raise ValueError(f"Unknown item type: {item_type}")

    def is_usable(self, player):
        """
        Determine if the item is usable in the current context.
        The base implementation always returns True.
        Subclasses should override this with specific conditions.
        """
        return False

    def use_item(self, target):
        """
        Default implementation for using an item. To be overridden by subclasses.
        :param target: The entity the item is used on.
        """
        print(f"{self.name} cannot be used directly.")

    def __repr__(self):
        return f"Item({self.name}, stackable={self.stackable}, value={self.gold_cost})"

#########################################################################################

class Consumable(Item):
    def __init__(self, ref, name, stackable, description, gold_cost, effect_type, effect_value, status_effect=None):
        """
        Consumable items with diverse effects.
        :param effect_type: The type of effect ("restore_hp", "restore_mp", "remove_status", "apply_status").
        :param effect_value: The magnitude of the effect (e.g., amount of HP restored).
        :param status_effect: A StatusEffect object to apply, if applicable.
        """
        super().__init__(ref, name, stackable=stackable, description=description, gold_cost=gold_cost)
        self.effect_type:str = effect_type  # "restore_hp", "restore_mp", etc.
        self.effect_value:int = effect_value
        self.status_effect:str = status_effect

    def use_item(self, player:Player)->None:
        """
        Apply the consumable's effect to the player.
        :param player: The player using the item.
        """
        if self.effect_type == "restore_hp":
            player.stats.modify_hp(self.effect_value)
            print(f"{self.name} restored {self.effect_value} HP")
        elif self.effect_type == "restore_mp":
            player.stats.modify_mp(self.effect_value)
            print(f"{self.name} restored {self.effect_value} MP")
        elif self.effect_type == "remove_status" and self.status_effect:
            if player.stats.status_manager.has_effect(self.status_effect):
                player.stats.status_manager.remove_effect(self.status_effect, player)
                print(f"{self.name} removed {self.status_effect}.")
            else:
                print(f"{self.name} had no effect. {player.name} does not have {self.status_effect.name}.")
        elif self.effect_type == "apply_status" and self.status_effect:
            player.stats.status_manager.add_effect(self.status_effect, player)
            print(f"{self.name} applied {self.status_effect.name} to {player.name}.")
        else:
            print(f"{self.name} had no effect.")

    def is_usable(self, player:Player)->bool:
        """
        Check if the item is usable in the current context.
        :param player: The entity the item is used on.
        :return: True if the item can be used, otherwise False.
        """
        if self.effect_type == "restore_hp" and player.stats.resources["hp"] >= player.stats.derived_stats["max_hp"]:
            return False  # Cannot use if HP is full
        if self.effect_type == "restore_mp" and player.stats.resources["mp"] >= player.stats["max_mp"]:
            return False  # Cannot use if MP is full
        if self.effect_type == "remove_status" and self.status_effect:
            return player.stats.status_manager.has_effect(self.status_effect)
        return True
    
#########################################################################################
class PlotItem(Item):
    def __init__(self, ref, name, stackable, description, gold_cost, quest_name):
        """
        Plot items, usually for quests or story progression.
        :param quest_name: The name of the quest this item is tied to.
        """
        super().__init__(ref, name, stackable=stackable|False, description=description, gold_cost=gold_cost)
        self.quest_name = quest_name

    def use_item(self, target):
        """
        Plot items typically cannot be used directly.
        """
        print(f"{self.name} is a plot item and cannot be used directly.")

    def is_usable(self, player):
        """
        Determine if the item is usable in the current context.
        Plot Items are always unusable.
        """
        return False

#########################################################################################
class Equipment(Item):
    def __init__(self, ref, name, stackable, description, gold_cost, slot, stats: list[dict[str,int]]=[{}], required_stats:list[dict[str, int]]=[{}]):
        """
        Equipment items like weapons or armor.
        :param slot: The equipment slot (e.g., "weapon", "armor").
        :param stats: A list of dictionariues of stat modifiers (e.g., [{"strength": 5}, {"agility": 2}]).
        :param required_stats: A list of minimum stats required to equip the item (e.g., [{"strength": 10}]).
        """
        super().__init__(ref, name, stackable=stackable|False, description=description, gold_cost=gold_cost)
        self.slot = slot
        self.stats = stats # Default to an empty dict if not provided
        self.required_stats = required_stats  # Default to an empty dict if not provided

    def is_usable(self, player: Player)->bool:
        """
        Determine if the item is usable (equippable) by checking required stats.
        :param player: The player attempting to equip the item.
        :return: True if the player meets the required stats, otherwise False.
        """
        for stat_requirement in self.required_stats:
            for stat, required_value in stat_requirement.items():  # Iterate over items
                if player.stats.explicit_stats.get(stat, 0) < required_value:
                    print(f"Cannot equip {self.name}. {stat.capitalize()} {required_value} required. (current stat is {player.stats.explicit_stats.get(stat, 0)})")
                    return False
        return True
        
    def use_item(self, player:Player):
        """
        Attempt to equip the item to the proper slot.
        :param player: The player attempting to equip the item.
        """
        if not self.is_usable(player):
            print(f"{self.name} cannot be equipped due to insufficient stats.")
            return

        # Attempt to equip the item via the EquipmentManager
        if player.equipment_manager:
            player.equipment_manager.equip(self)
        else:
            print(f"{player.name} does not have an EquipmentManager.")
