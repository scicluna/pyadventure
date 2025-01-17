from typing import TYPE_CHECKING, TypedDict
from Events.choice import Choice
if TYPE_CHECKING:
    from classes.Player.player import Player
    
class StructuredEvent(TypedDict):
    name: str
    event_text: str
    background_img: str
    background_music: str
    choices: list[str]

class Event:
    def __init__(
        self,
        reference_number: int,
        name: str,
        event_text: str,
        choices: list[Choice],
        background_img: str,
        background_music: str,
    ):
        """
        Represents a game event with text, choices, and multimedia.
        :param reference_number: A unique identifier for the event.
        :param name: The name of the event.
        :param event_text: The descriptive text of the event.
        :param choices: All possible choices for this event.
        :param background_img: Path to the background image.
        :param background_music: Path to the background music.
        """
        self.reference_number = reference_number
        self.name = name
        self.event_text = event_text
        self.choices = choices
        self.background_img = background_img
        self.background_music = background_music

    def get_available_choices(self, player:Player) -> list[Choice]:
            """
            Filters the choices based on player attributes, inventory, flags, etc.
            :param player: The player object to evaluate choice conditions.
            :return: A list of choices available to the player.
            """
            return [choice for choice in self.choices if choice.is_available(player)]
    
    def display_event(self, player:Player) -> dict:
        """
        Returns the event details and available choices for display.
        :param player: The player object to evaluate choice conditions.
        :return: A dictionary with event details and filtered choices.
        """
        available_choices = self.get_available_choices(player)
        structured_dict: StructuredEvent =  {
            "name": self.name,
            "event_text": self.event_text,
            "background_img": self.background_img,
            "background_music": self.background_music,
            "choices": [choice.text for choice in available_choices],
        }
        return structured_dict