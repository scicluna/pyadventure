from __future__ import annotations
import copy
from typing import TYPE_CHECKING
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
        self.test_player = player
        self.test_player2 = copy.deepcopy(player)

    def test(self):
        """Run tests for the Player class and its related systems."""
        print("Starting Player class tests...")

        print("\n--- Testing Stat Modifications ---")
        self.test_player.stats.modify_stat({"strength": 5, "stamina": -3})
        assert self.test_player.stats.strength == 15, "Strength modification failed."
        assert self.test_player.stats.stamina == 7, "Stamina modification failed."
        print("Stat modifications passed.")

        print("\n--- Testing Status Effects ---")
        print("\n--- Current HP = ", self.test_player.stats.hp)
        poison = StatusEffect(name="Poison", stat="hp", value=-5, duration=3)
        self.test_player.stats.status_manager.add_effect(poison, self.test_player.stats)
        assert self.test_player.stats.status_manager.has_effect("Poison"), "Failed to apply Poison status."
        self.test_player.stats.status_manager.update_effects(self.test_player.stats)
        assert self.test_player.stats.hp == max(0, self.test_player.stats.max_hp - 5), f"Poison damage failed. - HP recorded = {self.test_player.stats.hp}, Expected = {max(0, self.test_player.stats.max_hp - 5)}"
        print("Status effects passed.")

        print("\n--- Testing Consumables ---")
        potion = Consumable(name="Health Potion", description="Restores 50 HP.", gold_cost=10, effect_type="restore_hp", effect_value=50)
        self.test_player.inventory.add_item(potion, count=3)
        self.test_player.inventory.use(0, self.test_player)
        assert self.test_player.stats.hp == min(self.test_player.stats.max_hp, self.test_player.stats.hp + 50), "Health potion failed."
        print("Consumables passed.")

        print("\n--- Testing Equipment ---")
        sword = Equipment(name="Steel Sword", description="A sturdy steel sword.", gold_cost=100, slot="weapon", stats={"strength": 5}, required_stats={"strength": 10})
        armor = Equipment(name="Iron Armor", description="Heavy iron armor.", gold_cost=150, slot="armor", stats={"stamina": 8}, required_stats={"stamina": 12})

        # Equip sword
        self.test_player.equipment_manager.equip(sword, inventory_index=None)
        assert self.test_player.equipment_manager.is_equipped("Steel Sword"), "Failed to equip sword."
        assert self.test_player.stats.strength == 20, "Sword stats not applied correctly."

        # Replace sword with a shield and test inventory swap
        shield = Equipment(name="Iron Shield", description="A sturdy iron shield.", gold_cost=80, slot="weapon", stats={"stamina": 5})
        self.test_player.inventory.add_item(shield)
        self.test_player.equipment_manager.equip(shield, inventory_index=None)
        assert self.test_player.equipment_manager.is_equipped("Iron Shield"), "Failed to equip shield."
        assert not self.test_player.equipment_manager.is_equipped("Steel Sword"), "Failed to unequip sword."
        assert self.test_player.stats.strength == 15, "Failed to remove sword stats."
        assert self.test_player.stats.stamina == 12, "Shield stats not applied correctly."

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
        assert self.test_player2.stats.strength == 15, "Strength modification failed."
        assert self.test_player2.stats.stamina == 7, "Stamina modification failed."
        assert self.test_player2.stats.agility == 12, "Agility modification failed."
        print("Stat modifications passed.")

        print("\n--- Testing Status Effects ---")
        poison = StatusEffect(name="Poison", stat="hp", value=-5, duration=3)
        blessing = StatusEffect(name="Blessing", stat="strength", value=3, duration=2)
        self.test_player2.stats.status_manager.add_effect(poison, self.test_player2.stats)
        self.test_player2.stats.status_manager.add_effect(blessing, self.test_player2.stats)
        assert self.test_player2.stats.status_manager.has_effect("Poison"), "Failed to apply Poison status."
        assert self.test_player2.stats.status_manager.has_effect("Blessing"), "Failed to apply Blessing status."
        self.test_player2.stats.status_manager.update_effects(self.test_player2.stats)
        assert self.test_player2.stats.hp == max(0, self.test_player2.stats.max_hp - 5), "Poison damage failed."
        assert self.test_player2.stats.strength == 18, "Blessing stat boost failed."
        self.test_player2.stats.status_manager.update_effects(self.test_player2.stats)
        assert not self.test_player2.stats.status_manager.has_effect("Blessing"), "Blessing did not expire."
        print("Status effects passed.")

        print("\n--- Testing Consumables ---")
        potion = Consumable(name="Health Potion", description="Restores 50 HP.", gold_cost=10, effect_type="restore_hp", effect_value=50)
        antidote = Consumable(name="Antidote", description="Removes Poison.", gold_cost=15, effect_type="remove_status", status_effect=poison)
        self.test_player2.inventory.add_item(potion, count=3)
        self.test_player2.inventory.add_item(antidote)
        self.test_player2.inventory.use(0, self.test_player2)  # Use potion
        assert self.test_player2.stats.hp == min(self.test_player2.stats.max_hp, self.test_player2.stats.hp + 50), "Health potion failed."
        self.test_player2.inventory.use(1, self.test_player2)  # Use antidote
        assert not self.test_player2.stats.status_manager.has_effect("Poison"), "Antidote failed to remove Poison."
        print("Consumables passed.")

        print("\n--- Testing Equipment ---")
        sword = Equipment(name="Steel Sword", description="A sturdy steel sword.", gold_cost=100, slot="weapon", stats={"strength": 5}, required_stats={"strength": 10})
        heavy_armor = Equipment(name="Heavy Armor", description="Requires high stamina.", gold_cost=200, slot="armor", stats={"stamina": 10}, required_stats={"stamina": 15})
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
        stackable_item = Consumable(name="Mana Potion", description="Restores 50 MP.", gold_cost=12, effect_type="restore_mp", effect_value=50)
        self.test_player2.inventory.add_item(stackable_item, count=98)  # Add near max
        self.test_player2.inventory.add_item(stackable_item, count=5)  # Exceed stack max
        print("\n--- Current Inventory ---")
        print(self.test_player2.inventory.list_items())
        assert len(self.test_player2.inventory.items) > 1, "Failed to create a new stack for overflow."
        self.test_player2.inventory.remove_item("Mana Potion", count=50)  # Partial stack removal
        print("\n--- Current Inventory ---")
        print(self.test_player2.inventory.list_items())
        remaining_count = sum(item.count for item in self.test_player2.inventory.items if item.name == "Mana Potion")
        assert remaining_count == 53, f"Expected 53 Mana Potions, found {remaining_count}."
        print("Inventory tests passed.")

        print("\n--- All tests passed! ---")
