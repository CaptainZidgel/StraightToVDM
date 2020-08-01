'''
 VDM appears to be VDF (Valve Demo Format).
 There are other modules that already implement read/write for VDF
 But I decided to write my own for 2 reasons:
 0 - I like writing code :)
 1 - I didn't want to have to learn an external module
 2 - VDM files are extremely simple anyway and I don't feature any nesting or reading functions (to reiterate: This does not support nesting)
'''

class VDF:
	def __init__(self, path, header="demoactions"):
		self.path = path
		self.header = header
		self.buffer = ''
		self.elements = 0
		
	def commit(self, dictionary, indent=1):
		self.elements += 1
		indent = "\t" * indent
		indent2 = indent + "\t"
		self.buffer += '{}"{}"\n{}{{\n'.format(indent, self.elements, indent)	# "1" \n { \n
		for key,value in dictionary.items():
			self.buffer += indent2+'{} "{}"\n'.format(key, value)
		self.buffer += indent+'}\n'

	def write(self):
		with open(self.path, "w+") as f:
			f.write("{}\n{{\n".format(self.header))	#header \n { \n
			f.write(self.buffer)
			f.write("}\n")

	def __str__(self):
		return self.buffer

def Test():
	vdf = VDF("testvdf.vdm")
	vdf.commit({"factory": "SkipAhead", "name": "skip", "starttick": 1, "skiptotick": "19490"})
	vdf.commit({"factory": "PlayCommands", "name": "startec", "starttick": 26261, "commands": "startrecording"})
	vdf.write()
