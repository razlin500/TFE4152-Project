//-----------------------------------------------------------------------------
//
// Title       : flipflop2
// Design      : TsetlinMachine
// Author      : NTNU
// Company     : NTNU
//
//-----------------------------------------------------------------------------
//
// File        : m:\TFE4152 Prosjekt\TFE4152-Project\Digital\TsetlinMachine\TsetlinMachine\src\flipflop2.v
// Generated   : Thu Nov 13 09:05:33 2025
// From        : interface description file
// By          : Itf2Vhdl ver. 1.22
//
//-----------------------------------------------------------------------------
//
// Description : 
//
//-----------------------------------------------------------------------------
// `timescale 1 ns / 1 ps

//{{ Section below this comment is automatically maintained
//   and may be overwritten
//{module {flipflop2}}
module flipflop2 (
    input  D,
    input  clk,
    input  reset,   // Active-high asynchronous reset
    output Q
);

    wire not_D, not_clk, not_reset;
    wire t1, t2, t3, t4, not_t3, t5, t6, t8;
    wire Q_int;

    // Basic inversions
    not (not_D, D);
    not (not_clk, clk);
    not (not_reset, reset);

    // Master latch (gated by not_clk)
    nand (t1, D, not_clk);
    nand (t2, not_D, not_clk);
    nand (t3, t1, t4);
    nand (t4, t3, t2);
    not  (not_t3, t3);

    // Slave latch (gated by clk)
    nand (t5, t3, clk);
    nand (t6, not_t3, clk);

    // Add reset into the feedback latch
    nand (Q_int, t5, t8, not_reset);  // If reset=1, Q_int forced low
    nand (t8, t6, Q_int);
endmodule

