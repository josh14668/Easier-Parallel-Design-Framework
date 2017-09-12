
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
  val in50 = Vec(n,UInt(w.W)
  val in51 = Vec(n,UInt(w.W)
  val in60 = Vec(n,UInt(w.W)
  val in61 = Vec(n,UInt(w.W)
  val in70 = Vec(n,UInt(w.W)
  val in71 = Vec(n,UInt(w.W)
}
class outputPacket extends Bundle{
        
  val out00 = Bool()
  val out10 = Bool()
  val out20 = Bool()
  val out30 = Bool()
  val out40 = Bool()
  val out50 = Bool()
  val out60 = Bool()
  val out70 = Bool()
}
    
class MainModule extends Module{
    val io = IO(new Bundle{
        val input = Input(new inputPacket)
        val output = Output(new outputPacket)
})
    val VectorAdders1 = Array.fill(8)(Module(new VectorAdder()).io)
    val VectorMuls1 = Array.fill(8)(Module(new VectorMul()).io)
    val FSMs1 = Array.fill(8)(Module(new FSM()).io)
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
    VectorAdders1(5).vec1 := io.input.in50
    VectorAdders1(5).vec2 := io.input.in51
    VectorAdders1(6).vec1 := io.input.in60
    VectorAdders1(6).vec2 := io.input.in61
    VectorAdders1(7).vec1 := io.input.in70
    VectorAdders1(7).vec2 := io.input.in71
    VectorMul1.vec1  := VectorAdder1.out  
    VectorMul1.vec2  := VectorAdder1.None
    FSM1.nickel  := VectorMul1.out  
    FSM1.dime    := VectorMul1.None
    io.output.out00 := FSMs1(0).valid  
    io.output.out10 := FSMs1(1).valid  
    io.output.out20 := FSMs1(2).valid  
    io.output.out30 := FSMs1(3).valid  
    io.output.out40 := FSMs1(4).valid  
    io.output.out50 := FSMs1(5).valid  
    io.output.out60 := FSMs1(6).valid  
    io.output.out70 := FSMs1(7).valid  
    

    
    }
    