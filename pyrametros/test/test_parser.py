from ..parser import Line, parse_file
import os
import unittest

EXPECTED_TABLE = [{'MAJOR': '0', 'op_prop': 'shift', 'integer verilog': 'RD = RT << imm', 'FW': '0', 'IW': '1', 'syntax': 'rd,rs,imm', 'JUMP': '0', 'MW': '0', 'registers': 'xxxxxtttttdddddiiiii', 'opcode': 'sll', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': '0'},
 {'MAJOR': '0', 'op_prop': '', 'integer verilog': 'RD = $signed(RT) >>> imm', 'FW': '0', 'IW': '1', 'syntax': 'rd,rs,imm', 'JUMP': '0', 'MW': '0', 'registers': 'xxxxxtttttdddddiiiii', 'opcode': 'sra', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': '3'},
 {'MAJOR': '0', 'op_prop': '', 'integer verilog': 'New_PC = RS', 'FW': '0', 'IW': '0', 'syntax': 'rs', 'JUMP': '1', 'MW': '0', 'registers': 'sssssxxxxxxxxxxxxxxx', 'opcode': 'jr', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': '8'},
 {'MAJOR': '0', 'op_prop': '', 'integer verilog': 'RD = RS + RT', 'FW': '0', 'IW': '1', 'syntax': 'rd,rs,rt', 'JUMP': '0', 'MW': '0', 'registers': 'ssssstttttdddddxxxxx', 'opcode': 'addu', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': '33'},
 {'MAJOR': '0', 'op_prop': '', 'integer verilog': 'RD = RS - RT', 'FW': '0', 'IW': '1', 'syntax': 'rd,rs,rt', 'JUMP': '0', 'MW': '0', 'registers': 'ssssstttttdddddxxxxx', 'opcode': 'subu', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': '35'},
 {'MAJOR': '0', 'op_prop': '', 'integer verilog': 'RD = RS & RT', 'FW': '0', 'IW': '1', 'syntax': 'rd,rs,rt', 'JUMP': '0', 'MW': '0', 'registers': 'ssssstttttdddddxxxxx', 'opcode': 'and', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': '36'},
 {'MAJOR': '0', 'op_prop': '', 'integer verilog': 'RD = RS | RT', 'FW': '0', 'IW': '1', 'syntax': 'rd,rs,rt', 'JUMP': '0', 'MW': '0', 'registers': 'ssssstttttdddddxxxxx', 'opcode': 'or', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': '37'},
 {'MAJOR': '0', 'op_prop': '', 'integer verilog': 'RD = RS ^ RT', 'FW': '0', 'IW': '1', 'syntax': 'rd,rs,rt', 'JUMP': '0', 'MW': '0', 'registers': 'ssssstttttdddddxxxxx', 'opcode': 'xor', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': '38'},
 {'MAJOR': '0', 'op_prop': '', 'integer verilog': 'RD = ~(RS | RT)', 'FW': '0', 'IW': '1', 'syntax': 'rd,rs,rt', 'JUMP': '0', 'MW': '0', 'registers': 'ssssstttttdddddxxxxx', 'opcode': 'nor', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': '39'},
 {'MAJOR': '0', 'op_prop': '', 'integer verilog': 'RD = $signed(RS)<$signed(RT)', 'FW': '0', 'IW': '1', 'syntax': 'rd,rs,rt', 'JUMP': '0', 'MW': '0', 'registers': 'ssssstttttdddddxxxxx', 'opcode': 'slt', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': '42'},
 {'MAJOR': '0', 'op_prop': '', 'integer verilog': 'RD = $unsigned(RS)<$unsigned(RT)', 'FW': '0', 'IW': '1', 'syntax': 'rd,rs,rt', 'JUMP': '0', 'MW': '0', 'registers': 'ssssstttttdddddxxxxx', 'opcode': 'sltu', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': '43'},
 {'MAJOR': '2', 'op_prop': '', 'integer verilog': "New_PC={EX_PC[31:28],Imm26,2'd0}", 'FW': '0', 'IW': '0', 'syntax': 'Imm26', 'JUMP': '1', 'MW': '0', 'registers': 'iiiiiiiiiiiiiiiiiiii', 'opcode': 'j', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': 'iiiiii'},
 {'MAJOR': '3', 'op_prop': '', 'integer verilog': "New_PC={EX_PC[31:28],Imm26,2'd0}", 'FW': '0', 'IW': '0', 'syntax': 'Imm26', 'JUMP': '1', 'MW': '0', 'registers': 'iiiiiiiiiiiiiiiiiiii', 'opcode': 'jal', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': 'iiiiii'},
 {'MAJOR': '', 'op_prop': '', 'integer verilog': '$31 = PC+8', 'FW': '', 'IW': '', 'syntax': '', 'JUMP': '', 'MW': '', 'registers': '', 'opcode': '', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': ''},
 {'MAJOR': '4', 'op_prop': '', 'integer verilog': 'New_PC = (RS==RT) ? PC+Imm16+4', 'FW': '0', 'IW': '0', 'syntax': 'Imm16', 'JUMP': '1', 'MW': '0', 'registers': 'ssssstttttiiiiiiiiii', 'opcode': 'beq', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': 'iiiiii'},
 {'MAJOR': '5', 'op_prop': '', 'integer verilog': 'New_PC = (RS!=RT) ? PC+Imm16+4', 'FW': '0', 'IW': '0', 'syntax': 'Imm16', 'JUMP': '1', 'MW': '0', 'registers': 'ssssstttttiiiiiiiiii', 'opcode': 'bneq', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': 'iiiiii'},
 {'MAJOR': '9', 'op_prop': '', 'integer verilog': 'RT = RS + Imm16', 'FW': '0', 'IW': '1', 'syntax': 'rt,rs,Imm16', 'JUMP': '0', 'MW': '0', 'registers': 'ssssstttttiiiiiiiiii', 'opcode': 'addiu', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': 'iiiiii'},
 {'MAJOR': '10', 'op_prop': '', 'integer verilog': 'RT = ($signed(RS) < $signed(Imm16))', 'FW': '0', 'IW': '1', 'syntax': 'rt,rs,Imm16', 'JUMP': '0', 'MW': '0', 'registers': 'ssssstttttiiiiiiiiii', 'opcode': 'slti', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': 'iiiiii'},
 {'MAJOR': '11', 'op_prop': '', 'integer verilog': 'RT = ($unsigned(RS) < $unsigned(Imm16))', 'FW': '0', 'IW': '1', 'syntax': 'rt,rs,Imm16', 'JUMP': '0', 'MW': '0', 'registers': 'ssssstttttiiiiiiiiii', 'opcode': 'sltiu', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': 'iiiiii'},
 {'MAJOR': '12', 'op_prop': '', 'integer verilog': "RT = RS & {16'd0,Imm16}", 'FW': '0', 'IW': '1', 'syntax': 'rt,rs,Imm16', 'JUMP': '0', 'MW': '0', 'registers': 'ssssstttttiiiiiiiiii', 'opcode': 'andi', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': 'iiiiii'},
 {'MAJOR': '13', 'op_prop': '', 'integer verilog': "RT = RS | {16'd0,Imm16}", 'FW': '0', 'IW': '1', 'syntax': 'rt,rs,Imm16', 'JUMP': '0', 'MW': '0', 'registers': 'ssssstttttiiiiiiiiii', 'opcode': 'ori', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': 'iiiiii'},
 {'MAJOR': '15', 'op_prop': '', 'integer verilog': "RT = {Imm16,16'd0}", 'FW': '0', 'IW': '1', 'syntax': 'rt,Imm16', 'JUMP': '0', 'MW': '0', 'registers': 'xxxxxtttttiiiiiiiiii', 'opcode': 'lui', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': 'iiiiii'},
 {'MAJOR': '28', 'op_prop': '', 'integer verilog': 'RD = (RS * RT)', 'FW': '0', 'IW': '1', 'syntax': 'rd,rs,rt', 'JUMP': '0', 'MW': '0', 'registers': 'ssssstttttdddddxxxxx', 'opcode': 'mul', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': '2'},
 {'MAJOR': '28', 'op_prop': '', 'integer verilog': 'RD(Thread:RT) = RS', 'FW': '0', 'IW': '1', 'syntax': 'rd,rs,rt', 'JUMP': '0', 'MW': '0', 'registers': 'ssssstttttdddddxxxxx', 'opcode': 'tmove', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': '16'},
 {'MAJOR': '31', 'op_prop': '', 'integer verilog': 'Fork_Req = 1', 'FW': '0', 'IW': '1', 'syntax': 'rd,rs,rt', 'JUMP': '0', 'MW': '0', 'registers': 'ssssstttttdddddxxxxx', 'opcode': 'fork', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': '8'},
 {'MAJOR': '31', 'op_prop': '', 'integer verilog': 'Yield    = RS', 'FW': '0', 'IW': '0', 'syntax': 'rs', 'JUMP': '1', 'MW': '0', 'registers': 'sssssxxxxxxxxxxxxxxx', 'opcode': 'yield', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': '9'},
 {'MAJOR': '31', 'op_prop': '', 'integer verilog': 'RD = sign_ext8(RT)', 'FW': '0', 'IW': '1', 'syntax': 'rd,rt', 'JUMP': '0', 'MW': '0', 'registers': 'xxxxxtttttdddddxxxxx', 'opcode': 'sext', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': '32'},
 {'MAJOR': '31', 'op_prop': '', 'integer verilog': 'RD = sign_ext16(RT)', 'FW': '0', 'IW': '1', 'syntax': 'rd,rt', 'JUMP': '0', 'MW': '0', 'registers': 'xxxxxtttttdddddxxxxx', 'opcode': 'sext', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': '33'},
 {'MAJOR': '32', 'op_prop': '', 'integer verilog': 'RT = *$signed(RS)+$signed(Imm16)', 'FW': '0', 'IW': '1', 'syntax': 'rt,rs,Imm16', 'JUMP': '0', 'MW': '0', 'registers': 'ssssstttttiiiiiiiiii', 'opcode': 'lb', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': 'iiiiii'},
 {'MAJOR': '33', 'op_prop': '', 'integer verilog': 'RT = *$signed(RS)+$signed(Imm16)', 'FW': '0', 'IW': '1', 'syntax': 'rt,rs,Imm16', 'JUMP': '0', 'MW': '0', 'registers': 'ssssstttttiiiiiiiiii', 'opcode': 'lh', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': 'iiiiii'},
 {'MAJOR': '35', 'op_prop': '', 'integer verilog': 'RT = *$signed(RS)+$signed(Imm16)', 'FW': '0', 'IW': '1', 'syntax': 'rt,rs,Imm16', 'JUMP': '0', 'MW': '0', 'registers': 'ssssstttttiiiiiiiiii', 'opcode': 'lw', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': 'iiiiii'},
 {'MAJOR': '36', 'op_prop': '', 'integer verilog': 'RT = *$signed(RS)+$signed(Imm16)', 'FW': '0', 'IW': '1', 'syntax': 'rt,rs,Imm16', 'JUMP': '0', 'MW': '0', 'registers': 'ssssstttttiiiiiiiiii', 'opcode': 'lbu', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': 'iiiiii'},
 {'MAJOR': '37', 'op_prop': '', 'integer verilog': 'RT = *$signed(RS)+$signed(Imm16)', 'FW': '0', 'IW': '1', 'syntax': 'rt,rs,Imm16', 'JUMP': '0', 'MW': '0', 'registers': 'ssssstttttiiiiiiiiii', 'opcode': 'lhu', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': 'iiiiii'},
 {'MAJOR': '40', 'op_prop': '', 'integer verilog': '*$signed(RS)+$signed(Imm16) = RT[7:0]', 'FW': '0', 'IW': '0', 'syntax': 'rt,rs,Imm16', 'JUMP': '0', 'MW': '1', 'registers': 'ssssstttttiiiiiiiiii', 'opcode': 'sb', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': 'iiiiii'},
 {'MAJOR': '41', 'op_prop': '', 'integer verilog': '*$signed(RS)+$signed(Imm16) = RT[15:0]', 'FW': '0', 'IW': '0', 'syntax': 'rt,rs,Imm16', 'JUMP': '0', 'MW': '1', 'registers': 'ssssstttttiiiiiiiiii', 'opcode': 'sh', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': 'iiiiii'},
 {'MAJOR': '43', 'op_prop': '', 'integer verilog': '*$signed(RS)+$signed(Imm16) = RT[31:0]', 'FW': '0', 'IW': '0', 'syntax': 'rt,rs,Imm16', 'JUMP': '0', 'MW': '1', 'registers': 'ssssstttttiiiiiiiiii', 'opcode': 'sw', 'float verilog': '', 'argA': '', 'argB': '', 'argC': '', 'MINOR': 'iiiiii'}]

class TestParser(unittest.TestCase):
    def setUp(self):
        example_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "./static/")
        self.isa_rows = parse_file(os.path.join(example_dir, "testtable.txt"))
        self.org_rows = parse_file(os.path.join(example_dir, "testtable.org"))

    def test_isa_table(self):
        for r, expected in zip(self.isa_rows, EXPECTED_TABLE):
            for h,c in r.iteritems():
                self.assertEquals(c, expected[h])

    def test_org_mode_table(self):
        for r, expected in zip(self.org_rows, EXPECTED_TABLE):
            for h,c in r.iteritems():
                self.assertEquals(c, expected[h])


if __name__ == "__main__":
    unittest.main()
