
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

def storeTxt(fname):
    fhand = open(fname)
    text = []
    for line in fhand:
        text.append(line)
    return text

def parseTx(fname,HWList):
    fhand = open(fname)

    inputList = []
    for idx,line in enumerate(fhand):
        # if "IN" in line:
        #     s = line[line.find("->")+2:].rstrip()
        #     print(line)
        #     print(s)
        #     s = s.split(".")
        #     print(s)
        #     whichMod = s[0][3]
        #     whichInstances = s[1]
        #     whichInputs = s[3]
        #     print("Which module:" + whichMod)
        #     print("Which instances:"+whichInstances)
        #     print("Which Inputs: " + whichInputs)
        #
        #     hwMod = HWList[int(whichMod)]
        #     print(hwMod.getName())
        #     if len(whichInstances) == 1:
        #         print("this is a number")
        #     print("++++++++++++++++++++++++++++++++++")
        # if "OUT" in line:
        #     s = line[:line.find("->")]
        #     s = s.split(".")
        #     print(s)
        #     whichMod = s[0][3]
        #     whichInstances = s[1]
        #     whichInputs = s[3]
        #     print(whichMod)
        #     print(whichInstances)
        #     print(whichInputs)
        #
        #     hwMod = HWList[int(whichMod)]
        if 'IN' not in line:
            if 'OUT' not in line:
                s = line[:line.find("->")]
                s = s.split(".")
                print(s)
                s2 = line[line.find("->")+2:]
                print(s2)
                whichMod = s[0][3]
                whichInstances = s[1]
                whichInputs = s[3]
                print(whichMod)
                print(whichInstances)
                print(whichInputs)
                print("+++++++++++++++++++++++++++=")

def getInput(text):
    inp = []

    for line in text:
        if 'IN' in line:
            inp.append(line)
    return inp

def getOutput(text):
    out = []

    for line in text:
        if 'OUT' in line:
            out.append(line)
    return out

def getConns(text):
    conns = []

    for line in text:
        if ('IN' not in line):
            if ('OUT' not in line):
                if('->' in line):

                    conns.append(line.rstrip())

    return conns

def readModules(text):
    li = []
    for line in text:
        if 'IN' in line:
            break
        s= line.rstrip()
        s = s.split(':')

        li.append(s)

    return li




def generateMainModule(HWList,structuretxt):
    fhand = open(srcDirectory+"MainModuleTest2.scala","w")

    ins = getInput(structuretxt)
    outs = getOutput(structuretxt)
    conns = getConns(structuretxt)
    #print(ins)
    #print(outs)
    #print(conns)


    fhand.write("""
package scala
import chisel3._
    """)

    fhand.write("""
class inputPacket extends Bundle{
    """)

    inList = []
    inCount =0
    for count,line in enumerate(ins):

        s = line[line.find("->")+2:].rstrip()
        s = s.split(".")
        whichMod = s[0][3]
        whichInstances = s[1]
        whichInputs = s[3]
        #print(whichInputs)

        hwBlock = HWList[int(whichMod)]

        if whichInstances == "all":
            if whichInputs == "all":

                for i in range(hwBlock.numInstances):
                    for j in range(hwBlock.getNumInputs()):
                        fhand.write("""
    val in"""+str(inCount)+""" = """+str(hwBlock.inputTypes.values()[j])
                    )
                        ins =s[0] +"(" + str(i) +")."+hwBlock.inputTypes.keys()[j]+ ":= io.input.in"+str(inCount)
                        inList.append(ins)
                        inCount +=1

            elif ":" in whichInputs:
                #print("True")
                num1 = int(whichInputs[1])
                num2 = int(whichInputs[3])
                totalInputs = (num2-num1)+1
                #print(num1,num2)
                #print("total Inputs:" + str(totalInputs))

                totalInsCount = 0
                for i in range(hwBlock.numInstances):
                    for j in range(hwBlock.getNumInputs()):
                        totalInsCount = totalInsCount+1
                        fhand.write("""
    val in"""+str(inCount)+""" = """+str(hwBlock.inputTypes.values()[j])
                                    )
                        ins = s[0]+"("+str(i)+")"+"."+hwBlock.inputTypes.keys()[j]+":=io.input.in"+str(inCount)
                        inCount+=1
                        inList.append(ins)

                        if totalInsCount>=totalInputs:

                            break




    fhand.write("""
    }""")


    fhand.write("""
class outputPacket extends Bundle{
        """)

    outList = []
    for count,line in enumerate(outs):
        s = line[:line.find("->")].rstrip()
        s = s.split(".")
        whichMod = s[0][3]
        whichInstances = s[1]
        whichInputs = s[3]

        hwBlock = HWList[int(whichMod)]
        outCount = 0
        if whichInstances == "all":
            if whichInputs == "all":

                for j in range(hwBlock.numInstances):
                    for k in range(hwBlock.getNumOutputs()):
                        fhand.write("""
    val out"""+str(outCount)+""" = """ + str(hwBlock.outputTypes.values()[k])
                  )
                        out = "io.output.out" + str(outCount) +":=" + s[0] +"(" + str(j) +")."+hwBlock.outputTypes.keys()[k]
                        outCount += 1
                        outList.append(out)

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
        valName = "mod" + str(idx)
        numInstances = elem.getNumInstances()

        fhand.write("""
    val """ + str(valName) + " = Array.fill("+str(numInstances)+")(Module(new " + str(name) +"()).io)")

    fhand.write("""
    """)

    for line in inList:
        fhand.write(line)
        fhand.write("""
    """)
    fhand.write("""
    """)
    for line in outList:
        fhand.write(line)
        fhand.write("""
    """)

    for line in conns:
        sOut = line[:line.find("->")]
        sOut = sOut.split(".")
        sIn = line[line.find("->")+2:]
        sIn = sIn.split(".")
        print(sOut),
        print("->"),
        print(sIn)

        whichModOut = sOut[0][3]
        whichInstancesOut = sOut[1]
        whichOutputs = sOut[3]
        print(whichModOut,whichInstancesOut,whichOutputs)

        whichModIn = sIn[0][3]
        whichInstancesIn = sIn[1]
        whichInputs = sIn[3]
        print(whichModIn,whichInstancesIn,whichInputs)

        HWBlockOutput= HWList[int(whichModOut)]
        HWBlockInput= HWList[int(whichModIn)]


        if whichInstancesOut == 'all' and len(whichInstancesIn) == 1:
            for i in range(int(HWBlockOutput.getNumInstances())):
                for j in range(int(HWBlockInput.getNumInputs())):
                    fhand.write(sIn[0]+"("+whichInstancesIn+")."+HWBlockInput.inputTypes.keys()[j]+":=" +sOut[0] + "("+str(i)+")."+HWBlockOutput.inputTypes.keys()[j])
                    fhand.write(
        """
    """)



    #print(conns)


#     for i in range(inputInstances):
#         for j in range(numInputs):
#             fhand.write("""
# mod0("""+str(i)+")."+inBlock.inputTypes.keys()[j]+":= io.input.in"""+str(i)+str(j))
#     fhand.write(
#     """
#     """)
#
#     for i in range(outputInstances):
#         for j in range(numOutputs):
#             fhand.write("""
# io.output.out"""+str(i)+str(j)+" := mod"+str(len(HWList)-1)+"("+str(i)+")."+outBlock.outputTypes.keys()[j])
#     fhand.write(
#     """
#     """)




# bits = int(raw_input("How many bits per clock: "))
text = storeTxt("struc2.txt")

modules = readModules(text)
numHWModules = len(modules)

#print(modules)
HWList = []

for i in modules:

    name = i[0]
    numInst = int(i[1])
    inOut = inputsOutputs(srcDirectory + name +".scala")
    inputs = inOut[0]
    outputs = inOut[1]

    HWList.append(Module(name,inputs,outputs,numInst))

#text = storeTxt("struc2.txt")
#print(text)
generateMainModule(HWList,text)
#print(getConns(text))
#print(readModules(text))
#parseTx("struc2.txt",HWList)
