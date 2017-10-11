
package scala
import chisel3._
    
class inputPacket extends Bundle{
    
    val in0 = Vec(n,UInt(w.W)
    val in1 = Vec(n,UInt(w.W)
    val in2 = Vec(n,UInt(w.W)
    val in3 = Vec(n,UInt(w.W)
    val in4 = Vec(n,UInt(w.W)
    }
class outputPacket extends Bundle{
        
    val out0 = Vec(n,UInt(w.W)
}
    
class MainModule extends Module{
    val io = IO(new Bundle{
        val input = Input(new inputPacket)
        val output = Output(new outputPacket)
})
    
    val mod0 = Array.fill(1)(Module(new VectorAdder()).io)
    val mod1 = Array.fill(2)(Module(new VectorAdder()).io)
    val mod2 = Array.fill(1)(Module(new VectorAdder()).io)
    mod1(0).vec1 :=io.input.in0
    mod1(0).vec2 :=io.input.in1
    mod1(1).vec1 :=io.input.in2
    mod0(0).vec1 := io.input.in3
    mod0(0).vec2 := io.input.in4
    
    io.output.out0:=mod2(0).out  
    mod1(1).vec1 :=mod0(0).vec1 
    mod1(1).vec2 :=mod0(0).vec2 
    