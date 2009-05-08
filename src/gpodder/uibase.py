# -*- coding: utf-8 -*-
"""
UI Base Module for GtkBuilder

Based on SimpleGladeApp.py Copyright (C) 2004 Sandino Flores Moreno
"""

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

import os
import sys
import re

import tokenize

import gtk

class GtkBuilderWidget(object):
    def __init__(self, ui_folder, textdomain, **kwargs):
        """
        Loads the UI file from the specified folder (with translations
        from the textdomain) and initializes attributes.

        ui_folder:
            Folder with GtkBuilder .ui files

        textdomain:
            The textdomain to be used for translating strings

        **kwargs:
            Keyword arguments will be set as attributes to this window
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.builder = gtk.Builder()
        #self.builder.set_translation_domain(textdomain)

        print >>sys.stderr, 'Creating new from file', self.__class__.__name__

        ui_file = '%s.ui' % self.__class__.__name__.lower()
        self.builder.add_from_file(os.path.join(ui_folder, ui_file))

        self.builder.connect_signals(self)
        self.set_attributes()

        self.new()

    def set_attributes(self):
        """
        Convert widget names to attributes of this object.

        It means a widget named vbox-dialog in GtkBuilder
        is refered using self.vbox_dialog in the code.
        """
        for widget in self.builder.get_objects():
            if not hasattr(widget, 'get_name'):
                continue

            widget_name = widget.get_name()
            widget_api_name = '_'.join(re.findall(tokenize.Name, widget_name))
            widget.set_name(widget_api_name)
            if hasattr(self, widget_api_name):
                raise AttributeError("instance %s already has an attribute %s" % (self,widget_api_name))
            else:
                setattr(self, widget_api_name, widget)
    
    @property
    def main_window(self):
        """Returns the main window of this GtkBuilderWidget"""
        return getattr(self, self.__class__.__name__)

    def new(self):
        """
        Method called when the user interface is loaded and ready to be used.
        At this moment, the widgets are loaded and can be refered as self.widget_name
        """
        pass

    def main(self):
        """
        Starts the main loop of processing events.
        The default implementation calls gtk.main()

        Useful for applications that needs a non gtk main loop.
        For example, applications based on gstreamer needs to override
        this method with gst.main()

        Do not directly call this method in your programs.
        Use the method run() instead.
        """
        gtk.main()

    def quit(self):
        """
        Quit processing events.
        The default implementation calls gtk.main_quit()
        
        Useful for applications that needs a non gtk main loop.
        For example, applications based on gstreamer needs to override
        this method with gst.main_quit()
        """
        gtk.main_quit()

    def run(self):
        """
        Starts the main loop of processing events checking for Control-C.

        The default implementation checks wheter a Control-C is pressed,
        then calls on_keyboard_interrupt().

        Use this method for starting programs.
        """
        try:
            self.main()
        except KeyboardInterrupt:
            self.on_keyboard_interrupt()

    def on_keyboard_interrupt(self):
        """
        This method is called by the default implementation of run()
        after a program is finished by pressing Control-C.
        """
        pass
