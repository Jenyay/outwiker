#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Увеличить новер версии на 1. Т.к. скрипт не попадет к пользователям, то никаких проверок нет.
"""

# Файл с номером версии
fname = u"src/version.txt"

with open (fname) as fp_in:
    lines = fp_in.readlines()

lines[1] = str (int (lines[1]) + 1) + "\n"

result = u"".join (lines)

with open (fname, "w") as fp_out:
    fp_out.write (result)

print result
