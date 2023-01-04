import wx

from layoutdata import LayoutData
from blocksettings import BlockSettings
from nextblocklist import NextBlockListCtrl
from blocksequence import BlockSequenceListCtrl
		
class TrainDlg(wx.Dialog):
	def __init__(self, parent, train):
		self.parent = parent
		
		self.layout = None
		wx.Dialog.__init__(self, self.parent, style=wx.DEFAULT_FRAME_STYLE)

		self.trainObject = train		
		self.trainid = train.GetTrainID()
		self.locoid = 7000
		self.trainTrigger = train.GetTrigger()
		self.east = train.IsEast()
		
		self.blockList = [x for x in train.GetSteps()]
		
		self.title = "Edit Train Step Sequence Dialog"
		self.Bind(wx.EVT_CLOSE, self.OnClose)

		self.availableBlocks = None

		boxStartLoc = wx.StaticBox(self, wx.ID_ANY, " Starting Location ")

		self.chStartBlock = wx.Choice(boxStartLoc, wx.ID_ANY, choices=[], size=(60, -1))
		self.chStartSubBlock = wx.Choice(boxStartLoc, wx.ID_ANY, choices=[], size=(60, -1))
		self.chStartSubBlock.Enable(False)

		self.nextBlockList = NextBlockListCtrl(self)
		self.blockSequence = BlockSequenceListCtrl(self)

		self.bAdd = wx.Button(self, wx.ID_ANY, "Add >>")
		self.Bind(wx.EVT_BUTTON, self.OnBAdd, self.bAdd)
		self.bAdd.Enable(False)
		self.bDel = wx.Button(self, wx.ID_ANY, "<< Del")
		self.Bind(wx.EVT_BUTTON, self.OnBDel, self.bDel)
		self.bDel.Enable(False)

		self.bGenSim = wx.Button(self, wx.ID_ANY, "Simulator\nScript", size=(80, 50))
		self.Bind(wx.EVT_BUTTON, self.OnBGenSim, self.bGenSim)
		self.bGenSim.Enable(False)
		self.bGenAR = wx.Button(self, wx.ID_ANY, "Automatic\nRouter", size=(80, 50))
		self.Bind(wx.EVT_BUTTON, self.OnBGenAR, self.bGenAR)
		self.bGenAR.Enable(False)
		self.bOK = wx.Button(self, wx.ID_ANY, "OK", size=(80, 50))
		self.Bind(wx.EVT_BUTTON, self.OnBOK, self.bOK)
		self.bCancel = wx.Button(self, wx.ID_ANY, "Cancel", size=(80, 50))
		self.Bind(wx.EVT_BUTTON, self.OnBCancel, self.bCancel)

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
		vszr.AddSpacer(20)

		hsz = wx.BoxSizer(wx.HORIZONTAL)
		hsz.AddSpacer(20)
		hsz.Add(vszl)
		hsz.AddSpacer(20)
		hsz.Add(vszm)
		hsz.AddSpacer(20)
		hsz.Add(vszr)
		hsz.AddSpacer(20)
		
		vsz = wx.BoxSizer(wx.VERTICAL)
		vsz.Add(hsz)
		vsz.AddSpacer(10)
		
		hsz = wx.BoxSizer(wx.HORIZONTAL)
		hsz.Add(self.bOK)
		hsz.AddSpacer(20)
		hsz.Add(self.bCancel)
		hsz.AddSpacer(50)
		hsz.Add(self.bGenSim)
		hsz.AddSpacer(30)
		hsz.Add(self.bGenAR)
		
		vsz.Add(hsz, 0, wx.ALIGN_CENTER_HORIZONTAL)
		vsz.AddSpacer(20)

		self.SetSizer(vsz)
		self.Fit()
		self.Layout()

		self.startBlock = None
		self.startSubBlock = None
		self.blockList = []
		wx.CallAfter(self.Initialize)

	def ShowTitle(self):
		titleString = "%s: %s(%s)" % (self.title, self.trainid, self.locoid)

		self.SetTitle(titleString)

	def Initialize(self):
		self.modified = False
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

		for step in self.trainObject.GetSteps():		
			self.blockSequence.AddBlock(step[0], step[1], step[2], step[3])

		
	def SetModified(self, flag=True):
		print("modified")
		self.modified = flag

	def OnChStartBlock(self, event):
		self.SetModified()
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
		self.SetModified()
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
		self.SetModified()
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
		self.SetModified()
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
				
	def GetResults(self):
		return self.blockSequence.GetBlocks()

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
		self.DoCancel()
		
	def OnBOK(self, _):
		self.EndModal(wx.ID_OK)
		
	def OnBCancel(self, _):
		self.DoCancel()
		
	def DoCancel(self):
		if self.modified:
			dlg = wx.MessageDialog(self, 'Train steps have been modified.\nAre you sure you want to cancel?\nPress "Yes" to exit and lose changes,\nor "No" to return and save them.',
					'Changes will be lost', wx.YES_NO | wx.ICON_WARNING)
			rc = dlg.ShowModal()
			dlg.Destroy()
			if rc != wx.ID_YES:
				return
			
		self.EndModal(wx.ID_CANCEL)
