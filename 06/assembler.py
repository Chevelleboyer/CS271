import os, sys
compValues = {'0':'0101010', '1':'0111111', '-1':'0111010', 'D':'0001100', 'A':'0110000', '!D':'0001101', '!A':'0110001', '-D':'0001111', '-A':'0110011', 'D+1':'0011111', 'A+1':'0110111', 'D-1':'0001110', 'A-1':'0110010', 'D+A':'0000010', 'D-A':'0010011', 'A-D':'0000111', 'D&A':'0000000', 'D|A':'0010101', 'M':'1110000', '!M':'1110001', '-M':'1110011', 'M+1':'1110111', 'M-1':'1110010', 'D+M':'1000010', 'D-M':'1010011', 'M-D':'1000111', 'D&M':'1000000', 'D|M':'1010101'}
destValues = {'null':'000', 'M':'001', 'D':'010', 'MD':'011', 'A':'100', 'AM':'101', 'AD':'110', 'AMD':'111'}
jumpValues = {'null':'000', 'JGT':'001', 'JEQ':'010', 'JGE':'011', 'JLT':'100', 'JNE':'101', 'JLE':'110', 'JMP':'111'}
symbolTable = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4, "SCREEN": 16384, "KBD": 24576}
variableMemory = 16
for i in range(0,16):
  symbol = "R" + str(i)
  symbolTable[symbol] = i

def parse(line):
		line = line.strip()
		line = line.replace(" ", "")
		if "//" in line:
			line = line.split("//")
			line = line[0]
			#return line
		return line

def allocateMemory(variable):
	global variableMemory
	symbolTable[variable] = variableMemory
	variableMemory += 1
	return symbolTable[variable]

def addNull(instruction):
	if ";" not in instruction:
		instruction = instruction + ";null"
	if "=" not in instruction:
		instruction = "null=" + instruction
	return instruction

def convertToBinary(instruction):
	if instruction[0] == "@":
		if instruction[1].isalpha():
			symbolValue = symbolTable.get(instruction[1:], "DNE")
			if symbolValue == "DNE":
				symbolValue = allocateMemory(instruction[1:])
				binaryInstruction = bin(int(symbolValue))[2:].zfill(16)
			binaryInstruction = bin(int(symbolValue))[2:].zfill(16)
		else:
			binaryInstruction = bin(int(instruction[1:]))[2:].zfill(16)
		return binaryInstruction
	elif "@" not in instruction:
		instruction = addNull(instruction)
		instruction = instruction.split("=")
		destVal = destValues.get(instruction[0])
		jcInstruction = instruction[1].split(";")
		jmpVal = jumpValues.get(jcInstruction[1])
		compVal = compValues.get(jcInstruction[0])
		return "111" + compVal + destVal + jmpVal

def firstStage():
	assemblyFile = open(sys.argv[1] + ".asm")
	tempFile = open(sys.argv[1] + ".tmp", "w")
	assemblylines = assemblyFile.readlines()
	assemblyFile.close()

	romAddress = 0

	for line in assemblylines:
		parsedLine = parse(line)
		line = line.replace("\n", "")
		if parsedLine != "":
			if parsedLine[0] == "(":
				symbol = parsedLine[1:-1]
				symbolTable[symbol] = romAddress
				parsedLine = ""
			else:
				romAddress += 1
				tempFile.write(parsedLine + "\n")
	tempFile.close()

def assembler():
	tempFile = open(sys.argv[1] + ".tmp")
	tempLines = tempFile.readlines()
	tempFile.close()
	hackFile = open(sys.argv[1] + ".hack", "w")

	for line in tempLines:
		line = line.replace("\n", "")
		binaryInstruction = convertToBinary(line)
		hackFile.write(binaryInstruction + "\n")

	hackFile.close()
	os.remove(sys.argv[1] + ".tmp")

firstStage()
assembler()














