
package scala
import chisel3._
import chisel3.iotesters.{PeekPokeTester, Driver, ChiselFlatSpec,SteppedHWIOTester}


class MainModuleTest(c:MainModule) extends PeekPokeTester(c){
  for(t <- 0 until 6){

      for(i<- 0 until 2){
        poke(c.io.in(i),rnd.nextInt(1<<3))


    }
    step(1)




  }
}


class MainModuleTester extends ChiselFlatSpec {
  behavior of "MainModule"
  backends foreach {backend =>
    it should s"correctly add randomly generated vectors in $backend" in {
      Driver(() => new MainModule, backend)(c => new MainModuleTest(c)) should be (true)
    }
  }
}
