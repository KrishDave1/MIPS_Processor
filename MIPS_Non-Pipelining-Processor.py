from Task1 import dave_list,InstructionHashmap,listOfInstructions

Main_memory = [6,2,4,3,1]

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

def Jumpinstructions(loop_name, instrDictionary, PC_list):
    temp_index = 0
    if loop_name == 'end_sort':
        exit()
    for i in range(len(PC_list)):
        if PC_list[i][0] == loop_name:
            temp_index = i
            break
    starting_address = PC_list[temp_index][1][0]
    print(starting_address)
    # end_address = PC_list[temp_index][1][1]
    end_address = 4194376 + len(instrDictionary)*4
    print(end_address)
    for i in range(starting_address, end_address, 4):
        instruction = instrDictionary[i]
        print(instruction)
        Execute_Phase(instruction, instrDictionary, PC_list)

def Execute_Phase(instruction, instrDictionary, PC_list):

    PC_address = 0
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
    elif instruction[0] == 'lw': 
        # inst ,reg, imm, reg
        temp_index = 0
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[1]:
                temp_index = i
                break
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[3]:
                Register_Array[temp_index][1] = Main_memory[(Register_Array[i][1] + int(instruction[2]))//4]
                break
    elif instruction[0] == 'sw':
        temp_index = 0
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[1]:
                temp_index = i
                break
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[3]:
                new = (Register_Array[i][1] + int(instruction[2]))//4
                Main_memory[new] = Register_Array[temp_index][1]
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
    elif instruction[0] == 'bne':
        temp_index = 0
        temp_index_1 = 0
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[1]:
                temp_index = i
            if Register_Array[i][0] == instruction[2]:
                temp_index_1 = i
        if Register_Array[temp_index][1] != Register_Array[temp_index_1][1]:
            Jumpinstructions(instruction[3], instrDictionary, PC_list)
    elif instruction[0] == 'beq':
        temp_index = 0
        temp_index_1 = 0
        for i in range(len(Register_Array)):
            if Register_Array[i][0] == instruction[1]:
                temp_index = i
            if Register_Array[i][0] == instruction[2]:
                temp_index_1 = i
        if Register_Array[temp_index][1] == Register_Array[temp_index_1][1]:
            Jumpinstructions(instruction[3], instrDictionary, PC_list)
    elif instruction[0] == 'j':
        Jumpinstructions(instruction[1], instrDictionary, PC_list)
    else:
        print("Wrong instruction")

# print(listOfInstructions)

PC_list = dave_list
for i in range(len(PC_list)):
    PC_list[i][1][0] = int(PC_list[i][1][0])

for i in range(len(listOfInstructions)):
    Execute_Phase(listOfInstructions[i], InstructionHashmap, PC_list)
    print()
    # print(Register_Array)