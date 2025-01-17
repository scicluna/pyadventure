class FlagManager:
    def __init__(self):
        """Initialize the flag manager."""
        self.flags = {}

    def set_flag(self, key:str, value=True)->None:
        """Sets a flag with the given key and value."""
        self.flags[key] = value

    def check_flag(self, key:str)->None:
        """Checks the value of a flag."""
        return self.flags.get(key, False)

    def clear_flag(self, key:str)->None:
        """Removes a flag."""
        if key in self.flags:
            del self.flags[key]

    def set_flags(self, flags_dict: dict[str, bool])->None:
        """Sets multiple flags from a dictionary."""
        self.flags.update(flags_dict)

    def clear_flags(self, keys: list[str])->None:
        """Clears multiple flags by their keys."""
        for key in keys:
            self.flags.pop(key, None)

    def list_flags(self)->dict[str, bool]:
        """Lists all flags."""
        return self.flags
    
    def filter_flags(self, value:str=None)->dict[str, bool]:
        """Returns flags with the specified value."""
        return {k: v for k, v in self.flags.items() if v == value or value is None}