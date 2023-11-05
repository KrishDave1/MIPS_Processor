from Task1 import dave_list,InstructionHashmap,listOfInstructions

Main_memory = [67,38,45,15,0]

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
def Jumpinstructions(loop_name, PC_list):
    temp_index = 0
    # if loop_name == '1048605':
    #     loop_name = 'loop4'
    for i in range(len(PC_list)):
        if PC_list[i][0] == loop_name:
            temp_index = i
            break
    starting_address = PC_list[temp_index][1][0]
    return starting_address

def Execute_Phase(instruction, PC_list,PC_address):
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
                Register_Array[temp_index][1] = Main_memory[(Register_Array[i][1] + int(instruction[2]))//4]
                break
    elif instruction[0] == 'sw':
        PC_address += 4
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
            PC_address = Jumpinstructions(instruction[3], PC_list)
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
            PC_address = Jumpinstructions(instruction[3], PC_list)
        else:
            PC_address += 4
    elif instruction[0] == 'j':
        PC_address = Jumpinstructions(instruction[1], PC_list)
    else:
        print("Wrong instruction")
    return PC_address

PC_list = dave_list
for i in range(len(PC_list)):
    PC_list[i][1][0] = int(PC_list[i][1][0])

#For Sorting uncomment this
# PC_address = 4194380
# while PC_address < 4194516:
#     # print(str(PC_address) + " " + str(InstructionHashmap[PC_address]))
#     PC_address = Execute_Phase(InstructionHashmap[PC_address],PC_list,PC_address)
# print(Main_memory)

# For Fibonacci uncomment this
PC_address = 4194304
while PC_address < 4194340:
    PC_address = Execute_Phase(InstructionHashmap[PC_address],PC_list,PC_address)
print(Register_Array[10][0] + " " + str(Register_Array[10][1])) # The answer of fibonacci is stored in t4.