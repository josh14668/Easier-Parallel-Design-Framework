from readModule import *

inputs = int(raw_input("How Many Inputs:"))

#outputs = int(raw_input("How Many Outputs:"))

inputRate = int(raw_input("What is the input rate(bits/clock):"))

num_modules = int(raw_input("How Many HW modules:"))

out_put = raw_input("What is the output called:")

modules = []
print "module file names:"
sentinel = ' '
i = 0
for line in iter(raw_input,sentinel):
    modules.append(line)
    i = i+1
    if(i==num_modules):
        break

#for line in modules:
#    print line
#specifyModule = modules[1]
all_mods={}

for element in modules:

    readLine = read_Scala(srcDirectory + element + '.scala')

    if readLine==1:
        print "Invalid File"
    else:
        moduleName=readLine[0]
        moduleParams=readLine[1]


    ioList= read_inputs_outputs(srcDirectory + element + '.scala')
    list_inputs = ioList[0]
    list_outputs = ioList[1]
    all_mods[moduleName]=ioList
    #print moduleName
    #print list_inputs
    #print list_outputs

    write_Scala(tstDirectory,moduleName,ioList[0],inputs,inputRate)

for key in all_mods.keys():
   print key
   print all_mods[key][1]

connect_modules(srcDirectory,inputRate,inputs,all_mods,out_put)

ioList= read_inputs_outputs(srcDirectory + "MainModule.scala")
