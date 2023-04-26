# parser.py
#

shift   = lambda inp: bool(inp) and (inp[0], inp[1:])
nothing = lambda inp: (None, inp) # Opposing function of shift, have input but do nothing

assert shift('bar') == ('b', 'ar')
assert shift('ar') == ('a', 'r')
assert shift('r') == ('r', '')
assert shift('') == False

assert nothing('bar') == (None, 'bar')

# A Parsing System
# rules, only use the two parsers provided (shift & nothing)
# and allowed to create new parsers with lambda based on the
# existing parsers.

# Apply a predicate to the result of a parser
filt = lambda predicate: (
         lambda parser:
           lambda inp: (m:=parser(inp)) and predicate(m[0]) and m)

digit = filt(str.isdigit)(shift)
letter = filt(str.isalpha)(shift)

assert digit('456') == ('4', '56')
assert letter('456') == False

# Filter for exactly matching a literal
literal = lambda value: filt(lambda v: v == value)
# Filter where values must come from a predefined set of accetable values
memberof = lambda values : filt(lambda v: v in values)

dot = literal('.')(shift)
even = memberof('02468')(digit)

assert dot('.456') == ('.', '456')
assert dot('45.6') == False
assert even('456') == ('4', '56')
assert even('345') == False

# simplify
char = lambda v: literal(v)(shift)

dot = char('.')
assert dot('.456') == ('.', '456')

# The opposite of filter - which ignores things - is to do things -> map
# fmap takes a function and parser as input and creates a new parser
# wherein the supplied function is applied
fmap = lambda f: (
         lambda parser:
           lambda inp: (m:=parser(inp)) and (f(m[0]), m[1]))

# transform values
ndigit = fmap(int)(digit)
assert ndigit('456') == (4, '56')
tenx = fmap(lambda x: 10*x)
assert tenx(ndigit)('456') == (40, '56')
assert tenx(digit)('456') == ('4444444444', '56')

def one_or_more(parser):         # input is a parser
    def parse(inp):             # create a new parser
        result = [ ]
        while (m:=parser(inp)):  # while input parser parse - until False - 
            value, inp = m       # get value and inp
            result.append(value) # append value
        return bool(result) and (result, inp) # new parser
    return parse # return the parser

digit = filt(str.isdigit)(shift)
digits = one_or_more(digit)
assert digits('456') == (['4', '5', '6'], '')
assert digits('bar') == False

# if you want them back together, use fmap
# digits = fmap(''.join)(one_or_more(digit))
# digits('456') == ('456', '')

# Sequencing operator
# multiple parsers as input which all needs to succeed
# for a successful parse
def seq(*parsers):
    def parse(inp):
        result = [ ]
        for p in parsers:
            if not (m:=p(inp)):
                return False
            value, inp = m
            result.append(value)
        return (result, inp)
    return parse

assert seq(letter, digit, letter)('a4x') == (['a', '4', 'x'], '')
assert seq(letter, digit, letter)('bar') == False
assert seq(letter, fmap(''.join)(one_or_more(digit)))('x12345') == (['x', '12345'], '')

left = lambda p1, p2: fmap(lambda p: p[0])(seq(p1, p2))
right = lambda p1, p2: fmap(lambda p: p[1])(seq(p1, p2))

assert left(letter, digit)('a4') == ('a', '')
assert right(letter, digit)('a4') == ('4', '')

# Choice

either = lambda p1, p2: (lambda inp: p1(inp) or p2(inp))
alnum = either(letter, digit)
assert alnum('4a') == ('4', 'a')
assert alnum('a4') == ('a', '4')
assert alnum('$4') == False

maybe = lambda parser: either(parser, nothing)
assert maybe(digit)('456') == ('4', '56')
assert maybe(digit)('abc') == (None, 'abc')

zero_or_more = lambda parser: either(one_or_more(parser), seq())
assert zero_or_more(digit)('456') == (['4', '5', '6'], '')
assert zero_or_more(digit)('abc') == ([], 'abc')

choice = lambda parser, *parsers: (
            either(parser, choice(*parsers)) if parsers else parser)

# Numbers
#
# Integers or Decimals
# Decimals: 12.34, 12., or .34

dot = char('.')
digit = filt(str.isdigit)(shift)
digits = fmap(''.join)(one_or_more(digit))
decdigits = fmap(''.join)(choice(
               seq(digits, dot, digits),
               seq(digits, dot),
               seq(dot, digits)))

integer = fmap(int)(digits)
decimal = fmap(float)(decdigits)
number = choice(decimal, integer)

# Let's try it out
assert number('1234') == (1234, '')
assert number('12.3') == (12.3, '')
assert number('.123') == (0.123, '')
assert number('123.') == (123.0, '')
assert number('.foo') == False

# Key-value pairs

letter = filt(str.isalpha)(shift)
letters = fmap(''.join)(one_or_more(letter))
ws = zero_or_more(filt(str.isspace)(shift))
token = lambda p: right(ws, p)
eq = token(char('='))
semi = token(char(';'))
name = token(letters)
value = token(number)
keyvalue = seq(left(name, eq), left(value, semi))

assert keyvalue('xyz=123;') == (['xyz', 123], '')
assert keyvalue('    pi = 3.14   ;') == (['pi', 3.14], '')

# Dictionary

keyvalues = fmap(dict)(zero_or_more(keyvalue))

assert keyvalues('x=2; y=3.4; z=.789;') == ({'x': 2, 'y': 3.4, 'z': 0.789}, '')
assert keyvalues('') == ({}, '')
