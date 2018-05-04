# -*- coding=utf-8 -*-
import re
register = {
    '$zero':'00000',
    '$at':'00001',
    '$v0':'00010',
    '$v1':'00011',
    '$a0':'00100',
    '$a1': '00101',
    '$a2': '00110',
    '$a3': '00111',
    '$t0': '01000',
    '$t1': '01001',
    '$t2': '01010',
    '$t3': '01011',
    '$t4': '01100',
    '$t5': '01101',
    '$t6': '01110',
    '$t7': '01111',
    '$s0': '10000',
    '$s1': '10001',
    '$s2': '10010',
    '$s3': '10011',
    '$s4': '10100',
    '$s5': '10101',
    '$s6': '10110',
    '$s7': '10111',
    '$t8': '11000',
    '$t9': '11001',
    '$k0': '11010',
    '$k1': '11011',
    '$gp': '11100',
    '$sp': '11101',
    '$fp': '11110',
    '$ra': '11111',

    'r0':'00000',
    'r1':'00001',
    'r2':'00010',
    'r3':'00011',
    'r4':'00100',
    'r5': '00101',
    'r6': '00110',
    'r7': '00111',
    'r8': '01000',
    'r9': '01001',
    'r10': '01010',
    'r11': '01011',
    'r12': '01100',
    'r13': '01101',
    'r14': '01110',
    'r15': '01111',
    'r16': '10000',
    'r17': '10001',
    'r18': '10010',
    'r19': '10011',
    'r20': '10100',
    'r21': '10101',
    'r22': '10110',
    'r23': '10111',
    'r24': '11000',
    'r25': '11001',
    'r26': '11010',
    'r27': '11011',
    'r28': '11100',
    'r29': '11101',
    'r30': '11110',
    'r31': '11111',

    'R0':'00000',
    'R1':'00001',
    'R2':'00010',
    'R3':'00011',
    'R4':'00100',
    'R5': '00101',
    'R6': '00110',
    'R7': '00111',
    'R8': '01000',
    'R9': '01001',
    'R10': '01010',
    'R11': '01011',
    'R12': '01100',
    'R13': '01101',
    'R14': '01110',
    'R15': '01111',
    'R16': '10000',
    'R17': '10001',
    'R18': '10010',
    'R19': '10011',
    'R20': '10100',
    'R21': '10101',
    'R22': '10110',
    'R23': '10111',
    'R24': '11000',
    'R25': '11001',
    'R26': '11010',
    'R27': '11011',
    'R28': '11100',
    'R29': '11101',
    'R30': '11110',
    'R31': '11111',
}
funcr = {'add':'100000',
        'addu':'100001',
        'sub':'100010',
        'subu':'100011',
        'and':'100100',
        'or':'100101',
        'xor':'100110',
        'nor':'100111',
        'slt':'101010',
        'sltu':'101011',
        'sll':'000000',
        'srl':'000010',
        'sra':'000011',
        'sllv':'000100',
        'srlv':'000110',
        'srav':'000111',
        'jr':'001000'}
funci = {'addi':'001000',
         'addiu':'001001',
         'andi':'001100',
         'ori':'001101',
         'xori':'001110',
         'lui':'001111',
         'lw':'100011',
         'sw':'101011',
         'beq':'000100',
         'bne':'000101',
         'slti':'001010',
         'sltiu':'001011'
}
funcj = {'j':'000010',
         'jal':'000011'
}


def asm(line_num,string):
    if ':' in string:
        print 32*' '+'\t'+string
        return
    instruction = '00000000000000000000000000000000'
    strlist =  string.rstrip('\n').strip().split(' ',1)    #去除首尾空格并且用空格分隔字符串
    if funcr.has_key(strlist[0]):   #如果是r型指令
        instruction = '000000' + instruction[6:]
        if(strlist[0] == 'jr'):
            registerlist = strlist[1].replace(' ', '').replace(';', '')
            instruction = instruction[:6] + register[registerlist] + instruction[11:]
        elif(strlist[0] in ['sll','srl','sra',]):
            registerlist = strlist[1].replace(' ', '').replace(';', '').split(',')
            instruction = instruction[:6]+'00000'+instruction[11:]
            instruction = instruction[:11] + register[registerlist[1]] + instruction[16:]
            instruction = instruction[:16] + register[registerlist[0]] + instruction[21:]
            shamt = str('{0:b}'.format(int(registerlist[2]))).zfill(5)
            instruction = instruction[:21] + str(shamt) + instruction[26:]
        else:   #add,sub等
            registerlist = strlist[1].replace(' ','').replace(';','').split(',')

            instruction = instruction[:6]+register[registerlist[1]]+instruction[11:]    #rs
            instruction = instruction[:11] + register[registerlist[2]] + instruction[16:]    #rt
            instruction = instruction[:16] + register[registerlist[0]] + instruction[21:]
        instruction = instruction[:26] + funcr[strlist[0]]  # 更新func

    elif funci.has_key(strlist[0]):   #是i型指令
        if(strlist[0] == 'lui'):
            registerlist = strlist[1].replace(' ', '').replace(';', '').split(',')
            instruction = funci[strlist[0]] + instruction[6:]
            instruction = instruction[:6] + '00000' + instruction[11:]
            instruction = instruction[:11] + register[registerlist[0]] + instruction[16:]
            shamt = str('{0:b}'.format(int(registerlist[1]))).zfill(16)
            instruction = instruction[:16] + str(shamt)
        elif (strlist[0] in ['sw', 'lw']):
            registerlist = strlist[1].replace(' ', '').replace(';', '').split(',')
            instruction = funci[strlist[0]] + instruction[6:]
            shamt = str('{0:b}'.format(int(registerlist[1].split('(')[0]))).zfill(16)
            instruction = instruction[:16] + str(shamt)
            instruction = instruction[:6] + register[re.findall(".*\((.*)\).*", registerlist[1])[0]] + instruction[11:]
            instruction = instruction[:11] + register[registerlist[0]] + instruction[16:]
        elif (strlist[0] in ['beq', 'bne']):
            registerlist = strlist[1].replace(' ', '').replace(';', '').split(',')
            instruction = funci[strlist[0]] + instruction[6:]
            instruction = instruction[:6] + register[registerlist[1]] + instruction[11:]
            instruction = instruction[:11] + register[registerlist[0]] + instruction[16:]
            if tag.has_key(registerlist[2]):
                shamt = (bin(((1 << 16) - 1) & (int(tag[registerlist[2]]) - line_num - 1))[2:]).zfill(16)
            else:
                shamt = str('{0:b}'.format(int(registerlist[2]))).zfill(16)
            instruction = instruction[:16] + str(shamt)
        else:
            registerlist = strlist[1].replace(' ', '').replace(';', '').split(',')
            instruction = funci[strlist[0]]+instruction[6:]
            instruction = instruction[:6] + register[registerlist[1]] + instruction[11:]
            instruction = instruction[:11] + register[registerlist[0]] + instruction[16:]
            shamt = str('{0:b}'.format(int(registerlist[2]))).zfill(16)
            instruction = instruction[:16] + str(shamt)

    elif funcj.has_key(strlist[0]): #是j型指令
        instruction = funcj[strlist[0]] + instruction[6:]
        registerlist = strlist[1].replace(' ', '').replace(';', '')
        if tag.has_key(registerlist):
            shamt = (bin(((1 << 26) - 1) & (int(tag[registerlist])-line_num-1))[2:]).zfill(26)
        else:
            shamt = str('{0:b}'.format(int(registerlist))).zfill(26)
        instruction = instruction[:6]+str(shamt)


    print instruction+'\t'+string

################################################################################################
#begin
tag = {}
file_object = open('asm.txt','rU')
line_num = 0
flag = 0
try:
    for line in file_object:
        line = line.rstrip('\n').split('//')[0].split('#')[0]
        if ':' in line:
            flag = 1
            tmptag = line.strip().split(' ',1)[0][:-1]
        if(flag == 1):
            if(len(line.rstrip('\n').strip().split(' ',1))>1):
                tag[tmptag] = line_num
                flag = 0
        line_num = line_num+1
finally:
    file_object.close()

line_num = 0
file_object = open('asm.txt','rU')
try:
    for line in file_object:
        asm(line_num,line.rstrip('\n').split('//')[0].split('#')[0]) #line带"\n",过滤注释
        line_num = line_num+1
finally:
    file_object.close()

