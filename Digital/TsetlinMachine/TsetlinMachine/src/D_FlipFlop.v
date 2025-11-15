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
//Comment out when using as module
//`timescale 1 ns / 1 ps

//{{ Section below this comment is automatically maintained
//   and may be overwritten
//{module {D_FlipFlop}}
module D_FlipFlop (input D , 
	input clk, 
	output Q);


//}} End of automatically maintained section

not(not_D, D);
not(not_clk, clk);

nand(t1, D, not_clk);
nand(t2, not_D, not_clk);

nand(t3, t1, t4);
nand(t4, t3, t2);

not(not_t3, t3);

nand(t5, t3, clk);
nand(t6, not_t3, clk);

nand(Q, t5, t8);
nand(t8, t6, Q);

// -- Enter your statements here -- //

endmodule
