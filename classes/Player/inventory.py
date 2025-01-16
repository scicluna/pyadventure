from classes.Player.items import Item
from classes.Player.player import Player


class Inventory:
    def __init__(self):
        """Initialize an empty inventory."""
        self.items: list[Item] = []

    def add_item(self, item:Item, count:int=1)->None:
        """
        Add an item to the inventory. Stack if possible.
        :param item: The item to add.
        :param count: The quantity to add (for stackable items).
        """
        if item.stackable:
            # Look for an existing stack of the same item
            for inv_item in self.items:
                if inv_item.name == item.name:
                    # Increase the stack count, but cap it at 99
                    if inv_item.count < 99:
                        added = min(99 - inv_item.count, count)
                        inv_item.count += added
                        count -= added
                        print(f"Added {added} {item.name}(s) to the stack. Current count: {inv_item.count}.")
                        if count <= 0:
                            return
            # If there's remaining count, add a new stack
            if count > 0:
                item.count = count
                self.items.append(item)
                print(f"Created a new stack of {item.name} with {count}.")
        else:
            # Add non-stackable items directly
            for _ in range(count):
                self.items.append(item)
                print(f"Added {item.name} to the inventory.")

    def remove_item(self, identifier, count=1):
        """
        Remove an item from the inventory.
        :param identifier: The name of the item or its index in the inventory.
        :param count: The quantity to remove (for stackable items).
        """
        if isinstance(identifier, int):  # Index-based removal
            if 0 <= identifier < len(self.items):
                item = self.items[identifier]
                if item.stackable:
                    if item.count > count:
                        item.count -= count
                        print(f"Removed {count} {item.name}(s). Remaining: {item.count}.")
                    else:
                        print(f"Removed the entire stack of {item.name}.")
                        self.items.pop(identifier)
                else:
                    print(f"Removed {item.name} from the inventory.")
                    self.items.pop(identifier)
            else:
                print("Invalid inventory slot.")
        elif isinstance(identifier, str):  # Name-based removal
            for item in self.items:
                if item.name == identifier:
                    if item.stackable:
                        if item.count > count:
                            item.count -= count
                            print(f"Removed {count} {item.name}(s). Remaining: {item.count}.")
                            return
                        else:
                            print(f"Removed the entire stack of {item.name}.")
                            self.items.remove(item)
                            return
                    else:
                        print(f"Removed {item.name} from the inventory.")
                        self.items.remove(item)
                        return
            print(f"Item '{identifier}' not found in the inventory.")
        else:
            print("Invalid identifier type. Must be an index or name.")

    def check_item(self, required_item:str)->bool:
        """Check if an item is present in the inventory."""
        return any(item.name == required_item for item in self.items)

    def sort_items(self, key:function=None, reverse:bool=False)->list[Item]:
        """
        Sort the inventory.
        :param key: A function to extract a comparison key (e.g., lambda x: x.name).
        :param reverse: Whether to sort in descending order.
        """
        return self.items.sort(key=key, reverse=reverse)
    
    def use(self, slot_index: int, player: Player) -> None:
        """
        Use the item in the specified inventory slot.
        :param slot_index: The index of the item in the inventory.
        :param player: The player using the item.
        """
        if 0 <= slot_index < len(self.items):
            item = self.items[slot_index]

            # Check if the item is usable
            if item.is_usable(player):
                # Use the item
                item.use_item(player)

                # Handle stackable items
                if item.stackable:
                    item.count -= 1
                    if item.count <= 0:
                        self.items.pop(slot_index)
                        print(f"{item.name} stack is empty and has been removed.")
                else:
                    # Remove non-stackable items
                    self.items.pop(slot_index)
                    print(f"{item.name} has been removed from the inventory.")
            else:
                print(f"{item.name} cannot be used in the current context.")
        else:
            print("Invalid inventory slot.")



    def list_items(self)->list[str]:
        """List all items in the inventory."""
        return [item.name for item in self.items]

    def swap_items(self, index1:int, index2:int)->None:
        """
        Swap two items in the inventory by index.
        :param index1: Index of the first item.
        :param index2: Index of the second item.
        """
        if 0 <= index1 < len(self.items) and 0 <= index2 < len(self.items):
            self.items[index1], self.items[index2] = self.items[index2], self.items[index1]
            print(f"Swapped items at index {index1} and {index2}.")
        else:
            print("Invalid indices for swapping.")