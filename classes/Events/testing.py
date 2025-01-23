import copy
import json
from typing import Dict
from classes.Player.player import Player
from classes.Events.event import Event
from classes.Events.choice import Choice, Outcome


class EventTestManager:
    def __init__(self, player: Player, events_file: str):
        self.player = player
        self.events_file = events_file
        self.events: Dict[int, Event] = self.load_events()

    def load_events(self) -> Dict[int, Event]:
        """Load events from the JSON file and return a dictionary of Event objects."""
        with open(self.events_file, "r") as f:
            data = json.load(f)

        events = {}
        for event_id, event_data in data["events"].items():
            choices = []
            for choice_data in event_data["choices"]:
                outcomes = [
                    Outcome(
                        threshold=outcome["threshold"],
                        text=outcome["text"],
                        effects=outcome["effects"]
                    )
                    for outcome in choice_data["outcomes"]
                ]
                choices.append(
                    Choice(
                        text=choice_data["text"],
                        screen_fx=choice_data["screen_fx"],
                        min_requirement=choice_data["min_requirement"],
                        outcomes=outcomes,
                    )
                )
            events[int(event_id)] = Event(
                reference_number=int(event_id),
                name=event_data["name"],
                event_text=event_data["event_text"],
                choices=choices,
                background_img=event_data["background_img"],
                background_music=event_data["background_music"],
            )
        return events

    def test_event_flow(self):
        """Test the flow of events, choices, and outcomes."""
        player = copy.deepcopy(self.player)
        current_event_id = 1
        print("\n--- Starting Event Flow Test ---")

        while current_event_id > 0:
            event = self.events[current_event_id]
            print(f"\n--- Event: {event.name} ---")
            print(event.event_text)

            # Display available choices
            available_choices = event.get_available_choices(player)
            assert available_choices, f"No available choices for Event {current_event_id}."

            print(f"\nAvailable Choices:")
            for idx, choice in enumerate(available_choices, start=1):
                print(f"{idx}. {choice.text}")

            # Simulate player selecting the first choice
            selected_choice = available_choices[0]
            print(f"\nSelected Choice: {selected_choice.text}")

            # Capture player state before applying the choice
            prev_hp = player.stats.resources["hp"]
            prev_xp = player.stats.explicit_stats["exp"]

            # Find and apply the best outcome using apply_outcome
            applied_outcome = False
            for outcome in selected_choice.outcomes:
                if all(
                    player.stats.explicit_stats.get(stat, 0) >= value
                    for condition in outcome["threshold"]
                    for stat, value in condition.items()
                ):
                    print(f"Applying Outcome: {outcome['text']}")
                    selected_choice.apply_outcome(outcome, player)
                    applied_outcome = True
                    break

            assert applied_outcome, f"No valid outcome found for {selected_choice.text}."

            # Extract the next event ID from the outcome's effects
            next_event_effect = next(
                (effect for effect in outcome["effects"] if effect["action"] == "set_next_event"),
                None,
            )
            current_event_id = next_event_effect["value"] if next_event_effect else -1

            # Assertions to validate player state changes
            if current_event_id == 2:
                assert player.stats.explicit_stats["exp"] >= prev_xp + 20, "XP not updated correctly after Event 1."
                assert player.stats.resources["hp"] == prev_hp - 5, "HP not updated correctly after Event 1."
            elif current_event_id == 3:
                assert player.stats.explicit_stats["level"] > 1, "XP not updated correctly after Event 2."
                assert player.stats.resources["hp"] == prev_hp - 10, "HP not updated correctly after Event 2."

        print("\n--- Event Flow Test Completed Successfully ---")
