from classes.Player.equipment_manager import EquipmentManager
from classes.Player.flag_manager import FlagManager
from classes.Player.inventory import Inventory
from classes.Player.spell_manager import SpellManager
from classes.Player.stats import Stats


class Player:
    def __init__(self):
        self.stats = Stats()
        self.inventory = Inventory()
        self.equipment_manager = EquipmentManager(self)
        self.flags = FlagManager()
        self.spell_manager = SpellManager(self)