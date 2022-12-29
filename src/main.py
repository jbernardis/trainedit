import wx

from mainframe import MainFrame 


class App(wx.App):
	def OnInit(self):
		self.frame = MainFrame("HEX", 7600, True)
		self.frame.Show()
		return True


app = App(False)
app.MainLoop()