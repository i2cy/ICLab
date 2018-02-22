# ICLab Command Shell Working Table #
  It is kind of like a cmd shell of *system shell* + *custom shell* + *custom module(which is ***VERY SCALABLE****)*
  and its custom stuff will be encrypted with your own password so that your data will be very safe

## Instructions ##
- to run on **Windows**, you can just run **Table.cmd** or use command to execute
 the **Table.py**
- to run on **linux**, just run the **Table.py**

## Module Formant ##
- every module must be python scripts(definitely)
- every module must has a global tag **INFO** in it    
  ***INFO*** is a dict-type tag with a formant of *{<command_name>:(<function_name>,<short_description>)}*    
  which is used to register the command in module
- example:   
~~~
INFO = {"example":("test","This is an example mod")}

def test(cmd):
	print(cmd)
~~~
