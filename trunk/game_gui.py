#!/usr/bin/env python
#
# This file is part of MMBN Online
# MMBN Online is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# MMBN Online is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with MMBN Online.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2008-2009 Chris Santiago
# http://mmbnonline.net/

"""MMBNOnline GUI, powered by wxPython and Twisted."""

from wx import wx
from twisted.internet import wxreactor; wxreactor.install()
from twisted.internet import reactor

class MMBNOFrame(wx.MDIParentFrame):
    """All windows and their respective event mappings are handled
    by `MMBNOFrame`, being a subclass of `wx.Frame`."""
    
    def __init__(self, parent, frame_id, title):
        """The window typically starts off with the Dashboard; the menubar
        persists throughout the program. In the dashboard, we let the user 
        choose between editing his chip folders or just joining a server."""
        wx.Frame.__init__(self, parent, frame_id, title, wx.DefaultPosition,
            wx.Size(608, 357))
        background = wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT)
        self.SetBackgroundColour(background)
        self.CreateStatusBar()
        self.bsizer_dashboard = wx.BoxSizer(wx.VERTICAL)
        self.bttn = {}
        buttons = {
            'chips': [u'Chips Folder', self._chipsfolder],
            'join': [u'Join Server', self._joinserver]
        }
        self.dashboard_buttons(buttons)
        self.SetSizer(self.bsizer_dashboard)
        self.SetMenuBar(self.dashboard_menubar())
        self.Layout()

    def dashboard_buttons(self, buttons):
        """Creates the navigational buttons using a dictionary containing
        the label and the event-handler function, and append then
        append them to the box sizer."""
        button_font = wx.Font(20, 70, 90, 92, False, 'Trebuchet MS')
        button_fg = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)
        button_bg = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        button_size = wx.Size(300, 50)
        button_alignment = wx.BU_BOTTOM|wx.BU_EXACTFIT
        button_position = wx.ALIGN_CENTER_HORIZONTAL|wx.ALL
        button_event = wx.EVT_LEFT_DCLICK

        for k in buttons:
            self.bttn[k] = wx.Button(self, wx.ID_ANY, buttons[k][0],
            wx.Point(-1, -1), wx.DefaultSize, button_alignment)
            self.bttn[k].SetFont(button_font)
            self.bttn[k].SetForegroundColour(button_fg)
            self.bttn[k].SetBackgroundColour(button_bg)
            self.bttn[k].SetMinSize(button_size)
            self.bttn[k].SetMaxSize(button_size)
            self.bttn[k].Bind(button_event, buttons[k][1])
            self.bsizer_dashboard.Add(self.bttn[k], 0, button_position, 5)

    def dashboard_menubar(self):
        """Create the menubar, which perists throughout the application."""
        menubar = wx.MenuBar()

        menu_file = wx.Menu()
        menu_file.Append(wx.ID_ANY, u'New Folder...')
        menu_file.Append(wx.ID_ANY, u'Load Folder...')

        menu_tools = wx.Menu()
        menu_tools.Append(wx.ID_ANY,  u'Program Settings')

        menu_information = wx.Menu()
        menu_information.Append(wx.ID_ANY, u'Chip Library')
        menu_information.Append(wx.ID_ANY, u'Website')
        menu_information.Append(wx.ID_ANY, 'About')

        menubar.Append(menu_file, u'&File')
        menubar.Append(menu_tools, u'&Tools')
        menubar.Append(menu_information, u'&Information')

        return menubar

    def _chipsfolder(self, event):
        """Chip folder management"""
        d = wx.FileDialog(None, message=u'Load a Folder', style=wx.OPEN)
        if d.ShowModal() == wx.ID_OK:
           print 'Selected:', d.GetPath()

    def _joinserver(self, event):
        """Grabs a list of servers that are connected to the registry."""
        pass


class MMBNO(wx.App):
    """This class doesn't do much except take care of instantiating the
    MMBNOFrame class."""

    def OnInit(self):
        """Create the window (`MMBNOFrame`), set it as the top window and
        display it."""
        frame = MMBNOFrame(None, -1, u'MMBN Online')
        frame.Show(True)
        self.SetTopWindow(frame)
        return True


reactor.registerWxApp(MMBNO(0))
reactor.run()