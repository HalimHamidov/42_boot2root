import os
import re

arr = os.listdir('./')
nums = []
lines = []
for path in arr:
    with open(path, 'r') as f:
        line = f.readline()
        code = ""
        num = None
        while line:
            if line.startswith('//'):
                regres = re.search(r'\d+', line)
                if regres:
                    num = int(regres.group())
            else:
                code += line
            line = f.readline()
        if num:
            nums.append(num)
            lines.append(code)

print(len(nums), len(lines))
res = [None] * len(nums)
for i in range(0, len(nums)):
    if nums[i] is not None:
        res[nums[i] - 1] = lines[i]

with open('../prog.c', 'w') as f:
    for line in res:
        if line is not None:
            print(line, file = f)