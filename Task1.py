clock_cycle = 0

dictionary = {
    '00000': 'zero',
    '00001': 'at',
    '10001': 's1',
    '10010': 's2',
    '10011': 's3',
    '10100': 's4',
    '10110': 's6',
    '01001': 't1',
    '01010': 't2',
    '01011': 't3',
    '01100': 't4',
    '01101': 't5',
    '11000': 't8',
    '11001': 't9',
    '100001': 'move', # function
    '001000': 'addi',
    '100010': 'sub',  # function
    '100011': 'lw',
    '101011': 'sw',
    '101010': 'slt',  # function
    '000100': 'beq',
    '000101': 'bne',
    '000010': 'j',
 
}

def binaryToDecimal(binary):
    decimal = 0
    for digit in binary:
        decimal = decimal*2 + int(digit)
    return str(decimal)


def flip(c): 
    return '1' if (c == '0') else '0' 


def twos_comp(bin): # Function prints the one's and two's complement of binary number bin
    n = len(bin)
    ones = ""
    twos = "" 
    for i in range(n): # Compute the one's complement by flipping the bits
        ones += flip(bin[i])

    ones = list(ones.strip("")) 
    twos = list(ones) # Compute 2's complement by adding 1 to the one's complement

    for i in range(n - 1, -1, -1):  # Start from the rightmost bit and keep flipping the bits until we find a 1 
        if (ones[i] == '1'):
            twos[i] = '0'

        else:
            twos[i] = '1'
            break

    i -= 1
    if (i == -1):
        twos.insert(0, '1')

    return twos # Return the 2's complement


def rTypeDecoder(machineCode):
    rs = machineCode[6:11]
    rt = machineCode[11:16]
    rd = machineCode[16:21]
    shamt = machineCode[21:26]
    funct = machineCode[26:32]

    if(dictionary[funct] == 'move'):
        return [dictionary[funct],dictionary[rd] ,dictionary[rt]]
    
    return [dictionary[funct],dictionary[rd] ,dictionary[rs] , dictionary[rt]]


def iTypeDecoder(machineCode):
    opcode = machineCode[0:6]
    rs = machineCode[6:11]
    rt = machineCode[11:16]
    immediate = machineCode[16:32]

    if(dictionary[opcode] == 'sw' or dictionary[opcode] == 'lw'):
        return [dictionary[opcode],dictionary[rt], binaryToDecimal(immediate), dictionary[rs]]
    
    if(immediate[0] == "0"):
        return [dictionary[opcode],dictionary[rs], dictionary[rt], binaryToDecimal(immediate)]
    
    return [dictionary[opcode],dictionary[rs], dictionary[rt], binaryToDecimal(twos_comp(immediate))]


def jTypeDecoder(machineCode):
    opcode = machineCode[0:6]
    address = machineCode[6:32]

    return [dictionary[opcode], binaryToDecimal(address)]


def instructionDecoder(machineCode):
    # clock_cycle += 1
    if(machineCode[0:6] == '000000'):
        return rTypeDecoder(machineCode)
    
    elif(machineCode[0:6] == '000010'):
        return jTypeDecoder(machineCode)
    
    else:
        return iTypeDecoder(machineCode)



instructions = [
"00000000000000001001000000100001",
"00000000000010111011000000100001",
"00000000000010101000100000100001",
"00000001001100100000100000101010",
"00010100001000000000000000011100",
"00100010010100100000000000000001",
"00000000000101100101100000100001",
"00000000000100010101000000100001",
"00000000000000001001100000100001",
"00000000000000001010000000100001",
"00100010011100110000000000000001",
"00000001001100101100000000100010",
"00000011000100110000100000101010",
"00010100001000001111111111110101",
"10001101010011000000000000000000",
"10001101010011010000000000000100",
"00000001101011000000100000101010",
"00010000001000000000000000001010",
"00000000000011001010000000100001",
"00000000000011010110000000100001",
"00000000000101000110100000100001",
"10101101011011000000000000000000",
"10101101011011010000000000000100",
"10101101010011000000000000000000",
"10101101010011010000000000000100",
"00100001011010110000000000000100",
"00100001010010100000000000000100",
"00001000000100000000000000011101",
"10101101011011000000000000000000",
"10101101011011010000000000000100",
"00100001010010100000000000000100",
"00100001011010110000000000000100",
"00001000000100000000000000011101",
"00000000000101100101100000100001"
]

listOfInstructions = []
InstructionHashmap = {} # Key: PC, Value:
dave_list = []
pc = 4194380;


for i in instructions:
    clock_cycle += 1
    listOfInstructions.append(instructionDecoder(i))
    InstructionHashmap[pc] = instructionDecoder(i)
    pc += 4


def identify_labels(InstructionHashmap):
    labels = {}
    loop_count = 0 # for naming the labels

    for i in InstructionHashmap:
        if(InstructionHashmap[i][0] == 'beq' or InstructionHashmap[i][0] == 'bne'):
            loop_count += 1
            pc_key = int(i) + 4 + (4 * int(InstructionHashmap[i][3]))
            labels[pc_key] = f"loop{loop_count}"

        elif(InstructionHashmap[i][0] == 'j'):
            loop_count += 1
            pc_key = int(InstructionHashmap[i][1]) * 4
            labels[pc_key] = f"loop{loop_count}"
    
    sorted_labels = dict(sorted(labels.items()))
    return sorted_labels

label_dict = identify_labels(InstructionHashmap)


for i in label_dict:
    temp = [label_dict[i], [i]]
    dave_list.append(temp)


print(dave_list)






















# def getCodeFromLabel(label):
#     instructions = []
#     res = list(labels.keys()).index(label)
#     ind_ll = list(labels)[res]
#     ind_ul = list(labels)[res+1]

#     for i in range(labels[ind_ll], labels[ind_ul] ,4):
#         instructions.append(listOfInstructions[i//4])

#     return instructions




                                
    



