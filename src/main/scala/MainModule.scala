
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
  val in40 = Vec(n,UInt(w.W)
  val in41 = Vec(n,UInt(w.W)
}
class outputPacket extends Bundle{
        
  val out00 = Vec(n,UInt(w.W)
  val out10 = Vec(n,UInt(w.W)
  val out20 = Vec(n,UInt(w.W)
  val out30 = Vec(n,UInt(w.W)
  val out40 = Vec(n,UInt(w.W)
}
    
class MainModule extends Module{
    val io = IO(new Bundle{
        val input = Input(new inputPacket)
        val output = Output(new outputPacket)
})
    val VectorAdders1 = Array.fill(5)(Module(new VectorAdder()).io)
    val VectorMuls1 = Array.fill(5)(Module(new VectorMul()).io)
    VectorAdders1(0).vec1 := io.input.in00
    VectorAdders1(0).vec2 := io.input.in01
    VectorAdders1(1).vec1 := io.input.in10
    VectorAdders1(1).vec2 := io.input.in11
    VectorAdders1(2).vec1 := io.input.in20
    VectorAdders1(2).vec2 := io.input.in21
    VectorAdders1(3).vec1 := io.input.in30
    VectorAdders1(3).vec2 := io.input.in31
    VectorAdders1(4).vec1 := io.input.in40
    VectorAdders1(4).vec2 := io.input.in41
    VectorMuls1(0).vec1 := VectorAdders1(0).out  
    VectorMuls1(0).vec2 := VectorAdders1(0).None
    VectorMuls1(1).vec1 := VectorAdders1(1).out  
    VectorMuls1(1).vec2 := VectorAdders1(1).None
    VectorMuls1(2).vec1 := VectorAdders1(2).out  
    VectorMuls1(2).vec2 := VectorAdders1(2).None
    VectorMuls1(3).vec1 := VectorAdders1(3).out  
    VectorMuls1(3).vec2 := VectorAdders1(3).None
    VectorMuls1(4).vec1 := VectorAdders1(4).out  
    VectorMuls1(4).vec2 := VectorAdders1(4).None
    io.output.out00 := VectorMuls1(0).out  
    io.output.out10 := VectorMuls1(1).out  
    io.output.out20 := VectorMuls1(2).out  
    io.output.out30 := VectorMuls1(3).out  
    io.output.out40 := VectorMuls1(4).out  
    

    
    }
    