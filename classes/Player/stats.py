from __future__ import annotations
from classes.Player.status_effects import StatusManager

class Stats:
    def __init__(self, strength:int=10, agility:int=10, stamina:int=10, willpower:int=10, charisma:int=10, level:int=1):
        # Explicit stats
        self.strength = strength
        self.agility = agility
        self.stamina = stamina
        self.willpower = willpower
        self.charisma = charisma
        self.level = level

        # Experience and derived stats
        self.exp:int = 0
        self.exp_to_next_level:int = self.calculate_exp_to_next_level()

        # Initialize Derived stats
        self.max_hp = self.calculate_hp()
        self.max_mp = self.calculate_mana()
        self.hit = self.calculate_hit()
        self.damage = self.calculate_damage()
        self.ac = self.calculate_ac()
        
        # Temporary stats
        self.hp:int = self.max_hp
        self.mp:int = self.max_mp

        # Track days
        self.day:float = 1

        # Track status effects
        self.status_manager = StatusManager()

    def calculate_hp(self)->int:
        """Calculate Hit Points based on stamina and level."""
        return (self.stamina * 10) + (self.level * 5)

    def calculate_mana(self)->int:
        """Calculate Mana based on willpower and level."""
        return (self.willpower * 8) + (self.level * 3)

    def calculate_hit(self)->int:
        """Calculate Hit (accuracy) based on agility and level."""
        return (self.agility * 2) + (self.level * 1)

    def calculate_damage(self)->int:
        """Calculate Damage based on strength and level."""
        return (self.strength * 3) + (self.level * 2)

    def calculate_ac(self, armor_bonus:int=0)->int:
        """Calculate Armor Class (AC) based on agility and equipped armor."""
        base_ac = 10
        return base_ac + self.agility + armor_bonus

    def calculate_exp_to_next_level(self)->int:
        """Calculate the EXP needed for the next level."""
        base_exp = 0
        multiplier = 50  # Adjust as needed for curve steepness
        return base_exp + (self.level ** 2 * multiplier)

    def gain_exp(self, amount:int)->None:
        """Adds EXP and checks for level-up."""
        self.exp += amount
        print(f"Gained {amount} EXP. Total: {self.exp}")

        # Check for level-up
        while self.exp >= self.exp_to_next_level:
            self.exp -= self.exp_to_next_level
            self.level_up()

    def level_up(self)->None:
        """Handles leveling up the player."""
        self.level += 1
        print(f"Level Up! New Level: {self.level}")

        # Recalculate stats
        self.exp_to_next_level = self.calculate_exp_to_next_level()
        self.recalculate_derived_stats()

    def check_stat(self, stat:str, required_value:int)->None:
        """Check if a stat meets a required value."""
        return getattr(self, stat) >= required_value

    def modify_stat(self, stats: dict[str, int]) -> None:
        """
        Modify explicit stats and update derived stats.
        :param stats: A dictionary where keys are stat names and values are the amounts to modify.
        """
        for stat, value in stats.items():
            if hasattr(self, stat):
                setattr(self, stat, getattr(self, stat) + value)
            else:
                print(f"Stat '{stat}' not found.")
        # Recalculate derived stats after all modifications
        self.recalculate_derived_stats()

    def advance_day(self, days:int=1)->None:
        """Advance the in-game day by the specified number of days."""
        self.day += days
        print(f"Advanced {days} day(s). Current Day: {self.day}")

    def check_hp(self, required_hp:int)->bool:
        """Check if there is sufficient HP for a given action."""
        return self.hp >= required_hp

    def modify_hp(self, amount:int)->None:
        """Adjust HP by a given amount, ensuring it stays within bounds."""
        self.hp = max(0, min(self.hp + amount, self.max_hp))
        if self.hp == 0:
            print("The player is down!")
            
    def check_mp(self, required_mp:int)->bool:
        """Check if there is sufficient MP for a given action."""
        return self.mp >= required_mp

    def modify_mp(self, amount:int)->None:
        """Adjust MP by a given amount, ensuring it stays within bounds."""
        self.mp = max(0, min(self.mp + amount, self.max_mp))

    def recalculate_derived_stats(self)->None:
        """Recalculate all derived stats based on current explicit stats."""
        self.max_hp = self.calculate_hp()
        self.max_mp = self.calculate_mana()
        self.hit = self.calculate_hit()
        self.damage = self.calculate_damage()
        self.ac = self.calculate_ac()

        # Ensure temporary stats like HP/MP are still within their bounds
        self.hp = min(self.hp, self.max_hp)
        self.mp = min(self.mp, self.max_mp)

    def show_stats(self)->str:
        """Display the player's current stats."""
        return f"Stats: HP={self.hp}/{self.max_hp}, MP={self.mp}/{self.max_mp}, Level={self.level}, EXP={self.exp}/{self.exp_to_next_level}, Day={self.day}"