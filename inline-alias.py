import fileinput
import re

reg_names = {
  'r0':0, 'r1':1, 'r2':2, 'r3':3,
  'r4':4, 'r5':5, 'r6':6, 'r7':7,
  'r8':8, 'r9':9, 'r10':10, 'r11':11,
  'r12':12, 'r13':13, 'r14':14, 'r15':15,
  'sp':13, 'lr':14, 'pc':15 }

registers = [None] * 16
inline_re = re.compile(r'\w+:\w+')
unreq_re = re.compile(r'\s*\.unreq\s+all')
for line in fileinput.input():
    inline_defs = inline_re.findall(line)
    for idef in inline_defs:
        alias, reg = idef.split(':')
        line = line.replace(idef, alias, 1)
        if alias in registers:
            registers[registers.index(alias)] = None
        reglow = reg.lower()
        if reglow in reg_names:
            regnum = reg_names[reg.lower()]
            if registers[regnum] is not None:
                print('    .unreq', registers[regnum])
            registers[regnum] = alias
        print('   ', alias, '.req', reg)
    if unreq_re.match(line):
        for alias in registers:
            if alias is not None:
                print('    .unreq', alias)
        registers = [None] * 16
    else:
        print(line.strip('\n'))

