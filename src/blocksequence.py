import wx


class BlockSequenceListCtrl(wx.ListCtrl):
	def __init__(self, parent):
		self.parent = parent

		wx.ListCtrl.__init__(
			self, parent, wx.ID_ANY, size=(340, 300),
			style=wx.LC_REPORT|wx.LC_VIRTUAL|wx.LC_VRULES
			)

		self.blocks = []
		self.selected = None

		self.InsertColumn(0, "Block")
		self.InsertColumn(1, "Signal")
		self.InsertColumn(2, "OS")
		self.InsertColumn(3, "Route")
		self.SetColumnWidth(0, 80)
		self.SetColumnWidth(1, 80)
		self.SetColumnWidth(2, 80)
		self.SetColumnWidth(3, 80)

		self.SetItemCount(0)

		self.normalA = wx.ItemAttr()
		self.normalB = wx.ItemAttr()
		self.normalA.SetBackgroundColour(wx.Colour(225, 255, 240))
		self.normalB.SetBackgroundColour(wx.Colour(138, 255, 197))

		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)

	def AddBlock(self, blk, sig, os, rte):
		self.blocks.append([blk, sig, os, rte])
		self.refreshItemCount()

	def DelBlock(self):
		self.blocks.pop()
		self.refreshItemCount()
		if len(self.blocks) == 0:
			return None

		return self.blocks[-1]
			
	def GetBlocks(self):
		return self.blocks

	def refreshItemCount(self):
		self.parent.reportNonEmpty(len(self.blocks) != 0)
		self.SetItemCount(len(self.blocks))

	def setSelection(self, tx):
		self.selected = tx;
		if tx is not None:
			self.Select(tx)

	def GetSelection(self):
		return self.selected

	def OnItemSelected(self, event):
		self.setSelection(event.Index)

	def OnGetItemText(self, item, col):
		return self.blocks[item][col]

	def OnGetItemAttr(self, item):
		if item % 2 == 1:
			return self.normalB
		else:
			return self.normalA
