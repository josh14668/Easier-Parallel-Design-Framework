
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



def generateMainModule(HWList):
    fhand = open(srcDirectory+"MainModuleTestDontChangeMain.scala","w")

    inBlock = HWList[0]
    outBlock = HWList[len(HWList)-1]

    inputTypes = inBlock.inputTypes
    outputTypes = outBlock.outputTypes

    numInputs = len(inputTypes)
    inputInstances = inBlock.numInstances

    numOutputs = len(outputTypes)
    outputInstances = outBlock.numInstances

    print(inputInstances)
    print(numInputs)

    fhand.write("""
package scala
import chisel3._
    """)

    fhand.write("""
class inputPacket extends Bundle{
    """)

    for i in range(inputInstances):
        for j in range(numInputs):
            fhand.write("""
  val in"""+str(i)+str(j)+""" = """+str(inputTypes.values()[j])
        )
    fhand.write("""
}""")


    fhand.write("""
class outputPacket extends Bundle{
        """)
    for j in range(outputInstances):
        for k in range(numOutputs):
            fhand.write("""
  val out"""+str(j)+str(k)+""" = """ + str(outputTypes.values()[k])
      )

    fhand.write("""
}
    """)


    fhand.write("""
class MainModule extends Module{
    val io = IO(new Bundle{
        val input = Input(new inputPacket)
        val output = Output(new outputPacket)
})
    """)



    for idx,elem in enumerate(HWList):
        name = elem.getName()
        print(name)
        valName = "mod" + str(idx)
        numInstances = elem.getNumInstances()

        fhand.write("""
val """ + str(valName) + " = Array.fill("+str(numInstances)+")(Module(new " + str(name) +"()).io)")


    for i in range(inputInstances):
        for j in range(numInputs):
            fhand.write("""
mod0("""+str(i)+")."+inBlock.inputTypes.keys()[j]+":= io.input.in"""+str(i)+str(j))
    fhand.write(
    """
    """)

    for i in range(outputInstances):
        for j in range(numOutputs):
            fhand.write("""
io.output.out"""+str(i)+str(j)+" := mod"+str(len(HWList)-1)+"("+str(i)+")."+outBlock.outputTypes.keys()[j])
    fhand.write(
    """
    """)






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

generateMainModule(HWList)

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
