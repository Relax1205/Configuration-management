stack = [0, 0, 0, 0, 0]
sp = -1
def push(x):
    global sp
    sp+=1
    stack[sp] = x
def pop():
    global sp
    x = stack[sp]
    sp-=1
    return x

def bop(op):
    rhs = pop()
    lhs = pop()
    push(op(lhs, rhs))

x = 4
y = 5
push(x)
push(2)
bop(lambda x,y:x<<y)
push(4)
bop(lambda x,y:x+y)
push(3)
bop(lambda x,y:x-y)
print(pop())