INFO = {"netscan":("icy_shadow_net_scanner","ISPY TCP scanner")}
RLTS = {"cls":("temp_struck","threading","socket","time"),"funcs":("echo","get_args"),"vars":()}
ISPY_VERSION = "1.3"




def icy_shadow_net_scanner(cmd): # main cmd part
	opts = get_args(cmd)
	if opts == {}:
		echo(1,"[ERROR] syntax error, try \"-h\" fo help")
		return
	scan_part = tcp_net_scanner()
	ips = False
	ports = False
	for i in opts:
		if i in ('-h','--help'):
			echo(1,"""Icy Shadow TCP Network Scanner [v.""" + ISPY_VERSION + """]

usage: netscan <-t> <target_ip> <-p> <target_port> [-m] <message> [-timeout] <timeout> [-maxthreads] <max_thread_number> [-c] <coding_type> [-o]

 -t --target <target_ip>         - target IP, format: xx.xx.xx.xx,
                                   "*" is aviliable
 -p --port <target_ports>        - target port number, format:
 	                              xxxx,xxxx,xxxx,(...)
                                   "*" is aviliable
 -m --message <message>          - an utf-8 message which will be
                                   send to target
 -timeout --timeout <timeout>    - set timeout for TCP socket
 -maxtheads --maxthreads <num>   - set max threading program number
 -o --openonly                   - only print results which are
                                   open
 -c -coding <coding_type>        - set the coding type of received
                                   TCP message(hex,string,...)

Example:
 >netscan -t 192.168.0.1 -p 22,80 -m "test" -timeout 1 -maxthreads 50 -o -c "utf-8"

""")
			return
		elif i in ("-t","--target"):
			ips = opts[i]
		elif i in ("-p","--port"):
			ports = opts[i]
		elif i in ("-m","--message"):
			try:
				scan_part.msgs((opts[i]).encode())
			except Exception as err:
				echo(1,"[ERROR] failed to set message, feedback: " + str(err))
				return
		elif i in ("-timeout","--timeout"):
			try:
				scan_part.timeouts(int(opts[i]))
			except Exception as err:
				echo(1,"[ERROR] failed to set timeout")
				return
		elif i in ("-maxthreads","--maxthreads"):
			try:
				scan_part.maxtc(int(opts[i]))
			except Exception as err:
				echo(1,"[ERROR] failed to set max threading program number")
				return
		elif i in ("-o","--openonly"):
			scan_part.echomode("print_open")
		elif i in ("-c","--coding"):
			scan_part.coding(opts[i])
		else:
			echo(1,"[ERROR] unhandled option \"" + i + "\", try \"-h\" tag for help")
			return
	try:
		temp = ips.split(".")
		temp2 = None
		if len(temp) == 4:
			for i in temp:
				if i == "*":
					pass
				else:
					temp2 = int(i)
					if temp2 in range(0,256):
						pass
					else:
						temp = False
						break
		else:
			temp = False
	except Exception:
		temp = False
	if temp != False:
			ips = ips.split(".")
	else:
		try:
			ips = (((socket.getaddrinfo(ips,22)[0])[4])[0])
			ips = ips.split(".")
		except Exception as err:
			echo(1,"[ERROR] failed to connect to \"" + str(ips) + "\", feedback: " + str(err))
			return
	if ips != False and ports != False:
		try:
			echo(1,"scanning target: " + ips[0] + "." + ips[1] + "." + ips[2] + "." + ips[3] + "(" + ports + ")")
			ports = ports.split(",")
			scan_part.target(ips,ports)
		except Exception:
			echo(1,"[ERROR] failed to set target")
			return
	else:
		echo(1,"[ERROR] No target set yet")
		return
	scan_part.scan()




class tcp_net_scanner:
	def __init__(self):
		# defaults
		self.timeout = 15
		self.max_thread_count = 20
		self.echo_mode = "print_all" # ( "print_all": print all result, "print_open": print open result)
		self.msg = b""
		self.ips = []
		self.ports = []
		self.code = "hex"
	def target(self,ips,ports): # ports must be []
		n = 0
		for i in ips:
			if i == "*":
				ips[n] = range(1,256)
			else:
				ips[n] = [i]
			n += 1
		for i in ips[0]:
			for i2 in ips[1]:
				for i3 in ips[2]:
					for i4 in ips[3]:
						self.ips.append(str(i)+"."+str(i2)+"."+str(i3)+"."+str(i4))
		if ports == ["*"]:
			self.ports = range(1,65536)
		else:
			for i in ports:
				self.ports.append(int(i))
	def maxtc(self,num):
		self.max_thread_count = num
	def coding(self,mode):
		self.code = mode
	def echomode(self,mode):
		if mode in ("print_all","print_open"):
			self.echo_mode = mode
		else:
			raise Exception("echo mode only support \"print_all\" & \"print_open\"")
	def msgs(self,msg):
		if type(msg) == type(b"example"):
			self.msg = msg
		else:
			raise Exception("message must be byte(s)")
	def timeouts(self,num):
		self.timeout = num
	def scan(self): # action
		thread_num = temp_struck()
		thread_num.set({0:0})
		for i in self.ips:
			for i2 in self.ports:
				scan_thread = threading.Thread(target=net_scanner,args=(self,thread_num,i,int(i2)))
				while thread_num.read(0) > self.max_thread_count:
					time.sleep(0.2)
				scan_thread.start()
		while thread_num.read(0) != 0:
			time.sleep(2)
		return




def net_scanner(scanner_class,thread_num,ip,port): # thread A0
	thread_num.set({0:thread_num.read(0)+1})
	res = "| " + ip + "(" + str(port) + ")" + (3-int((4+len(ip+str(port)))/8))*"\t" + " |"
	temp = TCP_talk((ip,port),scanner_class.msg,scanner_class.timeout)
	if (temp[0])[0] == 0:
		res += "OPEN |"
	elif (temp[0])[0] == 1:
		res += "CLOSE| (failed to connect:" + (temp[0])[1] + ")"
	else:
		res += "OPEN | (failed to send message:" + (temp[0])[1] + ")"
	if (temp[0])[0] in (0,2):
		if type(temp[2]) == type(b'example'):
			if scanner_class.code == "hex":
				for i in temp[2]:
					data = (hex(i)[2:]).upper()
					if len(data) == 1:
						data = "0" + data
					res += " " + data
			elif scanner_class.code == "string":
				res += " " + str(temp[2])
			else:
				try:
					data = temp[2].decode(scanner_class)
					res += " " + data
				except Exception:
					res += " (can't decode) " + str(temp[2])
		else:
			res += ' (failed to receive message: ' + temp[2] + ')'
	if scanner_class.echo_mode == "print_all":
		echo(0,res)
	else:
		if (temp[0])[0] == 1:
			pass
		else:
			echo(0,res)
	thread_num.set({0:thread_num.read(0)-1})




def TCP_talk(host,msg,timeout): #TCP send/recv thread (top)
	res = [(0,None),None,b'']
	clt = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	clt.settimeout(timeout)
	datas = temp_struck()
	datas.set({"recv":None})
	try:
		clt.connect(host)
		try:
			clt.sendall(msg)
		except Exception as err:
			res[0] = (2,str(err))
		temp = TCP_recv(clt)
		res[1] = temp[0]
		res[2] = temp[1]
	except Exception as err:
		res[0] = (1,str(err))
	return res




def TCP_recv(clt):
	temp = b''
	try:
		while True:
			data = clt.recv(4096)
			temp += data
			if len(data) < 4096:
				break
		return (0,temp)
	except Exception as err:
		if len(temp) > 0:
			return (0,temp)
		else:
			return (1,str(err))



# [AUTORUN]
import threading, socket