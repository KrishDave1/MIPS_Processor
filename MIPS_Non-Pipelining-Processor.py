from Task1 import dave_list,InstructionHashmap,listOfInstructions
Input_array = [12,15,1,4,5,2,3,5,7,8,2,6,4,5,9,2,4,7,8,1]

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
                Temp_memory_value = (Register_Array[i][1] + int(instruction[2]))//4
                # Register_Array[temp_index][1] = Main_memory[(Register_Array[i][1] + int(instruction[2]))//4]
                Memory_Phase(Temp_memory_value,temp_index,instruction[0])
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
                # Main_memory[new] = Register_Array[temp_index][1]
                Memory_Phase(new,temp_index,instruction[0])
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

PC_list = dave_list
for i in range(len(PC_list)):
    PC_list[i][1][0] = int(PC_list[i][1][0])

PC_address = 4194380
Temp_PC_address = PC_address

Clock_cycles = 0

#For Sorting uncomment this
# while PC_address < Temp_PC_address + 4*(len(InstructionHashmap)):
#     Clock_cycles += 1
#     PC_address = Execute_Phase(InstructionHashmap[PC_address],PC_list,PC_address)
#     WriteBack_Phase()
# print('Total Clock cycles:' + " " + str(Clock_cycles))
# print(Main_memory)

# For Fibonacci uncomment this
while PC_address < (Temp_PC_address + 4*(len(InstructionHashmap))):
    Clock_cycles += 1
    PC_address = Execute_Phase(InstructionHashmap[PC_address],PC_list,PC_address)
    WriteBack_Phase()
print("Total Clock Cycles:" + " " + str(Clock_cycles))
print('The answer of fibonacci is:' + " " + str(Register_Array[10][1])) # The answer of fibonacci is stored in t4.v

