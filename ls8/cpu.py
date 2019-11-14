"""CPU functionality."""

import sys


LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0]*8 #these are like our variables... R0, R1,... R7
        self.ram = [0]*256 #or should we do 255?
        self.SP = 7
        self.reg[self.SP] = 0xf4 #initialize SP to empty stack 



    def load(self):
        """Load a program into memory."""

        

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8.... save value 8 in register 0
            
        #     0b00000000, #argument for R0
            
        #     0b00001000, #argument.... value of 8

        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        


        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        
        address = 0

        if len(sys.argv) != 2:
            print("usage: ls8.py filename")
            sys.exit(1)
        
        progname = sys.argv[1]


        with open(progname) as f:
            for line in f:
                line = line.split("#")[0]
                line = line.strip() #lose whitespace 

                if line == "":
                    continue

                val = int(line, 2) #binary so it's base 2

                self.ram[address] = val
                address += 1





    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    # ram_read() should accept the address to read and return the value stored there.
    def ram_read(self, memory_address):
        return self.ram[memory_address]

    # ram_write() should accept a value to write, and the address to write it to.
    def ram_write(self, memory_address, value):
        self.ram[memory_address] = value


    def run(self):
        """Run the CPU."""
        while self.ram_read(self.pc) != HLT:

            # instruction = memory[pc]
            instruction = self.ram_read(self.pc)

            # LDI: load "immediate", store a value in a register, or "set this register to this value".
            if instruction == LDI:
                # read the bytes at PC+1 and PC+2 from RAM into variables operand_a and operand_b
                operand_register = self.ram_read(self.pc + 1)
                operand_value = self.ram_read(self.pc + 2)

                # Set the value of a register to an integer.
                # register[reg_num] = value
		        # pc += 3

                self.reg[operand_register] = operand_value

                #3 byte instruction
                self.pc += 3


            # PRN: a pseudo-instruction that prints the numeric value stored in a register.
            elif instruction == PRN:
                operand_register = self.ram_read(self.pc + 1)

                print(self.reg[operand_register])

                #2 byte instruction so add 2
                self.pc += 2

            elif instruction == MUL:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

            elif instruction == PUSH:
                self.reg[self.SP] -= 1 # decrement sp 

                # need register number... push is a two byte instruction 
                reg_num = self.ram_read(self.pc + 1)
                
                # now need value so we can copy it into memory where the stack pointer is 
                reg_value = self.reg[reg_num]

                
                # copy register value into memory at the address SP
                self.ram[self.reg[self.SP]] = reg_value

                self.pc += 2 # 2 byte instruction
            
            elif instruction == POP:
                # get the value out of memory where the stack pointer is pointing
                val = self.ram[self.reg[self.SP]]

                reg_num = self.ram[self.pc + 1]

                self.reg[reg_num] = val  # copy val from memory at SP into register 

                self.reg[self.SP] += 1 #incremeent the SP

                self.pc += 2 # 2 byte instruction

