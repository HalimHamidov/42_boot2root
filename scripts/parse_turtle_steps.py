import re

def parse_line(line):
    regres = re.search(r'\d+', line)
    if regres:
        size = int(regres.group())
        if line.startswith('Tourne gauche'):
            return f't.left({size})\n'
        elif line.startswith('Tourne droite'):
            return f't.right({size})\n'
        elif line.startswith('Avance'):
            return f't.forward({size})\n'
        elif line.startswith('Recule'):
            return f't.backward({size})\n'
        else:
            print(line)
            return ""
    else:
        print(line)
        return ""

result = 'import turtle\ns = turtle.Screen()\nt = turtle.Turtle()\n'
with open('./turtle', 'r') as f:
    line = f.readline()
    while line:
        result += parse_line(line)
        line = f.readline()

with open('./turtle_script.py', 'w') as f:
    print(result, file=f)