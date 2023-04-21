# Python universe with only single argumented functions - lambda
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

# Passing a 'second' argument is called Currying in lambda, although the function
# only accepts one argument
# https://en.wikipedia.org/wiki/Currying
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
# NOT(FALSE) is the opposite and gets executed as FALSE(FALSE)(TRUE) which is true,
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

# Numbers
# They are not numbers, but behaviours
# https://en.wikipedia.org/wiki/Church_encoding
# API for a number f(x)

ZERO = lambda f: lambda x: x   # no use of the 'f' function, same impl as false. Do nothing
ONE = lambda f: lambda x: f(x) # do one function call on x
TWO = lambda f: lambda x: f(f(x)) # Two functions call on x
THREE = lambda f: lambda x: f(f(f(x)))
FOUR = lambda f: lambda x: f(f(f(f(x))))

# Debug, so that you can 'see' what the behaviour is of the functions
def incr(x):
    return x + 1    # Illegal in rules

assert incr(0) == 1
assert incr(incr(0)) == 2
assert THREE(incr)(0) == 3 # do three times incr with starting point 0
# doing FOUR(THREE) which will be 81... crazy! :0
assert FOUR(THREE)(incr)(0) == 81 # 3^4 -> 3 * 3 * 3 * 3
assert ZERO(incr)(0) == 0

# Math
# Successor, which will get to the next number
# SUCC(TWO) --> THREE
# The 'API' of a number is f(x), in order to implement a successor
# you must add an other function too it and then call the API of number.
SUCC = lambda n: (lambda f: lambda x: f(n(f)(x)))

assert SUCC(FOUR)(incr)(0) == 5 # successor of 4 -> 5
assert SUCC(SUCC(FOUR))(incr)(0) == 6

# Add
ADD = lambda x: lambda y: y(SUCC)(x) # Take SUCC and apply it times the other
assert ADD(FOUR)(THREE)(incr)(0) == 7

# Multi
MUL = lambda x: lambda y: lambda f: y(x(f)) # Execute y times the function with x
assert MUL(FOUR)(THREE)(incr)(0) == 12
