INFO = {"initwin":("init_window","Window initializer(only for Windows)")}

def init_window(cmd):
	global ECHO
	opts = get_args(cmd)
	for i in opts:
		if i in ("-h,--help"):
			echo("""Window initializer(only for Windows)

 the configs of window color, title, etc. are in the basic user config.
 to edit please use the command of \"edconf\"
 for window color code please use \"color /help\" for help

Usage: chpwd
 -h --help                      - display this page

Examples:
 >initwin
""")
		else:
			echo("[ERROR] unhandled option \"" + i + "\", try \"-h\" tag for help")
			return
	try:
		configs = BLOCK.read("user/user.json")
		coder = iccode(PWD)
		configs = coder.decode(configs)
		configs = json.loads(configs)
		if PWD != configs["iccode_key"]:
			raise Exception("user config file value didn't match")
		else:
			pass
	except Exception as err:
		echo("[ERROR] Failed to read block config file: " + str(err) + ", file may be broken")
		return
	stat = "window_color" in configs and "window_title" in configs
	if not stat:
		echo("windowinit configs not found, creating by default")
		ECHO = False
		edit_userconf("-e window_color -v 07")
		edit_userconf("-e window_title -v ICLab")
		ECHO = True
	try:
		configs = BLOCK.read("user/user.json")
		coder = iccode(PWD)
		configs = coder.decode(configs)
		configs = json.loads(configs)
		if PWD != configs["iccode_key"]:
			raise Exception("user config file value didn't match")
		else:
			pass
	except Exception as err:
		echo("[ERROR] Failed to read block config file: " + str(err) + ", file may be broken")
		return
	if OS == "win":
		os.system("title " + configs["window_title"])
		os.system("color " + configs["window_color"])
	else:
		pass

# [AUTORUN]
init_window("")
