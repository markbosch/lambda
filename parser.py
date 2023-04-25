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

