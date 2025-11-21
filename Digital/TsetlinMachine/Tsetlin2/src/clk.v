//-----------------------------------------------------------------------------
//
// Title       : CLK
// Design      : TsetlinMachine
// Author      : NTNU
// Company     : NTNU
//
//-----------------------------------------------------------------------------
//
// File        : M:\TFE4152 Prosjekt\TFE4152-Project\Digital\TsetlinMachine\TsetlinMachine\src\CLK.v
// Generated   : Thu Nov  6 09:36:12 2025
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
//{module {CLK}}
module CLK (output reg clk );

//}} End of automatically maintained section

initial clk = 0;

always begin
    #500000000 clk = ~clk;  // 1s clock period (in ns)
end


// -- Enter your statements here -- //

endmodule
