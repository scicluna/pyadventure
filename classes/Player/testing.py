from __future__ import annotations
import copy
import json
import os
from typing import TYPE_CHECKING
from classes.Player.save_manager import SaveManager
from classes.Player.status_effects import StatusEffect, StatusManager
from classes.Player.items import Consumable, Equipment
if TYPE_CHECKING:
    from classes.Player.equipment_manager import EquipmentManager
    from classes.Player.inventory import Inventory
    from classes.Player.player import Player
    from classes.Player.stats import Stats



class TestManager:
    """A class that manages testing for the player."""
    def __init__(self, player:Player):
        self.test_player = copy.deepcopy(player)
        self.test_player2 = copy.deepcopy(player)
        self.test_player3 = copy.deepcopy(player)
        self.test_player35 = copy.deepcopy(player)
        
    def test(self):
        """Run tests for the Player class and its related systems."""
        print("Starting Player class tests...")

        print("\n--- Testing Stat Modifications ---")
        self.test_player.stats.modify_stat({"strength": 5, "stamina": -3})
        assert self.test_player.stats.explicit_stats["strength"] == 15, "Strength modification failed."
        assert self.test_player.stats.explicit_stats["stamina"] == 7, "Stamina modification failed."
        print("Stat modifications passed.")

        print("\n--- Testing Status Effects ---")
        print("\n--- Current HP = ", self.test_player.stats.resources["hp"])
        poison = StatusEffect(name="Poison", stat="hp", value=-5, duration=3)
        self.test_player.stats.status_manager.add_effect(poison, self.test_player.stats)
        assert self.test_player.stats.status_manager.has_effect("Poison"), "Failed to apply Poison status."
        self.test_player.stats.status_manager.update_effects(self.test_player.stats)
        assert self.test_player.stats.resources["hp"] == max(0, self.test_player.stats.derived_stats["max_hp"] - 5), f"Poison damage failed. - HP recorded = {self.test_player.stats.resources['hp']}, Expected = {max(0, self.test_player.stats.derived_stats['max_hp'] - 5)}"
        print("Status effects passed.")

        print("\n--- Testing Consumables ---")
        potion = Consumable(name="Health Potion", stackable=True, description="Restores 50 HP.", gold_cost=10, effect_type="restore_hp", effect_value=50)
        self.test_player.inventory.add_item(potion, count=3)
        self.test_player.inventory.use(0, self.test_player)
        assert self.test_player.stats.resources["hp"] == min(self.test_player.stats.derived_stats["max_hp"], self.test_player.stats.resources["hp"] + 50), "Health potion failed."
        print("Consumables passed.")

        print("\n--- Testing Equipment ---")
        sword = Equipment(name="Steel Sword", stackable=False, description="A sturdy steel sword.", gold_cost=100, slot="weapon", stats={"strength": 5}, required_stats={"strength": 10})
        armor = Equipment(name="Iron Armor", stackable=False, description="Heavy iron armor.", gold_cost=150, slot="armor", stats={"stamina": 8}, required_stats={"stamina": 12})

        # Equip sword
        self.test_player.equipment_manager.equip(sword, inventory_index=None)
        assert self.test_player.equipment_manager.is_equipped("Steel Sword"), "Failed to equip sword."
        assert self.test_player.stats.explicit_stats["strength"] == 20, "Sword stats not applied correctly."

        # Replace sword with a shield and test inventory swap
        shield = Equipment(name="Iron Shield", stackable=False, description="A sturdy iron shield.", gold_cost=80, slot="weapon", stats={"stamina": 5})
        self.test_player.inventory.add_item(shield)
        self.test_player.equipment_manager.equip(shield, inventory_index=None)
        assert self.test_player.equipment_manager.is_equipped("Iron Shield"), "Failed to equip shield."
        assert not self.test_player.equipment_manager.is_equipped("Steel Sword"), "Failed to unequip sword."
        assert self.test_player.stats.explicit_stats['strength'] == 15, "Failed to remove sword stats."
        assert self.test_player.stats.explicit_stats['stamina'] == 12, "Shield stats not applied correctly."

        print("Equipment tests passed.")

        print("\n--- Testing Inventory ---")
        print("\n--- Current Inventory ---")
        print(self.test_player.inventory.list_items())
        print(self.test_player.equipment_manager.list_equipped_items())
        assert self.test_player.inventory.check_item("Steel Sword"), "Failed to add Steel Sword to inventory."
        self.test_player.inventory.remove_item("Steel Sword")
        assert not self.test_player.inventory.check_item("Steel Sword"), "Failed to remove Steel Sword from inventory."
        print("Inventory tests passed.")

        print("\n--- All tests passed! ---")
    
    def test2(self):
        """Run tests for the Player class and its related systems."""
        print("Starting Player class tests...")

        print("\n--- Starting Stats ---")
        print(self.test_player2.stats.show_stats())
        print("\n--- Testing Stat Modifications ---")
        self.test_player2.stats.modify_stat({"strength": 5, "stamina": -3, "agility": 2})
        assert self.test_player2.stats.explicit_stats['strength'] == 15, "Strength modification failed."
        assert self.test_player2.stats.explicit_stats['stamina'] == 7, "Stamina modification failed."
        assert self.test_player2.stats.explicit_stats['agility'] == 12, "Agility modification failed."
        print("Stat modifications passed.")

        print("\n--- Testing Status Effects ---")
        poison = StatusEffect(name="Poison", stat="hp", value=-5, duration=3)
        blessing = StatusEffect(name="Blessing", stat="strength", value=3, duration=2)
        self.test_player2.stats.status_manager.add_effect(poison, self.test_player2.stats)
        self.test_player2.stats.status_manager.add_effect(blessing, self.test_player2.stats)
        assert self.test_player2.stats.status_manager.has_effect("Poison"), "Failed to apply Poison status."
        assert self.test_player2.stats.status_manager.has_effect("Blessing"), "Failed to apply Blessing status."
        self.test_player2.stats.status_manager.update_effects(self.test_player2.stats)
        assert self.test_player2.stats.resources["hp"] == max(0, self.test_player2.stats.derived_stats["max_hp"] - 5), "Poison damage failed."
        assert self.test_player2.stats.explicit_stats['strength'] == 18, "Blessing stat boost failed."
        self.test_player2.stats.status_manager.update_effects(self.test_player2.stats)
        assert not self.test_player2.stats.status_manager.has_effect("Blessing"), "Blessing did not expire."
        print("Status effects passed.")

        print("\n--- Testing Consumables ---")
        potion = Consumable(name="Health Potion", stackable=True, description="Restores 50 HP.", gold_cost=10, effect_type="restore_hp", effect_value=50)
        antidote = Consumable(name="Antidote", stackable=True, description="Removes Poison.", gold_cost=15, effect_type="remove_status", status_effect=poison)
        self.test_player2.inventory.add_item(potion, count=3)
        self.test_player2.inventory.add_item(antidote)
        self.test_player2.inventory.use(0, self.test_player2)  # Use potion
        assert self.test_player2.stats.resources["hp"] == min(self.test_player2.stats.derived_stats["max_hp"], self.test_player2.stats.resources["hp"] + 50), "Health potion failed."
        self.test_player2.inventory.use(1, self.test_player2)  # Use antidote
        assert not self.test_player2.stats.status_manager.has_effect("Poison"), "Antidote failed to remove Poison."
        print("Consumables passed.")

        print("\n--- Testing Equipment ---")
        sword = Equipment(name="Steel Sword", stackable=False, description="A sturdy steel sword.", gold_cost=100, slot="weapon", stats={"strength": 5}, required_stats={"strength": 10})
        heavy_armor = Equipment(name="Heavy Armor", stackable=False, description="Requires high stamina.", gold_cost=200, slot="armor", stats={"stamina": 10}, required_stats={"stamina": 15})
        self.test_player2.inventory.add_item(sword)
        self.test_player2.equipment_manager.equip(sword, inventory_index=0)
        assert self.test_player2.equipment_manager.is_equipped("Steel Sword"), "Failed to equip sword."
        try:
            self.test_player2.equipment_manager.equip(heavy_armor)
        except Exception as e:
            print(f"Expected failure when equipping Heavy Armor: {e}")
        assert not self.test_player2.equipment_manager.is_equipped("Heavy Armor"), "Equipped Heavy Armor despite failing requirements."
        print("Equipment tests passed.")

        print("\n--- Testing Inventory ---")
        stackable_item = Consumable(name="Mana Potion", stackable=True, description="Restores 50 MP.", gold_cost=12, effect_type="restore_mp", effect_value=50)
        self.test_player2.inventory.add_item(stackable_item, count=98)  # Add near max
        self.test_player2.inventory.add_item(stackable_item, count=5)  # Exceed stack max
        assert len(self.test_player2.inventory.items) > 1, "Failed to create a new stack for overflow."
        self.test_player2.inventory.remove_item("Mana Potion", count=50)  # Partial stack removal
        remaining_count = sum(item.count for item in self.test_player2.inventory.items if item.name == "Mana Potion")
        assert remaining_count == 53, f"Expected 53 Mana Potions, found {remaining_count}."
        print("Inventory tests passed.")

        print("\n--- Testing SpellManager ---")
        self.test_player2.stats.resources["mp"] = 29 # Set mana to 29 for testing
        # Add a new spell
        fireball = {"name": "Fireball", "description": "A blazing ball of fire.", "mana_cost": 15, "rank": 1}
        self.test_player2.spell_manager.add_spell(fireball)
        assert self.test_player2.spell_manager.has_spell("Fireball"), "Failed to add Fireball spell."
        print("Added Fireball.")

        # Attempt to cast Fireball with sufficient mana
        self.test_player2.spell_manager.use_spell("Fireball", self.test_player2)
        assert self.test_player2.stats.resources["mp"] == 14, "Mana not reduced correctly after casting Fireball."
        print("Casted Fireball successfully.")

        # Attempt to cast Fireball with insufficient mana

        self.test_player2.spell_manager.use_spell("Fireball", self.test_player2)
        assert self.test_player2.stats.resources["mp"] == 14, "Mana should not change when casting with insufficient mana."
        print("Handled insufficient mana correctly.")

        # Add an upgraded version of Fireball
        fireball_rank2 = {"name": "Fireball", "description": "A more powerful fireball.", "mana_cost": 25, "rank": 2}
        self.test_player2.spell_manager.add_spell(fireball_rank2)
        assert any(spell["rank"] == 2 for spell in self.test_player2.spell_manager.spells), "Failed to upgrade Fireball spell."
        print("Upgraded Fireball to rank 2.")

        # Attempt to cast the upgraded Fireball with insufficient mana
        self.test_player2.spell_manager.use_spell("Fireball", self.test_player2)
        assert self.test_player2.stats.resources["mp"] == 14, "Mana should not change when casting upgraded Fireball with insufficient mana."
        print("Handled insufficient mana for upgraded spell correctly.")

        # Add another spell
        lightning = {"name": "Lightning Bolt", "description": "A strike of electricity.", "mana_cost": 10, "rank": 1}
        self.test_player2.spell_manager.add_spell(lightning)
        assert self.test_player2.spell_manager.has_spell("Lightning Bolt"), "Failed to add Lightning Bolt spell."
        print("Added Lightning Bolt.")

        # Cast Lightning Bolt
        self.test_player2.spell_manager.use_spell("Lightning Bolt", self.test_player2)
        assert self.test_player2.stats.resources["mp"] == 4, "Mana not reduced correctly after casting Lightning Bolt."
        print("Casted Lightning Bolt successfully.")

        # List spells
        spell_list = self.test_player2.spell_manager.list_spells()
        assert len(spell_list) == 2, "Spell list should contain exactly 2 spells."
        print("Spell list is accurate:", spell_list)

        print("\nAll tests passed for SpellManager!")


        print("\n--- All tests passed! ---")

    def save_test1(self):
        """Test the SaveManager functionality."""     
        # File paths
        save_dir = "saves"
        data_dir = "data"
        os.makedirs(save_dir, exist_ok=True)
        os.makedirs(data_dir, exist_ok=True)

        test_save_file = os.path.join(save_dir, "test_save.json")
        dummy_save_file = os.path.join(save_dir, "dummy_save.json")
        consumables_file = os.path.join(data_dir, "consumables.json")
        equipment_file = os.path.join(data_dir, "equipment.json")
        plotitems_file = os.path.join(data_dir, "plotitems.json")

        # Initialize SaveManager with test files
        save_manager = SaveManager(
            player=self.test_player3,
            save_file=test_save_file,
            consumables_file=consumables_file,
            equipment_file=equipment_file,
            plotitems_file=plotitems_file,
        )

        # Test saving
        print("\n--- Testing Save ---")
        player = self.test_player3

        # Modify player state
        player.stats.modify_stat({"strength": 5})
        player.inventory.add_item(save_manager.create_item("Health Potion"), count=3)
        player.equipment_manager.equip(save_manager.create_item("Steel Sword"))

        # Save the game
        save_manager.save_game(player)

        # Verify saved file content
        with open(test_save_file, "r") as f:
            saved_data = json.load(f)
        assert saved_data["stats"]["explicit_stats"]["strength"] == 20
        assert len(saved_data["inventory"]) == 1
        assert saved_data["inventory"][0]["name"] == "Health Potion"
        assert saved_data["inventory"][0]["count"] == 3
        assert saved_data["equipment"]["weapon"] == "Steel Sword"
        print("Save test passed.")

        # Test loading
        print("\n--- Testing Load ---")
        dummy_save = {
            "stats": {
                "explicit_stats": {"strength": 10, "agility": 12, "stamina": 8, "willpower": 14, "charisma": 10, "level": 2, "exp": 100},
                "resources": {"hp": 52, "mp": 110},
                "meta_info": {"day": 5, "location": 2},
            },
            "flags": {"defeated_dragon": True},
            "inventory": [{"name": "Health Potion", "count": 5}],
            "equipment": {"weapon": "Steel Sword"}
        }

        with open(dummy_save_file, "w") as f:
            json.dump(dummy_save, f)

        # Load the dummy save
        player = self.test_player35
        save_manager.save_file = dummy_save_file
        save_manager.load_game(player)

        # Verify loaded player state
        assert player.stats.explicit_stats["strength"] == 15
        assert player.stats.meta_info["day"] == 5
        assert player.stats.resources["hp"] == 52
        assert player.flags.check_flag("defeated_dragon") is True
        assert len(player.inventory.items) == 1
        assert player.inventory.items[0].name == "Health Potion"
        assert player.inventory.items[0].count == 5
        assert player.equipment_manager.is_equipped("Steel Sword")
        print("Load test passed.")

        # Cleanup: Remove save files only
        os.remove(test_save_file)
        os.remove(dummy_save_file)