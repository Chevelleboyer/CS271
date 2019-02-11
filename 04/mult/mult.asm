// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

	@i
	M=1
	@0
	D=A
	@R2
	M=D
(LOOP)
	@i     //a=i
	D=M    //d=i
	@R1    //a=R1
	D=D-M  //d=i-(whatever is at R1)
	@END
	D;JGT  //end if i-R1 is > 0
	@R0     //a=R0
	D=M     //d=R0
	@R2     //a=R2
	M=D+M     //stores D+M value in R2
	@i
	M=M+1    //stores i+1 in i (i is incremented)
	@LOOP
	0;JMP
(END)
	@END
	0;JMP