#! /bin/python3
# parse Alves instructions and save in a .csv with the same name

DEBUG = True

import os

clear_color = '''\033[0m'''

class Pretty:
    if DEBUG:
        print('DEBUG MODE IS ON')
        file = 'test.txt'
    else:
        file = os.environ['FILE']

    def __init__(self, file):
        self.f = file

    def strip_blanklines(self):
        '''Remove any blank lines in list object'''
        new_list = []
        for i in self.f:
            if len(i) > 1:
                new_list.append(i)
        return new_list

    def color_numbers(self):
        # iterate over entire file
        for i in self.f:
            # split apart numbers and instructions
            split_point = self.f[i].index('>')
            number = self.f[i][:split_point]
            instr = self.f[i][split_point + 1:]
            # format step numbers
            for j in range(len(number)):
                # skip over . and redefine color for only numbers
                if number[j] != '.':
                    number[j] = '\033[38;5;' + str(j) + 'm' + ' ' + number[j] + ' ' + clear_color
            self.f[i] = number + instr     
        return self.f

    def save_new_file(self):
        pass

    with open(file, 'r') as f:
        f = f.readlines()
        f = f.strip_blanklines()
        f = f.color_numbers()
        f.save_new_file()
