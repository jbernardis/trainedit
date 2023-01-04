import json

class Train:
	def __init__(self, tid):
		self.tid = tid
		self.east = True
		self.trigger = 'B'    # 'B'lovk specified triggering
		self.steps = []
		
	def SetDirection(self, direction):
		self.east = direction
		
	def SetTrigger(self, trigger):
		self.trigger = trigger
		
	def GetTrainID(self):
		return self.tid
	
	def IsEast(self):
		return self.east
	
	def GetTrigger(self):
		return self.trigger
	
	def SetSteps(self, steps):
		self.steps = [x for x in steps]
		print(json.dumps(steps))
		
	def GetSteps(self):
		return [x for x in self.steps]
	
	def ToJSON(self):
		return {self.tid: {"eastbound": self.east, "trigger": self.trigger, "steps": self.steps}}
	
class Trains:
	def __init__(self):
		try:
			with open("trains.json", "r") as jfp:
				TrainsJson = json.load(jfp)
		except:
			TrainsJson = {}
			
		self.trainlist = []
		self.trainmap = {}
		for tid, trData in TrainsJson.items():
			tr = self.AddTrain(tid, trData["trigger"], trData["eastbound"])
			tr.SetSteps(trData["steps"])
		
	def Save(self):
		TrainsJson = {}
		for tr in self.trainlist:
			TrainsJson.update(tr.ToJSON())
			
		with open("trains.json", "w") as jfp:
			json.dump(TrainsJson, jfp, sort_keys=True, indent=2)
		
	def GetTrainList(self):
		return [tr.GetTrainID() for tr in self.trainlist]
	
	def AddTrain(self, tid, trig, east):
		tr = Train(tid)
		tr.SetDirection(east)
		tr.SetTrigger(trig)
		self.trainlist.append(tr)
		self.trainmap[tid] = tr
		return tr
		
	def GetTrainById(self, tid):
		if tid not in self.trainmap:
			return None
		
		return self.trainmap[tid]
	