# import hotshot
# _prof = hotshot.Profile("hotshot.prf")

import os, traceback

import wx

# from MiscEvent import KeyFunctionSinkAR
from pwiki.wxHelper import appendToMenuByMenuDesc

from pwiki.WindowLayout import LayeredControlPanel
from pwiki.Configuration import isWindows

from . import DatedWikiWordFilters

from .TimelinePanel import TimelinePanel
from .CalendarPanel import CalendarPanel
from .VersioningGui import VersionExplorerPanel

class TimeViewCtrl(wx.Notebook):
    def __init__(self, parent, ID, mainControl):
        wx.Notebook.__init__(self, parent, ID)

        self.mainControl = mainControl

        wikiWordFilter = DatedWikiWordFilters.DatedWikiWordFilterModified()

        self.modifiedPanel = LayeredControlPanel(self, -1)
        self.versionPanel = LayeredControlPanel(self, -1)

        tlp = TimelinePanel(self.modifiedPanel, -1, self.mainControl,
                wikiWordFilter)
#         tlp = CalendarPanel(self.modifiedPanel, -1, self.mainControl,
#                 wikiWordFilter)
        self.modifiedPanel.setSubControl("timeline", tlp)
        self.modifiedPanel.switchSubControl("timeline")

#         self.modifiedPanel = TimelinePanel(self, -1, self.mainControl, wikiWordFilter)
#         self.modifiedPanel = CalendarPanel(self, -1, self.mainControl, wikiWordFilter)
        self.AddPage(self.modifiedPanel, wikiWordFilter.getDisplayName())


        vep = VersionExplorerPanel(self.versionPanel, -1, self.mainControl)
        self.versionPanel.setSubControl("version explorer", vep)
        self.versionPanel.switchSubControl("version explorer")
        
        self.AddPage(self.versionPanel, _(u"Versions"))
        
        self.notebookPages = [self.modifiedPanel, self.versionPanel]
        self.runningPageChangedEvent = False

#         for i, w in enumerate(self.notebookPages):
#             w.setLayerVisible(0 == i)

        lastTab = self.mainControl.getConfig().get("main",
                "timeView_lastSelectedTab")

        if lastTab == u"version":
            tabIdx = 1
        else:
            tabIdx = 0
        
        self.ChangeSelection(tabIdx)
        self._adjustVisibilitySubControls(tabIdx)


        wx.EVT_CONTEXT_MENU(self, self.OnContextMenu)
        wx.EVT_NOTEBOOK_PAGE_CHANGED(self, self.GetId(),
                self.OnNotebookPageChanged)


    def close(self):
        """
        """
        lastTab = (u"modified", u"version")[self.GetSelection()]

        self.mainControl.getConfig().set("main",
                "timeView_lastSelectedTab", lastTab)
        
        for p in self.notebookPages:
            p.close()
        
        self.notebookPages = []


    def miscEventHappened(self, miscevt):
        """
        Handle misc events
        """
        pass


    def setLayerVisible(self, vis, scName=""):
        pass


    def OnContextMenu(self, evt):
        pos = self.ScreenToClient(wx.GetMousePosition())
        tab = self.HitTest(pos)[0]
        if tab == wx.NOT_FOUND:
            return
        
        activeWindow = self.GetPage(tab).getCurrentSubControl()
        # Show menu
        activeWindow.showContextMenuOnTab()

        
    def OnNotebookPageChanged(self, evt):
        # Tricky hack to set focus to the notebook page
        tabIdx = evt.GetSelection()
        self._adjustVisibilitySubControls(tabIdx)
        nbPage = self.notebookPages[tabIdx]

        # Now we can set the focus back to the presenter
        # which in turn sets it to the active subcontrol
        wx.CallAfter(self._postponedOnNotebookPageChanged, nbPage)
        evt.Skip()
#         self.mainControl.Freeze()


    def _postponedOnNotebookPageChanged(self, nbPage):
#         try:
        nbPage.SetFocus()
#         finally:
#             self.mainControl.Thaw()


#     def OnNotebookPageChanged(self, evt):
#         if self.runningPageChangedEvent:
#             self.runningPageChangedEvent = False
#             evt.Skip()
#             print "--Ran notebook"
#             return
# 
#         try:
#             # Flag the event to ignore and resend it.
#             # It is then processed by wx.Notebook code
#             # where the focus is set to the notebook itself
#             self.runningPageChangedEvent = True
#             tabIdx = evt.GetSelection()
# 
#             nbPage = self.notebookPages[tabIdx]
#             self._adjustVisibilitySubControls(tabIdx)
# 
#             self.ProcessEvent(evt)
# 
#             # Now we can set the focus back to the presenter
#             # which in turn sets it to the active subcontrol
#             print "--SetFocus", repr(nbPage)
#             nbPage.SetFocus()
#         finally:
#             self.runningPageChangedEvent = False


    def _adjustVisibilitySubControls(self, selIdx):
        for i, w in enumerate(self.notebookPages):
            w.setLayerVisible(selIdx == i)






