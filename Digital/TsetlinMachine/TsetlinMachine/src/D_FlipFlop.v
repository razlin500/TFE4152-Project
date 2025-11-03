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
module D_FlipFlop ( D ,Q , not_Q ,clk );

output Q;
wire Q;
input D;
wire D;
input clk;
wire clk;
output not_Q;
wire not_Q;

//}} End of automatically maintained section

not(not_D, D);

nand(t1, D, CLK);
nand(t2, not_D, CLK);

nand(Q, t1, t4);
nand(not_Q, Q, t2);

// -- Enter your statements here -- //

endmodule
