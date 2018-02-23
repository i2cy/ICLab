INFO = {"rpy":("run_py","Run a python scripts with ICLab environment")}

def run_py(cmd): # run python scripts
	opts = get_args(cmd)
	for i in opts:
		if i in ("-h","--help"):
			print("""Python Script Executer

Usage: rpy <command>

 -h --help                      - display this page

Example:
 > rpy print("test")

""")
			return
		else:
			pass
	try:
		exec(cmd)
	except Exception as err:
		echo("[ERROR] failed to execute script, result: " + str(err))
