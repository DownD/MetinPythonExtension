import sys, os
#chat.AppendChat(3,"PythonDumper: Starting")
f = open('pythonDump.txt','w')
modules_key = sys.modules.keys()
modules_dic = sys.modules
built_in = sys.builtin_module_names
for mod in modules_key:
    if mod not in built_in:
        print >>f,'\n-----MODULE------'
        print >>f,str(mod)
        print >>f,'-----------------\n'
        funcs = dir(modules_dic.get(mod))
        for func in funcs:
            print >>f,str(func)
			
#chat.AppendChat(3,"Path: " + str(os.path.realpath(f.name)))
f.close()
#chat.AppendChat(3,"PythonDumper: Done")