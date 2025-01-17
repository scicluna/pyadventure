from classes.Player.player import Player
from classes.Player.testing import TestManager

def main():
    player = Player()
    test_manager = TestManager(player)
    test_manager.test()
    test_manager.test2()
    test_manager.save_test1()

if __name__ == "__main__":
    main()
