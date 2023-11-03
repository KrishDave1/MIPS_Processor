from Task1 import *

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
Register_Array = [
    ['zero', 0],
    ['at', 0],
    ['s1', 0],
    ['s2', 0],
    ['s3', 0],
    ['s4', 0],
    ['s6', 0],
    ['t1', 0],
    ['t2', 0],
    ['t3', 0],
    ['t4', 0],
    ['t5', 0],
    ['t8', 0],
    ['t9', 0]
]


reversed_a = {}

for key, value in a.items():
    if isinstance(value, list):
        reversed_a[value[0]] = key
    else:
        reversed_a[value] = key



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


for i in listOfInstructions:

    if(i[0] == 'j' or i[0] == 'beq' or i[0] == 'bne'):
        break

    Execute_Phase(i)

print(Register_Array)