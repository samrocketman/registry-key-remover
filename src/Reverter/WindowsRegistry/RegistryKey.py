import re

class RegistryKey:
    """Represents an entire key and value name in the Windows
    registry.  This class represents the key, subkey, and value
    name.  A sample key is 'HKEY_CURRENT_USER.'  A sample
    subkey is 'Control Panel\Accessibility.'  A sample value name
    is 'MinimumHitRadius.'"""

    SEPARATOR = '\\'
    
    def __init__(self, key):
        """Creates this.  key is the full key, including key, subkey,
        and value name."""
        self.groups = key.split(self.SEPARATOR)

    def makeFullKey(self):
        """Returns the full key as given to the init method."""
        return self.SEPARATOR.join(self.groups)

    def parts(self):
        """Returns each component of this key as an array.  As an
        example, consider the key "HKEY_CURRENT_USER\Control
        Panel\Accessibility\MinimumHitRadius," this method would
        return the array containing 'HKEY_CURRENT_USER,'
        'Control Panel,' 'Accessibility,' and 'MinimumHitRadius.'"""
        return self.groups

    def toString(self):
        """String represention of this registry key.  The string
        representation consist of the entire key, including key,
        subkey, and value name."""
        print self.makeFullKey()