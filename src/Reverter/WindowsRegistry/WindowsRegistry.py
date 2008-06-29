"""This file contains classes for working with the Windows
registry.

Author: Michael Venable"""

from _winreg import OpenKey, QueryValueEx

#Define exceptions
class WindowsRegistryException(Exception):
    """Represents an error that has occurred while interacting
    with the Windows registry."""
    def __init__(self, message, source):
        """Initializes this exception.  Includes a message describing
        why the error occurred and a source exception."""
        Exception.__init__(self, message)
        self.source = source
class CantOpenKeyException(WindowsRegistryException):
    """Indicates a registry key could not be accessed."""
    def __init__(self, message, source):
        WindowsRegistryException.__init__(self, message, source)
class CantRemoveKeyException(WindowsRegistryException):
    """INDICATEs a registry key could not be deleted."""
    def __init__(self, message, source):
        WindowsRegistryException.__init__(self, message, source)

class WindowsRegistry:
    """Abstraction of the Windows registry."""

    def getValue(self, key):
        """Retrieves the value data associated with the given
        key and value name.  Throws a CantOpenKeyException if
        the key does not exist or could not be accessed."""
        try:
            keyHandle = OpenKey( key.hive(), key.subKey() );
            value = QueryValueEx(keyHandle, key.valueName())
            keyHandle.Close()
            return value[0]
        except _winreg.EnvironmentError, e:
            raise CantOpenKeyException("Unable to open the key " + key, e)
        
    def removeKey(self, key):
        """Permanently removes the specified key from the
        registry.  Throws an exception is the key does not
        exist or could not be removed."""
        raise Exception("This method is not implemented.")

    def removeValue(self, key):
        """Permanently removed the specified value from teh
        registry."""
        raise Exception("This method is not implemented.")

class RegistryKey:
    """Represents an entire key and value name in the Windows
    registry.  This class represents the key, subkey, and value
    name.  A sample key is 'HKEY_CURRENT_USER.'  A sample
    subkey is 'Control Panel\Accessibility.'  A sample value name
    is 'MinimumHitRadius.'"""

    SEPARATOR = '\\'
    
    def __init__(self, key):
        """Creates this.  key is the full key, including hive, subkey,
        and value name. A sample key is 'HKEY_CURRENT_USER\Console\CursorSize'."""
        self.keys = key.split(self.SEPARATOR)

    def __getitem__(self, key):
        """Accesses a piece of this key. For example, if the key is
        'HKEY_CURRENT_USER\Console\CurrentUser', then key[1] is
        'Console'."""
        return self.keys[key]

    def hive(self):
        """Returns the hive of this key.  The hive is a constant
        defined in _winreg and can be one of _winreg.HKEY_CLASSES_ROOT,
        _winreg.HKEY_CURRENT_USER, _winreg.HKEY_LOCAL_MACHINE,
        _winreg.HKEY_USERS, _winreg.HKEY_CURRENT_CONFIG."""
        if self.hiveName() == "HKEY_CLASSES_ROOT":
            return wreg.HKEY_CLASSES_ROOT
        elif self.hiveName() == "HKEY_CURRENT_USER":
            return wreg.HKEY_CURRENT_USER
        elif self.hiveName() == "HKEY_LOCAL_MACHINE":
            return wreg.HKEY_LOCAL_MACHINE
        elif self.hiveName() == "HKEY_USERS":
            return wreg.HKEY_USERS
        elif self.hiveName() == "HKEY_CURRENT_CONFIG":
            return wreg.HKEY_CURRENT_CONFIG
        
    def __len__(self):
        """Returns the number of parts that make up this key.
        For example, for the key "ROOT\aaa\bbb\ccc", len(self) is four."""
        return len(self.keys)

    def __setitem__(self, key, item):
        """Sets a piece of this key.  See __getitem__ for an example."""
        self.keys[key] = item

    def __str__(self):
        return self.makeFullKey()

    def makeFullKey(self):
        """Returns the full key as given to the init method."""
        return self.SEPARATOR.join(self.keys)

    def subKey(self):
        """Returns this key's subkey.  For example, if this key is
        'HKEY_CURRENT_USER\Console\Cursors\CursorSize', then self.subKey() is
        'Console\Cursors'."""
        return self.SEPARATOR.join( self[1: len(self)-1] )

    def hiveName(self):
        """Returns the name of the top-level key or hive.
        For example, if this key is 'HKEY_CURRENT_USER\Console\CursorSize',
        then self.hiveName() is 'HKEY_CURRENT_USER'."""
        return self[0];
    
    def valueName(self):
        """Returns this key's value name.  For example, if this key is
        'HKEY_CURRENT_USER\Console\CursorSize', then self.valueName() is
        'CursorSize'."""
        return self[ len(self)-1 ]