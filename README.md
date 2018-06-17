# ICLab Command Shell Working Table *(icshell)* #
  It is kind of like a cmd shell of *system shell* + *custom shell* + *custom module(which is ****VERY SCALABLE****)*,   
  and its custom stuff(such as modules, userdata) will be encrypted with your own password so that your data will be    
  very safe(I do believe my encryption algorithm is awesome)


## Instructions ##
- to run on **Windows**, you can just run **Table.cmd** or by using command to execute
  the **Table.py**
- to run on **linux**, just run the **Table.py**
- for **icshell command help** please use command **"ichelp"** in **icshell**


## Block Instructions ##
  Block is a ICLab's encrypted storage zip file, which can be create by using command   
  **"createblock"** in icshell to create one
- To redirect console message to a file please use "**>**", with a formant like **>** *[target_path]*   
  example:   
    scan -t ./ >result.txt


## Module Instructions ##
- every module must be python scripts(definitely)
- every module must has global tags **INFO** and **RLTS** in it    
  ***INFO*** is a dict-type tag with a formant like this: *{<command_name>:(<function_name>,<short_description>)}*
  which is used to register the command in module   
  ***RLTS*** is a dict_type tag with a formant like this: *{"cls":(<related_classes>,...),"funcs":(<related_functions>,...),
  "vars":(<related_variables>,...)}*
  which is used to declare the relateds that this module need to have
- to install a module, please load a **block file** first and use the command of **"edmods"**
- example(***example_mod.py*** in ***mods***):   
~~~
INFO = {"example":("test","This is an example mod")}
RLTS = {"cls":(),"funcs":("echo",),"vars":()}

def test(cmd):
	echo(cmd)
~~~

## Compatibility Mode ##
- to enable **Compatibility Mode**, you need to create a file named **"c_mode.icl"** in the *folder* which is the same as "Table.py"
- *Compatibility Mode* is need to be used when you find you can't run *ICLab* normally. It will disable some features such as
  "cover_input" to make you can run ICLab normally
