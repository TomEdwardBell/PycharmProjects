# Precedence rules
# (
# + - )
# * /
# ^

def infix2polish(str):
    items = str.split(' ')
    precedence = {
                '+': 1,
                '-': 1,
                '*': 2,
                '/': 2,
                '^': 3,
                    }




def calc_reverse(str):
    stack = []
    for item in str.split(' '):
        try:
            float(item)
            stack.append(float(item))
        except:
            if item == '+':
                o1, o2 = stack.pop(), stack.pop()
                stack.append(o2 + o1)
            if item == '-':
                o1, o2 = stack.pop(), stack.pop()
                stack.append(o2 - o1)
            if item == '*':
                o1, o2 = stack.pop(), stack.pop()
                stack.append(o2 * o1)
            if item == '/':
                o1, o2 = stack.pop(), stack.pop()
                stack.append(o2 / o1)
            if item == '^':
                o1, o2 = stack.pop(), stack.pop()
                stack.append(o2 ** o1)

    print(stack[0])