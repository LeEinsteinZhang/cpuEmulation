import re

# Define the instruction formats
INSTRUCTION_SET = {
    '.word': ('W'),
    'add':  ('R', (3, 0), '000000', '100000'),
    'sub':  ('R', (3, 0), '000000', '100010'),
    'mult': ('R', (2, 0), '000000', '011000'),
    'multu':('R', (2, 0), '000000', '011001'),
    'div':  ('R', (2, 0), '000000', '011010'),
    'divu': ('R', (2, 0), '000000', '011011'),
    'mfhi': ('R', (1, 2), '000000', '010000'),
    'mflo': ('R', (1, 2), '000000', '010010'),
    'lis':  ('R', (1, 2), '000000', '010100'),
    'lw':   ('I', '100011'),
    'sw':   ('I', '101011'),
    'slt':  ('R', (3, 0), '000000', '101010'),
    'sltu': ('R', (3, 0), '000000', '101011'),
    'beq':  ('I', '000100'),
    'bne':  ('I', '000101'),
    'jr':   ('R', (1, 0), '000000', '001000'),
    'jalr': ('R', (1, 0), '000000', '001001'),
    'addi': ('I', '001000'),
    'j':    ('J', '000010'),
    'jal':  ('J', '000011'),
}

# Register to binary conversion
REGISTER_MAP = {
    '$zero': '00000', '$0': '00000',
    '$at': '00001', '$1': '00001',
    '$v0': '00010', '$2': '00010',
    '$v1': '00011', '$3': '00011',
    '$a0': '00100', '$4': '00100',
    '$a1': '00101', '$5': '00101',
    '$a2': '00110', '$6': '00110',
    '$a3': '00111', '$7': '00111',
    '$t0': '01000', '$8': '01000',
    '$t1': '01001', '$9': '01001',
    '$t2': '01010', '$10': '01010',
    '$t3': '01011', '$11': '01011',
    '$t4': '01100', '$12': '01100',
    '$t5': '01101', '$13': '01101',
    '$t6': '01110', '$14': '01110',
    '$t7': '01111', '$15': '01111',
    '$s0': '10000', '$16': '10000',
    '$s1': '10001', '$17': '10001',
    '$s2': '10002', '$18': '10010',
    '$s3': '10003', '$19': '10011',
    '$s4': '10004', '$20': '10100',
    '$s5': '10005', '$21': '10101',
    '$s6': '10006', '$22': '10110',
    '$s7': '10007', '$23': '10111',
    '$t8': '11000', '$24': '11000',
    '$t9': '11001', '$25': '11001',
    '$k0': '11010', '$26': '11010',
    '$k1': '11011', '$27': '11011',
    '$gp': '11100', '$28': '11100',
    '$sp': '11101', '$29': '11101',
    '$fp': '11110', '$30': '11110',
    '$ra': '11111', '$31': '11111'
}

# Helper functions
def to_bin_str(num, length):
    return format(num & (2**length - 1), '0{}b'.format(length))

def parse_register(reg):
    return REGISTER_MAP.get(reg, None)

def parse_immediate(imm):
    if imm.startswith('0x'):
        return to_bin_str(int(imm, 16), 16)
    else:
        return to_bin_str(int(imm), 16)

def parse_label(label, label_dict, pc):
    label_pos = label_dict[label]
    return str((label_pos - (pc + 4)) // 4)

def jump_immediate(imm):
    if imm.startswith('0x'):
        return to_bin_str(int(imm, 16), 26)
    else:
        return to_bin_str(int(imm), 26)


# Assembler function
def assemble_instruction(instruction, label_dict, pc):
    parts = re.split(r'[,\s()]+', instruction.strip())
    opcode = parts[0]
    instr_type, *code = INSTRUCTION_SET[opcode]
    if instr_type == 'W':
        print(parts[1])
    elif instr_type == 'R':
        num_registers, start_pos = code[0]
        std = ['00000', '00000', '00000']
        
        if num_registers == 3:
            std[2] = parse_register(parts[1])  # d
            std[0] = parse_register(parts[2])  # s
            std[1] = parse_register(parts[3])  # t
        elif num_registers == 2:
            std[0] = parse_register(parts[1])  # s
            std[1] = parse_register(parts[2])  # t
        elif num_registers == 1:
            std[start_pos] = parse_register(parts[1])  # s/d
        
        shamt = '00000'
        funct = code[2]
        return '{}{}{}{}{}{}'.format(code[1], std[0], std[1], std[2], shamt, funct)
    
    elif instr_type == 'I':
        if opcode == 'addi':
            rt = parse_register(parts[1])
            rs = parse_register(parts[2])
        else:
            rs = parse_register(parts[1])
            rt = parse_register(parts[2])
        if opcode == 'lw' or opcode == 'sw':
            rs = parse_register(parts[3])
            rt = parse_register(parts[1])
            imm = parse_immediate(parts[2])
        else:
            if parts[3] in label_dict:
                imm = parse_immediate(parse_label(parts[3], label_dict, pc))
            else:
                imm = parse_immediate(parse_immediate(parts[3]))
        return '{}{}{}{}'.format(code[0], rs, rt, imm)
    
    elif instr_type == 'J':
        print(parts, code)
        label = parts[1]
        if parts[1] not in label_dict:
            address = jump_immediate(label)
        else:
            address = jump_immediate(parse_label(label, label_dict, pc))
        return '{}{}'.format(code[0], address)
    
    else:
        raise ValueError('Unsupported instruction type')

def assemble_program(program):
    # First pass: resolve labels
    lines = program.strip().split('\n')
    label_dict = {}
    pc = 0
    for line in lines:
        clean_line = line.split(';')[0].strip()
        if clean_line == '':
            continue
        if ':' in clean_line:
            clean_line_parts = clean_line.split(':')
            label = clean_line_parts[0].strip()
            instruction = clean_line_parts[1].strip()
            label = clean_line.split(':')[0].strip()
            label_dict[label] = pc
            if instruction:
                pc += 4
        else:
            pc += 4

    # Second pass: assemble instructions
    pc = 0
    binary_instructions = []
    for line in lines:
        clean_line = line.split(';')[0].strip()
        if clean_line == '':
            continue
        if ':' in clean_line:
            instruction = clean_line.split(':')[1].strip()
            if instruction:
                binary_instructions.append(assemble_instruction(instruction, label_dict, pc))
                pc += 4
        else:
            binary_instructions.append(assemble_instruction(clean_line, label_dict, pc))
            pc += 4

    return '\n'.join(binary_instructions)

def hex_output(b_output):
    binary_hex = '\n'.join('0x' + format(int(b, 2), '08x') for b in b_output.split('\n'))
    return binary_hex

# Example program with comments and labels
example_program = """
        addi $10, $0, 10    ; 0 initial $10 with constant 10
loop:   beq $1, $0, end     ; 1 if $1 equal to zero end the loop
        div $1, $10         ; 2 calculate the quotient and reminder with $1 and 10
        mflo $1             ; 3 store the quotient to $1
        mfhi $4             ; 4 store the reminder (last digit) to $4
        div $4, $2          ; 5 calculate the quotient and reminder with $4 and $2
        mfhi $5             ; 6 store reminder to $5
        beq $5, $0, add_to  ; 7 if reminder equal 0 add number to result
        beq $0, $0, loop    ; 8 back to the loop
add_to: add $3, $3, $4      ; 9 add last digit to $3
        beq $0, $0, loop    ; 10 back to the loop
end:    jr $31              ; 11 return
"""

# ans = """
# 00100000000010100000000000001010
# 0001000000100000iiiiiiiiiiiiiiii
# 00000000001010100000000000011010
# 00000000000000000000100000010010
# 00000000000000000010000000010000
# 00000000100000100000000000011010
# 00000000000000000010100000010000
# 0001000010100000iiiiiiiiiiiiiiii
# 0001000000000000iiiiiiiiiiiiiiii
# 00000000011001000001100000100000
# 0001000000000000iiiiiiiiiiiiiiii
# 00000011111000000000000000001000
# """

ans = """00100000000010100000000000001010
00010000001000000000000000101000
00000000001010100000000000011010
00000000000000000000100000010010
00000000000000000010000000010000
00000000100000100000000000011010
00000000000000000010100000010000
00010000101000000000000000001000
00010000000000001111111111100000
00000000011001000001100000100000
00010000000000001111111111011000
00000011111000000000000000001000
"""

# Assemble the example program
binary_output = assemble_program(example_program)
def checker(s1, s2):
    s1 = s1.split()
    s2 = s2.split()
    l_s1 = len(s1)
    l_s2 = len(s2)
    result = []
    if l_s1 == l_s2:
        for i in range(l_s1):
            if s1[i] == s2[i]:
                result.append(1)
            else:
                result.append(0)
                print(i, s1[i], s2[i])
        ans = 1
        for i in range(l_s1):
            ans *= result[i]
        if ans:
            return True
        else:
            return False
    else:
        return False


# print(checker(binary_output,ans))
#
#
# print(binary_output)
temp = assemble_program("""
;; CS230 - Assignment 5 - Question 1b
;; Name:     Le Zhang
;; Quest ID: l652zhan
;; This program is a subroutine to check if the array elements are 
;;   word aligned and process them using a predicate function wordaligned. 
;;   It then produces the result array address and size.
;; Registers: $1 ->  input/output, base address of original/filtered array
;;            $2 ->  input/output, length of original/filtered array
;;               |-> result of subroutine the base address of filtered array
;;            $3 ->  result of subroutine the length of filtered array
;;            $4 -> predicate function address
;;            $5 -> base address of the original array
;;            $6 -> length of the original array
;;            $8 -> temporary register for most memory read and write
        addi $4, $0, wordaligned ; assign the predicate function address to $4
        add $5, $1, $0           ; assign base address of the original array to $5
        add $6, $2, $0           ; assign the length of the original array to $6
        addi $30, $30, -4        ; move to next stack slot
        sw $31, 0($30)           ; store pc
        jal filter               ; call filter function
        lw $31, 0($30)           ; restore pc
        addi $30, $30, 4         ; release one stack slot 

        add $1, $2, $0           ; copy the base address of the filtered array to $1
        add $2, $3, $0           ; copy the length of the filtered array to $1

        jr $31                   ; end the program, return

wordaligned:
        addi $8, $0, 4           ; a constant 4 for bytes calculation
        div $4, $8               ; divide input by 4
        mfhi $8                  ; load reminder into $8
        beq $8, $0, true         ; if reminder is zero jump to true (aligned)
        addi $3, $0, 0           ; set $3 to 0 for false (not aligned)
        beq $0, $0, w_end        ; jump to the w_end

true:   addi $8, $0, -1          ; a constant -1 for checking non-negative number
        slt $8, $8, $4           ; if the number is larger than -1 $8 set to 1
        addi $3, $0, 1           ; set $3 to 1 for 4 mutiplied
        mult $3, $8              ; use mutiplication as AND (non-negative and 4 mutiplied)
        mflo $3                  ; load the AND result to $3

w_end:  jr $31                   ; end the program, return
;; CS230 - Assignment 5 - Question 1a
;; Name:     Le Zhang
;; Quest ID: l652zhan
;; This program is a subroutine to processe an array and checks if each element by 
;;   predicate function then produce the result array address and size
;; Registers: $2 -> result,   the base address of filtered array
;;            $3 -> result,   the length of of filtered array
;;            $4 -> argument, predicate function address
;;            $5 -> argument, the base address of original array
;;            $6 -> argument, the length of original array
;;            $8 -> temporary register for most memory read and write
;;            $9 -> temporary register
filter: 
        addi $8, $0, 4     ; a constant 4 for bytes calculation
        mult $8, $6        ; multiply item counter by 4 (byte size)
        mflo $8            ; store the result in $8
        add $8, $5, $8     ; calculate the first element address following original array
        addi $30, $30, -4  ; move to next stack slot
        sw $8, 0($30)      ; store the first element address following original array to stack
        addi $30, $30, -4  ; move to next stack slot
        sw $0, 0($30)      ; store the number of element of the result array to stack

f_loop: beq $6, $0, end_f  ; if $6 equals 0, jump to end_f
        addi $30, $30, -4  ; move to next stack slot
        sw $8, 0($30)      ; store the current element address to stack

        lw $8, 0($5)       ; read the current element in array
        addi $5, $5, 4     ; move to next array element address
        addi $6, $6, -1    ; decrement $6 by 1
        addi $30, $30, -4  ; move to next stack slot
        sw $8, 0($30)      ; store current array element to stack

        add $9, $4, $0     ; copy the predicate function address to $9

        addi $30, $30, -4  ; move to next stack slot
        sw $4, 0($30)      ; store predicate function address to stack
        addi $30, $30, -4  ; move to next stack slot
        sw $5, 0($30)      ; store the first array element to stack
        addi $30, $30, -4  ; move to next stack slot
        sw $6, 0($30)      ; store the length of original array to stack

        add $4, $8, $0     ; assign the current array element to argument $4
        addi $30, $30, -4  ; move to next stack slot
        sw $31, 0($30)     ; store pc
        jalr $9            ; call predicate function
        lw $31, 0($30)     ; restore pc
        addi $30, $30, 4   ; release one stack slot 

        lw $6, 0($30)      ; restore the length of original array from stack
        addi $30, $30, 4   ; release one stack slot 
        lw $5, 0($30)      ; restore the first array element from stack
        addi $30, $30, 4   ; release one stack slot 
        lw $4, 0($30)      ; restore predicate function address from stack
        addi $30, $30, 4   ; release one stack slot 
        lw $9, 0($30)      ; restore current array element from stack
        addi $30, $30, 4   ; release one stack slot 
        lw $8, 0($30)      ; restore the current element address from stack
        addi $30, $30, 4   ; release one stack slot 

        bne $3, $0, add_to ; if $3 is not 0, jump to add_to
        beq $0, $0, f_loop ; back to f_loop

add_to: sw $9, 0($8)       ; store current array element to current element address
        addi $8, $8, 4     ; move to next array element
        lw $9, 0($30)      ; restore number of element of the result array from stack
        addi $9, $9, 1     ; increment 1 for the number of element of the result array
        sw $9, 0($30)      ; store number of element of the result array to stack
        beq $0, $0, f_loop ; back to f_loop

end_f:  lw $3, 0($30)      ; restore the number of element of the result array from stack to $3
        addi $30, $30, 4   ; release one stack slot 
        lw $2, 0($30)      ; restore the first element address following original array from stack to $2
        addi $30, $30, 4   ; release one stack slot 
        jr $31             ; end the program, return

""")

binary_hex = hex_output(temp)


print(temp)
