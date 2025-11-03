//-----------------------------------------------------------------------------
//
// Title       : combinatorics
// Design      : tsetlin
// Author      : 
// Company     : 
//
//-----------------------------------------------------------------------------
//
// File        : c:\My_Designs\TFE4152\tsetlin\src\combinatorics.v
// Generated   : Thu Oct 30 10:59:53 2025
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
//{module {combinatorics}}
module combinatorics ( beta ,b2 ,b1 ,b0 ,b2o ,b1o ,b0o , alpha);

output b2o ;
wire b2o ;
output b1o ;
wire b1o ;
output b0o ;
wire b0o ;
output alpha;
wire alpha;

input beta ;
wire beta ;
input b2 ;
wire b2 ;
input b1 ;
wire b1 ;
input b0 ;
wire b0 ;


//}} End of automatically maintained section

// -- Enter your statements here -- //

not(notb1, b1);
and(t1, b2, notb1, beta);
and(t2, b2, notb1, b0);
not(notb2, b2);
and(t3, notb2, b1, b0, beta);  
and(b2o, t1, t2, t3);

not(notbeta, beta);
and(u1, notb2, b1, notbeta);
and(u2, notb2, b0, notbeta);
not(notb0, b0);
and(u3, b2, notb1, notb0, notbeta);
and(b2o, u1, u2, u3);

and(v1, notb2, notb0, beta);
and(v2, notb2, notb0, notbeta);
and(v3, b2, notb1, notb0);
and(b0o, v1, v2, t1, v3);

and(w1, notb2, b1, notb0, notbeta);
and(w2, b2, notb1);
and(alpha, w1, t3 ,w2);

endmodule
