
package scala
import chisel3._
    
class inputPacket extends Bundle{
    
    val in00 = Vec(n,UInt(w.W)
    val in01 = Vec(n,UInt(w.W)
    val in10 = Vec(n,UInt(w.W)
    val in11 = Vec(n,UInt(w.W)
    }
class outputPacket extends Bundle{
        
    val out00 = Vec(n,UInt((w+w)
}
    
class MainModule extends Module{
    val io = IO(new Bundle{
        val input = Input(new inputPacket)
        val output = Output(new outputPacket)
})
    
    val mod0 = Array.fill(2)(Module(new VectorAdder()).io)
    val mod1 = Array.fill(1)(Module(new VectorMul()).io)
    mod0(0).vec1 := io.input.in00
    mod0(0).vec2 := io.input.in01
    mod0(1).vec1 := io.input.in10
    mod0(1).vec2 := io.input.in11
    
    io.output.out00:=mod1(0).out  
    