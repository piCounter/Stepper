#! /bin/python3
# Program to step through a set of instructions, one line at a time to assist in keeping your place
# by piCounter Oct, 2022
DEBUG = False
# Import file
import os
if DEBUG:
    print('DEBUG MODE IS ON, check')
    file = 'test.txt'
else:
    file = os.environ['FILE']
height = 12 #set to default height of terminal
clear_color = '''\033[0m'''


def _strip_blanklines(file):
    ''' remove whitespace and empty lists '''
    new_list = []
    for i in file:
        if len(i) > 1:
            new_list.append(i)
    return new_list

        
def _fg_color(num):
    '''foreground color from 0-255'''
    return '\033[38;5;' + str(num) + 'm'


def _bg_color(num):
    '''background color from 0-255'''
    try:
#        colors = {
#                '0' : '1',      #red
#                '1' : '40',     #green
#                '2' : '11',     #yellow
#                '3' : '129',    #purple
#                '4' : '154',    #greenyellow
#                '5' : '126',    #purplered
#                '6' : '202',    #orangered
#                '7' : '43',     #bluegreen
#                '8' : '21',     #blue
#                '9' : '208',    #orange
#        }
        # shades of blue green
        colors = {
                '0' : '19',
                '1' : '24',
                '2' : '29',
                '3' : '34',
                '4' : '21',
                '5' : '26',
                '6' : '31',
                '7' : '36',
                '8' : '41',
                '9' : '46',
        }
        color = colors[num]
    except:
        color = num
#    return '\033[48;5;' + str(num) + 'm'
    return '\033[48;5;' + str(color) + 'm'


#def _color_step_number_as_list(step_number_list):
#    '''format step numbers'''
#    for num in range(len(step_number_list)):
#        step_number_list[num] = _bg_color(num) + ' ' + step_number_list[num] + ' ' + clear_color
#    return step_number_list

def _color_step_by_number_as_list(step_number_list):
    '''format step numbers'''
    index = 0
    for num in step_number_list:
        step_number_list[index] = _bg_color(num) + ' ' + step_number_list[index] + ' ' + clear_color
        index += 1
    return step_number_list

def _color_step_instr(step_instructions, offset):
    '''format step instructions'''
    offset = abs(offset-1)
    if offset == 0:
        highlight = 186
    else:
        highlight = 255 - offset
    return _fg_color(highlight)+step_instructions


def _color_step_number_list_to_string(step_number_list):
    '''print single formatted line'''
   # color step numbers
#    step_colored_list = _color_step_number_as_list(step_number_list)
    step_colored_list = _color_step_by_number_as_list(step_number_list)
    step_number_string = ''
    for i in range(len(step_number_list)):
        step_number_string += step_colored_list[i]
    return step_number_string


def split_line(line, offset):
    # split up each line for formatting
    try:
        cut_index = list_file[line].index('>')
    except:
        cut_index = 0

    # extract step numbers
    step_numbers_string = str(list_file[line][:cut_index])
    step_numbers_list = step_numbers_string.split('.')
    # extract instructions
    step_instructions_string = str(list_file[line][cut_index+0:]).strip('\n')
    instructions = _color_step_instr(step_instructions_string, offset)
    step_number = _color_step_number_list_to_string(step_numbers_list)
    colored_line_list = [ step_number, instructions ]
    return colored_line_list


def print_line(colored_line_list):
    '''print single line '''
    print("{}{}{}\n".format(colored_line_list[0], colored_line_list[1], clear_color))
    return None


def print_lines(height, current_line_number):
    '''print fill screen of lines'''
    for i in range(height):
        distance_from_center = round((height)/2)-i
        print_line(split_line(current_line_number - distance_from_center, distance_from_center))
    return None


# main run area
with open(file, 'r') as raw_file:
    '''
    read file as large string. parce into list by line.
    split list items (lines) by step number and instruction.
    color step number to highlight stepping in and out of steps
    print screen of lines with middle most line highlighted for emphasis.
    have step color fade around current instruction
    terminate gracefully
    '''
    list_file_w_blanklines = raw_file.readlines()
    global list_file
    list_file = _strip_blanklines(list_file_w_blanklines)
    current_line_number = 1
    while current_line_number <= len(list_file):
        if len(list_file) < height:
            height = len(list_file)
        print_lines(height, current_line_number)
        ans = str(input("(q)uit\t(x) to jump steps\n"))
        if ans == 'q':
            break
        try:
            current_line_number += int(ans)
        except:
            pass
        current_line_number += 1

