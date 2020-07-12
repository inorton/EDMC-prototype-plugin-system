"""
Prototype new EDMC Plugin system
"""
import os
import sys
import tkinter
import importlib
from EDMCPlugin.base import EDMCPluginBase
from EDMCPlugin.ui import EDMCUIPluginBase, EDMCUIDisplayRow, EDMCUIDisplayRowspan, EDMCUIDisplayTable
try:
    import config
except ImportError:
    config = None


API_PLUGINS_FOLDER = "experimental-new-plugins"
API_PLUGIN_LOADER = "load.py"


class EDMCPluginController(object):

    def __init__(self):
        self.plugins = []

    def find_plugins(self):
        """
        Scan for plugins to load
        :return:
        """
        if len(self.plugins):
            # only let this happen once per launch
            return

        if config:
            path = os.path.abspath(os.path.join(os.path.dirname(config.config.plugin_dir), API_PLUGINS_FOLDER))
            for item in sorted(os.listdir(path)):
                loader_file = os.path.join(path, item, API_PLUGIN_LOADER)
                if os.path.exists(loader_file):
                    print("Found plugin file: {}".format(loader_file))
                    loader_dir = os.path.join(path, item)
                    orig_path = list(sys.path)
                    try:
                        if loader_dir not in sys.path:
                            sys.path.append(loader_dir)
                        plugin_module = importlib.machinery.SourceFileLoader(
                            'plugin_{}'.format(item.encode(
                                encoding='ascii',
                                errors='replace').decode('utf-8').replace('.', '_')),
                            loader_file).load_module()
                        if "__plugin__" in dir(plugin_module):
                            plugin = plugin_module.__plugin__
                            if not isinstance(plugin, EDMCPluginBase):
                                raise ValueError("{} from {} is not a subclass of EDMCPluginBase".format(
                                    str(plugin), item))
                            print("Loaded plugin {} from module {}".format(str(plugin), item))
                            self.plugins.append(plugin)

                        else:
                            raise AttributeError("plugin {} lacks __plugin__".format(loader_dir))
                    except Exception as err:
                        print("Error attempting to discover plugin {} : {}".format(loader_file, err))
                        sys.path = orig_path

    def start_plugins(self):
        """
        Start each plugin, and load it's GUI elements
        :return:
        """
        good_plugins = []
        for plugin in list(self.plugins):
            print("Starting plugin: {}".format(plugin))
            try:
                plugin.plugin_start()
                good_plugins.append(plugin)
            except Exception as err:
                print("Error starting plugin {}".format(err))
        self.plugins = good_plugins

    def journal_entry(self, cmdr, event):
        """
        Send a journal entry to all plugins
        :param cmdr:
        :param event:
        :return:
        """
        for plugin in self.plugins:
            try:
                plugin.journal_event(cmdr, event)
            except Exception as err:
                print("Error sending journal to {} plugin {}".format(plugin, err))

    def dashboard_entry(self, cmdr, event):
        """
        Send a dashboard entry to all plugins
        :param cmdr:
        :param event:
        :return:
        """
        for plugin in self.plugins:
            try:
                plugin.dashboard_event(cmdr, event)
            except Exception as err:
                print("Error sending dashboard to {} plugin {}".format(plugin, err))

    def setup_ui_entries(self, parent):
        """
        Create the UI elements for a plugin
        :return:
        """
        def add_row(left, right):
            rowoffset = parent.grid_size()[1]
            if left:
                left.grid(row=rowoffset, column=0, sticky=tkinter.W)
            if right:
                right.grid(row=rowoffset, column=1, sticky=tkinter.EW)

        for plugin in self.plugins:
            if isinstance(plugin, EDMCUIPluginBase):
                try:
                    tkinter.Frame(parent, highlightthickness=1).grid(columnspan=2, sticky=tkinter.EW)  # separator
                    row = parent.grid_size()[1]
                    if isinstance(plugin, EDMCUIDisplayRow):
                        left, right = plugin.create_row(parent)
                        add_row(left, right)

                    elif isinstance(plugin, EDMCUIDisplayTable):
                        plugin_rows = plugin.create_rows(parent)
                        for item in plugin_rows:
                            left, right = item[0], item[1]
                            add_row(left, right)

                    elif isinstance(plugin, EDMCUIDisplayRowspan):
                        plugin_rowspan = plugin.create_rowspan(parent)
                        if plugin_rowspan:
                            plugin_rowspan.grid(row=row, column=0, columnspan=2, sticky=tkinter.EW)

                except Exception as err:
                    print("Error setting up UI element for {} : {}".format(plugin, err))


manager = EDMCPluginController()


def plugin_start3(ignored):
    manager.find_plugins()
    manager.start_plugins()


def journal_entry(cmdr, isbeta, system, station, entry, state):
    if not entry:
        entry = {}

    event = {
        "beta": isbeta,
        "system": system,
        "station": station,
        "entry": entry,
        "state": state
    }

    manager.journal_entry(cmdr, event)


def dashboard_entry(cmdr, isbeta, entry):
    if not entry:
        entry = {
            "Flags": 0
        }
    event = {
        "beta": isbeta,
        "cmdr": cmdr,
        "entry": entry
    }
    manager.dashboard_entry(cmdr, event)


def plugin_app(parent):
    manager.setup_ui_entries(parent)
