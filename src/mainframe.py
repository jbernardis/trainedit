import wx
import json

from traindlg import TrainDlg
from train import Trains
from blocksequence import BlockSequenceListCtrl
from layoutdata import LayoutData
from blocksettings import BlockSettings


class MainFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, style=wx.DEFAULT_FRAME_STYLE)
		self.title = "PSRY Train Editor"
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		
		self.cbTrain = wx.ComboBox(self, wx.ID_ANY, "", size=(100, -1),
			 choices=[],
			 style=wx.CB_DROPDOWN | wx.TE_PROCESS_ENTER | wx.CB_SORT)
		self.Bind(wx.EVT_COMBOBOX, self.OnCbTrain, self.cbTrain)
		self.Bind(wx.EVT_TEXT_ENTER, self.OnCbTrainTextEnter, self.cbTrain)
				
		self.chbEast = wx.CheckBox(self, wx.ID_ANY, "EastBound: ")
		self.chbEast.SetValue(True)
		self.Bind(wx.EVT_CHECKBOX, self.OnChbEastbound, self.chbEast)

		self.teStartBlock = wx.TextCtrl(self, wx.ID_ANY, "", size=(80, -1), style=wx.TE_READONLY)	
		
		self.blockSeq = BlockSequenceListCtrl(self, height=200, readonly=True)
		
		
		self.bEditSteps = wx.Button(self, wx.ID_ANY, "Edit\nRoute", size=(80, 50))
		self.Bind(wx.EVT_BUTTON, self.OnBEditSteps, self.bEditSteps)
		self.bDelTrain = wx.Button(self, wx.ID_ANY, "Delete\nTrain", size=(80, 50))
		self.Bind(wx.EVT_BUTTON, self.OnBDelTrain, self.bDelTrain)
		
		trsz = wx.BoxSizer(wx.HORIZONTAL)
		trsz.Add(wx.StaticText(self, wx.ID_ANY, "Train: "), 0, wx.TOP, 5)
		trsz.AddSpacer(5)
		trsz.Add(self.cbTrain)
		
		self.bSave = wx.Button(self, wx.ID_ANY, "Save", size=(80, 50))
		self.Bind(wx.EVT_BUTTON, self.OnBSave, self.bSave)
		self.bExit = wx.Button(self, wx.ID_ANY, "Exit", size=(80, 50))
		self.Bind(wx.EVT_BUTTON, self.OnBExit, self.bExit)
		self.bRevert = wx.Button(self, wx.ID_ANY, "Revert", size=(80, 50))
		self.Bind(wx.EVT_BUTTON, self.OnBRevert, self.bRevert)
		self.bGenSim = wx.Button(self, wx.ID_ANY, "Simulator\nScript", size=(80, 50))
		self.Bind(wx.EVT_BUTTON, self.OnBGenSim, self.bGenSim)
		self.bGenSim.Enable(False)
		self.bGenAR = wx.Button(self, wx.ID_ANY, "Automatic\nRouter", size=(80, 50))
		self.Bind(wx.EVT_BUTTON, self.OnBGenAR, self.bGenAR)
		self.bGenAR.Enable(False)
		
		buttonsz = wx.BoxSizer(wx.HORIZONTAL)
		buttonsz.Add(self.bGenSim)
		buttonsz.AddSpacer(10)
		buttonsz.Add(self.bGenAR)
		buttonsz.AddSpacer(50)
		buttonsz.Add(self.bSave)
		buttonsz.AddSpacer(20)
		buttonsz.Add(self.bRevert)
		buttonsz.AddSpacer(50)
		buttonsz.Add(self.bExit)
		
		vszl = wx.BoxSizer(wx.VERTICAL)
		vszl.AddSpacer(20)
		vszl.Add(trsz, 0, wx.ALIGN_CENTER_HORIZONTAL)
		vszl.AddSpacer(20)
		vszl.Add(self.chbEast, 0, wx.ALIGN_CENTER_HORIZONTAL)
		vszl.AddSpacer(20)
		
		vszr = wx.BoxSizer(wx.VERTICAL)
		vszr.AddSpacer(10)
		hsz = wx.BoxSizer(wx.HORIZONTAL)
		hsz.Add(wx.StaticText(self, wx.ID_ANY, "Starting Block: "))
		hsz.AddSpacer(5)
		hsz.Add(self.teStartBlock)
		vszr.Add(hsz, 0, wx.ALIGN_CENTER_HORIZONTAL)
		vszr.AddSpacer(10)
		vszr.Add(self.blockSeq)
		vszr.AddSpacer(20)
		
		hsz = wx.BoxSizer(wx.HORIZONTAL)
		hsz.Add(self.bEditSteps)
		hsz.AddSpacer(20)
		hsz.Add(self.bDelTrain)
		vszr.Add(hsz, 0, wx.ALIGN_CENTER_HORIZONTAL)
		
		vszr.AddSpacer(20)
		
		hsz = wx.BoxSizer(wx.HORIZONTAL)
		hsz.AddSpacer(20)
		hsz.Add(vszl)
		hsz.AddSpacer(20)
		hsz.Add(vszr)
		hsz.AddSpacer(20)
		
		vsz = wx.BoxSizer(wx.VERTICAL)
		vsz.Add(hsz)
		vsz.AddSpacer(20)
		vsz.Add(buttonsz, 0, wx.ALIGN_CENTER_HORIZONTAL)
		vsz.AddSpacer(20)

		self.SetSizer(vsz)
		self.Fit()
		self.Layout()

		self.layout = LayoutData()
		wx.CallAfter(self.Initialize)
		self.blockSettings = BlockSettings()
		
	def Initialize(self):
		self.selectedTrain = None
		self.modified = False
		self.ShowTitle()
		self.EnableButtons(False)
		self.loadTrains()
		self.SetTrainChoices(self.trains.GetTrainList())
		
	def EnableButtons(self, flag=True):
		self.bEditSteps.Enable(flag)
		
	def loadTrains(self):
		self.trains = Trains()
		
	def SetTrainChoices(self, trlist=None):
		if trlist is not None:
			self.trainChoices = sorted([x for x in trlist])
			
		self.cbTrain.SetItems(self.trainChoices)
		if self.selectedTrain is not None:
			try:
				tx = self.trainChoices.index(self.selectedTrain)
			except ValueError:
				self.selectedTrain = None
				
		if self.selectedTrain is None and len(self.trainChoices) > 0:
			tx = 0
			self.UpdateTrainSelection(self.trainChoices[0])
		elif self.selectedTrain is None:
			self.UpdateTrainSelection(None)
				
		if self.selectedTrain is not None:
			self.cbTrain.SetSelection(tx)
			
		self.bDelTrain.Enable(self.selectedTrain is not None)
		self.bGenAR.Enable(self.selectedTrain is not None)
		self.bGenSim.Enable(self.selectedTrain is not None)
				
	def AddTrainChoice(self, newtid):
		if newtid in self.trainChoices:
			return False
		
		dlg = wx.MessageDialog(self, "Train %s does not yet exist.\nDo you wish to add it?" % newtid, 'Train does not exist', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION)
		rc = dlg.ShowModal()
		dlg.Destroy()
		
		if rc != wx.ID_YES:
			return False
		
		self.trainChoices.append(newtid)
		self.trainChoices = sorted(self.trainChoices)
		self.trains.AddTrain(newtid, self.chbEast.IsChecked())
		self.SetTrainChoices()
		
		self.SetModified()
		
		return True

	def ShowTitle(self):
		titleString = self.title
		if self.modified:
			titleString += " *"
		self.SetTitle(titleString)
		
	def OnCbTrain(self, evt):
		tx = self.cbTrain.GetSelection()
		if tx is None or tx == wx.NOT_FOUND:
			tid = None
		else:
			tid = self.cbTrain.GetString(tx)

		self.UpdateTrainSelection(tid)
	
	def OnCbTrainTextEnter(self, evt):
		tid = evt.GetString()
		self.UpdateTrainSelection(tid)
		
	def UpdateTrainSelection(self, tid):
		self.selectedTrain = tid
		if tid is None:
			self.EnableButtons(False)
			self.currentTrain = None
			self.blockSeq.SetItems([])
			return
		if tid not in self.trainChoices:
			if not self.AddTrainChoice(tid):
				self.EnableButtons(False)
				self.currentTrain = None
				self.blockSeq.SetItems([])
				return
			
		self.EnableButtons(True)
		
		tr = self.trains.GetTrainById(tid)
		self.currentTrain = tr
		
		self.chbEast.SetValue(tr.IsEast())
		
		self.blockSeq.SetItems(self.currentTrain.GetSteps())
		self.startBlock = self.currentTrain.GetStartBlock()
		self.startSubBlock = self.currentTrain.GetStartSubBlock()

		self.ShowStartBlock()
		
	def ShowStartBlock(self):		
		if self.startBlock is not None:
			if self.startSubBlock is None:
				sbString = self.startBlock
			else:
				sbString = "%s(%s)" % (self.startBlock, self.startSubBlock)
				
			self.teStartBlock.SetValue(sbString)
		else:
			self.teStartBlock.SetValue("")
			
	def OnChbEastbound(self, evt):
		self.currentTrain.SetDirection(self.chbEast.IsChecked())
		self.SetModified()

	def OnBEditSteps(self, _):
		dlg = TrainDlg(self, self.currentTrain, self.layout)
		rc = dlg.ShowModal()
		if rc == wx.ID_OK:
			results = dlg.GetResults()
			
		dlg.Destroy()
		
		if rc != wx.ID_OK:
			return
		
		self.currentTrain.SetSteps(results["steps"])
		self.currentTrain.SetStartBlock(results["startblock"])
		self.currentTrain.SetStartSubBlock(results["startsubblock"])
		self.blockSeq.SetItems(self.currentTrain.GetSteps())
		self.startBlock = self.currentTrain.GetStartBlock()
		self.startSubBlock = self.currentTrain.GetStartSubBlock()
		self.ShowStartBlock()
		self.SetModified()
		
	def OnBDelTrain(self, _):
		if self.currentTrain is None:
			return
		
		tid = self.currentTrain.GetTrainID()
		dlg = wx.MessageDialog(self, "Are you sure you want to delete train %s?\nPress \"Yes\" to continue,\nor \"No\" to cancel." % tid,
				'Confirm train deletion', wx.YES_NO | wx.ICON_WARNING)
		rc = dlg.ShowModal()
		dlg.Destroy()
		if rc != wx.ID_YES:
			return

		self.trainChoices.remove(tid)
		self.trains.DelTrainByTID(tid)
		self.SetTrainChoices()
		
		self.SetModified()

	def OnBGenSim(self, _):
		locoid = 7600
		trainid = self.currentTrain.GetTrainID()
		east = self.currentTrain.IsEast()
		steps = []
		subBlocks = self.layout.GetSubBlocks(self.startBlock)
		if len(subBlocks) == 0:
			blks = [self.startBlock]
		else:
			if self.startSubBlock == subBlocks[-1]:
				blks = [b for b in reversed(subBlocks)]
			else:
				blks = subBlocks
		tm = self.blockSettings.GetBlockTraversalTime(blks[0])
		placeTrainCmd = {"block": self.startBlock, "name": trainid, "loco": locoid, "time": tm, "length": 3}
		if self.startSubBlock is not None:
			placeTrainCmd["subblock"] = blks[0]
			
		steps.append(json.dumps({"placetrain": placeTrainCmd}))

		if len(blks) > 1:
			for b in blks[1:]:
				tm = self.blockSettings.GetBlockTraversalTime(b)
				steps.append("{!movetrain!: {!block!: !%s!, !time!: %d}}" % (b, tm))

		for b in self.blockSeq.GetBlocks():
			subBlocks = self.layout.GetSubBlocks(b["block"])
			stopBlocks = self.layout.GetStopBlocks(b["block"])
			blks = []
			if len(subBlocks) == 0:
				subBlocks = [b["block"]]
			if east:
				if stopBlocks[1]:
					blks.append(stopBlocks[1])
				blks.extend(subBlocks) # one of these will need to be reversed
				if stopBlocks[0]:
					blks.append(stopBlocks[0])
			else:
				if stopBlocks[0]:
					blks.append(stopBlocks[0])
				blks.extend(subBlocks) # one of these will need to be reversed
				if stopBlocks[1]:
					blks.append(stopBlocks[1])
			blkString = ",".join(blks)
			steps.append("{!waitfor!: {!signal!: !%s!, !route!: !%s!, !os!: !%s!, !block!: !%s!}}" %
				(b["signal"], b["route"], b["os"], blkString))
			tm = self.blockSettings.GetBlockTraversalTime(b["os"])
			steps.append("{!movetrain!: {!block!: !%s!, !time!: %d}}" % (b["os"], tm))
			for blk in blks:
				tm = self.blockSettings.GetBlockTraversalTime(blk)
				steps.append("{!movetrain!: {!block!: !%s!, !time!: %d}}" % (blk, tm))

		print(",\n".join(steps).replace('!', '"'))

	def OnBGenAR(self, _):
		trainid = self.currentTrain.GetTrainID()
		lastBlock = self.startBlock
		script = ["{\n  !%s!: {" % trainid]
		steps = []
		for b in self.blockSeq.GetBlocks():
			trigger = 'F' if b["trigger"] == "Front" else 'B'			
			steps.append("    !%s!: {!route!: !%s!, !trigger!: !%s!}" % (lastBlock, b["route"], trigger))
			lastBlock = b["block"]
		script.append(",\n".join(steps))
		script.append("  }\n}")
		print("\n".join(script).replace('!', '"'))
		
	def SetModified(self, flag=True):
		self.modified = flag
		self.ShowTitle()
		
	def OnBSave(self, _):
		self.trains.Save()
		self.SetModified(False)
		
	def OnBExit(self, _):
		self.doExit()
		
	def OnBRevert(self, _):
		if self.modified:
			dlg = wx.MessageDialog(self, 'Train(s) have been modified.\nAre you sure you want to revert without saving?\nPress "Yes" to revert and lose changes,\nor "No" to return and save them.',
					'Changes will be lost', wx.YES_NO | wx.ICON_WARNING)
			rc = dlg.ShowModal()
			dlg.Destroy()
			if rc != wx.ID_YES:
				return
		
		self.Initialize()
		
	def OnClose(self, _):
		self.doExit()
		
	def doExit(self):
		if self.modified:
			dlg = wx.MessageDialog(self, 'Train(s) have been modified.\nAre you sure you want to exit without saving?\nPress "Yes" to exit and lose changes,\nor "No" to return and save them.',
					'Changes will be lost', wx.YES_NO | wx.ICON_WARNING)
			rc = dlg.ShowModal()
			dlg.Destroy()
			if rc != wx.ID_YES:
				return
		self.Destroy()
		
