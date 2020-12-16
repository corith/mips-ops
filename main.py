def main():
    instruction = input("Enter your instruction in either binary or assembly format: ")
    decode_instruction(instruction)


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
    print(decode_instr)


main()
