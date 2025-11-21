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
module D_FlipFlop (
    input  D,
    input  clk,
    output reg Q
);
    initial Q = 0;
    always @(posedge clk)
        Q <= D;
endmodule
