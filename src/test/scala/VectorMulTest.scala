
package scala
import chisel3._
import chisel3.iotesters.{PeekPokeTester, Driver, ChiselFlatSpec,SteppedHWIOTester}


class VectorMulTest(c:VectorMul) extends PeekPokeTester(c){
  for(t <- 0 until 6){
  
      for(i<- 0 until c.n){
        poke(c.io.vec1 (i),rnd.nextInt(1<<c.w))
        poke(c.io.vec2 (i),rnd.nextInt(1<<c.w))

    }
    step(1)


    

  }
}

    
class VectorMulTester extends ChiselFlatSpec {
  behavior of "VectorMul"
  backends foreach {backend =>
    it should s"correctly add randomly generated vectors in $backend" in {
      Driver(() => new VectorMul(w=3,n=2), backend)(c => new VectorMulTest(c)) should be (true)
    }
  }
}

    