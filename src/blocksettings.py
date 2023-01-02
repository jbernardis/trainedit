import json

class BlockSettings:
	def __init__(self):		
		with open("blocks.json", "r") as jfp:
			self.blocks = json.load(jfp)
			
	def GetBlockTraversalTime(self, block):
		if block not in self.blocks:
			print("Block %s not found in data files - using traversal time of 5000" % block)
			return 5000
		
		return self.blocks[block]["time"]
			
	def GetBlockTriggerPoint(self, block):
		if block not in self.blocks:
			print("Block %s not found in data files - using Frone trigger point")
			return "F"
		
		return self.blocks[block]["trigger"]
		
