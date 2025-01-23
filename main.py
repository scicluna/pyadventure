from classes.Events.testing import EventTestManager
from classes.Player.player import Player
from classes.Player.testing import TestManager

def main():
    player = Player()
    test_manager = TestManager(player)
    test_manager.test()
    test_manager.test2()
    test_manager.save_test1()
    event_test_manager = EventTestManager(player, "data/test_events.json")
    event_test_manager.test_event_flow()

if __name__ == "__main__":
    main()
