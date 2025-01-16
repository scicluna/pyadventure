from classes.Player.flag_manager import FlagManager
from classes.Player.inventory import Inventory
from classes.Player.stats import Stats


class Player:
    def __init__(self):
        self.stats = Stats()
        self.inventory = Inventory()
        self.flags = FlagManager()