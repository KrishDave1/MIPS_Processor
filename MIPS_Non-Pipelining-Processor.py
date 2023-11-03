Main_memory = [] # take input 

a = {}
a.update({'$zero': '00000'}) #Constant 0.
a.update({'$1': '00001'}) #Reserved for assembler.
a.update({'$s1': '10001'}) #Stores the starting address of the input array.
a.update({'$s2': '10010'})  # Loop counter for the outer loop (i.e., variable 'i').
a.update({'$s3':'10011'}) # Loop counter for the inner loop (i.e., variable 'j').
a.update({'$s4': '10100'}) #Temporary register used for swapping values.
a.update({'$s6': '10110'}) #Initially stores the starting address of the output array.
a.update({'$t1': '01001'}) #Number of integers to be sorted.
a.update({'$t2': '01010'})  # Starting address of the input array.
a.update({'$t3': '01011'})  # Starting address of the output array.
a.update({'$t4': '01100'})  # Temporary register used for loading and storing values
a.update({'$t5': '01101'})  # Temporary register used for loading and storing values
a.update({'$t8': '11000'}) # Temporary register used for calculation.
a.update({'$t9': '11001'}) # Temporary register used for calculation.
a.update({'move': ['000000','100001']}) #move is implemented as addu and its opcode is zero
a.update({'addi': '001000'}) #Add immediate (with overflow)
a.update({'sub': ['000000','100010']}) #Subtract without overflow
a.update({'lw': '100011'})  # Load word
a.update({'sw': '101011'})  # Store word
a.update({'slt': ['000000','101010']}) #Set on less than (signed)   
a.update({'beq': '000100'})  # Branch on equal
a.update({'bne': '000101'})  # Branch on not equal
a.update({'j': '000010'})  # Jump


# Initializing registers
Register_Array = []

Register_Array.append(['zero', 0])
Register_Array.append(['at', 0])
Register_Array.append(['s1', 0])
Register_Array.append(['s2', 0])
Register_Array.append(['s3', 0])
Register_Array.append(['s4', 0])
Register_Array.append(['s6', 0])
Register_Array.append(['t1', 0])
Register_Array.append(['t2', 0])
Register_Array.append(['t3', 0])
Register_Array.append(['t4', 0])
Register_Array.append(['t5', 0])
Register_Array.append(['t8', 0])
Register_Array.append(['t9', 0])

reversed_a = {}

for key, value in a.items():
    if isinstance(value, list):
        reversed_a[value[0]] = key
    else:
        reversed_a[value] = key

def binaryToDecimal(binary):
    decimal = 0
    for digit in binary:
        decimal = decimal*2 + int(digit)
    return decimal


def rTypeDecoder(machineCode):
    opcode = machineCode[0:6]
    rs = machineCode[6:11]
    rt = machineCode[11:16]
    rd = machineCode[16:21]
    shamt = machineCode[21:26]
    funct = machineCode[26:32]
    return [opcode, rs, rt, rd, shamt, funct]

def iTypeDecoder(machineCode):
    opcode = machineCode[0:6]
    rs = machineCode[6:11]
    rt = machineCode[11:16]
    immediate = machineCode[16:32]

    return opcode, rs, rt, immediate

def jTypeDecoder(machineCode):
    opcode = machineCode[0:6]
    address = machineCode[6:32]

    return opcode, address


def instructionDecoder(machineCode):
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


# Final Array 
# final_array = ["instruction","rs"]

def Execute_Phase(instruction):
    if instruction[0] == 'move':
        temp_index = 0
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[1]:
                temp_index = i # Store the index of the register that is being moved
                break
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[2]:
                Register_Array[temp_index][1] = Register_Array[i][1]
                break
    elif instruction[0] == 'addi':
        temp_index = 0
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[1]:
                temp_index = i
                break
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[2]:
                Register_Array[temp_index][1] = Register_Array[i][1] + int(instruction[3])
                break
    elif instruction[0] == 'sub':
        temp_index = 0
        temp_index_1 = 0
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[1]:
                temp_index = i
            if Register_Array[i][0] == instruction[2]:
                temp_index_1 = i
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[3]:
                Register_Array[temp_index][1] = Register_Array[temp_index_1][1] - Register_Array[i][1]
                break
    elif instruction[0] == 'lw': # inst ,reg, imm, reg
        temp_index = 0
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[1]:
                temp_index = i
                break
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[3]:
                Register_Array[temp_index][1] = Main_memory[Register_Array[i][1] + int(instruction[2])]
                break
    elif instruction[0] == 'sw':
        temp_index = 0
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[1]:
                temp_index = i
                break
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[3]:
                Main_memory[Register_Array[i][1] + int(instruction[2])] = Register_Array[temp_index][1]
                break
    elif instruction[0] == 'slt':
        temp_index = 0
        temp_index_1 = 0
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[1]:
                temp_index_1 = i
            if Register_Array[i][0] == instruction[2]:
                temp_index = i
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[3]:
                if Register_Array[temp_index][1] < Register_Array[i][1]:
                    Register_Array[temp_index_1][1] = 1
                else:
                    Register_Array[temp_index_1][1] = 0
                break
    elif instruction[0] == 'beq':
        temp_index = 0
        temp_index_1 = 0
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[1]:
                temp_index = i
            if Register_Array[i][0] == instruction[2]:
                temp_index_1 = i
        if Register_Array[temp_index][1] == Register_Array[temp_index_1][1]:
            PC = PC + int(instruction[3])
instruction = [
    'addi','s1','s2',10
]
Execute_Phase(instruction)
instruction = [
    'move','s2','s1'
]
Execute_Phase(instruction)

print(Register_Array)