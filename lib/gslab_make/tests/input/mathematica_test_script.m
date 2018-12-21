(* ::Title:: *)
(*Mathematica Test Script*)

TestPlot = Plot[2 x + 1, {x, -1, 1}];
Export["output_plot.eps", Show[TestPlot]];
Print["mathematica test ended"]