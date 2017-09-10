
package scala
import chisel3._
import chisel3.iotesters.{PeekPokeTester, Driver, ChiselFlatSpec,SteppedHWIOTester}

class FSMTests(c: FSM) extends PeekPokeTester(c) {

      for(i<- 0 until 20){
        poke(c.io.nickel ,rnd.nextInt(1<<2))
        poke(c.io.dime   ,rnd.nextInt(1<<2))
        step(1)
    }



    }
class FSMTester extends ChiselFlatSpec {
  behavior of "FSM"
  backends foreach {backend =>
    it should s"correctly add randomly generated vectors in $backend" in {
      Driver(() => new FSM, backend)(c => new FSMTests(c)) should be (true)
    }
  }
}

    