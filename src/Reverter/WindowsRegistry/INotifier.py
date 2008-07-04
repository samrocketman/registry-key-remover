"""
    Interface class that allows the Windows Registry class to notify it's caller 
    when events occur 
    author: Corey Fournier
"""
class INotifier:
    def keyRemoved(self,key):
        """Notifies the caller if when a key is removed"""
        pass
    def valueRemoved(self,key):
        """Notifies the caller if when a value is removed"""
        pass
    def allSubKeysRemoved(self,key):
        """Notifies the caller if when a parent and all Sub Keys are removed"""
        pass
    