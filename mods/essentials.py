#VERSION: 1.0

INFO = {}
RLTS = {"cls":(),"funcs":(),"vars":()}

class tagger: # edit global data tags
	def edit(name,value):
		exec(name + " = " + str(value))
		del name, value
		globals().update(locals())
	def remove(name):
		globals().pop(name)

class temp_struck:
	def __init__(self):
		self.data = {}
	def set(self,data):
		self.data.update(data)
	def read(self,name=None):
		if name in self.data:
			get = self.data[name]
			return get
		else:
			raise Exception("\"" + name + "\" not found")
		if name == None:
			return self.data
	def read_pop(self,name=None):
		res = read(name)
		if name == None:
			for i in res:
				pop(i)
		else:
			pop(name)
		return res
	def pop(self,name):
		self.data.pop(name)
