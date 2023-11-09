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
    '000010': 'srl',
    '000011': 'sra',
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

Input_array = [-4,7,100,100,100,21,21,7]

Main_memory = Input_array

# Initializing registers
Register_Array = []

Register_Array.append(['zero', 0])
Register_Array.append(['at', 0])
Register_Array.append(['s1', 0])
Register_Array.append(['s2', 0])
Register_Array.append(['s3', 0])
Register_Array.append(['s4', 0])
Register_Array.append(['s6', 0])
Register_Array.append(['t1', len(Main_memory)]) # t1 = n (number of instructions)
Register_Array.append(['t2', 0])
Register_Array.append(['t3', 0])
Register_Array.append(['t4', 0])
Register_Array.append(['t5', 0])
Register_Array.append(['t8', 0])
Register_Array.append(['t9', 0])

# Final Array of Registers
Final_Register_Array = Register_Array #Creating a final array of registers which is in memory to store the values of registers after each instruction

def Execute_Phase(instruction,PC_address):
    if instruction[0] == 'move':
        PC_address += 4
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
        PC_address += 4
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
        PC_address += 4
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
        PC_address += 4
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
        PC_address += 4
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
        PC_address += 4
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
        PC_address += 4
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
            PC_address += 4
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
            PC_address += 4
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



with open ("input.txt", "r") as file:
    numberOfInstructions = len(file.readlines())


diagramList = []
phaseList = ["IF", "ID" , "EX" , "MEM" , "WB"]


def E():
    pass

stageMap = {
    "IF": Fetch_Call,
    "ID": Decode_Phase,
    "EX": Execute_Phase,
    "MEM": Memory_Phase,
    "WB": WriteBack_Phase,
    "E": E
}

# A function that creates a pipeline diagram
def pipelined_diagram(): 

    padPred_Emptyfunct = 0

    for i in range(numberOfInstructions):
        discretePhase = []
        for phase in phaseList:
            discretePhase.append(phase)

        diagramList.append(discretePhase)
        discretePhase = []
    
    for i in range(1,numberOfInstructions):
        padPred_Emptyfunct += 1
        for j in range(padPred_Emptyfunct):
            diagramList[i].insert(0, "E")


    padSuc_Emptyfunct = len(diagramList[len(diagramList)-1]) - 5

    for i in range(0,numberOfInstructions):
        for j in range(padSuc_Emptyfunct):
            diagramList[i].insert(len(diagramList[i]), "E")    
        padSuc_Emptyfunct -= 1


Instruction_Memory = Fetch_Phase("input.txt")
End_PC_address = 4194516

Instruction_Hashmap = {}
PC_address = 4194380

Temp_PC_address = PC_address


# while PC_address < End_PC_address:
#     Fetch_Call(PC_address)
#     Decode_Phase(Instruction_Hashmap[PC_address],PC_address)
#     List = Execute_Phase(InstructionHashmap[PC_address],PC_address)
#     PC_address = int(List[0])
#     Memory_Phase(List[1],List[2],List[3])
#     WriteBack_Phase()
# print(Main_memory)
# print('Fibonacci value is ' + str(Final_Register_Array[10][1]))

List = []
f_Pc_address = 4194380
d_Pc_address = 4194380
e_Pc_address = 4194380
m_Pc_address = 4194380
w_Pc_address = 4194380
pipelined_diagram()
for j in range(len(diagramList[0])):
    for i in range(len(diagramList)):
        if diagramList[i][j] == "IF":
            Fetch_Call(f_Pc_address)
            f_Pc_address += 4
        elif diagramList[i][j] == "ID":
            Decode_Phase(Instruction_Hashmap[d_Pc_address],d_Pc_address)
            d_Pc_address += 4

        elif diagramList[i][j] == "EX":
            List = Execute_Phase(InstructionHashmap[e_Pc_address],e_Pc_address)
            print('Executed instruction is ' + str(InstructionHashmap[e_Pc_address]))
            e_Pc_address = int(List[0])
            if List[0] != f_Pc_address:
                f_Pc_address = int(List[0])
            if List[0] != d_Pc_address:
                d_Pc_address = int(List[0])

        elif diagramList[i][j] == "MEM":
            Memory_Phase(List[1],List[2],List[3])

        elif diagramList[i][j] == "WB":
            WriteBack_Phase()

        else:
            pass
    print(Instruction_Hashmap)
    print(InstructionHashmap)
    print('One column done')    

        # for j in range(len(diagramList[i])):
        #     if diagramList[i][j] == "E":
        #         pass
        #     else:
        #         diagramList[i][j] = InstructionHashmap[PC_address][0]
        #         PC_address += 4

    
    
print(Main_memory)
# print('Fibonacci value is ' + str(Final_Register_Array[10][1]))
