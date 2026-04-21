import RfuncEnum
import IOpsEnum


def main():
    instruction = input("Enter your instruction in either binary or assembly format: ")
    decode_instruction(instruction)
    get_mips_instruction(instruction)


# get the different sections of the instruction
def decode_instruction(instruction):
    decode_instr = bin(int(instruction, 16))[2:]
    print("32 bit instruction")
    for bit in range(6):
        if bit == 0:
            print(decode_instr[0:6])
        elif bit == 1:
            print(decode_instr[6:11])
        elif bit == 2:
            print(decode_instr[11:16])
        elif bit == 3:
            print(decode_instr[16:21])
        elif bit == 4:
            print(decode_instr[21:26])
        else:
            print(decode_instr[26:32])
    # print(decode_instr)
    print()
    print()


# get the func code if the instruction is an R instruction
def get_op_func(func_bits):
    func_bits = int(func_bits, 2)
    for func in RfuncEnum.Rfuncs:
        if hex(func.value) == hex(func_bits):
            print(func.name)


def is_an_I_op(op_code):
    # op_code = str(op_code)
    # print(type(op_code))
    print("op code from is an i op: ", end="")
    print( hex(int(op_code , 2)))
    for op in IOpsEnum.Iops:
        if str(hex(int(op_code, 16))) == str(hex(op.value)):
            return True
        else:
            return False


def is_an_R_op(op_code):
    op_code = int(op_code, 16)
    for op in RfuncEnum.Rfuncs:
        if op_code == hex(op.value):
            return True
        else:
            return False


def get_reg_rs(rs):
    return int(rs)


def get_reg_rt(rt):
    return int(rt)


def get_reg_rd(rd):
    return int(rd)


def get_mips_instruction(binary):
    instr = 0
    test = bin(int(binary, 16))[2:]
    print(is_an_I_op(test[0:6]))
    # if is_an_I_op(binary[0:8]):
    if is_an_I_op(test[0:6]):
        for op in IOpsEnum.Iops:
            if hex(op.value) == hex(binary[0:6]):
                instr = op.name
    print("Assembly Code: ", end="")
    print(instr)


main()
# print(is_an_I_op("0x2B"))
get_op_func("100000")
print(get_reg_rs(0b000101))
