import os
import itertools
from time import sleep
import sys


srcDirectory = "src/main/scala/"

tstDirectory = "src/test/scala/"



class MainModule(object):

    def __init__(self,inputTypes,outputTypes):
        self.inputTypes = inputTypes
        self.outputTypes = outputTypes
        self.head = None
        self.tail = None

    def getInputTypes(self):
        return self.inputTypes

    def getOuputTypes(self):
        return self.outputTypes

    def getHead(self):
        return self.head

    def getTail(self):
        return self.tail

    def setHead(self,newHead):
        self.head = newHead

    def setTail(self,newTail):
        self.tail  = newTail

    def getInternalModules(self):
        currentMod = self.head
        while(currentMod !=None):
            print(currentMod.getName(),currentMod.getNumInstances())
            currentMod = currentMod.getNext()

    def updateInstances(self, num):
        current = self.getHead()
        while current:
            current.setNumInstances(num)
            current = current.getNext()



class SubModule(MainModule):


    def __init__(self,name,inputTypes,outputTypes,numInstances,outPerCycle):
        self.name = name
        self.inputTypes = inputTypes
        self.outputTypes = outputTypes
        self.next = None
        self.numInstances = numInstances
        self.outPerCycle = outPerCycle

    def getNext(self):
        return self.next

    def setNext(self, newNext):
        self.next = newNext

    def getName(self):
        return self.name

    def append(self,newMod):
        currentMod = self
        while(currentMod.getNext()):
            currentMod = currentMod.getNext()
        currentMod.setNext(newMod)

    def getNumInputs(self):
        return len(inputTypes)


    def getNumOutputs(self):
        return len(outputTypes)

    def getNumInstances(self):
        return self.numInstances

    def setNumInstances(self,num):
        self.numInstances = num

def createModule(hwModule):
    hwModName = hwModule.getName()
    valName = hwModName + "1"

    return "val " + str(valName) + " = Module(new " + str(hwModName) +"()).io"

def createArray(hwModule):
    hwModName = hwModule.getName()
    valName = hwModName + "s1"
    numInstances = hwModule.getNumInstances()

    return "val " + str(valName) + " = Array.fill("+str(numInstances)+")(Module(new " + str(hwModName) +"()).io)"


def connectToNext(hwMod1):
    inputs = hwMod1.outputTypes
    outputs = hwMod2.inputTypes


    conArray = """
        for (i<-0 until n){
    """
    for outputElem,inputElem in itertools.izip_longest(hwMod1.getOuputTypes(),hwMod1.getNext().getInputTypes(),fillvalue='None'):
        print ('hello')




#Creates lists of the name of hardware modules in src main file
def listHWMods(directory):
    names = []
    for hwMod in os.listdir(directory):
        if '.scala' in hwMod:
            names.append(hwMod)
    return names

# Creates list of inputs and outputs of scala file
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

def checkParalleism(mainMod):
    current = mainMod.getHead()

    while current.getNext():
        hwMod1 = current
        hwMod2 = current.getNext()
        numOutputLen = len(hwMod1.getOuputTypes()) * hwMod1.getNumInstances()
        numInputLen = len(hwMod2.getInputTypes()) *  hwMod2.getNumInstances()
        if numOutputLen != numInputLen:
            print (hwMod1.getName() + " outputs don't connect to "+ hwMod2.getName() + " inputs")
        current = current.getNext()




def generateMainModule(mainMod):
    fhand = open(srcDirectory+"MainModule.scala","w")
    inputTypes = mainMod.getInputTypes()
    outputTypes = mainMod.getOuputTypes()

    numInputs = len(inputTypes)
    inputInstances = mainMod.getHead().getNumInstances()

    numOutputs = len(outputTypes)
    outputInstances = mainMod.getTail().getNumInstances()


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
  val in"""+str(i)+str(j)+""" = """+str(inputTypes[j])
        )
    fhand.write("""
}""")


    fhand.write("""
class outputPacket extends Bundle{
        """)
    for j in range(outputInstances):
        for k in range(numOutputs):
            fhand.write("""
  val out"""+str(j)+str(k)+""" = """ + str(outputTypes[k])
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
    current = mainMod.getHead()
    while current:

        fhand.write(
        createArray(current))
        fhand.write(
    """
    """)

        current = current.getNext()


    #for item in hwList.values():

    #    fhand.write(
    #    createModule(item))
    #    fhand.write("""
    #""")


    firstHWModule = mainMod.getHead()
    name1 = firstHWModule.getName()


    for i in range(inputInstances):
        for j in range(numInputs):
            fhand.write(name1+"s1("+str(i)+")."+firstHWModule.getInputTypes().keys()[j]+":= io.input.in"+str(i)+str(j))
            fhand.write("""
    """)

    checkParalleism(mainMod)

    currentElem = mainMod.getHead()
    while currentElem.getNext():
        for i in range(inputInstances):

            for outputElem,inputElem in             itertools.izip_longest(currentElem.getOuputTypes(),currentElem.getNext().getInputTypes(),fillvalue='None'):
                outName = currentElem.getName()
                inName = currentElem.getNext().getName()
            #print outputElem
            #print inputElem
                fhand.write(inName+"s1("+str(i)+")."+inputElem+ ":= " + outName+"s1("+str(i)+")."+outputElem)
                fhand.write(
    """
    """)
        currentElem = currentElem.getNext()


    lastHWModule = mainMod.getTail()
    name2 = lastHWModule.getName()



    for i in range(outputInstances):
        for j in range(numOutputs):
            fhand.write("io.output.out"+str(i)+str(j)+" := "+name2+"s1("+str(i)+")."+lastHWModule.getOuputTypes().keys()[j])
            fhand.write("""
    """)

    # for j in range(numOutputs):
    #     fhand.write("io.output.out"+str(j)+" := "+name2+"1."+lastHWModule.getOuputTypes().keys()[j])
    #     fhand.write("""
    # """)
    fhand.write("""

    """)
    fhand.write("""
    }
    """)




bits = int(raw_input("How many bits per clock: "))
numHWModules = int(raw_input("How Many Modules: "))

inputTypes = []
outputTypes = []
HWList = []
hwClassList = {}
head  = SubModule(None,None,None,None)

print("Input .scala files to be connected in specefied order")
for i in range(numHWModules):

    name = raw_input("HW Module "+str(i+1)+": ")
    outPerCycle = int(raw_input("Max output generated per cycle: "))
    numInst = int(raw_input("How many instances: "))
    HWList.append(name)
    inOut = inputsOutputs(srcDirectory + name +".scala")
    inputs = inOut[0]
    outputs = inOut[1]
    if i==0:
        head = SubModule(name,inputs,outputs,numInst,outPerCycle)
    else:
        head.append(SubModule(name,inputs,outputs,numInst))
    hwClassList[name] = SubModule(name,inputs,outputs,numInst)



tail = hwClassList[HWList[len(HWList)-1]]

#Inputs of 1st HW module to use as input of main module
inputTypes = hwClassList.values()[0].inputTypes.values()

#Outputs of last HW module to use and output of main
outputTypes = hwClassList.values()[len(hwClassList)-1].outputTypes.values()

mainMod = MainModule(inputTypes,outputTypes)

#mainMod.setHead(hwClassList[HWList[0]])
mainMod.setHead(head)
mainMod.setTail(tail)

if head.getNumInstances() != tail.getNumInstances():
    print("Input instances don't match output instances")
    ans = raw_input("Would you like to match instances y/n: ")
    if ans == 'y':
        inOut = raw_input("According to input or output instances in/out: ")
        if inOut == 'in':
            print("Updating instances to match input instances")

            tail.numInstances = head.numInstances
            mainMod.updateInstances(head.getNumInstances())
        elif inOut == 'out':
            print("Updating instances to match output instances")

            head.numInstances = tail.numInstances
            mainMod.updateInstances(tail.getNumInstances())

#TODO: Middle hw modules not checked if instances of input and output are the same


#print mainMod.getHead().name
#print mainMod.getTail().name


#for k,v in hwClassList.items():

#    print k
#    print v.inputTypes
#    print v.outputTypes




mainMod.getInternalModules()

generateMainModule(mainMod)


#genrateMainModule(inputTypes,outputTypes,hwClassList)
