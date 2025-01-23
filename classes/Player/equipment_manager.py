from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict
if TYPE_CHECKING:
    from classes.Player.items import Equipment
    from classes.Player.player import Player

class EquippedItems(TypedDict):
    weapon: Equipment
    armor: Equipment
    cloak: Equipment
    boots: Equipment
    bracer: Equipment
    head: Equipment
    belt: Equipment
    ring1: Equipment
    ring2: Equipment
    amulet: Equipment

class EquipmentManager:
    def __init__(self, player:Player):
        """
        Manages the equipment for a player.
        :param player: The player whose equipment is managed.
        """
        self.player = player
        self.equipped_items:EquippedItems = {
            "weapon": None,
            "armor": None,
            "cloak": None,
            "boots": None,
            "bracer": None,
            "head": None,
            "belt": None,
            "ring1": None,
            "ring2": None,
            "amulet": None,
        }

    def equip(self, item:Equipment, inventory_index=None):
        """
        Equip an item, replacing any existing item in the same slot.
        :param item: The Equipment object to equip.
        :param inventory_index: The index of the item in the inventory.
        """
        if not item.is_usable(self.player):
            return

        if item.slot not in self.equipped_items:
            print(f"Invalid equipment slot: {item.slot}")
            return
        
        # Ensure the item is removed from inventory if it exists there
        self.player.inventory.remove_item(item.name, count=1)

        # Handle swapping with an already equipped item
        if self.equipped_items[item.slot]:
            replaced_item = self.equipped_items[item.slot]
            self.equipped_items[item.slot] = None  # Temporarily unequip the replaced item

            # Remove the stats of the replaced item
            self.player.stats.modify_stats([{stat: -value for stat, value in item.items()} for item in replaced_item.stats])

            # Add the replaced item back to the inventory at the same index
            if inventory_index is not None:
                self.player.inventory.add_item(replaced_item, index=inventory_index)
            else:
                self.player.inventory.add_item(replaced_item)

            print(f"Replaced {replaced_item.name} with {item.name} in the {item.slot} slot.")

        # Equip the new item
        self.equipped_items[item.slot] = item
        print(f"Equipped {item.name} in the {item.slot} slot.")

        print(item.stats)
        # Apply the stats of the newly equipped item
        self.player.stats.modify_stats(item.stats)

    def unequip(self, slot):
        """
        Unequip the item in the specified slot.
        :param slot: The equipment slot to unequip.
        """
        if slot not in self.equipped_items:
            print(f"Invalid equipment slot: {slot}")
            return

        item = self.equipped_items[slot]
        if not item:
            print(f"No item equipped in the {slot} slot.")
            return

        # Remove the item
        print(f"Unequipped {item.name} from the {slot} slot.")
        self.equipped_items[slot] = None

        # Remove the stats of the unequipped item
        # Multiply by -1 to reverse the stat effects
        print("REMOVING STATS")
        self.player.stats.modify_stats([(-1 * stat, value) for stat, value in item.stats.items()])

        # Return the unequipped item to inventory
        self.player.inventory.add_item(item)

    def is_equipped(self, item_name: str, slot: str = None) -> bool:
        """
        Check if a specific item is equipped.
        :param item_name: The name of the item to check.
        :param slot: Optional, the slot to narrow the check.
        :return: True if the item is equipped, otherwise False.
        """
        if slot:
            # Check a specific slot
            equipped_item = self.equipped_items.get(slot)
            return equipped_item is not None and equipped_item.name == item_name
        else:
            # Check all slots
            return any(
                equipped_item is not None and equipped_item.name == item_name
                for equipped_item in self.equipped_items.values()
            )   
        
    def list_equipped_items(self):
        """List all currently equipped items."""
        for slot, item in self.equipped_items.items():
            if item:
                print(f"{slot.capitalize()}: {item.name}")
            else:
                print(f"{slot.capitalize()}: None")