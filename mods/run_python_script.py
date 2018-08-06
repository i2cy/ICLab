#VERSION: 1.1

INFO = {"rpy":("run_py","Run a python scripts with ICLab environment")}
RLTS = {"cls":(),"funcs":("echo","get_args"),"vars":()}

def run_py(cmd): # run python scripts
	opts = get_args(cmd)
	for i in opts:
		if i in ("-h","--help"):
			echo(0,"""Python Script Executer

Usage: rpy <command>

 -h --help                      - display this page

Example:
 > rpy print("test")

""")
			return
		else:
			pass
	exec(cmd)
