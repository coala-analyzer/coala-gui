import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GObject

from source.Searchbar.Searchbar import Searchbar
from source.support.EditableLabel import EditableLabel
from source.scrolledWindow.coalaScrolledWindow import coalaScrolledWindow
from source.greeter.GreeterWindow import GreeterWindow
from source.workspace.WorkspaceWindow import WorkspaceWindow


class coalaApp(Gtk.Application):
    def __init__(self,  data_path):
        GObject.type_register(coalaScrolledWindow)
        GObject.type_register(Searchbar)
        GObject.type_register(EditableLabel)
        Gtk.Application.__init__(self,
                                 application_id="org.coala",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        gresource = os.path.join(data_path, 'coala.gresource')
        self.resource = Gio.resource_load(gresource)
        Gio.Resource._register(self.resource)

        self.greeter = None
        self.workspace = None

        self.connect("activate", self.activate)

    def _setup_greeter(self, app):
        self.greeter = GreeterWindow(app)
        self.greeter.list_box.connect("row-activated",
                                      self._setup_workspace,
                                      app)

    def _setup_workspace(self, listbox, listboxrow, app):
        self.workspace = WorkspaceWindow(self,
                                         listboxrow.get_child().get_name())
        self.greeter.hide()
        self.workspace.show()

    def setup_workspace(self, src):
        self.workspace = WorkspaceWindow(self, src)
        self.greeter.hide()
        self.workspace.show()

    def activate(self, app):
        self._setup_greeter(app)
        self.greeter.show()
