class FlagManager:
    def __init__(self):
        self.flags = {}

    def set_flag(self, key, value=True):
        """Sets a flag with the given key and value."""
        self.flags[key] = value

    def get_flag(self, key):
        """Gets the value of a flag."""
        return self.flags.get(key, False)

    def clear_flag(self, key):
        """Removes a flag."""
        if key in self.flags:
            del self.flags[key]

    def list_flags(self):
        """Lists all flags."""
        return self.flags
