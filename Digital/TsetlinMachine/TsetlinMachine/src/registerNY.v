//-----------------------------------------------------------------------------
//
// Title       : registerNY
// Design      : tsetlin
// Author      : 
// Company     : 
//
//-----------------------------------------------------------------------------
//
// File        : c:\My_Designs\TFE4152\tsetlin\src\register.v
// Generated   : Thu Oct 30 11:03:13 2025
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
//{module {registerNY}}
module registerNY2 (input b2 ,
	input b1 ,
	input b0 ,
	input alpha,
	input beta,
	output b2o ,
	output b1o ,
	output b0o ,
	output alphaOut,
	output betaOut,
	input clk );

//}} End of automatically maintained section

`include "D_FlipFlop.v"
	D_FlipFlop u2 (.D(b2), 
	.clk(clk), 
	.Q(b2o));
	D_FlipFlop u1 (.D(b1), 
	.clk(clk), 
	.Q(b1o));
	D_FlipFlop u0 (.D(b0), 
	.clk(clk), 
	.Q(b0o));
	D_FlipFlop alpha_Flip (.D(alpha), 
	.clk(clk),
	.Q(alphaOut));	
	D_FlipFlop beta_Flip (.D(beta), 
	.clk(clk),
	.Q(betaOut));
	
endmodule




// -- Enter your statements here -- //

