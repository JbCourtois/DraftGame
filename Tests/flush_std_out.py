# -*- coding: utf-8 -*-
import sys
import os

is_windows = os.name == 'nt'


print(raw_input('Type something! '))
print('LOL')
sys.stdout.flush()
sys.stdin.flush()
print('Flushed')


print(raw_input('Type something! '))
print('LOL')
os.system('cls' if is_windows else 'clear')  # For Windows
print('Flushed')
