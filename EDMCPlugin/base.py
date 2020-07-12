"""
The Advanced Plugin Interface base class
"""
from abc import ABC, abstractmethod


class EDMCPluginBase(ABC):
    """
    The simplest abstract class for a plugin.
    """

    def __str__(self):
        return "EDMC Plugin {} {}".format(self.plugin_name(), self.plugin_version())

    @abstractmethod
    def plugin_name(self):
        pass

    @abstractmethod
    def plugin_version(self):
        pass

    @abstractmethod
    def plugin_start(self):
        pass

    def plugin_stop(self):
        pass

    def journal_event(self, cmdr, entry):
        pass

    def dashboard_event(self, cmdr, entry):
        pass

    def cmdr_event(self, cmdr):
        pass
