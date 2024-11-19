stack = [0, 0, 0, 0, 0]
sp = -1

def iconst(x):
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
    iconst(op(lhs, rhs))

def isub():
    bop(lambda x,y:x-y)

def irem():
    bop(lambda x,y:x%y)

def iadd():
    bop(lambda x,y:x+y)

def iload(i):
    iconst(args[i])

def ishl():
    bop(lambda x,y:x<<y)

def ishr():
    bop(lambda x,y:x>>y)

def ior():
    bop(lambda x,y:x|y)

def imul():
    bop(lambda x,y:x*y)

def idiv():
    bop(lambda x,y:x/y)

def iand():
    bop(lambda x,y:x&y)


args = [2, 4]
iload(1)
iconst(2)
isub()
iload(1)
iadd()
iload(0)
iconst(1)
ishr()
isub()
print(pop())