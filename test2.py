
srcDirectory = "src/main/scala/"

tstDirectory = "src/test/scala/"


class Module():


    def __init__(self,name,inputTypes,outputTypes,numInstances):
        self.name = name

        #inputTypes is a dictionary
        self.inputTypes = inputTypes
        #outputypes is a dictionary
        self.outputTypes = outputTypes

        self.numInstances = numInstances

    def getName(self):
        return self.name

    def getNumInputs(self):
        return len(self.inputTypes)

    def getNumOutputs(self):
        return len(self.outputTypes)

    def getNumInstances(self):
        return self.numInstances

    def setNumInstances(self,num):
        self.numInstances = num



def inputsOutputs(directory):
    fhand = open(directory)
    inputList = {}
    outputList = {}
    for line in fhand:
        if 'Input' in line:
            valName =line[line.find('l')+2:line.find('=')]
            valType=line[line.find('(')+1:line.find(')')+1]

            inputList[valName] = valType


        elif 'Output' in line:
            valName =line[line.find('l')+2:line.find('=')]
            valType=line[line.find('(')+1:line.find(')')+1]
            outputList[valName] = valType

    return [inputList,outputList]


bits = int(raw_input("How many bits per clock: "))
numHWModules = int(raw_input("How Many Modules: "))

HWList = []

print("Input .scala files to be connected in specefied order")
for i in range(numHWModules):

    name = raw_input("HW Module "+str(i+1)+": ")
    numInst = int(raw_input("How many instances: "))
    inOut = inputsOutputs(srcDirectory + name +".scala")
    inputs = inOut[0]
    outputs = inOut[1]
    HWList.append(Module(name,inputs,outputs,numInst))

for elem in HWList:
    print(elem.getName())

    print("Instances: "+str(elem.getNumInstances()))
    print("Inputs: ")
    for k,v in elem.inputTypes.items():
        print(k,v)
    print("Outputs: ")
    for k,v in elem.outputTypes.items():
        print(k,v)
    print "Total number of inputs: " + str(elem.getNumInstances()*elem.getNumInputs())
    print "Total number of outputs: " + str(elem.getNumInstances()*elem.getNumOutputs())
    print("==============================================")
