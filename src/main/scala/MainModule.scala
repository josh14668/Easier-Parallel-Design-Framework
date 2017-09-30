
package scala
import chisel3._
    
class inputPacket extends Bundle{
    
  val in00 = Vec(n,UInt(w.W)
  val in01 = Vec(n,UInt(w.W)
  val in10 = Vec(n,UInt(w.W)
  val in11 = Vec(n,UInt(w.W)
}
class outputPacket extends Bundle{
        
  val out00 = Vec(n,UInt(w.W)
}
    
class MainModule extends Module{
    val io = IO(new Bundle{
        val input = Input(new inputPacket)
        val output = Output(new outputPacket)
})
    val VectorAdders1 = Array.fill(2)(Module(new VectorAdder()).io)
    val VectorMuls1 = Array.fill(1)(Module(new VectorMul()).io)
    VectorAdders1(0).vec1 := io.input.in00
    VectorAdders1(0).vec2 := io.input.in01
    VectorAdders1(1).vec1 := io.input.in10
    VectorAdders1(1).vec2 := io.input.in11
    VectorMuls1(0).vec1 := VectorAdders1(0).out  
    VectorMuls1(0).vec2 := VectorAdders1(0).None
    VectorMuls1(1).vec1 := VectorAdders1(1).out  
    VectorMuls1(1).vec2 := VectorAdders1(1).None
    io.output.out00 := VectorMuls1(0).out  
    

    
    }
    