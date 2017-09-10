package scala

import chisel3._

class VectorMul(val w: Int,val n: Int) extends Module{
  val io = IO(new Bundle{
    val vec1 =  Input(Vec(n,UInt(w.W)))
    val vec2 =  Input(Vec(n,UInt(w.W)))
    val out  =  Output(Vec(n,UInt((w+w).W)))
  })

  val muls = Array.fill(n)(Module(new Mul(n=w)).io)

  //val reg0_vec16 = Reg(Vec(Seq.fill(w){ UInt(16.W) }))
  //val reg1_vec16 = Reg(Vec(Seq.fill(w){ UInt() }))

  val quotient   = Wire(Vec(n, UInt(w.W)))





  for(i <- 0 until n) {
    muls(i).in0 := io.vec1(i)
    muls(i).in1 := io.vec2(i)
    quotient(i) := muls(i).out
  }

  io.out := quotient


}
