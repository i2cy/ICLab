# ICLab Command Shell Working Table *(icshell)* #
  It is kind of like a cmd shell of *system shell* + *custom shell* + *custom module(which is ****VERY SCALABLE****)*,   
  and its custom stuff(such as modules, userdata) will be encrypted with your own password so that your data will be very safe(I do believe my encryption algorithm is awesome)


## Instructions ##
- to run on **Windows**, you can just run **Table.cmd** or by using command to execute
  the **Table.py**
- to run on **linux**, just run the **Table.py**
- for **icshell command help** please use command **"ichelp"** in **icshell**


## Block Instructions ##
  Block is a ICLab's encrypted storage zip file, which can be create by using command   
  **"createblock"** in icshell to create one
  


## Module Instructions ##
- every module must be python scripts(definitely)
- every module must has a global tag **INFO** in it    
  ***INFO*** is a dict-type tag with a formant of *{<command_name>:(<function_name>,<short_description>)}*    
  which is used to register the command in module
- to install a module, please load a **block file** first and use the command of **"edmods"**
- example(***example_mod.py*** in ***mods***):   
~~~
INFO = {"example":("test","This is an example mod")}

def test(cmd):
	print(cmd)
~~~
