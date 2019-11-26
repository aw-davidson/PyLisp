import re
# takes in a string and returns the ouput

# every expression evaluates to a value
# a Lisp expression is either an atom or a list
# atoms are strings or charachters - basically anything but parentheses
# a list is a number of expressions enclosed in parentheses
# Symbols are just entities that you can bind values to
# A list is just the symbol '(', followed by a series of elements separated by spaces, and then a closing ')'.

class Interpreter:
    def __init__(self):
        self.atoms = {
            '+': self.add,
            '-': self.subtract,
            '*': self.multiply,
            '/': self.divide,
            'define': self.define,
            'eq?': self.equals
        }
    # (/ (+ 10 2) 4) => 3
    def evaluate(self, expression):
        if self.isList(expression):
            return self.evaluateList(expression)
        return self.getAtom(expression)
    
    def getAtom(self, atom):
        if self.isInt(atom) or self.isFloat(atom):
            return atom
        return self.atoms[atom]

    def isNum(self, string):
        return self.isFloat(string) or self.isInt(string)

    def isFloat(self, string):
        match = re.match('[0-9]+.[0-9]+', string)
        if match is None:
            return False
        return len(string) == len(match.group())

    def isInt(self, string):
        match = re.match('[0-9]+', string)
        if match is None:
            return False
        return len(string) == len(match.group())


    def isList(self, expression):
        return expression[0] is '(' and expression[-1] is ')'

    def evaluateList(self, expression):
        openParens = expression[0]
        if openParens is not '(':
            raise ValueError(f"{expression} does not begin with (")
        while self.hasParens(expression):
            openInd = 0
            for ind, char in enumerate(expression):
                if char == '(':
                    openInd = ind
                if char == ')':
                    val = self.evaluateBaseList(expression[openInd:ind+1])
                    expression = expression[:openInd] + str(val) + expression[ind+1:]
                    break
        return expression

    def hasParens(self, expression):
        return '(' in expression and ')' in expression

    # (+ 2 3) => 5
    def evaluateBaseList(self, myList):
        myList = list(myList)
        del myList[0]
        del myList[-1]
        myList = "".join(myList)
        splitList = myList.split()
        function = splitList[0]
        vals = self.convertStrToTypes(splitList[1:])
        return self.atoms[function](vals)
    
    def convertStrToTypes(self, stringList):
        newList = []
        for val in stringList:
            if self.isNum(val):
                newList.append(float(val))
            else:
                newList.append(val)
        return newList


    def define(self, vals):
        symbol, expression = vals
        self.atoms[symbol] = self.evaluate(str(expression))

    def equals(self, vals):
        return vals[0] == vals[1]

    def add(self, vals):
        total = 0
        for val in vals:
            total += val
        return total

    def subtract(self, vals):
        total = vals[0]
        for val in vals[1:]:
            total -= val
        return total

    def multiply(self, vals):
        product = 1
        for val in vals:
            product *= val
        return product

    def divide(self, vals):
        product = vals[0]
        for val in vals[1:]:
            product /= val
        return product


inter = Interpreter()

# TESTS
print(inter.evaluate('(* 2 (+ 3 (- 2 1)))'), 8.0)
print(inter.convertStrToTypes(['convert', '22', '111', 'asdasdad']))
running = True
while running:
    userInput = input('Lisp Interpreter: ') 
    val = inter.evaluate(userInput)
    if val is not None:
        print(val)