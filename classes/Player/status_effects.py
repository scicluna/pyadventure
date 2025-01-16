from classes.Player.stats import Stats


class StatusEffect:
    def __init__(self, name, stat, value, duration, damage_per_day=0):
        """
        A status effect that affects stats or deals damage over time.
        
        :param name: Name of the effect (e.g., "Poison", "Blessing").
        :param stat: The stat this effect modifies (e.g., "strength").
        :param value: The magnitude of the effect (positive for buffs, negative for debuffs).
        :param duration: How many days the effect lasts.
        :param damage_per_day: Optional, damage dealt daily (e.g., from poison).
        """
        self.name: str = name
        self.stat: str = stat
        self.value: int = value
        self.duration: int = duration
        self.damage_per_day: int = damage_per_day

    def is_expired(self):
        """Check if the status effect has expired."""
        return self.duration <= 0

    def apply_effect(self, stats: Stats)->None:
        """Apply the effect's stat modification."""
        if hasattr(stats, self.stat):
            setattr(stats, self.stat, getattr(stats, self.stat) + self.value)

    def remove_effect(self, stats: Stats)->None:
        """Remove the effect's stat modification."""
        if hasattr(stats, self.stat):
            setattr(stats, self.stat, getattr(stats, self.stat) - self.value)

    def tick(self)->None:
        """Reduce duration by one day."""
        self.duration -= 1

######################################################################################

class StatusManager:
    def __init__(self):
        """Manages all active status effects for an entity."""
        self.effects: list[StatusEffect] = []

    def add_effect(self, effect: StatusEffect, stats: Stats) -> None:
        """Add a new status effect and apply its initial impact."""
        # Check if an effect with the same name already exists
        existing_effect = next((e for e in self.effects if e.name == effect.name), None)

        # Handle expired effects
        if existing_effect and existing_effect.is_expired():
            existing_effect.remove_effect(stats)
            self.effects.remove(existing_effect)
            existing_effect = None  # Clear reference to ensure a clean slate

        if existing_effect:
            # Compare the new effect's value/damage with the existing one
            if abs(effect.value) > abs(existing_effect.value) or abs(effect.damage_per_day) > abs(existing_effect.damage_per_day):
                # Remove the old effect's impact and replace it with the new one
                existing_effect.remove_effect(stats)
                effect.apply_effect(stats)
                self.effects.remove(existing_effect)
                self.effects.append(effect)
                print(f"Overwrote {effect.name} with a stronger version ({effect.value}, {effect.damage_per_day}).")
            else:
                # Otherwise, refresh the existing effect's duration if longer
                existing_effect.duration = max(existing_effect.duration, effect.duration)
                print(f"Refreshed {effect.name} duration to {existing_effect.duration} day(s).")
        else:
            # Add the new effect if none exists
            effect.apply_effect(stats)
            self.effects.append(effect)
            print(f"Applied {effect.name} for {effect.duration} day(s).")

        # Recalculate derived stats after adding the effect
        stats.recalculate_derived_stats()



    def update_effects(self, stats: Stats)->None:
        """Update all effects, removing expired ones and applying damage."""
        expired_effects = []

        for effect in self.effects:
            # Apply daily damage, if any
            if effect.damage_per_day > 0:
                stats.modify_hp(-effect.damage_per_day)
                print(f"{effect.name} dealt {effect.damage_per_day} damage.")

            # Reduce duration
            effect.tick()

            # Check for expiration
            if effect.is_expired():
                expired_effects.append(effect)

        # Remove expired effects
        for effect in expired_effects:
            effect.remove_effect(stats)
            self.effects.remove(effect)
            print(f"{effect.name} has expired.")
            
        # Recalculate derived stats after updating effects
        stats.recalculate_derived_stats()

    def has_effect(self, effect_name:str)->bool:
        """Check if a specific effect is currently active."""
        return any(effect.name == effect_name for effect in self.effects)
