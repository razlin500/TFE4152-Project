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
module registerNY2 (
    input  b2,
    input  b1,
    input  b0,
    input  alpha,
    input  beta,
	input reset,
    output b2o,
    output b1o,
    output b0o,
    output alphaOut,
    output betaOut,
    input  clk
);

//}} End of automatically maintained section


`include "flipflop2.v"
flipflop2 u2 (.D(b2), .clk(clk), .reset(reset), .Q(b2o));
flipflop2 u1 (.D(b1), .clk(clk), .reset(reset), .Q(b1o));
flipflop2 u0 (.D(b0), .clk(clk), .reset(reset), .Q(b0o));
flipflop2 alpha_Flip (.D(alpha), .clk(clk), .reset(reset), .Q(alphaOut));
flipflop2 beta_Flip  (.D(beta),  .clk(clk), .reset(reset), .Q(betaOut));
	
endmodule




// -- Enter your statements here -- //

