import time
dictionary = {
    '00000': 'zero',
    '00001': 'at',
    '00010': 'v0',
    '00011': 'v1',
    '00100': 'a0',
    '00101': 'a1',
    '00110': 'a2',
    '00111': 'a3',
    '10000': 's0',
    '10001': 's1',
    '10010': 's2',
    '10011': 's3',
    '10100': 's4',
    '10101': 's5',
    '10110': 's6',
    '10111': 's7',
    '01000': 't0',
    '01001': 't1',
    '01010': 't2',
    '01011': 't3',
    '01100': 't4',
    '01101': 't5',
    '01110': 't6',
    '11000': 't8',
    '11001': 't9',
    '01111': 't7',
    '11010': 'gp',
    '11011': 'sp',
    '11100': 'fp',
    '11101': 'sp',
    '000000': 'sll',
    '000100': 'sllv',
    '000110': 'srlv',
    '000111': 'srav',
    '001010': 'slti',
    '100000': 'add',
    '100001': 'addu',
    '100011': 'subu',
    '100100': 'and',
    '100101': 'or',
    '100001': 'move', # function
    '001000': 'addi',
    '001001': 'addiu', 
    '100010': 'sub',  # function
    '100011': 'lw',
    '101011': 'sw',
    '101010': 'slt',  # function
    '000100': 'beq',
    '000101': 'bne',
    '000010': 'j',
    '000011': 'jal',
    '11111': 'ra',
    '011100': 'mul'
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

    if(funct == '001000'):
        return ["jr", dictionary[rs]]

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
    
    elif(dictionary[opcode] == "slti" or dictionary[opcode] == "addi" or dictionary[opcode] == "addiu" ):
        return [dictionary[opcode],dictionary[rt], dictionary[rs], binaryToDecimal(immediate)]
    
    elif(dictionary[opcode] == "mul"):
        return [dictionary[opcode],dictionary[rs], dictionary[rt], dictionary[rt]]
    
    if(immediate[0] == "0"):
        return [dictionary[opcode],dictionary[rs], dictionary[rt], binaryToDecimal(immediate)]
    
    return [dictionary[opcode],dictionary[rs], dictionary[rt], str(-1*int(binaryToDecimal(twos_comp(immediate))))]


def jTypeDecoder(machineCode):
    opcode = machineCode[0:6]
    address = machineCode[6:32]

    return [dictionary[opcode], binaryToDecimal(address)]


def instructionDecoder(machineCode):
    # clock_cycle += 1
    if(machineCode[0:6] == '000000'):
        return rTypeDecoder(machineCode)
    
    elif(machineCode[0:6] == '000010' or machineCode[0:6] == '000010' or machineCode[0:6] == '000011') :
        return jTypeDecoder(machineCode)
    
    else:
        return iTypeDecoder(machineCode)

pc = 4194380

#Fibonacci
#f(0) = 1, f(1) = 1
# The last 5 digits of the first line are the input for the fibonacci function
listOfInstructions = []
InstructionHashmap = {} # Key: PC, Value:

#Read input from file
def Fetch_Phase(file_path):
    input_data = []
    with open(file_path, 'r') as file:
        input_data = file.read()
        input_data = input_data.split()
        for i in range(len(input_data)):
            input_data[i] = input_data[i].strip()
    return input_data

def Decode_Phase(input_instruction,PC_address):
    listOfInstructions.append(instructionDecoder(input_instruction))
    InstructionHashmap[PC_address] = instructionDecoder(input_instruction)

# Input_array = [-4,7,100,100,100,21,21,7]
Input_array = [4,2,3,228,-330,19191,6,9,1,10,-3,1,2,8,7,0]

Main_memory = Input_array

# Initializing registers
Register_Array = []

Register_Array.append(['zero', 0])
Register_Array.append(['at', 0])
Register_Array.append(['s0', 0])
Register_Array.append(['s1', 0])
Register_Array.append(['s2', 0])
Register_Array.append(['s3', 0])
Register_Array.append(['s4', 0])
Register_Array.append(['s6', 0])
Register_Array.append(['t1', len(Main_memory)]) # t1 = n (number of instructions)
Register_Array.append(['t0', 0])
Register_Array.append(['t2', 0])
Register_Array.append(['t3', 0])
Register_Array.append(['t4', 0])
Register_Array.append(['t5', 0])
Register_Array.append(['t6', 0])
Register_Array.append(['t7', 0])
Register_Array.append(['t8', 0])
Register_Array.append(['t9', 0])

# Final Array of Registers
Final_Register_Array = Register_Array #Creating a final array of registers which is in memory to store the values of registers after each instruction

def Execute_Phase(instruction,PC_address):
    if instruction[0] == 'move':
        # PC_address += 4
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
        # PC_address += 4
        temp_index = 0
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[1]:
                temp_index = i
                break
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[2]:
                Register_Array[temp_index][1] = Register_Array[i][1] + int(instruction[3])
                break
    elif instruction[0] == 'add':
        # PC_address += 4
        temp_index = 0
        temp_index_1 = 0
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[1]:
                temp_index = i
            if Register_Array[i][0] == instruction[2]:
                temp_index_1 = i
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[3]:
                Register_Array[temp_index][1] = Register_Array[temp_index_1][1] + Register_Array[i][1]
                break
    elif instruction[0] == 'sub':
        # PC_address += 4
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
    elif instruction[0] == 'lw': 
        # PC_address += 4
        # inst ,reg, imm, reg
        temp_index = 0
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[1]:
                temp_index = i
                break
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[3]:
                mem_address = (Register_Array[i][1] + int(instruction[2]))//4
                return [PC_address,mem_address,temp_index,instruction[0]]
                # Register_Array[temp_index][1] = Main_memory[(Register_Array[i][1] + int(instruction[2]))//4]
                # Memory_Phase(mem_address,temp_index,instruction[0])
    elif instruction[0] == 'sw':
        # PC_address += 4
        temp_index = 0
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[1]:
                temp_index = i
                break
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[3]:
                mem_address = (Register_Array[i][1] + int(instruction[2]))//4
                return [PC_address,mem_address,temp_index,instruction[0]]
                # Memory_Phase(new,temp_index,instruction[0])
    elif instruction[0] == 'slt':
        # PC_address += 4
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
    elif instruction[0] == 'bne':
        temp_index = 0
        temp_index_1 = 0
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[1]:
                temp_index = i
            if Register_Array[i][0] == instruction[2]:
                temp_index_1 = i
        if Register_Array[temp_index][1] != Register_Array[temp_index_1][1]:
            New_PC_address = PC_address + 4 + 4*int(instruction[3])
            PC_address = New_PC_address
        else:
            # PC_address += 4
            pass
    elif instruction[0] == 'beq':
        temp_index = 0
        temp_index_1 = 0
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[1]:
                temp_index = i
            if Register_Array[i][0] == instruction[2]:
                temp_index_1 = i
        if Register_Array[temp_index][1] == Register_Array[temp_index_1][1]:
            New_PC_address = PC_address + 4 + 4*int(instruction[3])
            PC_address = New_PC_address
        else:
            # PC_address += 4
            pass
    elif instruction[0] == 'j':
        New_PC_address = 4*int(instruction[1])
        PC_address = New_PC_address
    else:
        print("Wrong instruction")
    return [PC_address,0,0,'']

def Memory_Phase(Memory_value,index,instructionType):
    if instructionType == 'lw':
        if Memory_value >= 0 and Memory_value < len(Main_memory):
            Register_Array[index][1] = Main_memory[Memory_value]
        else:
            Register_Array[index][1] = 0
    elif instructionType == 'sw':
        if Memory_value >= 0 and Memory_value < len(Main_memory):
            Main_memory[Memory_value] = Register_Array[index][1]
        else:
            Register_Array[index][1] = 0

def WriteBack_Phase():
    # Just updating all the ragisters after one instruction
    for i in range(len(Register_Array)):
        Final_Register_Array[i][1] = Register_Array[i][1] 

def Fetch_Call(PC_address):
    Instruction_Hashmap[PC_address] = Instruction_Memory[(PC_address - 4194380)//4]

Register_to_PC = {
    '00000': -1,
    '00001': -1,
    '00010': -1,
    '00011': -1,
    '00100': -1,
    '00101': -1,
    '00110': -1,
    '00111': -1,
    '10000': -1,
    '10001': -1,
    '10010': -1,
    '10011': -1,
    '10100': -1,
    '10101': -1,
    '10110': -1,
    '10111': -1,
    '01000': -1,
    '01001': -1,
    '01010': -1,
    '01011': -1,
    '01100': -1,
    '01101': -1,
    '01110': -1,
    '11000': -1,
    '11001': -1,
    '01111': -1,
}

Addre_to_reg = {
}

Dependency_Hashmap = {
}

Instruction_Memory = Fetch_Phase("./temp.txt")
End_PC_address = 4194380 + len(Instruction_Memory)*4

for i in range(4194380,End_PC_address,4):
    Dependency_Hashmap[i] = -1

def Dependencies(PC_address):
    instruction = Instruction_Hashmap[PC_address]
    if instruction[0:6] == '000000':
        if dictionary[instruction[26:32]] == 'move':
            rs = instruction[6:11]
            PC_address1 = Register_to_PC[rs]
            if PC_address1 != -1 and abs(PC_address1 - PC_address) <= 3*4:
                Dependency_Hashmap[PC_address] = PC_address1
        else:
            rs = instruction[6:11]
            rt = instruction[11:16]
            PC_address1 = Register_to_PC[rs]
            PC_address2 = Register_to_PC[rt]
            if PC_address1 != -1 and abs(PC_address1 - PC_address) <= 3*4:
                Dependency_Hashmap[PC_address] = PC_address1
            if PC_address2 != -1 and abs(PC_address2 - PC_address) <= 3*4:
                Dependency_Hashmap[PC_address] = PC_address2
    elif instruction[0:6] == '000010' or instruction[0:6] == '000011':
        pass
    else:
        rs = instruction[6:11]
        rt = instruction[11:16]
        PC_address2 = Register_to_PC[rs]
        if PC_address2 != -1 and abs(PC_address2 - PC_address) <= 3*4:
            Dependency_Hashmap[PC_address] = PC_address2
        if dictionary[instruction[0:6]] == 'beq' or dictionary[instruction[0:6]] == 'bne' or dictionary[instruction[0:6]] == 'sw':
            PC_address1 = Register_to_PC[rt]
            if PC_address1 != -1 and abs(PC_address1 - PC_address) <= 3*4:
                Dependency_Hashmap[PC_address] = PC_address1

# Instruction_Memory = Fetch_Phase("../Fibonacci.txt")
# End_PC_address = 4194416

Instruction_Hashmap = {}
PC_address = 4194380
#Dependencies

while PC_address < End_PC_address:
    Fetch_Call(PC_address)
    instruction = Instruction_Hashmap[PC_address]
    if PC_address > 4194380:
        Dependencies(PC_address)
    Decode_Phase(instruction,PC_address)
    if instruction[0:6] == '000000':
        if dictionary[instruction[26:32]] == 'move':
            rt = instruction[16:21]
            Register_to_PC[rt] = PC_address
            Addre_to_reg[PC_address] = rt
        else:
            rd = instruction[16:21]
            Register_to_PC[rd] = PC_address
            Addre_to_reg[PC_address] = rd
    elif instruction[0:6] == '000010' or instruction[0:6] == '000011':
        pass
    else:
        if dictionary[instruction[0:6]] == 'addi' or dictionary[instruction[0:6]] == 'lw':
            rd = instruction[11:16]
            Register_to_PC[rd] = PC_address
            Addre_to_reg[PC_address] = rd
    PC_address += 4

print(Dependency_Hashmap)
IF_List = []
ID_List = []
EX_List = []
MEM_List = []
WB_List = []

EXE_to_MEM = {
}

PC_to_Stage = {
}

def Check_Termination():
    for i in range(4194380,End_PC_address,4):
        if PC_to_Stage[i] != '':
            return False
    return True

for i in range(4194380,End_PC_address,4):
    PC_to_Stage[i] = ''

Clock_cycles = 0

PC_address_1 = 4194380
PC_to_Stage[PC_address_1] = 'IF'
IF_List.append(PC_address_1)
Fetch_Call(PC_address_1)
PC_address_1 += 4
while not Check_Termination():
    Clock_cycles += 1
    print(PC_to_Stage)
    print(IF_List)
    print(ID_List)
    print(EX_List)
    print(MEM_List)
    print(WB_List)
    if len(WB_List) != 0:
        WriteBack_Phase()
        pc = WB_List[0]
        PC_to_Stage[pc] = ''
        WB_List.pop(0)
    if len(MEM_List) != 0:
        Execution_List = EXE_to_MEM[MEM_List[0]]
        Memory_Phase(Execution_List[1],Execution_List[2],Execution_List[3])
        PC_to_Stage[MEM_List[0]] = "WB"
        WB_List.append(MEM_List[0])
        MEM_List.pop(0)
    ans = False
    if (len(EX_List) != 0):
        List = Execute_Phase(InstructionHashmap[EX_List[0]],EX_List[0])
        if (List[0] != EX_List[0]):
            ans = True
            print(List)
            print(EX_List[0])
            IF_List.clear()
            ID_List.clear()
            for i in range(4194380,End_PC_address,4):
                PC_to_Stage[i] = ''
            PC_address_1 = List[0]
        EXE_to_MEM[EX_List[0]] = List
        PC_to_Stage[EX_List[0]] = "MEM"
        MEM_List.append(EX_List[0])
        EX_List.pop(0)
    if len(ID_List) != 0:
        if Dependency_Hashmap[ID_List[0]] == -1:
            pc = ID_List[0]
            Decode_Phase(Instruction_Hashmap[ID_List[0]],ID_List[0])
            print(InstructionHashmap[ID_List[0]])
            PC_to_Stage[ID_List[0]] = "EX"
            ID_List.pop(0)
            EX_List.append(pc)
        elif PC_to_Stage[Dependency_Hashmap[ID_List[0]]] == '':
            pc = ID_List[0]
            Decode_Phase(Instruction_Hashmap[ID_List[0]],ID_List[0])
            print(InstructionHashmap[ID_List[0]])
            PC_to_Stage[ID_List[0]] = "EX"
            ID_List.pop(0)
            EX_List.append(pc)
    if len(IF_List) != 0:
        pc = IF_List[0]
        Fetch_Call(pc)
        PC_to_Stage[pc] = "ID"
        IF_List.pop(0)
        ID_List.append(pc)
    if (PC_address_1 < End_PC_address):
        if (PC_to_Stage[PC_address_1] == ''):
            IF_List.append(PC_address_1)
            PC_to_Stage[PC_address_1] = 'IF'
            print(PC_to_Stage)
        if ans == False:
            PC_address_1 += 4

print(Final_Register_Array)

# Temp_PC_address = PC_address
# while PC_address < End_PC_address:
#     Fetch_Call(PC_address)
#     Decode_Phase(Instruction_Hashmap[PC_address],PC_address)
#     List = Execute_Phase(InstructionHashmap[PC_address],PC_address)
#     PC_address = int(List[0])
#     Memory_Phase(List[1],List[2],List[3])
#     WriteBack_Phase()
# print(Main_memory)
print(Clock_cycles)

print('Fibonacci value is ' + str(Final_Register_Array[10][1]))


#15,16,19,20,21,22,23
