"""This file contains classes for working with the Windows
registry.

Author: Michael Venable
"""

import _winreg

#Define exceptions
class WindowsRegistryException(Exception):
    """Represents an error that has occurred while interacting
    with the Windows registry.
    """
    def __init__(self, message, source=None):
        """Initializes this exception.

        message -   Description of the error.
        source -    Original exception that caused this error.  None
                    if there is no originating exception.
        """
        Exception.__init__(self, message)
        self.source = source

#Define classes
class WindowsRegistry:
    """Abstraction of the Windows registry."""

    def getValue(self, key):
        """Retrieves the value data associated with the given
        key and value name. 

        key -   The key/value to retrieve.  Example:
                RegistryKey("HKEY_CURRENT_USER\\Console\\CursorSize")
                
        Throws WindowsRegistryException if the value could not be
        accessed.
        """
        keyHandle = None
        try:
            keyHandle = _winreg.OpenKey( key.hive(), key.subKey() )
            value, type = _winreg.QueryValueEx(keyHandle, key.valueName())
            return value
        except Exception, e:
            raise WindowsRegistryException("Unable to open the key " + str(key), e)
        finally:
            if keyHandle is not None:
                keyHandle.Close()
        
    def removeKey(self, key):
        """Permanently removes the specified key from the
        registry. 

        key - Key to be removed. Example:
              RegistryKey("HKEY_CURRENT_USER\\Control Panel")

        Throws WindowsRegistryException if the key cannot be
        deleted.
        """
        keyHandle = None
        try:
            keyHandle = _winreg.OpenKey( key.hive(), key.subKey(), 0, _winreg.KEY_ALL_ACCESS )
            _winreg.DeleteKey(keyHandle, key.valueName())
        except Exception, e:
            raise WindowsRegistryException("Unable to open the key " + str(key), e)
        finally:
            if keyHandle is not None:
                keyHandle.Close()

    def removeValue(self, key):
        """Permanently removes the specified value from teh
        registry.  

        key -   The key/value to be removed.  Example:
                RegistryKey("HKEY_CURRENT_USER\\Control Panel\\buttoncolor")

        Throws WindowsRegistryException if the value cannot be
        removed.
        """
        keyHandle = None
        try:
            keyHandle = _winreg.OpenKey( key.hive(), key.subKey(), 0, _winreg.KEY_ALL_ACCESS )
            _winreg.DeleteValue(keyHandle, key.valueName())
        except Exception, e:
            raise WindowsRegistryException("Unable to open the key " + str(key), e)
        finally:
            if keyHandle is not None:
                keyHandle.Close()

class RegistryKey:
    """Represents an entire key and value name in the Windows
    registry, or represents only a key without the value name.
    """

    SEPARATOR = '\\'
    
    def __init__(self, key):
        """Creates this.

        key - the full key name, including hive, subkey, and
              optional value name.  Examples:
              "HKEY_CURRENT_USER\\Console\\CursorSize" if
              value name is included, or 
              "HKEY_CURRENT_USER\\Console" if value name is
              not included.
        """
        self.keys = key.split(self.SEPARATOR)

    def __getitem__(self, key):
        """Accesses a piece of this key. For example, if the key is
        'HKEY_CURRENT_USER\Console\CurrentUser', then key[1] will
        return 'Console'.
        """
        return self.keys[key]

    def __len__(self):
        """Returns the number of parts that make up this key.
        For example, for the key "ROOT\aaa\bbb\ccc", len(self) is four.
        """
        return len(self.keys)

    def __setitem__(self, key, item):
        """Sets a piece of this key.  See __getitem__ for an example."""
        self.keys[key] = item

    def __str__(self):
        """String representation of this key."""
        return self.makeFullKey()

    def hive(self):
        """Returns the hive of this key.  The hive is a constant
        defined in _winreg and can be one of _winreg.HKEY_CLASSES_ROOT,
        _winreg.HKEY_CURRENT_USER, _winreg.HKEY_LOCAL_MACHINE,
        _winreg.HKEY_USERS, _winreg.HKEY_CURRENT_CONFIG.

        Throws WindowsRegistryException if the hive name is not a
        valid Windows hive name.
        """
        if self.hiveName() == "HKEY_CLASSES_ROOT":
            return _winreg.HKEY_CLASSES_ROOT
        elif self.hiveName() == "HKEY_CURRENT_USER":
            return _winreg.HKEY_CURRENT_USER
        elif self.hiveName() == "HKEY_LOCAL_MACHINE":
            return _winreg.HKEY_LOCAL_MACHINE
        elif self.hiveName() == "HKEY_USERS":
            return _winreg.HKEY_USERS
        elif self.hiveName() == "HKEY_CURRENT_CONFIG":
            return _winreg.HKEY_CURRENT_CONFIG
        else:
            raise WindowsRegistryException(self.hiveName() + \
                " is not a Windows registry hive name.")
        
    def hiveName(self):
        """Returns the name of the top-level key or hive.
        For example, if this key is 'HKEY_CURRENT_USER\Console\CursorSize',
        then self.hiveName() is 'HKEY_CURRENT_USER'.
        """
        return self[0]
    
    def makeFullKey(self):
        """Returns the full key as given to the init method."""
        return self.SEPARATOR.join(self.keys)

    def subKey(self):
        """Returns this key's subkey.  For example, if this key is
        "HKEY_CURRENT_USER\Console\Cursors\CursorSize," then self.subKey() is
        'Console\Cursors'.  If the key contains only two components, as in
        "HKEY_CURRENT_USER\Console," then there is not subKey and this
        method returns an empty string.
        """
        return self.SEPARATOR.join( self[1: len(self)-1] )
    
    def valueName(self):
        """Returns this key's value name.  For example, if this key is
        "HKEY_CURRENT_USER\Console\CursorSize", then self.valueName() is
        "CursorSize."
        """
        return self[ len(self)-1 ]