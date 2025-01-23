import json
from typing import Optional, TYPE_CHECKING
from classes.Player.items import Consumable, Equipment, Item, PlotItem

if TYPE_CHECKING:
    from classes.Player.player import Player

class SaveManager:
    def __init__(
        self,
        player,
        save_file: str = "saves/savegame.json",
        consumables_file: str = "data/consumables.json",
        equipment_file: str = "data/equipment.json",
        plotitems_file: str = "data/plotitems.json",
    ) -> None:
        self.player = player
        self.save_file = save_file
        self.item_files = {
            "Consumable": consumables_file,
            "Equipment": equipment_file,
            "Plot": plotitems_file,
        }
        self.item_definitions = self.load_all_item_definitions()

    def load_all_item_definitions(self) -> dict[str, dict]:
        """Load all item definitions from multiple JSON files and flattens them into one dictionary."""
        item_defs = {}
        for file in self.item_files.values():
            with open(file, "r") as f:
                item_defs.update(json.load(f))
        return item_defs

    def create_item(self, item_ref: int) -> Optional[Item]:
        """Create an item instance based on its name."""
        return Item.create_item(item_ref, self.item_definitions)

    def save_game(self, player: "Player") -> None:  # Use string literal for forward reference
        """Save the player's game state to a JSON file."""
        data = {
            "stats": player.stats.to_dict(),
            "flags": player.flags.list_flags(),
            "inventory": [
                {"ref": item.ref, "count": item.count} for item in player.inventory.items
            ],
            "equipment": {
                slot: item.ref if item else None
                for slot, item in player.equipment_manager.equipped_items.items()
            },
        }
        print(data)
        with open(self.save_file, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Game saved to {self.save_file}.")

    def load_game(self, player: "Player") -> None:
        """Load the player's game state from a JSON file."""
        try:
            with open(self.save_file, "r") as f:
                data = json.load(f)

            # Restore stats
            player.stats.load_from_dict(data["stats"])

            # Restore flags
            player.flags.set_flags(data["flags"])

            # Restore inventory
            player.inventory.items = []
            for item_ref in data["inventory"]:
                item = self.create_item(item_ref["ref"])
                if item:
                    player.inventory.add_item(item, item_ref["count"])
                    
            # Restore equipment
            for slot, item_ref in data["equipment"].items():
                if item_ref:
                    item = self.create_item(item_ref)
                    if item:
                        player.equipment_manager.equip(item)

            print(f"Game loaded from {self.save_file}.")
        except FileNotFoundError:
            print(f"Save file {self.save_file} not found. Starting a new game.")
        except Exception as e:
            print(f"Error loading game: {e}")
