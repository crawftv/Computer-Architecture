"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram =[]
        self.register = [None]*8
        self.instruction_map ={
                0b0001:"HLT",
                0b0010:"LDI",
                }

    def load(self, f):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:


        with open(filename) as f:
            for line in f:
                 try:
                     l = line.split("#")
                     b = bin(l)
                 except ValueError:
                     continue
                self.ram_write(address,b)
                addres+=1
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self,address):
        return self.ram[address])
    def ram_write(self,address,value):
        self.ram[address] = value
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

    def _num_operands(binary):
        operands = 0b1100000 & binary
        operands = operands >>6
        return operands
    def _alu_operand(binary):
        alu = 0b0010000 & binary
        alu = alu>>5
        return alu
    def _set_pc(binary):
        pc = 0b0001000 & binary
        pc = pc >>4
        return pc
    def _instruction_identifier(binary):
        ii = 0b00001111 & binary
        
    def run(self):
        """Run the CPU."""
        self.load()
        print(self.ram)
        instruction_register = 0
        instruction = self.ram[instruction_register]
        if instruction == "HALT":
            pass
        else if instruction = "LDI":
            break



            
