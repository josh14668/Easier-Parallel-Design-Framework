
tstHeader = """
package scala
import chisel3._
import chisel3.iotesters.{PeekPokeTester, Driver, ChiselFlatSpec,SteppedHWIOTester}
"""


srcDirectory = "src/main/scala/"

tstDirectory = "src/test/scala/"




def poke_tester(inList):
    inputs = []
    for value in inList.viewkeys():
        inputs.append(value)

    return"""
      for(i<- 0 until c.n){
        poke(c.io."""+inputs[0]+"""(i),rnd.nextInt(1<<c.w))
        poke(c.io."""+inputs[1]+"""(i),rnd.nextInt(1<<c.w))

    }
    step(1)


    """

def generate_test_class(module,testitr,inputList):
    st= poke_tester(inputList)
    return"""

class """ +module+"""Test(c:"""+module+""") extends PeekPokeTester(c){
  for(t <- 0 until """+str(testitr)+"""){
  """+st+"""

  }
}

    """



def generate_flat_spec(module,w,n):
    return """
class """ + module+"Tester" +""" extends ChiselFlatSpec {
  behavior of """+"\""+module+"\"""""
  backends foreach {backend =>
    it should s"correctly add randomly generated vectors in $backend" in {
      Driver(() => new """+ module+ """(w="""+str(w)+""",n="""+str(n)+"""), backend)(c => new """ + module+"""Test(c)) should be (true)
    }
  }
}

    """




#return a list of input and output dictionary
def read_inputs_outputs(directory):
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

def print_module_name(line):
    return line[line.find('s')+3:line.find('(')]

def print_module_params(line):
    return line[line.find('('):line.find(')')+1]


def read_Scala(directory):
    try:
        fhand = open(directory)

        for line in fhand:
            if line.startswith('class'):
                module = line

        return [print_module_name(module),print_module_params(module)]
    except IOError:
        return 1



def write_Scala(directory,fileName,inputList,numInputs,inputRate):

    fhand = open(directory+fileName+"Test"+".scala","w")
    fhand.write(tstHeader)
    fhand.write(generate_test_class(fileName,6,inputList))
    fhand.write(generate_flat_spec(fileName,inputRate,numInputs))



def connect_modules(directory,inputWidth,numberInputs,modules,OutputName):
    fhand = open(directory+"MainModule.scala","w")

    fhand.write("""
package scala
import chisel3._
    """)


    fhand.write("""
class MainModule extends Module{
    val io = IO(new Bundle{
        val in = Input(Vec(n="""+str(numberInputs)+""",UInt("""+str(inputWidth)+""".W)))
        val out = Output(Vec(n="""+str(numberInputs)+""",UInt("""+str(inputWidth+inputWidth)+""".W)))
        })
    """)
    count = 0
    for key in modules.keys():
        fhand.write("""
    val """+key+""" = Module(new """+key+"""(w="""+str(inputWidth)+""",n="""+str(numberInputs)+""")).io
    """)

        inList = modules[key][0]
        outList = modules[key][1]
        print key
        count1 = 0
        for elem in inList.keys():
            if count ==0 and count1 == 0:

                fhand.write(key+"."+elem+":=io.in")
                fhand.write("""
    """)
            elif count1 ==1:
                fhand.write(key+"."+elem+":= Vec.fill("+str(numberInputs)+"){1.U("+str(inputWidth)+".W)}")
                fhand.write("""
    """)
            elif count == 1 :
                fhand.write(key+"."+elem+":=VectorMul.out")
                fhand.write("""
    """)
            count1=count1+1
        print elem
        count =count+1
    fhand.write("""
    """)
    fhand.write("io.out:="+OutputName)
    fhand.write("""
    """)
    fhand.write("}")


    #
    #     for elema,elemb in zip(inList.keys(),outList.keys()):
    #         fhand.write(key+"."+elema+":=")
    #         fhand.write("""
    # """)
    #         fhand.write(key+"."+elemb+":=")
    #         print elema
    #         print elemb
        #print inList
        #print outList
