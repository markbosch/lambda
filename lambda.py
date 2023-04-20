# Python universe with only single argumented functions
#
# It's illegal to have numbers, strings, operators, control flow etc.
# PyCon 2019 Tutorial https://www.youtube.com/watch?v=5C6sv7-eTKg
# But, what can you build with it?

# Switch
def LEFT(a):
    def f(b):
        return a # return first argument
    return f

def RIGHT(a):
    def f(b):
        return b # return second argument
    return f

assert LEFT('v5')('gnd') == 'v5'
assert RIGHT('v5')('gnd') == 'gnd'

# lambda = function with parameter(s) e.g. lambda x: x -> creates a function with x as param and returns x
incr = lambda x: x + 1
assert incr(41) == 42

# The truth
def TRUE(x):
    return lambda y: x # return the first argument

def FALSE(x):
    return lambda y: y # return the second argument

assert TRUE('v5')('gnd') == 'v5'
assert FALSE('v5')('gnd') == 'gnd'

assert TRUE(TRUE)(FALSE) is TRUE  # return function TRUE
assert TRUE(FALSE)(TRUE) is FALSE
assert FALSE(FALSE)(TRUE) is TRUE

# The bools
def NOT(x):
    return x(FALSE)(TRUE) # if not false

# NOT(TRUE) is FALSE because TRUE always returns the first argument
# it gets executed as -> TRUE(FALSE)(TRUE)
assert NOT(TRUE) is FALSE
# NOT(FALSE) is the oposit and gets executed as FALSE(FALSE)(TRUE) which is true,
# because FALSE returns the second argument
assert NOT(FALSE) is TRUE

def AND(x):
    return lambda y: x(y)(x)

assert AND(TRUE)(TRUE) is TRUE
assert AND(FALSE)(TRUE) is FALSE
assert AND(FALSE)(FALSE) is FALSE
assert AND(TRUE)(FALSE) is FALSE

def OR(x):
    return lambda y: x(x)(y)

assert OR(TRUE)(FALSE) is TRUE
assert OR(FALSE)(FALSE) is FALSE
assert OR(FALSE)(TRUE) is TRUE
