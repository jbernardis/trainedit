import wx
from traindlg import TrainDlg
from train import Trains


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

		self.triggerMap = {"B": "Block Setting", "F": "Front of Train", "R": "Rear of Train"}		
		self.chTrigger = wx.Choice(self, wx.ID_ANY, choices = sorted(list(self.triggerMap.values())))
		self.chTrigger.SetSelection(0)
		self.Bind(wx.EVT_CHOICE, self.OnChTrigger, self.chTrigger)
		
		self.bUpdateTrain = wx.Button(self, wx.ID_ANY, "Update\nTrain", size=(80, 50))
		self.Bind(wx.EVT_BUTTON, self.OnBUpdateTrain, self.bUpdateTrain)
		self.bEditSteps = wx.Button(self, wx.ID_ANY, "Edit\nSteps", size=(80, 50))
		self.Bind(wx.EVT_BUTTON, self.OnBEditSteps, self.bEditSteps)
		
		trsz = wx.BoxSizer(wx.HORIZONTAL)
		trsz.Add(wx.StaticText(self, wx.ID_ANY, "Train: "), 0, wx.TOP, 5)
		trsz.AddSpacer(5)
		trsz.Add(self.cbTrain)
		
		trigsz = wx.BoxSizer(wx.HORIZONTAL)
		trigsz.Add(wx.StaticText(self, wx.ID_ANY, "Trigger Point: "), 0, wx.TOP, 5)
		trigsz.AddSpacer(5)
		trigsz.Add(self.chTrigger)
		
		buttonsz = wx.BoxSizer(wx.HORIZONTAL)
		buttonsz.Add(self.bUpdateTrain)
		buttonsz.AddSpacer(20)
		buttonsz.Add(self.bEditSteps)
		
		vsz = wx.BoxSizer(wx.VERTICAL)
		vsz.AddSpacer(20)
		vsz.Add(trsz, 0, wx.ALIGN_CENTER_HORIZONTAL)
		vsz.AddSpacer(20)
		vsz.Add(self.chbEast, 0, wx.ALIGN_CENTER_HORIZONTAL)
		vsz.AddSpacer(20)
		vsz.Add(trigsz, 0, wx.ALIGN_CENTER_HORIZONTAL)
		vsz.AddSpacer(40)
		vsz.Add(buttonsz, 0, wx.ALIGN_CENTER_HORIZONTAL)
		vsz.AddSpacer(20)

		hsz = wx.BoxSizer(wx.HORIZONTAL)
		hsz.AddSpacer(20)
		hsz.Add(vsz)
		hsz.AddSpacer(20)

		self.SetSizer(hsz)
		self.Fit()
		self.Layout()

		wx.CallAfter(self.Initialize)
		
	def Initialize(self):
		self.selectedTrain = None
		self.modified = False
		self.ShowTitle()
		self.EnableButtons(False)
		self.loadTrains()
		self.SetTrainChoices(self.trains.GetTrainList())
		
	def EnableButtons(self, flag=True):
		self.bUpdateTrain.Enable(flag)
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
				
		if self.selectedTrain is not None:
			self.cbTrain.SetSelection(tx)
			
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
		self.trains.AddTrain(newtid, self.GetTriggerPoint(), self.chbEast.IsChecked())
		self.SetTrainChoices()
		
		self.SetModified()
		
		return True

	def ShowTitle(self):
		titleString = self.title
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
			return
		if tid not in self.trainChoices:
			if not self.AddTrainChoice(tid):
				self.EnableButtons(False)
				self.currentTrain = None
				return
			
		self.EnableButtons(True)
		
		tr = self.trains.GetTrainById(tid)
		self.currentTrain = tr
		
		self.chbEast.SetValue(tr.IsEast())
		
		trig = tr.GetTrigger()
		trigStr = self.triggerMap[trig]
		tx = self.chTrigger.FindString(trigStr)
		self.chTrigger.SetSelection(tx)
			
	def OnChbEastbound(self, evt):
		pass
		
	def OnChTrigger(self, evt):
		pass
		
	def GetTriggerPoint(self):
		sx = self.chTrigger.GetSelection()
		tr = self.chTrigger.GetString(sx)
		return tr[0]
	
	def OnBUpdateTrain(self, _):
		if self.currentTrain is None:
			return 
		
		self.currentTrain.SetTrigger(self.GetTriggerPoint())
		self.currentTrain.SetDirection(self.chbEast.IsChecked())
		self.SetModified()
		
	def OnBEditSteps(self, _):
		dlg = TrainDlg(self, self.currentTrain)
		rc = dlg.ShowModal()
		if rc == wx.ID_OK:
			steps = dlg.GetResults()
			
		dlg.Destroy()
		
		if rc != wx.ID_OK:
			return
		
		self.currentTrain.SetSteps(steps)
		self.SetModified()
		
	def SetModified(self, flag=True):
		self.modified = flag
		
	def OnClose(self, _):
		if self.modified:
			print("modified")
		self.trains.Save()
		self.Destroy()
		
