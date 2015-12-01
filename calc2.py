# Version 0.2
# Time: Dec,1,2015
# Auther: Jason Luo
# Content: An easy Interpreter that can only interpret a multidigit plus or minus another multidigit
# 
#*******************= New Features =********************
# 12.01 Support mutidigit calculation                  *
#       Support minus operation                        *
#*******************************************************


# Token Types:
# EOF: End-Of-File

INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'

class Token(object):
    def __init__(self, type, value):
        # Token types: INTEGER, PLUS, MINUS, EOF
        self.type = type
        # Token value: 0,1,2,3,4,5,6,7,8,9,+,None
        self.value = value

    def __str__(self):
        """
        The format of the print infomation

        For examle:
        Token(INTEGER, 3)
        Token(PLUS, '+')
        Token(MINUS, '-')
        """
        return 'Token({type},{value})'.format(
                type = self.type,
                value = repr(self.value)
                )

    def __repr__(self):
        return self.__str__()
    
class Interpreter(object):
    def __init__(self, text):
        # Process the whole input
        # e.g. 3+5
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error Parsing Error!')

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
        1. is pos past the end of the text?
        2. if so, return EOF
        3. get a character at pos, and decide its type depends on the single char
        4. if it is a space, advance the pos
        5. if it is a digit, then convert it to integer and return INTEGER token
        6. if it is a '+', then return PLUS token
        7. if it is a '-', then return MINUS token
        """

        while self.current_char is not None:

            if self.pos > len(self.text) - 1:
                return Token(EOF, None)

            current_char = self.text[self.pos]

            if current_char.isspace():
                self.skip_whitespace()
                continue

            if current_char.isdigit():
                return Token(INTEGER, self.integer())

            if current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if current_char == '-':
                self.advance()
                return Token(MINUS, '-')
            
        
            self.error()

        return Token(EOF, None)

    def eat(self, token_type):
        # compare the current token with the passed token type
        # if they match then eat the current token and assign next token to the self.current_token
        # otherwise raise an Exception

        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()
    
    def expr(self):
        # expr -> INTEGER PLUS INTEGER
        # expr -> INTEGER MINUS INTEGER
        
        self.current_token = self.get_next_token()

        left = self.current_token
        self.eat(INTEGER)

        op = self.current_token

        if op.type == PLUS:
            self.eat(PLUS)
        else:
            self.eat(MINUS)

        right = self.current_token
        self.eat(INTEGER)

        if op.type == PLUS:
            result = left.value + right.value
        else:
            result = left.value - right.value
        return result
    
def main():
    while True:
        try:
            text = raw_input('cal> ')
        except EOFError:
            break
        if not text:
            continue

        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()
                        
        


        

