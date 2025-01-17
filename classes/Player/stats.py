from __future__ import annotations
from typing import TypedDict
from classes.Player.status_effects import StatusManager

class ExplicitStats(TypedDict):
    strength: int
    agility: int
    stamina: int
    willpower: int
    charisma: int
    level: int
    exp: int

class DerivedStats(TypedDict):
    exp_to_next_level: int
    max_hp: int
    max_mp: int
    hit: int
    damage: int
    ac: int

class Resources(TypedDict):
    hp: int
    mp: int

class MetaInfo(TypedDict):
    day: int
    location: int

class Stats:
    def __init__(self, initial_explicit:dict[str,int]=None)->None:
        """
        Initialize stats using dictionaries for explicit and derived stats.
        :param initial_explicit: A dictionary of initial explicit stats.
        """
        # Explicit stats
        self.explicit_stats: ExplicitStats  = initial_explicit or {
            "strength": 10,
            "agility": 10,
            "stamina": 10,
            "willpower": 10,
            "charisma": 10,
            "level": 1,
            "exp": 0,
        }

        # Derived stats (will be recalculated)
        self.derived_stats: DerivedStats = {
            "exp_to_next_level": 0,
            "max_hp": self.calculate_hp(),
            "max_mp": self.calculate_mana(),
            "hit": 0,
            "damage": 0,
            "ac": 0,
        }

        # Temporary stats
        self.resources: Resources = {
            "hp": self.derived_stats["max_hp"],
            "mp": self.derived_stats["max_mp"],
        }

        self.recalculate_derived_stats()

        # Other
        self.meta_info: MetaInfo = {
            "day": 1,
            "location": 0
        }

        self.status_manager = StatusManager()

    def recalculate_derived_stats(self) -> None:
        """Recalculate derived stats based on explicit stats."""
        self.derived_stats["exp_to_next_level"] = self.calculate_exp_to_next_level()
        self.derived_stats["max_hp"] = self.calculate_hp()
        self.derived_stats["max_mp"] = self.calculate_mana()
        self.derived_stats["hit"] = self.calculate_hit()
        self.derived_stats["damage"] = self.calculate_damage()
        self.derived_stats["ac"] = self.calculate_ac()

        # Ensure temporary stats remain within bounds
        self.resources["hp"] = min(self.resources["hp"], self.derived_stats["max_hp"])
        self.resources["mp"]= min(self.resources["mp"], self.derived_stats["max_mp"])

    # Calculation methods for derived stats
    def calculate_hp(self) -> int:
        return (self.explicit_stats["stamina"] * 10) + (self.explicit_stats["level"] * 5)

    def calculate_mana(self) -> int:
        return (self.explicit_stats["willpower"] * 8) + (self.explicit_stats["level"] * 3)

    def calculate_hit(self) -> int:
        return (self.explicit_stats["agility"] * 2) + (self.explicit_stats["level"])

    def calculate_damage(self) -> int:
        return (self.explicit_stats["strength"] * 3) + (self.explicit_stats["level"] * 2)

    def calculate_ac(self, armor_bonus: int = 0) -> int:
        base_ac = 10
        return base_ac + self.explicit_stats["agility"] + armor_bonus

    def calculate_exp_to_next_level(self) -> int:
        multiplier = 50
        return (self.explicit_stats["level"] ** 2) * multiplier

    # Stat modification methods
    def get(self, stat: str) -> int:
        """Get the value of a stat, derived stat, or resource."""
        value = (
            self.explicit_stats.get(stat) or
            self.derived_stats.get(stat) or
            self.resources.get(stat) or
            self.meta_info.get(stat)
        )
        if value is None:
            raise KeyError(f"Stat '{stat}' not found in any category.")
        return value

    def modify_stat(self, stat_modifications: dict[str, int]) -> None:
        """Modify explicit stats and recalculate derived stats."""
        for stat, value in stat_modifications.items():
            if stat in self.explicit_stats:
                self.explicit_stats[stat] += value
            else:
                print(f"Stat '{stat}' not found in explicit stats.")
        self.recalculate_derived_stats()

    def gain_exp(self, amount: int) -> None:
        """Adds EXP and handles leveling up."""
        self.derived_stats["exp"] += amount
        while self.derived_stats["exp"] >= self.derived_stats["exp_to_next_level"]:
            self.derived_stats["exp"] -= self.derived_stats["exp_to_next_level"]
            self.level_up()

    def level_up(self) -> None:
        """Handles leveling up."""
        self.explicit_stats["level"] += 1
        print(f"Level Up! New Level: {self.explicit_stats['level']}")
        self.recalculate_derived_stats()

    # Temporary stats
    def modify_hp(self, amount: int) -> None:
        self.resources["hp"] = max(0, min(self.resources["hp"] + amount, self.derived_stats["max_hp"]))

    def modify_mp(self, amount: int) -> None:
        self.resources["mp"]= max(0, min(self.resources["mp"] + amount, self.derived_stats["max_mp"]))

    # Utility methods
    def to_dict(self) -> dict:
        """Return all stats as a dictionary."""
        return {
            "explicit_stats": self.explicit_stats,
            "derived_stats": self.derived_stats,
            "resources": self.resources,
            "meta_info": self.meta_info,
        }

    def load_from_dict(self, data: dict) -> None:
        """Load stats from a dictionary with validation."""
        for key in ["explicit_stats", "resources", "meta_info"]:
            if key in data and isinstance(data[key], dict):
                getattr(self, key).update(data[key])
            else:
                print(f"Warning: Missing or invalid data for {key}.")
        self.recalculate_derived_stats()

    def show_stats(self):
        """Print all stats to the console."""
        print("\n--- Explicit Stats ---")
        for stat, value in self.explicit_stats.items():
            print(f"{stat.capitalize()}: {value}")
        print("\n--- Derived Stats ---")
        for stat, value in self.derived_stats.items():
            print(f"{stat.capitalize()}: {value}")
        print("\n--- Resources ---")
        for stat, value in self.resources.items():
            print(f"{stat.capitalize()}: {value}")
        print("\n--- Meta Info ---")
        for stat, value in self.meta_info.items():
            print(f"{stat.capitalize()}: {value}")