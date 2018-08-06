#VERSION: 1.0

INFO = {"scan":("path_find","Scan a target path and its sub files")}
RLTS = {"cls":("os",),"funcs":("echo","get_args"),"vars":()}

def path_find(cmd): # path finder
	cmd_version = "1.1"
	kwd = ""
	target = ""
	opts = get_args(cmd)
	if opts == {}:
		echo(1,"[ERROR] syntax error, try \"-h\" tag for help")
		return
	for i in opts:
		if i in ("-h","--help"):
			echo(1,"""Path/File Finder ( v""" + cmd_version + """ )

Usage: scan <-t> <target_name> [-k]

 -t --target <target_name>      - set a target path to scan
 -k --keyword [key_word]        - set a keyword so that the scanner
                                  can display those matched result
                                  leave it empty or not set to display
                                  all the result
 -h --help                      - display this page

Examples:
 > scan -t /home -k icy
""")
			return
		elif i in ("-k","--keyword"):
			kwd = opts[i]
		elif i in ("-t","--target"):
			target = opts[i]
		else:
			echo(1,"[ERROR] unhandled option \"" + i + "\", try \"-h\" tag for help")
			return
	if not os.path.exists(target):
		echo(1,"[ERROR] target path \"" + target + "\" not found")
		return
	else:
		pass
	if not os.path.isdir(target):
		echo(1,"[ERROR] target \"" + target + "\" is a file")
		return
	else:
		pass
	echo(1,"scanning \"" + target + "\"...")
	files = scan_path(target,"all")
	echo(0,"--------------- [Paths] ---------------")
	for i in files[0]:
		temp = read_path(i[:-1])[1]
		if kwd in temp:
			echo(0,i)
		else:
			pass
	echo(0,"--------------- [Files] ---------------")
	for i in files[1]:
		temp = read_path(i)[1]
		if kwd in temp:
			echo(0,i)
		else:
			pass
