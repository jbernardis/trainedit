import wx
import wx.lib.newevent

from layoutdata import LayoutData
from blocksettings import BlockSettings
from nextblocklist import NextBlockListCtrl
from blocksequence import BlockSequenceListCtrl


class MainFrame(wx.Frame):
	def __init__(self, trainid, locoid, east):
		self.layout = None
		wx.Frame.__init__(self, None, style=wx.DEFAULT_FRAME_STYLE)
		
		self.trainid = trainid
		self.locoid = locoid
		self.trainTrigger = "R"
		self.east = east
		
		self.title = "PSRY Train Editor"
		self.Bind(wx.EVT_CLOSE, self.OnClose)

		self.availableBlocks = None

		boxStartLoc = wx.StaticBox(self, wx.ID_ANY, " Starting Location ")

		self.chStartBlock = wx.Choice(boxStartLoc, wx.ID_ANY, choices=[], size=(60, -1))
		self.chStartSubBlock = wx.Choice(boxStartLoc, wx.ID_ANY, choices=[], size=(60, -1))
		self.chStartSubBlock.Enable(False)

		self.nextBlockList = NextBlockListCtrl(self)

		self.blockSequence = BlockSequenceListCtrl(self);

		self.bAdd = wx.Button(self, wx.ID_ANY, "Add >>")
		self.Bind(wx.EVT_BUTTON, self.OnBAdd, self.bAdd)
		self.bAdd.Enable(False)
		self.bDel = wx.Button(self, wx.ID_ANY, "<< Del")
		self.Bind(wx.EVT_BUTTON, self.OnBDel, self.bDel)
		self.bDel.Enable(False)

		self.bGenSim = wx.Button(self, wx.ID_ANY, "Sim Script")
		self.Bind(wx.EVT_BUTTON, self.OnBGenSim, self.bGenSim)
		self.bGenSim.Enable(False)
		self.bGenAR = wx.Button(self, wx.ID_ANY, "Auto Router")
		self.Bind(wx.EVT_BUTTON, self.OnBGenAR, self.bGenAR)
		self.bGenAR.Enable(False)

		topBorder = boxStartLoc.GetBordersForSizer()[0]
		bsizer = wx.BoxSizer(wx.VERTICAL)
		bsizer.AddSpacer(10+topBorder)

		hsz = wx.BoxSizer(wx.HORIZONTAL)

		hsz.AddSpacer(20)

		vsz = wx.BoxSizer(wx.VERTICAL)
		vsz.Add(wx.StaticText(boxStartLoc, wx.ID_ANY, "Block"))
		vsz.AddSpacer(5)
		vsz.Add(self.chStartBlock)
		hsz.Add(vsz)
		hsz.AddSpacer(20)
		vsz = wx.BoxSizer(wx.VERTICAL)
		vsz.Add(wx.StaticText(boxStartLoc, wx.ID_ANY, "Sub-block"))
		vsz.AddSpacer(5)
		vsz.Add(self.chStartSubBlock)
		hsz.Add(vsz)

		hsz.AddSpacer(20)

		bsizer.Add(hsz)
		bsizer.AddSpacer(20)

		boxStartLoc.SetSizer(bsizer)

		vszl = wx.BoxSizer(wx.VERTICAL)
		vszl.AddSpacer(20)
		vszl.Add(boxStartLoc)
		vszl.AddSpacer(20)
		vszl.Add(wx.StaticText(self, wx.ID_ANY, "Next Available Blocks"), 1, wx.ALIGN_CENTER_HORIZONTAL)
		vszl.AddSpacer(10)
		vszl.Add(self.nextBlockList)
		vszm = wx.BoxSizer(wx.VERTICAL)
		vszm.AddSpacer(220)
		vszm.Add(self.bAdd, 0, wx.ALIGN_CENTER_HORIZONTAL)
		vszm.AddSpacer(10)
		vszm.Add(self.bDel, 0, wx.ALIGN_CENTER_HORIZONTAL)
		vszm.AddSpacer(20)

		vszr = wx.BoxSizer(wx.VERTICAL)
		vszr.AddSpacer(20)
		vszr.Add(wx.StaticText(self, wx.ID_ANY, "Blocks in Train Route"), 1, wx.ALIGN_CENTER_HORIZONTAL)
		vszr.AddSpacer(10)
		vszr.Add(self.blockSequence)
		vszr.AddSpacer(10)
		hsz = wx.BoxSizer(wx.HORIZONTAL)
		hsz.Add(self.bGenSim)
		hsz.AddSpacer(30)
		hsz.Add(self.bGenAR)
		vszr.Add(hsz, 0, wx.ALIGN_CENTER_HORIZONTAL)
		vszr.AddSpacer(20)

		hsz = wx.BoxSizer(wx.HORIZONTAL)
		hsz.AddSpacer(20)
		hsz.Add(vszl)
		hsz.AddSpacer(20)
		hsz.Add(vszm)
		hsz.AddSpacer(20)
		hsz.Add(vszr)
		hsz.AddSpacer(20)

		self.SetSizer(hsz)
		self.Fit()
		self.Layout()

		self.startBlock = None
		self.startSubBlock = None
		self.blockList = []
		wx.CallAfter(self.Initialize)

	def ShowTitle(self):
		titleString = self.title
		self.SetTitle(titleString)

	def Initialize(self):
		self.ShowTitle()
		self.layout = LayoutData()
		self.blockSettings = BlockSettings()

		self.blockList = self.layout.GetBlocks()
		self.chStartBlock.SetItems(self.blockList)
		self.startBlock = self.blockList[0]
		self.chStartBlock.SetSelection(0)
		self.GetAvailableBlocks(self.startBlock)
		self.nextBlockList.SetBlocks(self.availableBlocks)
		self.Bind(wx.EVT_CHOICE, self.OnChStartBlock, self.chStartBlock)
		self.Bind(wx.EVT_CHOICE, self.OnChStartSubBlock, self.chStartSubBlock)

	def OnChStartBlock(self, event):
		self.startBlock = event.GetString()
		self.GetAvailableBlocks(self.startBlock)
		self.nextBlockList.SetBlocks(self.availableBlocks)
		subBlocks = self.layout.GetSubBlocks(self.startBlock)
		if len(subBlocks) == 0:
			self.startSubBlock = None
			self.chStartSubBlock.Enable(False)
		else:
			self.chStartSubBlock.Enable(True)
			self.chStartSubBlock.SetItems(subBlocks)
			self.startSubBlock = subBlocks[0]
			self.chStartSubBlock.SetSelection(0)

	def OnChStartSubBlock(self, event):
		self.startSubBlock = event.GetString()

	def reportNonEmpty(self, seqNotEmpty):
		self.bDel.Enable(seqNotEmpty)
		self.bGenSim.Enable(seqNotEmpty)
		self.bGenAR.Enable(seqNotEmpty)

	def reportSelection(self, tx, activate):
		if tx is None:
			self.bAdd.Enable(False)
		else:
			if activate:
				self.SelectNextBlock(tx)
			else:
				self.bAdd.Enable(True)

	def OnBAdd(self, _):
		tx = self.nextBlockList.GetSelection()
		if tx is not None:
			self.SelectNextBlock(tx)

	def SelectNextBlock(self, tx):
		self.chStartBlock.Enable(False)
		self.chStartSubBlock.Enable(False)
		nextBlock  = self.availableBlocks[tx][0]
		nextSignal = self.availableBlocks[tx][1]
		nextOS     = self.availableBlocks[tx][2]
		nextRoute  = self.availableBlocks[tx][3]

		self.blockSequence.AddBlock(nextBlock, nextSignal, nextOS, nextRoute)
		self.GetAvailableBlocks(nextBlock)
		self.nextBlockList.SetBlocks(self.availableBlocks)

	def OnBDel(self, _):
		r = self.blockSequence.DelBlock()
		if r is None:
			self.bDel.Enable(False)
			self.bAdd.Enable(False)
			self.chStartBlock.Enable(True)
			self.chStartSubBlock.Enable(True)
			self.GetAvailableBlocks(self.startBlock)
			self.nextBlockList.SetBlocks(self.availableBlocks)
		else:
			self.GetAvailableBlocks(r[0])
			self.nextBlockList.SetBlocks(self.availableBlocks)

	def GetAvailableBlocks(self, blk):
		rteList = self.layout.GetRoutesForBlock(blk)
		self.availableBlocks = []
		for r in rteList:
			e = self.layout.GetRouteEnds(r)
			s = self.layout.GetRouteSignals(r)
			os = self.layout.GetRouteOS(r)
			if e[0] == blk:
				self.availableBlocks.append([e[1], s[0], os, r])
			elif e[1] == blk:
				self.availableBlocks.append([e[0], s[1], os, r])

	def OnBGenSim(self, _):
		steps = []
		tm = self.blockSettings.GetBlockTraversalTime(self.startBlock)
		steps.append("{!placetrain!: {!block!: !%s!, !name!: !%s!, !loco!: !%s!, !time!: %d, !length!: %d}}" %
				(self.startBlock, self.trainid, self.locoid, tm, 3))

		for b in self.blockSequence.GetBlocks():
			subBlocks = self.layout.GetSubBlocks(b[0])
			stopBlocks = self.layout.GetStopBlocks(b[0])
			print(str(subBlocks))
			print(str(stopBlocks))
			blks = []
			if self.east:
				if stopBlocks[1]:
					blks.append(stopBlocks[1])
				blks.append(b[0])
				if stopBlocks[0]:
					blks.append(stopBlocks[0])
			else:
				if stopBlocks[0]:
					blks.append(stopBlocks[0])
				blks.append(b[0])
				if stopBlocks[1]:
					blks.append(stopBlocks[1])
			blkString = ",".join(blks)
			steps.append("{!waitfor!: {!signal!: !%s!, !route!: !%s!, !os!: !%s!, !block!: !%s!}}" %
				(b[1], b[3], b[2], blkString))
			tm = self.blockSettings.GetBlockTraversalTime(b[2])
			steps.append("{!movetrain!: {!block!: !%s!, !time!: %d}}" % (b[2], tm))
			for blk in blks:
				tm = self.blockSettings.GetBlockTraversalTime(blk)
				steps.append("{!movetrain!: {!block!: !%s!, !time!: %d}}" % (blk, tm))

		print(",\n".join(steps).replace('!', '"'))

	def OnBGenAR(self, _):
		lastBlock = self.startBlock
		script = ["{\n  !%s!: {" % self.trainid]
		steps = []
		for b in self.blockSequence.GetBlocks():
			if self.trainTrigger == "B":
				trigger = self.blockSettings.GetBlockTriggerPoint(lastBlock)
			else:
				trigger = self.trainTrigger
				
			steps.append("    !%s!: {!route!: !%s!, !trigger!: !%s!}" % (lastBlock, b[3], trigger))
			lastBlock = b[0]
		script.append(",\n".join(steps))
		script.append("  }\n}")
		print("\n".join(script).replace('!', '"'))

	def OnClose(self, _):
		self.Destroy()
