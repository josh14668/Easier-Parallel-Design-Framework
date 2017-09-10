
package scala
import chisel3._
import chisel3.iotesters.{PeekPokeTester, Driver, ChiselFlatSpec,SteppedHWIOTester}


class VectorAdderTest(c:VectorAdder) extends PeekPokeTester(c){
  for(t <- 0 until 6){
  
      for(i<- 0 until c.n){
        poke(c.io.vec1 (i),rnd.nextInt(1<<c.w))
        poke(c.io.vec2 (i),rnd.nextInt(1<<c.w))

    }
    step(1)


    

  }
}

    
class VectorAdderTester extends ChiselFlatSpec {
  behavior of "VectorAdder"
  backends foreach {backend =>
    it should s"correctly add randomly generated vectors in $backend" in {
      Driver(() => new VectorAdder(w=3,n=2), backend)(c => new VectorAdderTest(c)) should be (true)
    }
  }
}

    