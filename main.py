def main():
    instruction = input("Enter your instruction in either binary or assembly format: ")
    decode_instruction(instruction)


def decode_instruction(instruction):
    # if 0 <= int(instruction[0]) <= 1:
    decode_instr = bin(int(instruction, 16))[2:]
    print("32 bit instruction")
    i = 0
    for bit in range(6):
        # if i == 6:
        #     print(decode_instr[0:5] + "\n")
        # else:
        # print(bit)
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
        # print(decode_instr[12:17])
        # print(decode_instr[18:23])
        # print(decode_instr[24:29])
        # print(decode_instr[29:35])
    print(decode_instr)


main()
