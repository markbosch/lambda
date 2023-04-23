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

# Function definitions
# def AND(x):
#   def f(y):
#       return x(y)(x)
#   return f
#
# shorter with lambda
# def AND(x):
#     return lambda y: x(y)(x)
#
# Even shorter
# AND = lambda x: lambda y: x(y)(x) # or
# AND = lambda xy: x(y)(x) # although illegal, two argumented function
# AND = lambda: xy:xyx
# AND = lamdba: xy.xyx # :'D

# lambda = function with parameter(s) e.g. lambda x: x -> creates a function with x as param and returns x
#incr = lambda x: x + 1
#assert incr(41) == 42

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

# Arithmetic
# Add
ADD = lambda x: lambda y: y(SUCC)(x) # Take SUCC and apply it times the other
assert ADD(FOUR)(THREE)(incr)(0) == 7

# Multi
MUL = lambda x: lambda y: lambda f: y(x(f)) # Execute y times the function with x
assert MUL(FOUR)(THREE)(incr)(0) == 12

# Data (structures)
# define functions for representing a simple data structure (pair)
# In LISP
#
# cons is a pair (tuple) datastructure
# car will select the first
# cdr will select the second
# (cons 2 3)     -> (2, 3)
# (car p)        -> 2
# (cdr p)        -> 3
# car and cdr come from the IMB 704

# Illegal in the single arg. universe
def cons(a, b):
    def select(m):
        if m == 0:
            return a
        elif m == 1:
            return b
    return select

p = cons(2, 3)
p
p(0)
p(1)

def car(p):
    return p(0)

def cdr(p):
    return p(1)

# These are not illegal!
CONS = lambda a: lambda b: lambda s: s(a)(b) # s -> select left or right
CAR = lambda p: p(TRUE)  # TRUE selects the first one
CDR = lambda p: p(FALSE) # FALSE selects the second one

assert CONS(2)(3)(TRUE) == 2
assert CAR(CONS(2)(3)) == 2
assert CDR(CONS(2)(3)) == 3

# Linked list
CONS(2)(CONS(3)(4))

# Can you subtract? the reverse
# THREE, how to get TWO?

# tuple with + 1
# (0, 0)
# (1, 0)
# (2, 1)
# (3, 2)
# (n + 1, n)
def t(p):
    return (p[0]+1, p[0]) # Is illegal, because of the + 1

THREE(t)((0,0))

# Lambda version of t
# p[0] = CAR... the first / left one
# T = you have a pair, make a CONS and apply SUCC (is next value) on CAR (left value) of p
# which results in CAR + 1 and apply CAR again for the other value of the pair
# input (0, 0) -> output (1, 0)  
T = lambda p: CONS(SUCC(CAR(p)))(CAR(p)) 

assert CAR(FOUR(T)(CONS(ZERO)(ZERO)))(incr)(0) == 4
a = FOUR(T)(CONS(ZERO)(ZERO))
assert CAR(a)(incr)(0) == 4
assert CDR(a)(incr)(0) == 3 # reverse

# Predecessor
# count from 0 -> to x and then take the predecessor from pairs
PRED = lambda n: CDR(n(T)(CONS(ZERO)(ZERO)))
a = FOUR(THREE) # = 81 -> 3^4 -> 3 * 3 * 3 * 3
b = PRED(a) # (0, 0) (1, 0) (2, 1) ... etc (81, 80)
assert b(incr)(0) == 80

# Substract
SUB = lambda x: lambda y: y(PRED)(x)
assert SUB(FOUR)(TWO)(incr)(0) == 2

# Test a number for zero
# ZERO doesn't execute a function, therefor TRUE will be returned
# for all other numbers fALSE will be executed
ISZERO = lambda n: n(lambda f: FALSE)(TRUE)
ISZERO(ZERO) # returns TRUE function
ISZERO(ONE) # returns FALSE

# The assembly

# Recursion

# Factorial
def fact(n):
    if n == 0:
        return 1
    else:
        return n*fact(n-1)

assert fact(4) == 24 # Illegal

# Need a 'lazy' evaluation because both branches of ISZERO are
# getting evaluated which gives a max depth recursion error.

#FACT = lambda n: ISZERO(n)\
#                 (ONE)\
#                 (MUL(n)(FACT(PRED(n))))


LAZY_TRUE = lambda x: lambda y: x()
LAZY_FALSE = lambda x: lambda y: y()
ISZERO = lambda n: n(lambda f: LAZY_FALSE)(LAZY_TRUE)

FACT = lambda n: ISZERO(n)\
                 (lambda: ONE)\
                 (lambda: MUL(n)(FACT(PRED(n))))

assert FACT(THREE)(incr)(0) == 6
