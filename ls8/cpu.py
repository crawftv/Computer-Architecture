"""CPU functionality."""

import sys

filename = sys.argv[1]


class CPU:
    """Main CPU class."""

    def __init__(self, filename):
        """Construct a new CPU."""
        self.ram = [None] * 256
        self.register = [None] * 7 + [0xf4]
        self.instruction_map = {
            0b0001: "HLT",
            0b0111: "PRN",
            0b0010: "LDI",
            0b0000: "NOOP",
            0b0110: "POP",
            0b0101: "PUSH"
        }
        self.alu_map = {
            0b0010: "MULT"
        }
        self.filename = filename

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        with open(self.filename) as f:
            for line in f:
                try:
                    l = line.split("#")[0].strip()
                    b = bin(int(l, base=2))
                except ValueError:
                    continue
                self.ram_write(address, b)
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def _num_operands(self, binary):
        operands = 0b1100000 & binary
        operands = operands >> 6
        return operands

    def _alu_operand(self, binary):
        binary = int(binary, base=2)
        alu = 0b00100000 & binary
        alu = alu >> 5
        return alu

    def _set_pc(self, binary):
        pc = 0b0001000 & binary
        pc = pc >> 4
        return pc

    def _instruction_identifier(self, binary):
        ii = 0b00001111 & binary
        return ii

    def run(self):
        """Run the CPU."""
        self.load()
        program_counter = 0x00
        ii = None
        while ii != "HLT":
            instruction = self.ram[program_counter]
            ii = int(instruction, 2)
            ii = self._instruction_identifier(ii)
            if self._alu_operand(instruction):
                ii = self.alu_map[ii]
                if ii == "MULT":
                    reg_a = int(self.register[0], base=2)
                    reg_b = int(self.register[1], base=2)
                    self.register[0] = bin(reg_a*reg_b)
                    program_counter += 2
            else:
                ii = self.instruction_map[ii]
                if ii == "LDI":
                    # import pdb
                    # pdb.set_trace()
                    register = int(self.ram[program_counter+1], base=2)
                    immediate = self.ram[program_counter+2]

                    self.register[register] = immediate
                    program_counter += 2

                elif ii == "PRN":
                    reg_num = self.ram_read(program_counter+1)
                    register = self.register[int(reg_num, base=2)]

                    print(int(register, base=2))

                    program_counter += 1
                elif ii == "PUSH":
                    self.register[-1] += -1
                    reg_num = self.ram_read(program_counter+1)
                    self.ram_write(
                        self.register[-1],
                        self.register[int(reg_num, base=2)]
                    )

                    program_counter += 1
                elif ii == "POP":

                    reg_num = int(self.ram_read(program_counter+1), base=2)
                    stack_pointer = self.register[-1]

                    self.register[reg_num] = self.ram[stack_pointer]

                    self.register[-1] += 1
                    program_counter += 1

            program_counter += 1

        #    def trace(self):
    #        """
    #        Handy function to print out the CPU state. You might want to call this
    #        from run() if you need help debugging.
    #        """
    #
    #        print(f"TRACE: %02X | %02X %02X %02X |" % (
    #            self.pc,
    #            #self.fl,
    #            #self.ie,
    #            self.ram_read(self.pc),
    #            self.ram_read(self.pc + 1),
    #            self.ram_read(self.pc + 2)
    #            ),
    #            end='')
    #
    #        for i in range(8):
    #            print(" %02X" % self.reg[i], end='')
    #
    #        print()
