# Version 0.5
# Time: Dec,1,2015
# Auther: Jason Luo
# Content: An easy Interpreter that can interpret fundamental expression
#          (Plus, Minus, Multiplication, Division)
# 

#*************************= New Features =**************************
#  v0.5 Modify code for interpreting plus, minus, multiply and     *
#       integer division expression                                *
#------------------------------------------------------------------*
#  v0.4 Modify code for interpret multiplication and integer       *
#       division expression                                        *
#------------------------------------------------------------------*
#  v0.3 Support interpreting more than one mutidigits              *
#------------------------------------------------------------------*
#  v0.2 Support mutidigit calculation                              *
#       Support minus operation                                    *
#*******************************************************************


# Token Types:
# EOF: End-Of-File
INTEGER, PLUS, MINUS, MUL, DIV, EOF = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'EOF'
)
class Token(object):
    def __init__(self, type, value):
        # Token types: INTEGER, PLUS, MINUS, MUL, DIV, EOF
        self.type = type
        # Token value: 0,1,2,3,4,5,6,7,8,9,,+,-,*,/,None
        self.value = value

    def __str__(self):
        """
        The format of the print infomation

        For examle:
        Token(INTEGER, 3)
        Token(PLUS, '+')
        Token(MINUS, '-')
        TOKEN(MUL, '*')
        """
        return 'Token({type},{value})'.format(
                type = self.type,
                value = repr(self.value)
                )

    def __repr__(self):
        return self.__str__()
    
class Lexer(object):
    def __init__(self, text):
        # Process the whole input
        # e.g. 3+ 5 * 2 - 4/2
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character!')
    
    def advance(self):
        # Advance the pos and set current_char
        self.pos += 1

        if self.pos > len(self.text)-1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        # Skip space
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        # Support mutidigit integer
        result = ''
        
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        
        return int(result)

    def get_next_token(self):
        """
        Lexical Analyzer:

        Parsing the input into tokens.

        Strategy:
        1. dictate current char
        2. if it is a space, advance the pos
        3. if it is a digit, then convert it to integer and return INTEGER token
        4. if it is a '+', then return PLUS token
        5. if it is a '-', then return MINUS token
        6. if it is a '*', then return MUL token
        7. if it is a '/', then return DIV token
        """

        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')
            
        
            self.error()

        return Token(EOF, None)

class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        
    def error(self):
        raise Exception('Invalid Syntax')

    def eat(self, token_type):
        # compare the current token with the passed token type
        # if they match then eat the current token and assign next token to the self.current_token
        # otherwise raise an Exception

        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        # return an Integer Token's value
        # factor: Integer
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    
    def term(self):
        # term: factor( (MUL | DIV) factor)*
        # factor: Integer
        result = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token

            if token.type == MUL:
                self.eat(MUL)
                result = result * self.factor()
            elif token.type == DIV:
                self.eat(DIV)
                result = result / self.factor()

        return result

    def expr(self):
        # expr: term( (PLUS | MINUS) term)*
        # term: factor( (MUL | DIV) factor)*
        # factor: Integer
        result = self.term()
        
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()

        return result

def main():
    while True:
        try:
            text = raw_input('cal> ')
        except EOFError:
            break
        if not text:
            continue

        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()
