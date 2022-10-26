#! /bin/python3
# Program to step through a set of instructions, one line at a time to assist in keeping your place
# by piCounter Oct, 2022

DEBUG = True
# Import file
import os
if DEBUG:
    print('DEBUG MODE IS ON, check')
    file = 'test.txt'
else:
    file = os.environ['FILE']
height = 12 #default height of terminal
clear_color = '''\033[0m'''

'''
load file as string
parse string into list based on new lines
remove any empty newlines
parse each line for stepnumber and instruction
parse step number into list by '.'
color each number to indicate depth. return as string with uncolored '.' returned

print page of instructions with ambre coloring getting darker as instructions move away from center
in bash
    increment tail by i in a for loop
in python
    print list by i in a for loop
        i - abs(height/2)  ???????
'''



# def strip_blanklines(file):
#     ''' remove whitespace and empty lists '''
#     new_list = []
#     for i in file:
#         if len(i) > 1:
#             new_list.append(i)
#     return new_list

        
def fg_color(num):
    '''foreground color from 0-255'''
    return '\033[38;5;' + str(num) + 'm'


def bg_color(num):
    '''background color from 0-255'''
    return '\033[48;5;' + str(num) + 'm'


def color_step_number(step_number_list):
    '''format step numbers'''
    for num in range(len(step_number_list)):
        step_number_list[num] = bg_color(num) + ' ' + step_number_list[num] + ' ' + clear_color
    return step_number_list


def color_step_instr(step_instructions, offset):
    '''format step instructions'''
    if offset == 0:
        highlight = 186
    else:
        highlight = 255 - offset
    return fg_color(highlight)+step_instructions

def color_step_numbers(line, offset):
    '''print single formatted line
        offset = the center most line'''
    # split up each line for formatting
    # extract step numbers
    cut_index = file[line].index('>')
    step_numbers_string = str(file[line][:cut_index])
    step_numbers_list = step_numbers_string.split('.')
    # extract instructions
    step_instructions = str(file[line][cut_index+1:]).strip('\n')
    # color step numbers
    step_colored_list = color_step_number(step_numbers_list)
    step_number_string = ''
    for i in range(len(step_numbers_list)):
        step_number_string += step_colored_list[i]
    return color_step_instr(step_instructions, abs(offset))

def print_line(step_number_string, instr):
    '''print single line'''
    print("{}{}{}".format(step_number_string, instr, clear_color))
    return None


def print_lines(height, line_number):
    '''print fill screen of lines'''
    for i in range(height):
        offset = round((height+1)/2)-i
        print_line(line_number, offset)
    return None


# main run area
with open(file, 'r') as raw_file:
    list_file = raw_file.readlines()
    file = strip_blanklines(list_file)
    line_number = 1
    while line_number <= len(file):
        if len(file) < height:
            height = len(file)
        print_lines(height, line_number)
        ans = str(input("(q)uit\t(x) to jump steps\n"))
        if ans == 'q':
            break
        try:
            line_number += int(ans)
        except:
            pass
        line_number += 1

