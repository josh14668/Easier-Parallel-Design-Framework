from readModule import *



def poke_tester(inList):
    inputs = []
    for value in inList.viewkeys():
        print value
        inputs.append(value)

    return"""
      for(i<- 0 until 20){
        poke(c.io."""+inputs[0]+""",rnd.nextInt(1<<2))
        poke(c.io."""+inputs[1]+""",rnd.nextInt(1<<2))
        step(1)
    }



    """

def generate_flat_spec(module):
    return """
class """ + module+"Tester" +""" extends ChiselFlatSpec {
  behavior of """+"\""+module+"\"""""
  backends foreach {backend =>
    it should s"correctly add randomly generated vectors in $backend" in {
      Driver(() => new """+ module+ """, backend)(c => new """ + module+"""Tests(c)) should be (true)
    }
  }
}

    """



readLine = read_Scala(srcDirectory + "FSM" + '.scala')
ioList  = read_inputs_outputs(srcDirectory + "FSM" + '.scala')

for lin in ioList:
    print lin

inList = ioList[0]
outList = ioList[1]

for inp in inList:
    print inp,inList[inp]

for out in outList:
    print out,outList[out]

fhand = open(tstDirectory+"FSMTest"+".scala","w")
fhand.write(tstHeader)

fhand.write("""
class FSMTests(c: FSM) extends PeekPokeTester(c) {
""")

fhand.write(poke_tester(inList))

fhand.write("}")

fhand.write(generate_flat_spec("FSM"))
