# Version 0.1
# Time: Nov,30,2015
# Auther: Jason Luo
# Content: An easy Interpreter that can only interpret a single digit plus another single digit

# Token Types:
# EOF: End-Of-File

INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'

class Token(object):
    def __init__(self, type, value):
        # Token types: INTEGER, PLUS, EOF
        self.type = type
        # Token value: 0,1,2,3,4,5,6,7,8,9,+,None
        self.value = value

    def __str__(self):
        """
        The format of the print infomation

        For examle:
        Token(INTEGER, 3)
        Token(PLUS, '+')
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

    def error(self):
        raise Exception('Error Parsing Error!')

    def get_next_token(self):
        """
        Lexical Analyzer:

        Parsing the input into tokens.

        Strategy:
        1. is pos past the end of the text?
        2. if so, return EOF
        3. get a character at pos, and decide its type depends on the single char
        4. if it is a digit, then convert it to integer and return INTEGER token
        5. if it is a '+', then return PLUS token
        """
        text = self.text

        if self.pos > len(text) - 1:
            return Token(EOF, None)

        current_char = text[self.pos]

        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token
        
        self.error()

        
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
        self.current_token = self.get_next_token()

        left = self.current_token
        self.eat(INTEGER)

        op = self.current_token
        self.eat(PLUS)

        right = self.current_token
        self.eat(INTEGER)

        result = left.value + right.value
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
                        
        


        

