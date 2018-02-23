INFO = {}

class tagger: # edit global data tags
	def edit(name,value):
		exec(name + " = " + str(value))
		del name, value
		globals().update(locals())
	def remove(name):
		exec("del " + name)
		del name
		globals().update(locals())
