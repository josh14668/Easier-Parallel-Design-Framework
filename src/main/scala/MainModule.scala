
package scala
import chisel3._
    
class inputPacket extends Bundle{
    
  val in00 = Vec(n,UInt(w.W)
  val in01 = Vec(n,UInt(w.W)
  val in10 = Vec(n,UInt(w.W)
  val in11 = Vec(n,UInt(w.W)
  val in20 = Vec(n,UInt(w.W)
  val in21 = Vec(n,UInt(w.W)
  val in30 = Vec(n,UInt(w.W)
  val in31 = Vec(n,UInt(w.W)
}
class outputPacket extends Bundle{
        
  val out00 = Vec(n,UInt(w.W)
  val out10 = Vec(n,UInt(w.W)
  val out20 = Vec(n,UInt(w.W)
  val out30 = Vec(n,UInt(w.W)
}
    
class MainModule extends Module{
    val io = IO(new Bundle{
        val input = Input(new inputPacket)
        val output = Output(new outputPacket)
})
    val VectorAdders1 = Array.fill(4)(Module(new VectorAdder()).io)
    val VectorMuls1 = Array.fill(4)(Module(new VectorMul()).io)
    VectorAdder1.vec1 := io.input.in0
    VectorAdder1.vec2 := io.input.in1
    VectorMul1.vec1  := VectorAdder1.out  
    VectorMul1.vec2  := VectorAdder1.None
    io.output.out0 := VectorMul1.out  
    