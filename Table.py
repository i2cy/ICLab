#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Name: IC lab Table
# Author: Icy(enderman1024@foxmail.com)
# Description: IC Lab Work Table


# +++*** [ SOURCE VERSION ] ***+++




# global tags:

VERSION = "1.5.3"




class block: # block zip pack file manager
	def create(block_name):
		if os.path.isdir(block_name):
			raise Exception("Target block name is a existed path")
		zipper = zipfile.ZipFile(block_name,"w",zipfile.ZIP_DEFLATED,allowZip64=True)
		return zipper
	def load(block_name):
		if os.path.isdir(block_name):
			raise Exception("Target block name is a existed path")
		zipper = zipfile.ZipFile(block_name,"a",zipfile.ZIP_DEFLATED,allowZip64=True)
		return zipper




class iccode: # Simple Data encoder/decoder
	def __init__(self,keys):
		key = str(keys)
		if len(key) < 1:
			raise Exception("Key's length must be greater than 0")
		self.origin_key = key
		self.key = []
		keys = ""
		for i in key:
			keys = keys + str(ord(i))
		temp = ""
		for i in keys:
			temp = temp + i
			if int(temp[0]) < 5:
				if len(temp) == 3:
					self.key.append(int(temp))
					temp = ""
				else:
					pass
			else:
				if len(temp) == 2:
					self.key.append(int(temp))
					temp = ""
				else:
					pass
		if temp != "":
			self.key.append(int(temp))
		self.walk = 0
	def encode(self,data):
		res = b""
		for i in data:
			if self.walk >= len(self.key):
				self.walk = 0
				self.flush()
			code = i - self.key[self.walk]
			while code < 0:
				code = 256 + code
			res = res + bytes((code,))
			self.walk += 1
		return res
	def decode(self,data):
		res = b""
		for i in data:
			if self.walk >= len(self.key):
				self.walk = 0
				self.flush()
			code = i + self.key[self.walk]
			while code > 255:
				code = code - 256
			res = res + bytes((code,))
			self.walk += 1
		return res
	def flush(self):
		key = self.key
		n = 0
		if key[-1] == 0:
			last = 2
		else:
			last = key[-1]
		for i in key:
			self.key[-n-1] = str(i*last+last)
			if len(self.key[-n-1]) > 3:
				self.key[-n-1] = int((self.key[-n-1])[:3])
				if self.key[-n-1] > 512:
					self.key[-n-1] = self.key[-n-1] - 512
			else:
				self.key[-n-1] = int(self.key[-n-1])
			n += 1
			if i == 0:
				last = 2
			else:
				last = i
	def reset(self):
		keys = ""
		origin_ickey = []
		for i in self.origin_key:
			keys = keys + str(ord(i))
		temp = ""
		for i in keys:
			temp = temp + i
			if int(temp[0]) < 5:
				if len(temp) == 3:
					origin_ickey.append(int(temp))
					temp = ""
				else:
					pass
			else:
				if len(temp) == 2:
					origin_ickey.append(int(temp))
					temp = ""
				else:
					pass
		if temp != "":
			origin_ickey.append(int(temp))
		self.key = origin_ickey
		self.walk = 0
	def debug(self):
		keys = ""
		origin_ickey = []
		for i in self.origin_key:
			keys = keys + str(ord(i))
		temp = ""
		for i in keys:
			temp = temp + i
			if int(temp[0]) < 5:
				if len(temp) == 3:
					origin_ickey.append(int(temp))
					temp = ""
				else:
					pass
			else:
				if len(temp) == 2:
					origin_ickey.append(int(temp))
					temp = ""
				else:
					pass
		if temp != "":
			origin_ickey.append(int(temp))
		return (self.origin_key,origin_ickey,self.key,self.walk)




class _Getch: # main functions (usage: getch = _Getch()|while True:|  ch = getch())
	def __init__(self):
		try:
			self.impl = _GetchWindows()
		except ImportError:
			self.impl = _GetchUnix()
	def __call__(self):
		return self.impl()




class _GetchUnix: # sub class of nonblocking input to get character from Unix
	def __init__(self):
		import tty, sys
	def __call__(self):
		import sys, tty, termios
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		res = ""
		try:
			tty.setraw(sys.stdin.fileno(), termios.TCSANOW)
			ch = sys.stdin.read(1)
			if ch == "\x1b":
				ch = sys.stdin.read(1)
				if ch == "[":
					ch = sys.stdin.read(1)
					if ch == "A":
						res = b'\xe0\x48'
					elif ch == "B":
						res = b'\xe0\x50'
					elif ch == "D":
						res = b"\xe0\x4b"
					elif ch == "C":
						res = b"\xe0\x4d"
					else:
						res = ""
				else:
					res = ""
			else:
				res = ch
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return res




class _GetchWindows: # sub class of nonblocking input to get character from Windows
	def __init__(self):
		import msvcrt
	def __call__(self):
		import msvcrt
		temp = msvcrt.getch()
		if temp == b"\x00":
			temp = msvcrt.getch()
			try:
				res = temp.decode()
			except Exception:
				temp += msvcrt.getch()
				res = temp
			return res
		else:
			try:
				res = temp.decode()
			except Exception:
				temp += msvcrt.getch()
				res = temp
			return res




class temp_memo: # temp memory class
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
		if name == None:
			res = {}
			for i in self.data:
				res.update(self.data[i])
			self.data = {}
		else:
			res = self.data[name]
			self.data.pop(name)
		return res
	def pop(self,name):
		self.data.pop(name)




def echo(mode,msg): # console message printer ( can be redefine by package )
	global ECHO
	if mode == 1:
		msg = "<"+ HEAD + "> " + msg
	elif mode == 0:
		pass
	if ECHO == True:
		print(msg)
	elif ECHO == False:
		pass
	else:
		try:
			msg = msg.encode()
			if os.path.exists(ECHO):
				f = open(ECHO,"ab")
				f.write(msg+(os.linesep).encode())
				f.close()
			else:
				f = open(ECHO,"wb")
				f.write(msg+(os.linesep).encode())
				f.close()
		except Exception as err:
			f = ECHO
			msg = msg.decode()
			ECHO = True
			echo(1,"[ERROR] Failed to write console message to file \"" + f + "\",result: " + str(err))
			print(msg)




def ICLab_end(): # close ICLab
	try:
		shutil.rmtree(sys.path[0] + os.sep + "temp")
	except:
		pass
	sys.exit(0)




def scan_path(patho, mode): # list file(s) & folder(s)
	paths = []
	files = []
	pathx = ""
	for i in patho:
		if i in ("\\","/"):
			pathx += os.sep
		else:
			pathx += i
	if os.sep != pathx[-1:]:
		target_path = pathx + os.sep
	else:
		target_path = pathx
	if mode == "top":
		res = os.listdir(target_path)
		for i in res:
			if os.path.isfile(target_path + i):
				files.append(target_path + i)
			else:
				paths.append(target_path + i)
	elif mode == "all":
		res = os.walk(target_path)
		for path,d,filelist in res:
			if path[-1] != os.sep:
				paths.append(path + os.sep)
			else:
				paths.append(path)
			for filename in filelist:
				files.append(os.path.join(path,filename))
	return (paths,files)




def path_fixer(path): # path checker
	chk = ""
	for i in path:
		chk += i
		if os.sep == i:
			if not os.path.exists(chk):
				os.mkdir(chk)




def iccode_en(key ,target_file, finnal_file): # iccode file encrypter
	ft = open(target_file,"rb")
	ff = open(finnal_file,"wb")
	coder = iccode(key)
	while True:
		data = ft.read(1024)
		if len(data) == 0:
			break
		data = coder.encode(data)
		ff.write(data)
	ft.close()
	ff.close()
	return




def execute(cmd): # execute command and update loacls to globals
	__name__ = "__module__"
	exec(cmd)
	del __name__
	locals().pop("cmd")
	return locals()




def load_blockinfo(key,name): # block info loader
	global PWD, USER
	blk = block.load(name)
	data = blk.read("user/user.json")
	coder = iccode(key)
	data = coder.decode(data)
	data = data.decode()
	data = json.loads(data)
	PWD = ""
	if data["iccode_key"] == key:
		USER = data["username"]
		PWD = key
		return (True,blk)
	else:
		return (False,blk)




def passwd_input(head=""): # password input function, cover inputs
	if C_MODE:
		res = input(head)
		return res
	else:
		sys.stdout.write(head)
		sys.stdout.flush()
		getch = _Getch()
		res = ''
		while True:
			ch = getch()
			if ch == '\r':
				sys.stdout.write('\n')
				return res
			elif ch in (b'\xe0\x4b',b'\xe0\x48',b'\xe0\x4d',b'\xe0\x50'):
				pass
			elif ch in (chr(127),"\b"):
				res = res[:-1]
				sys.stdout.write('\b \r' + head + '*'*len(res))
				sys.stdout.flush()
			elif ch in (chr(3),chr(4)):
				raise KeyboardInterrupt()
			elif ch == chr(26):
				exit()
			else:
				try:
					res += ch
					sys.stdout.write('\r' + head + '*'*len(res))
					sys.stdout.flush()
				except Exception:
					pass




def cmd_input(head="",more=""): # command shell inputer
	global MEMO
	if C_MODE:
		res = input(head)
		return res
	else:
		sys.stdout.write(head)
		sys.stdout.flush()
		getch = _Getch()
		res = ""
		res2 = ""
		old = ""
		h = 0
		t = 0
		# react part
		while True:
			ch = getch()
			if t == 0:
				old = res + res2
			if ch == '\r':
				res = res + res2
				sys.stdout.write('\r' + head + res + '\n')
				temp = []
				for i in MEMO.read("input_history"):
					temp.append(i)
				temp.append(res)
				MEMO.set({"input_history":temp})
				return res
			elif ch == b'\xe0\x4b':
				if len(res) > 0:
					res2 = list(res2)
					res2.insert(0,res[-1])
					res2 = "".join(res2)
					res = res[:-1]
					sys.stdout.write('\r' + head + res)
					sys.stdout.flush()
				else:
					pass
			elif ch == b'\xe0\x4d':
				if len(res2) > 0:
					res += res2[0]
					res2 = res2[1:]
					sys.stdout.write('\r' + head + res + res2)
					sys.stdout.write('\r' + head + res)
					sys.stdout.flush()
				else:
					pass
			elif ch == b'\xe0\x48':
				history = MEMO.read("input_history")
				if len(history) > 0 and t < len(history):
					t += 1
					sys.stdout.write('\r'+ " "*(len(head+res+res2)-len(more)))
					res = history[-t]
					res2 = ""
					sys.stdout.write('\r' + head + res)
					sys.stdout.flush()
				else:
					pass
			elif ch == b'\xe0\x50':
				history = MEMO.read("input_history")
				if t > 1:
					t -= 1
					sys.stdout.write('\r'+ " "*(len(head+res+res2)-len(more)))
					res = history[-t]
					res2 = ""
					sys.stdout.write('\r' + head + res)
					sys.stdout.flush()
				else:
					t = 0
					sys.stdout.write('\r'+ " "*(len(head+res+res2)-len(more)))
					res = old
					res2 = ""
					sys.stdout.write('\r' + head + res)
					sys.stdout.flush()
			elif ch == "\t":
				if res == "":
					sys.stdout.write("\a")
					sys.stdout.flush()
				else:
					n = 0
					for i in res:
						if i == "\"":
							n += 1
					temp_y = n % 2 != 0
					if res[-1] == " " and not temp_y:
						if h == 1:
							h = 0
							temp = scan_path('./',"top")
							path = temp[0]
							file = temp[1]
							n = 0
							for i in path:
								path[n] = i[2:] + os.sep
								n += 1
							n = 0
							for i in file:
								file[n] = i[2:]
								n += 1
							path.sort()
							file.sort()
							temp = path + file
							sys.stdout.write("\n")
							sys.stdout.flush()
							for i in temp:
								echo(0,i)
							sys.stdout.write('\r' + head + res + res2)
							sys.stdout.write("\r" + head + res)
							sys.stdout.flush()
						else:
							h = 1
					else:
						if h == 1:
							h = 0
						else:
							h = 1
							continue
						if not ' ' in res and not res[:2] in (".\\","./"):
							temp = list(CMDS.keys())
							temp2 = []
							for i in temp:
								if res == i[:len(res)]:
									temp2.append(i)
							if len(temp2) == 0:
								sys.stdout.write("\a")
								sys.stdout.flush()
								continue
							elif len(temp2) == 1:
								res = temp2[0]
								sys.stdout.write('\r' + head + res + res2)
								sys.stdout.write("\r" + head + res)
								sys.stdout.flush()
							else:
								sys.stdout.write("\n")
								sys.stdout.flush()
								for i in temp2:
									echo(0,i)
								sys.stdout.write('\r' + head + res + res2)
								sys.stdout.write("\r" + head + res)
								sys.stdout.flush()
						else:
							if temp_y:
								temp = res.split("\"")
							else:
								temp = res.split(" ")
							temp = read_path(temp[-1])
							temp_i = False
							temp = list(temp)
							if temp[0] == "":
								temp_i = True
								temp[0] = "./"
							else:
								pass
							try:
								temp2 = scan_path(temp[0],"top")
							except Exception:
									sys.stdout.write("\a")
									sys.stdout.flush()
									continue
							path = temp2[0]
							file = temp2[1]
							n = 0
							for i in path:
								path[n] = i[len(temp[0]):] + os.sep
								n += 1
							n = 0
							for i in file:
								file[n] = i[len(temp[0]):]
								n += 1
							path.sort()
							file.sort()
							temp2 = path + file
							temp3 = []
							for i in temp2:
								if temp[1] == i[:len(temp[1])]:
									temp3.append(i)
							del temp2
							if len(temp3) == 1:
								if temp_i:
									temp[0] = ""
								temp[0] = list(temp[0])
								n = 0
								for i in temp[0]:
									if i in ("\\","/"):
										(temp[0])[n] = os.sep
									n += 1
								temp[0] = "".join(temp[0])
								res = res[:-len(temp[0]+temp[1])] + temp[0] + temp3[0]
								sys.stdout.write('\r' + head + res + res2)
								sys.stdout.write("\r" + head + res)
								sys.stdout.flush()
							if len(temp3) == 0:
								sys.stdout.write("\a")
								sys.stdout.flush()
								continue
							sys.stdout.write("\n")
							sys.stdout.flush()
							for i in temp3:
								echo(0,i)
							sys.stdout.write('\r' + head + res + res2)
							sys.stdout.write("\r" + head + res)
							sys.stdout.flush()
			elif ch in (chr(127),"\b"):
				sys.stdout.write('\r'+ " "*(len(head+res+res2)-len(more)))
				res = res[:-1]
				sys.stdout.write('\r' + head + res + res2)
				sys.stdout.write('\r' + head + res)
				sys.stdout.flush()
			elif ch in (chr(3),chr(4)):
				raise KeyboardInterrupt()
			elif ch == chr(26):
				exit()
			else:
				try:
					res += ch
					sys.stdout.write('\r' + head + res + res2)
					sys.stdout.write('\r' + head + res)
					sys.stdout.flush()
				except Exception:
					pass




def ICLab_cmd_loop(): # command shell loop
	global ECHO
	try:
		while True:
			try:
				temp = cmd_input("\033[1;7;36m" + USER + "\033[1;27;4;36m" + HEAD + "\033[0m\033[1;24;33m:" + PATH + ">\033[0m", "\033[1;7;36m\033[1;27;4;36m\033[0m\033[1;24;33m\033[0m")
				scripts_executer(temp)
			except KeyboardInterrupt:
				echo(0,"\nKeyboardInterrupt")
				continue
	except KeyboardInterrupt:
		echo(1,"keyboard interrupt detected, exitting")
		return




def get_args(opt): # decode command shell's argument(s)
	opts = []
	strin = False
	temp = ""
	for i in opt:
		if strin:
			if not i in ("\"","\'"):
				temp += i
			else:
				strin = False
			continue
		else:
			if i in ("\"","\'"):
				strin = True
				continue
		if i != " ":
			temp += i
		else:
			opts.append(temp)
			temp = ""
	if len(temp) > 0:
		opts.append(temp)
	argv = ""
	res = {}
	for i in opts:
		if len(argv) > 0 and "-" != i[0]:
			res.update({argv:i})
			argv = ""
		if "-" == i[0]:
			argv = i
			res.update({argv:""})
	if DEBUG:
		echo(0,res)
	return res




def scripts_error(name,script,pos,info): # scripts error traceback (ps: pos = (file,line,position))
	echo(0,"")
	echo(1,"ICLab scripts ERROR, Traceback:")
	echo(0,"  File \"" + pos[0] + "\", line " + str(pos[1]))
	echo(0,"  " + script)
	echo(0," "*(pos[2]+2) + "^")
	echo(0,name + ": " + info)




def scripts_processor(scr,filename="<consolo>"): # scripts preprocessor
	if "\n" in scr:
		if "\r" in scr:
			scr = scr.split("\r\n")
		else:
			scr = scr.split("\n")
	else:
		scr = [scr]
	funcs = {}
	scrs = []
	func = None
	line = 0
	for i in scr:
		line += 1
		if "::" == i[:2]:
			if len(i[2:]) == 0:
				scripts_error("SyntaxError",i,(filename,line,len(i)-1),"function name length must be more than 0")
				return
			elif i[2:] == " "*len(i[2:]):
				scripts_error("SyntaxError",i,(filename,line,len(i)-1),"function name can't be all filled with \" \"")
				return
			else:
				func = i[2:]
				funcs.update({func:[]})
		elif ":END" == i[:4]:
			func = None
		else:
			if func != None:
				temp = funcs[func]
				temp.append(i)
				funcs.update({func:temp})
			else:
				scrs.append(i)
	while len(scrs) > 0:
		temp = scrs.pop(0)
		res = scripts_executer(temp)
		if res == None:
			pass
		else:
			if res[0] == "func":
				if res[1] in funcs.keys():
					temp_2 = (funcs[res[1]])[::-1]
					for i in temp_2:
						scrs.insert(0,i)
				else:
					n = 0
					for i in scr:
						n += 1
						if i == temp:
							break
					scripts_error("NameError",temp,(filename,n,4),"function name \"" + res[1] + "\" not found")
					return
			elif res[0] == "error":
				n = 0
				for i in scr:
					n += 1
					if i == temp:
						break
				scripts_error((res[1])[0],i,(filename,n,(res[1])[1]),(res[1])[2])
				return
			else:
				pass




def scripts_executer(scr_scripts_executer): # scripts executer
	global ECHO, BLOCK
	try:
		cmd_scripts_executer = ""
		temp_2_scripts_executer = ""
		tag_scripts_executer = True
		for i_scripts_executer in scr_scripts_executer:
			if tag_scripts_executer:
				if i_scripts_executer == " ":
					tag_scripts_executer = False
					continue
				else:
					cmd_scripts_executer += i_scripts_executer
			else:
				temp_2_scripts_executer += i_scripts_executer
				continue
		if cmd_scripts_executer == "" or cmd_scripts_executer == len(cmd_scripts_executer)*" ":
			return
		elif cmd_scripts_executer == "RUN":
			return ("func",temp_2_scripts_executer)
		elif cmd_scripts_executer == "IF":
			a_scripts_executer = None
			b_scripts_executer = None
			n_scripts_executer = 0
			c_scripts_executer = 0
			for i2_scripts_executer in scr_scripts_executer:
				n_scripts_executer += 1
				if i2_scripts_executer == "(":
					if a_scripts_executer == None:
						a_scripts_executer = n_scripts_executer
					c_scripts_executer += 1
				if i2_scripts_executer == ")":
					if c_scripts_executer == 0:
						return ("error",("ConditionError",2,"condition not found"))
					elif c_scripts_executer == 1:
						b_scripts_executer = n_scripts_executer
						break
					else:
						c_scripts_executer -= 1
			if a_scripts_executer == None or b_scripts_executer == None or a_scripts_executer > b_scripts_executer:
				return ("error",("ConditionError",2,"condition not found"))
			else:
				temp_scripts_executer = scr_scripts_executer[a_scripts_executer:b_scripts_executer-1]
			try:
				exec("MEMO.set({\"scripts_executer_temp\":" + temp_scripts_executer + "})")
			except Exception as err_scripts_executer:
				n = 0
				for i2_scripts_executer in scr_scripts_executer:
					n_scripts_executer += 1
					if i2_scripts_executer == scr_scripts_executer:
						break
				return ("error",("ConditionError",b_scripts_executer-2,str(err_scripts_executer)))
			temp_scripts_executer = ""
			tag_scripts_executer = False
			for i_scripts_executer in scr_scripts_executer[b_scripts_executer:]:
				if tag_scripts_executer:
					temp_scripts_executer += i_scripts_executer
				else:
					if i_scripts_executer == " ":
						pass
					else:
						tag_scripts_executer = True
						temp_scripts_executer += i_scripts_executer
			if MEMO.read_pop("scripts_executer_temp"):
				res_scripts_executer = scripts_executer(temp_scripts_executer)
				return res_scripts_executer
			else:
				return
		elif cmd_scripts_executer[:2] in (".\\","./"):
			if scr_scripts_executer[-4:] == ".ics":
				scr_scripts_executer = "icsh " + scr_scripts_executer
		elif cmd_scripts_executer[0] == "#":
			return
		else:
			pass
		cmd_scripts_executer = ""
		args_scripts_executer = ""
		temp_2_scripts_executer = ""
		tag_scripts_executer = True
		to_scripts_executer = False
		for i_scripts_executer in scr_scripts_executer:
			if tag_scripts_executer:
				if not i_scripts_executer in (" ",">"):
					cmd_scripts_executer += i_scripts_executer
					continue
				if i_scripts_executer == " ":
					tag_scripts_executer = False
					continue
				elif i_scripts_executer == ">":
					tag_scripts_executer = False
					temp_2_scripts_executer += i_scripts_executer
			else:
				temp_2_scripts_executer += i_scripts_executer
				continue
	except KeyboardInterrupt:
		if len(scr_scripts_executer) == 0:
			scr_scripts_executer = " "
		return ("error",("KeyboardInterrupt",len(scr_scripts_executer)-1,""))
	if cmd_scripts_executer in CMDS:
		write_to_scripts_executer = ""
		for i_scripts_executer in temp_2_scripts_executer:
			if i_scripts_executer == ">":
				write_to_scripts_executer = ""
				to_scripts_executer = True
				continue
			if to_scripts_executer:
				write_to_scripts_executer += i_scripts_executer
		if write_to_scripts_executer != "":
			sc_scripts_executerr = temp_2_scripts_executer[:-(len(write_to_scripts_executer)+1)]
			for i_scripts_executer in scr_scripts_executer:
				if i_scripts_executer == "\"":
					a_scripts_executer = "\\" + i_scripts_executer
				elif i_scripts_executer == "\\":
					a_scripts_executer = "\\" + i_scripts_executer
				else:
					a_scripts_executer = i_scripts_executer
				args_scripts_executer += a_scripts_executer
			echo(1,"[INFO] console message is now redirected to \"" + write_to_scripts_executer + "\"")
			ECHO = write_to_scripts_executer
		else:
			for i_scripts_executer in temp_2_scripts_executer:
				if i_scripts_executer == "\"":
					a_scripts_executer = "\\" + i_scripts_executer
				elif i_scripts_executer == "\\":
					a_scripts_executer = "\\" + i_scripts_executer
				else:
					a_scripts_executer = i_scripts_executer
				args_scripts_executer += a_scripts_executer
		if not DEBUG:
			try:
				try:
					exec((CMDS[cmd_scripts_executer])[0]+ "(\"" + args_scripts_executer + "\")")
					if ECHO == write_to_scripts_executer:
						ECHO = True
				except KeyboardInterrupt:
					ECHO = True
					if len(scr_scripts_executer) == 0:
						scr_scripts_executer = " "
					return ("error",("KeyboardInterrupt",len(scr_scripts_executer)-1,""))
			except Exception as err_scripts_executer:
				ECHO = True
				echo(1,"[ERROR] Error while executing \"" + cmd_scripts_executer + "\", result: " + str(err_scripts_executer))
				return ("error",("Exception",len(scr_scripts_executer)-1,str(err_scripts_executer)))
		else:
			try:
				exec((CMDS[cmd_scripts_executer])[0]+ "(\"" + args_scripts_executer + "\")")
				if ECHO == write_to_scripts_executer:
					ECHO = True
			except KeyboardInterrupt:
				ECHO = True
				if len(scr_scripts_executer) == 0:
					scr_scripts_executer = " "
				return ("error",("KeyboardInterrupt",len(scr_scripts_executer)-1,""))
	else:
		try:
			os.system(scr_scripts_executer)
		except KeyboardInterrupt:
			if len(scr_scripts_executer) == 0:
				scr_scripts_executer = " "
			return ("error",("KeyboardInterrupt",len(scr_scripts_executer)-1,""))




def extract_block(): # extract block for edit
	global BLOCK
	BLOCK.close()
	BLOCK = block.load(BLOCK.filename)
	pathx = sys.path[0] + os.sep + "temp" + os.sep + "extracts" + os.sep
	if not os.path.exists(pathx):
		os.mkdir(pathx)
	else:
		shutil.rmtree(pathx)
		os.mkdir(pathx)
	BLOCK.extractall(path=pathx)




def update_block(): # zip files from extracts
	global BLOCK
	pathx = sys.path[0] + os.sep + "temp" + os.sep + "extracts" + os.sep
	files = scan_path(pathx,"all")
	BLOCK.close()
	BLOCK = BLOCK.filename
	BLOCK = block.create(BLOCK)
	for i in files[0]:
		temp = i[len(pathx):]
		temp = temp.replace("\\","/")
		if temp != "/":
			BLOCK.write(i,temp)
		else:
			pass
	for i in files[1]:
		temp = i[len(pathx):]
		BLOCK.write(i,temp)
	BLOCK.close()
	BLOCK = block.load(BLOCK.filename)
	shutil.rmtree(pathx)




def read_path(path): # Path String Reader
	pathx = ""
	name = ""
	temp = ""
	for i in path:
		temp += i
		if i == "\\" or i == "/":
			pathx += temp
			temp = ""
	name = temp
	return (pathx,name)




def ICLab_args_processor(): # process the cmd args when running ICLab by shell
	global ARGS
	parser = argparse.ArgumentParser(description='ICLab command shell [v'+VERSION+']')
	parser.add_argument('-s', action='store', dest='iclab_scripts_file',
						help='Execute an ICLab script')
	parser.add_argument('-b', action='store', dest='block_file',
						help='Load a Block file after ICLab initilized')
	parser.add_argument('-p', action='store', dest='block_file_passwords',
						help='Block file passwords')
	parser.add_argument('-k', action='store_true', default=False,
						dest='keep_shell_on',
						help='keep ICLab running after it executed scripts')
	args = parser.parse_args()
	file = None
	blk = None
	pwd = None
	keep = False
	if args.iclab_scripts_file:
		ARGS = True
		file = args.iclab_scripts_file
	if args.block_file:
		ARGS = True
		blk = args.block_file
	if args.keep_shell_on:
		ARGS = True
		keep = args.keep_shell_on
	if args.block_file_passwords:
		ARGS = True
		pwd = args.block_file_passwords
	if blk != None:
		if pwd == None:
			wait = True
			try:
				while wait:
					pwd = passwd_input("Block-Password: ")
					wait = False
					try:
						load_block("-t \"" + blk + "\" -p \"" + pwd + "\"")
						if type("") == type(BLOCK):
							wait = True
					except Exception as err:
						echo(1,"[ERROR] Failed to load block, result: " + str(err))
						wait = True
			except KeyboardInterrupt:
				echo(0,"")
				echo(1,"keyboard interrupt detected, skipping block loading")
		else:
			try:
				load_block("-t \"" + blk + "\" -p \"" + pwd + "\"")
			except Exception as err:
				echo(1,"[ERROR] Failed to load block, result: " + str(err))
				ICLab_end()
	if file != None:
		if not os.path.exists(file):
			echo(1,"[ERROR] file \"" + file + "\" not found")
			ICLab_end()
		if os.path.isdir(file):
			echo(1,"[ERROR] file \"" + file + "\" is a folder")
			ICLab_end()
		f = open(file)
		scr = f.read()
		f.close()
		del f
		try:
			scripts_processor(scr,filename=file)
			echo(0,"")
		except KeyboardInterrupt:
			exit_iclab("")
		if keep:
			pass
		else:
			exit_iclab("")
	return




def ICLab_init(): # initializer
	global sys, os, time, zipfile, json, shutil, OS, threading, argparse, BLOCK, CMDS, HEAD, PATH, OG, OCMDS, ECHO, DEBUG, C_MODE, MEMO, ARGS, USER
	USER = ""
	DEBUG = False
	HEAD = "ICLab"
	BLOCK = ""
	ECHO = True
	COVER = False
	ARGS = False
	CMDS = {"exit":("exit_iclab","Exit ICLab working table"),
	"createblock":("block_create","ICLab Block create guide"),
	"ichelp":("iclab_help","List all available ICLab commands"),
	"chd":("change_dir","Change ICLab working path"),
	"loadblk":("load_block","Load a ICLab block"),
	"unloadblk":("unload_block","Unload a ICLab block"),
	"edmods":("edit_module","Block module manager"),
	"edconf":("edit_userconf","Block user config editor"),
	"chpwd":("ch_pwd","Block password change guide"),
	"icdebug":("iclab_debug","ICLab debug mode"),
	"icsh":("run_scripts","Run IClab scripts")}
	echo(1,"Initilizing...")
	import sys, os, time, zipfile, json, shutil, threading, argparse
	echo(1,'ICLab ( Version: ' + VERSION + ' )')
	# python version check
	if float(sys.version[:3]) < 3.4:
		echo(1,"ICLab only support Python3.4+ environment, please go visit https://www.python.org/downloads download a Python3.4+ environment if you haven't installed yet")
		sys.exit(1)
	else:
		echo(1,"python version check: PASS")
	# temp_global_memory setup
	MEMO = temp_memo()
	echo(1,"global memory class: PASS")
	# os check
	if os.name == "nt":
		OS = "win"
		TITLE = "ICLab (v" + VERSION + ")"
	else:
		OS = "linux"
	echo(1,"os name checked: " + OS)
	# set title if windows
	if OS == "win":
		os.system("title " + TITLE)
		echo(1,"title setting status: PASS")
		CMDS.update({"chdir":CMDS["chd"]})
	else:
		CMDS.update({"cd":CMDS["chd"]})
	CMDS.pop("chd")
	# import by os
	if OS == "win":
		pass
	else:
		pass
	echo(1,"import by OS status: PASS")
	# record input
	MEMO.set({"input_history":[]})
	echo(1,"input history class: PASS")
	# work path check
	if os.getcwd() != sys.path[0] and sys.path[0] != "":
		echo(1,"moving work path to \"" + sys.path[0] + "\"")
		os.chdir(sys.path[0])
	else:
		echo(1,"work path check: PASS")
	PATH = os.getcwd()
	# compatibility check ( serch a file in ./ named "c_mode.icl" )
	if os.path.exists("./c_mode.icl"):
		C_MODE = True
		echo(1,"compatibility mode: Activated")
	else:
		C_MODE = False
		echo(1,"compatibility mode: Inactivated")
	# path check & make
	temp = ("temp"+os.sep,"."+os.sep)
	for i in temp:
		path_fixer(i)
	echo(1,"folder check: PASS")
	OCMDS = {}
	for i in CMDS:
		OCMDS.update({i:CMDS[i]})
	OG = {}
	for i in globals():
		OG.update({i:globals()[i]})
	echo(1,"backup globals: PASS")
	echo(1,"Initialization compeleted\n")




def ICLab_search_blk(): # block search & load guide
	global BLOCK, ARGS
	if ARGS:
		return
	files = scan_path("." + os.sep,"top")[1]
	blocks = []
	for i in files:
		if i[-4:] == ".blk":
			blocks.append(i)
		else:
			pass
	if len(blocks) == 1:
		echo(1,"block package found: " + blocks[0])
		BLOCK = blocks[0]
	elif len(blocks) == 0:
		echo(1,"can't find a ICLab block file, use \"createblock\" to create a block file")
	else:
		echo(1,"more than 1 block file found, please choose one to load(input the number before the one you want to choose)")
		n = 1
		for i in blocks:
			echo(0," " + str(n) + ". " + i[2:])
			n += 1
		wait = True
		try:
			while wait:
				temp = input("\nChoice: ")
				try:
					BLOCK = blocks[int(temp)-1]
					wait = False
				except Exception:
					echo(0,"Please input correct number, example \"1\"")
		except KeyboardInterrupt:
			echo(0,"")
			echo(1,"keyboard interrupt detected, skipping block loading")
	if len(BLOCK) > 0 and type("") == type(BLOCK):
		wait = True
		try:
			while wait:
				temp = passwd_input("Block-Password: ")
				wait = False
				try:
					load_block("-t \"" + BLOCK + "\" -p \"" + temp + "\"")
					if type("") == type(BLOCK):
						wait = True
				except Exception as err:
					echo(1,"[ERROR] Failed to load block, result: " + str(err))
					wait = True
		except KeyboardInterrupt:
			echo(0,"")
			echo(1,"keyboard interrupt detected, skipping block loading")




# --||||-- [ BUILTIN FUNCTIONS ] --||||--




def iclab_help(cmd): # iclab help
	echo(1,"ICLab help ( ICLab Version: " + VERSION + """ )

( for details please try "<command> -h" or "<command> --help" )
""")
	cmds = []
	for i in CMDS:
		cmds.append(i)
	cmds.sort()
	for i in cmds:
		temp = "  " + i
		echo(0,temp + (3-int(len(temp)/8))*"\t" + "- " + (CMDS[i])[1])
	echo(0,"")
	return




def exit_iclab(cmd): # exit iclab
	if type(BLOCK) != type(""):
		echo(1,"unloading block")
		unload_block("")
	else:
		pass
	echo(1,"cleanning up caches")
	ICLab_end()




def iclab_debug(cmd): # iclab debug mode switch
	global DEBUG
	if DEBUG:
		DEBUG = False
		echo(1,"debug mode OFF")
	else:
		DEBUG = True
		echo(1,"debug mode ON")




def edit_module(cmd): # module adder
	global BLOCK
	dlt = ""
	add = ""
	yes = False
	lists = False
	opts = get_args(cmd)
	target = ""
	if opts == {}:
		echo(1,"[ERROR] syntax error, try \"-h\" tag for help")
		return
	for i in opts:
		if i in ("-h","--help"):
			echo(1,"""ICLab Block Module Add/Remover

Usage: edmods <-a,-d> <module_name> [-l] [-y]

 -a --add <module_name>         - add module to block
 -d --delete <module_name>      - delete module from block
 -l --list                      - list all modules in the block
 -y --yes                       - confirm Yes during the process
 -h --help                      - display this page

Examples:
 > edmods -l
 > edmods -a test.py -d example.py -l -y
""")
			return
		elif i in ("-a","--add"):
			add = opts[i]
		elif i in ("-d","--delete"):
			dlt = opts[i]
		elif i in ("-l","--list"):
			lists = True
		elif i in ("-y","--yes"):
			yes = True
		else:
			echo(1,"[ERROR] unhandled option \"" + i + "\", try \"-h\" tag for help")
			return
	if type("") == type(BLOCK):
		echo(1,"[ERROR] no block loaded, please load a block first")
		return
	else:
		mods = []
		for i in BLOCK.namelist():
			if i[:5] == "mods/" and i != "mods/":
				mods.append(i[5:])
	if len(add) > 0:
		pathx = sys.path[0] + os.sep + "temp" + os.sep + "extracts" + os.sep
		if not os.path.exists(add):
			echo(1,"[ERROR] can't find \"" + add + "\"")
			return
		else:
			pass
		temp = read_path(add)[1]
		echo(1,"add module")
		if temp in mods:
			if not yes:
				echo(1,"\"" + temp + "\" module already exist, overwrite?(input \"y\" for yes, else for not)")
				choice = input("")
			else:
				choice = "y"
			if choice == "y":
				echo(1,"extracting block")
				try:
					extract_block()
				except Exception as err:
					echo(1,"[ERROR] can't extract block: " + str(err) + ", exiting")
					return
				echo(1,"editing files")
				os.remove(pathx + "mods" + os.sep + temp)
				echo(1,"encrypting")
				iccode_en(PWD,add,pathx + "mods" + os.sep + temp)
				echo(1,"updating block and deleting caches")
				try:
					update_block()
				except Exception as err:
					echo(1,"[ERROR] can't update block: " + str(err) + ", exiting")
					return
				echo(1,"\"" + add + "\" module added, please reload block to update")
			else:
				pass
		else:
			echo(1,"encrypting")
			iccode_en(PWD,add,sys.path[0] + os.sep + "temp" + os.sep + "module.temp")
			echo(1,"updating block")
			try:
				BLOCK.write(sys.path[0] + os.sep + "temp" + os.sep + "module.temp","mods" + os.sep + temp)
			except Exception as err:
				echo(1,"[ERROR] can't update block: " + str(err) + ", exiting")
				return
			echo(1,"deleting caches")
			os.remove(sys.path[0] + os.sep + "temp" + os.sep + "module.temp")
			echo(1,"\"" + add + "\" module added, please reload block to update")
	if len(dlt) > 0:
		pathx = sys.path[0] + os.sep + "temp" + os.sep + "extracts" + os.sep
		if not dlt in mods:
			echo(1,"[WARNING] no module named \"" + dlt + " in block")
		else:
			echo(1,"extracting block")
			try:
				extract_block()
			except Exception as err:
				echo(1,"[ERROR] can't extract block: " + str(err) + ", exiting")
				return
			echo(1,"editing files")
			os.remove(pathx + "mods" + os.sep + dlt)
			echo(1,"updating block and deleting caches")
			try:
				update_block()
			except Exception as err:
				echo(1,"[ERROR] can't update block: " + str(err) + ", exiting")
				return
			echo(1,"\"" + dlt + "\" module deleted, please reload block to update")
	if lists:
		echo(1,"modules in block:")
		for i in mods:
			echo(0," - " + i)
		echo(0,"")




def run_scripts(cmd): # ICLab scripts runner
	opts = get_args(cmd)
	for i in opts:
		if i in ("-h","--help"):
			echo(1,"""ICLab Scripts Executer

Usage: icsh <scripts_file_name,-h>

 -h --help                      - display this page

Examples:
 > icsh test.ics
 > .""" + os.sep + """test.ics
""")
			return
		else:
			echo(1,"[ERROR] unhandled option \"" + i + "\", try \"-h\" tag for help")
			return
	if not os.path.exists(cmd):
		echo(1,"[ERROR] file \"" + cmd + "\" not found")
		return
	if os.path.isdir(cmd):
		echo(1,"[ERROR] \"" + cmd + "\" is a folder")
		return
	try:
		f = open(cmd)
		scr = f.read()
		f.close()
	except Exception as err:
		echo(1,"[ERROR] error while reading scripts, result: " + str(err))
		return
	scripts_processor(scr,read_path(cmd)[1])




def unload_block(cmd): # unload block
	global BLOCK, CMDS, HEAD, OG, PWD
	opts = get_args(cmd)
	target = ""
	for i in opts:
		if i in ("-h","--help"):
			echo(1,"""ICLab Block unloader

Usage: unloadblk

 -h --help                      - display this page

Examples:
 > unloadblk
""")
			return
		else:
			echo(1,"[ERROR] unhandled option \"" + i + "\", try \"-h\" tag for help")
			return
	if type("") == type(BLOCK):
		echo(1,"[ERROR] No block loaded, no need to unload")
		return
	else:
		pass
	echo(1,"deleting loaded globals")
	gbs_now = {}
	for i in globals():
		gbs_now.update({i:globals()[i]})
	for i in OG:
		gbs_now.pop(i)
	for i in gbs_now:
		globals().pop(i)
	echo(1,"reseting header")
	HEAD = "ICLab"
	USER = ""
	echo(1,"reseting block tag")
	BLOCK.close()
	BLOCK = BLOCK.filename
	PWD = ""
	CMDS = {}
	for i in OCMDS:
		CMDS.update({i:OCMDS[i]})
	echo(1,"block unloaded")




def load_block(cmd): # load block
	global BLOCK, CMDS, INFO, RLTS
	opts = get_args(cmd)
	target = ""
	temp = None
	if opts == {}:
		echo(1,"[ERROR] syntax error, try \"-h\" tag for help")
		return
	for i in opts:
		if i in ("-h","--help"):
			echo(1,"""ICLab Block Loader

Usage: loadblk -t <block_name> -p <password>

 -t --target <block_name>       - target block name
 -p --password <password>       - block password
 -h --help                      - display this page

Examples:
 > loadblk -t "ic.blk" -p "example"
""")
			return
		elif i in ("-t","--target"):
			target = opts[i]
		elif i in ("-p","--password"):
			temp = opts[i]
		else:
			echo(1,"[ERROR] unhandled option \"" + i + "\", try \"-h\" tag for help")
			return
	if type("") != type(BLOCK):
		echo(1,"[ERROR] a block has already loaded, try \"unloadblk\" to unload first")
		return
	else:
		target = os.path.abspath(target)
	if not os.path.exists(target):
		echo(1,"[ERROR] \"" + target + "\" not found")
		return
	else:
		pass
	if temp == None:
		temp = passwd_input("Block-Password: ")
	else:
		pass
	echo(1,"loading block infos...")
	try:
		blk = load_blockinfo(temp,target)
		if blk[0]:
			BLOCK = blk[1]
		else:
			raise Exception()
	except Exception as err:
		echo(1,"[ERROR] Can't load \"" + target + "\", wrong password or block file has been broken")
		return
	echo(1,"scanning additional modules...")
	files = BLOCK.namelist()
	mods = []
	for i in files:
		if i[:5] == "mods/" and i != "mods/":
			mods.append(i)
		else:
			pass
	if len(mods) > 0:
		echo(1,str(len(mods)) + " modules found, loading modules...")
		loaded = 0
		coder = iccode(PWD)
		mod_relateds = {}
		mod_relateds_ = {}
		for i in mods:
			try:
				temp = BLOCK.read(i)
				temp = coder.decode(temp)
				coder.reset()
				imported = execute(temp)
				globals().update(imported)
				CMDS.update(INFO)
				mod_relateds.update({i:RLTS})
				mod_relateds_.update({i:RLTS})
				loaded += 1
			except Exception as err:
				echo(1,"[WARNING] failed to load \"" + i + "\", result: " + str(err))
				continue
		echo(1,"checking relateds...")
		for i in mod_relateds:
			cls = (mod_relateds[i])["cls"]
			funcs = (mod_relateds[i])['funcs']
			vars = (mod_relateds[i])['vars']
			missed = [[],[],[]]
			for i2 in cls:
				if i2 in globals().keys():
					pass
				else:
					missed[0].append(i2)
			for i2 in funcs:
				if i2 in globals().keys():
					pass
				else:
					missed[1].append(i2)
			for i2 in vars:
				if i2 in globals().keys():
					pass
				else:
					missed[2].append(i2)
			if missed == [[],[],[]]:
				pass
			else:
				msg = "module \"" + i + "\" need extra"
				if missed[0] != []:
					msg += " class(es):"
					for i2 in missed[0]:
						msg += " \"" + i2 + "\""
					msg += ","
				if missed[1] != []:
					msg += " function(s):"
					for i2 in missed[1]:
						msg += " \"" + i2 + "\""
					msg += ","
				if missed[2] != []:
					msg += " variable(s):"
					for i2 in missed[2]:
						msg += " \"" + i2 + "\""
					msg += ","
				msg = msg[:-1]
				msg += " to execute, unloading \"" + i + "\"..."
				echo(1,msg)
				loaded -= 1
				mod_relateds_.pop(i)
				others = []
				for i2 in ("cls","funcs","vars"):
					for i3 in mod_relateds_:
						others.append((mod_relateds_[i3])[i2])
				temp = BLOCK.read(i)
				temp = coder.decode(temp)
				coder.reset()
				imported = execute(temp)
				if imported['INFO'] == {}:
					pass
				else:
					CMDS.pop(list((imported['INFO']).keys())[0])
				imported.pop("INFO")
				imported.pop("RLTS")
				for i2 in imported:
					if i2 in others or i2 in OG:
						pass
					else:
						globals().pop(i2)
		echo(1,str(loaded) + " modules loaded")
		if loaded != 0:
			del INFO, RLTS
		else:
			pass
	else:
		echo(1,"no modules found")
	echo(1,"block \"" + target + "\" loaded")
	return




def change_dir(cmd): # change work path
	global PATH
	opts = get_args(cmd)
	target = ""
	for i in opts:
		if i in ("-h","--help"):
			echo(1,"""Change ICLab working path

Usage: <chdir/cd> <target_path> [-h]

 -h --help                      - display this page

Examples:
 >cd "/home"
""")
			return
		else:
			echo(1,"[ERROR] unhandled option \"" + i + "\", try \"-h\" tag for help")
			return
	if len(target) == 0:
		target = cmd
	if os.path.exists(target):
		os.chdir(target)
		PATH = os.getcwd()
		return
	else:
		echo(1,"[ERROR] \"" + target + "\" not found")
		return




def ch_pwd(cmd): # change block password
	opts = get_args(cmd)
	for i in opts:
		if i in ("-h,--help"):
			echo(1,"""ICLab Block User Password Editor

Usage: chpwd

 -h --help                      - display this page

Examples:
 > chpwd
""")
		else:
			echo(1,"[ERROR] unhandled option \"" + i + "\", try \"-h\" tag for help")
			return
	if type("") == type(BLOCK):
		echo(1,"[ERROR] no block loaded yet, please load a block first")
		return
	else:
		pass
	try:
		temp = passwd_input("Old password: ")
	except KeyboardInterrupt:
		echo(0,"")
		echo(1,"keyboard interrupt detected, exiting")
		return
	if temp != PWD:
		echo(1,"[ERROR] wrong password")
		return
	else:
		pass
	try:
		wait = True
		while wait:
			password = passwd_input("New password: ")
			temp = passwd_input("Verify password: ")
			wait = False
			if temp != password:
				echo(1,"password verification failed, please try again")
				wait = True
			if len(password) < 4:
				echo(1,"password length must be at least 4 words")
				wait = True
			if len(password) > 30:
				echo(1,"password length must be less than 30 words")
				wait = True
	except KeyboardInterrupt:
		echo(0,"")
		echo(1,"keyboard interrupt detected, exiting")
		return
	try:
		configs = BLOCK.read("user/user.json")
		coder = iccode(PWD)
		configs = coder.decode(configs)
		configs = configs.decode()
		configs = json.loads(configs)
		if PWD != configs["iccode_key"]:
			raise Exception("user config file value didn't match")
		else:
			pass
	except Exception as err:
		echo(1,"[ERROR] Failed to read block config file: " + str(err) + ", file may be broken")
	new_coder = iccode(temp)
	pwd = temp
	pathx = sys.path[0] + os.sep + "temp" + os.sep + "extracts" + os.sep
	echo(1,"updating data")
	configs.update({"iccode_key":temp})
	echo(1,"encoding data")
	temp = (json.dumps(configs)).encode()
	echo(1,"encrypting")
	coder.reset()
	temp = coder.encode(temp)
	echo(1,"extracting block")
	extract_block()
	echo(1,"editing file")
	f = open(pathx + os.sep + "user" + os.sep + "user.json","wb")
	f.write(temp)
	f.close()
	echo(1,"encrypting files in new password")
	files = scan_path(pathx,"all")
	patho = sys.path[0] + os.sep + "temp" + os.sep + "new_extracts" + os.sep
	if os.path.exists(patho):
		shutil.rmtree(patho)
	else:
		pass
	for i in files[0]:
		path_fixer(patho+i[len(pathx):])
	for i in files[1]:
		coder.reset()
		new_coder.reset()
		f1 = open(i,"rb")
		f2 = open(patho+i[len(pathx):],"wb")
		while True:
			data = f1.read(1024)
			if data == b"":
				break
			data = coder.decode(data)
			data = new_coder.encode(data)
			f2.write(data)
		f1.close()
		f2.close()
	shutil.rmtree(pathx)
	os.rename(patho,pathx)
	echo(1,"updating block")
	update_block()
	echo(1,"reloading block")
	unload_block("")
	load_block("-t \"" + BLOCK + "\" -p \"" + pwd + "\"")
	echo(1,"password changed")




def edit_userconf(cmd): # edit user config
	opts = get_args(cmd)
	edit_key = ""
	delete_key = ""
	edits = None
	lists = False
	if opts == {}:
		echo(1,"[ERROR] syntax error, try \"-h\" tag for help")
		return
	for i in opts:
		if i in ("-h,--help"):
			echo(1,"""ICLab Block User Configs Editor

Usage: edconf <-e,-d> <key_name> [-l,-v]

 -e --edit <key_name>           - edit a key's value
 -d --delete <key_name>         - delete a key
 -v --value [key_value]         - new value of the editing key
 -l --list                      - list all key and its value
 -h --help                      - display this page

Examples:
 > edconf -e iccode_key -d window_color
 > edconf -l
""")
		elif i in ("-e","--edit"):
			edit_key = opts[i]
		elif i in ("-d","--delete"):
			delete_key = opts[i]
		elif i in ("-l","--list"):
			lists = True
		elif i in ("-v","--value"):
			edits = opts[i]
		else:
			echo(1,"[ERROR] unhandled option \"" + i + "\", try \"-h\" tag for help")
			return
	if type("") == type(BLOCK):
		echo(1,"[ERROR] no block loaded yet, please load a block first")
		return
	else:
		pass
	try:
		configs = BLOCK.read("user/user.json")
		coder = iccode(PWD)
		configs = coder.decode(configs)
		configs = configs.decode()
		configs = json.loads(configs)
		if PWD != configs["iccode_key"]:
			raise Exception("user config file value didn't match")
		else:
			pass
	except Exception as err:
		echo(1,"[ERROR] Failed to read block config file: " + str(err) + ", file may be broken")
	if len(edit_key) > 0:
		if edit_key == "iccode_key":
			echo(1,"[WARNING] you are trying to edit block password key, this editor is not allowed to do that, try \"chpwd\" command instead")
		else:
			if edits == None:
				edits = input("Values for \"" + edit_key + "\": ")
			else:
				pass
			configs.update({edit_key:edits})
			echo(1,"key \"" + edit_key + "\" = \"" + edits + "\" updated")
	if len(delete_key) > 0:
		if delete_key == "iccode_key":
			echo(1,"[WARNING] operation rejected, block password key can't be deleted")
		elif delete_key == "username":
			echo(1,"[WARNING] operation rejected, block username can't be deleted")
		else:
			if not delete_key in configs:
				echo(1,"key \"" + delete_key + "\" dosen't exist, can't delete")
			else:
				configs.pop(delete_key)
				echo(1,"key \"" + delete_key + "\" deleted")
				delete_key = None
	if edits != None or delete_key == None:
		echo(1,"saving changes to block, extracting")
		extract_block()
		pathx = sys.path[0] + os.sep + "temp" + os.sep + "extracts" + os.sep
		echo(1,"encoding data")
		temp = (json.dumps(configs)).encode()
		echo(1,"encrypting")
		coder.reset()
		temp = coder.encode(temp)
		echo(1,"editing file")
		f = open(pathx + os.sep + "user" + os.sep + "user.json","wb")
		f.write(temp)
		f.close()
		echo(1,"updating block")
		update_block()
		echo(1,"changes updated")
	if lists:
		echo(1,"configs key in block:")
		echo(0," |\t[Key_names]\t| \t\t[Values]\t\t|")
		for i in configs:
			temp = " | " + i
			if temp != " | iccode_key":
				echo(0,temp + (3-int(len(temp)/8))*"\t" + "| " + str(configs[i]) + (5-int((len(configs[i])+2)/8))*"\t" + "|")
			else:
				echo(0,temp + (3-int(len(temp)/8))*"\t" + "| " + "*"*len(configs[i]) + (5-int((len(configs[i])+2)/8))*"\t" + "|")
		echo(0,"")




def block_create(cmd): # block file create guide
	opts = get_args(cmd)
	for i in opts:
		if i in ("-h","--help"):
			echo(1,"""ICLab Block Create Guide

Usage: createblock

 -h --help                      - display this page

""")
			return
		else:
			echo(1,"[ERROR] unhandled option \"" + i + "\", try \"-h\" tag for help")
			return
	echo(1,"=+= ICLab Block Create Guide =+=")
	echo(1,"please follow the steps to create a block file")
	wait = True
	# input file name
	try:
		while wait:
			blk_name = input("Block file name: ")
			wait = False
			if blk_name[-4:] == ".blk":
				pass
			else:
				blk_name = blk_name + ".blk"
			temp = ("/","\\","\"","*","|","?","<",">",":")
			for i in temp:
				if i in blk_name:
					echo(1,"block file name mustn't include '" + i + "'")
					wait = True
					break
	except KeyboardInterrupt:
		echo(0,"")
		echo(1,"keyboard interrupt detected, stopping create block")
		return
	# input username
	try:
		username = input("Username: ")
	except KeyboardInterrupt:
		echo(0,"")
		echo(1,"keyboard interrupt detected, stopping create block")
	# input iccode key
	try:
		wait = True
		while wait:
			password = passwd_input("Password: ")
			temp = passwd_input("Verify password: ")
			wait = False
			if temp != password:
				echo(1,"password verification failed, please try again")
				wait = True
			if len(password) < 4:
				echo(1,"password length must be at least 4 words")
				wait = True
			if len(password) > 30:
				echo(1,"password length must be less than 30 words")
				wait = True
	except KeyboardInterrupt:
		echo(0,"")
		echo(1,"keyboard interrupt detected, stopping create block")
	echo(1,"Block basic info:")
	echo(0," File name: " + blk_name)
	echo(0," Username : " + username)
	echo(0," Password : " + ("*" * len(password)))
	try:
		temp = input("(press ENTER to continue, Ctrl+C to stop)")
	except KeyboardInterrupt:
		echo(0,"")
		echo(1,"keyboard interrupt detected, stopping create block")
	echo(1,"releasing basic config file")
	temp = {"username":username,"iccode_key":password}
	try:
		f = open("./temp/user_t","w")
		json.dump(temp,f,indent=2)
		f.close()
		echo(1,"encrypting file")
		iccode_en(password,"./temp/user_t","./temp/user.json")
	except Exception as err:
		echo(1,"[ERROR] failed to write file, result: " + str(err))
		return
	echo(1,"creating blank block file \"" + blk_name + "\"")
	try:
		blk = block.create(blk_name)
		echo(1,"writing data to block file")
		blk.write("temp/user.json","user/user.json")
		blk.close()
	except Exception as err:
		echo(1,"[ERROR] Failed to create block file, result: " + str(err))
		return
	echo(1,"block file create successfully")
	echo(1,"cleanning up caches")
	try:
		os.remove("temp/user_t")
		os.remove("temp/user.json")
	except Exception as err:
		echo(1,"Failed to clean caches, result: " + str(err))
		return
	return




# --||||-- [ PROCESS FUNCTIONS ] --||||--




def main(): # main processor
	ICLab_init()
	ICLab_args_processor()
	ICLab_search_blk()
	ICLab_cmd_loop()
	ICLab_end()




if __name__ == '__main__': # debug processor
	main()
else:
	ICLab_init()
