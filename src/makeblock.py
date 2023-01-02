import json

with open("layout.json", "r") as jfp:
	j = json.load(jfp)
	
try:
	with open("blocks.json", "r") as jfp:
		blks = json.load(jfp)
except FileNotFoundError:
	print("file not found error")
	blks = {}
	
bnames = []
for b in j["blocks"]:
	for sb in ["sbeast", "sbwest"]:
		if j["blocks"][b][sb] is not None:
			bnames.append(j["blocks"][b][sb])
	if b in j["subblocks"]:
		for bn in j["subblocks"][b]:
			bnames.append(bn)
	else:
		bnames.append(b)
	
for b in bnames:
	if b not in blks: # leave existing values alone
		blks[b] = {"time": 5000, "trigger": "F"}
		print("adding block %s" % b)
	
	
with open("blocks.json", "w") as jfp:
	json.dump(blks, jfp, indent=2, sort_keys=True)
	
