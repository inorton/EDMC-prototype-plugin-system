"""
A Basic plugin that provides some user interface elements for the main EDMC window
"""
from .base import EDMCPluginBase
from abc import abstractmethod


class EDMCUIPluginBase(EDMCPluginBase):
    """
    A Plugin that adds a Tk UI element to the EDMC window
    """

    def create_prefs_tab(self):
        """
        Return a new preferences tab
        :return:
        """
        pass


class EDMCUIDisplayRow(object):
    """
    A Plugin Mixin to display one row of two widgets
    """

    @abstractmethod
    def create_row(self, parent):
        pass


class EDMCUIDisplayRowspan(object):
    """
    A Plugin Mixin to display a widget that spans the whole UI
    """

    @abstractmethod
    def create_rowspan(self, parent):
        pass


class EDMCUIDisplayTable(object):
    """
    A Plugin Mixin to display a 2 by X table.
    """

    @abstractmethod
    def create_rows(self, parent):
        pass