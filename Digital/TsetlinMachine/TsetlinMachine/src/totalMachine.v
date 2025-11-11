//-----------------------------------------------------------------------------
//
// Title       : totalMachine
// Design      : TsetlinMachine
// Author      : Rasmus Nummelin
// Company     : NTNU
//
//-----------------------------------------------------------------------------
//
// File        : C:/Users/razli/ikke_onedrive/H2025/TFE4152/TFE4152-Project/Digital/TsetlinMachine/TsetlinMachine/src/totalMachine.v
// Generated   : Tue Nov  4 14:11:40 2025
// From        : Interface description file
// By          : ItfToHdl ver. 1.0
//
//-----------------------------------------------------------------------------
//
// Description : 
//
//-----------------------------------------------------------------------------

`timescale 1ps / 1ps

//{{ Section below this comment is automatically maintained
//    and may be overwritten
//{module {totalMachine}}

module totalMachine (output alphaz ,
	input betaz, 
	input clk);

//}} End of automatically maintained section

// Enter your statements here //

`include "combinatorics.v"
`include "register2.v"
//module combinatorics ( beta ,b2 ,b1 ,b0 ,b2o ,b1o ,b0o , alpha);
combinatorics c (.beta(beta), 
				.b2(bz2), 
				.b1(bz1), 
				.b0(bz0), 
				.b2o(bz2o), 
				.b1o(bz1o), 
				.b0o(bz0o), 
				.alpha(alpha));
				
/*module register (input b2 ,
	input b1 ,
	input b0 ,
	output b2o ,
	output b1o ,
	output b0o ,
	input clk );
*/

register r(.b2(bz2o), .b1(bz1o), .b0(bz0o), .b2o(bz2), .b1o(bz1), .b0o(bz0), .clk(clk));

endmodule
