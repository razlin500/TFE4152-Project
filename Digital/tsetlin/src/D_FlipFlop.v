//-----------------------------------------------------------------------------
//
// Title       : D_FlipFlop
// Design      : tsetlin
// Author      : NTNU
// Company     : NTNU
//
//-----------------------------------------------------------------------------
//
// File        : c:\My_Designs\TFE4152\tsetlin\src\D_FlipFlop.v
// Generated   : Sat Nov  1 12:21:45 2025
// From        : interface description file
// By          : Itf2Vhdl ver. 1.22
//
//-----------------------------------------------------------------------------
//
// Description : 
//
//-----------------------------------------------------------------------------
`timescale 1 ns / 1 ps

//{{ Section below this comment is automatically maintained
//   and may be overwritten
//{module {D_FlipFlop}}
module D_FlipFlop ( D ,Q ,clk );

output reg Q;
input D;
input clk;

//}} End of automatically maintained section
always @(posedge clk) 
begin												
 Q <= D; 
end 
// -- Enter your statements here -- //

endmodule
