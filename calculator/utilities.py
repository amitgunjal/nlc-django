'''
Natural language calculator by Evan Fredericksen
'''

import re
from calculator import constants
from calculator import objects
from calculator import shunt

DELIMETERS = [' ', 'and']

DIGITS = {
    'zero': '0',
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}

TEENS = {
    'ten': '10',
    'eleven': '11',
    'twelve': '12',
    'thirteen': '13',
    'fourteen': '14',
    'fifteen': '15',
    'sixteen': '16',
    'seventeen': '17',
    'eighteen': '18',
    'nineteen': '19',
}

TENS = {
    'twenty': '20',
    'thirty': '30',
    'forty': '40',
    'fifty': '50',
    'sixty': '60',
    'seventy': '70',
    'eighty': '80',
    'ninety': '90',
}

LARGER = {
    'hundred': '100',
    'thousand': '1000',
    'million': '1000000',
    'billion': '1000000000',
    'trillion': '1000000000000',
}

NUMBERS = (DIGITS, TEENS, TENS, LARGER)

OPERATORS = {
    'plus': '+',
    'minus': '-',
    'times': '*',
    '\\': '/',
    'over': '/',
    '^': '^',
    'mod': '%',
    'modulus': '%',
    'negative': '-',
}
OTHER = {
    '(': '(',
    ')': ')',
    'dot': '.',
    'point': '.',
}

TERMS = (
    'mph',
)

def process_string(user_input):
    '''
    Process user input. Return processed input and value to which it
    evaluates.
    '''
    token_list = split_tokens(user_input)
    # Convert alphabetic strings to corresponding digits
    combined_token_list = combine(token_list)
    rpn = shunt.infix_to_rpn(combined_token_list)
    evaluation = shunt.evaluate_rpn(rpn)
    if evaluation is None: return None
    evaluation = str(evaluation).replace('(', '').replace(')', '')
    if '.' in str(evaluation): return float(evaluation)
    return int(evaluation)
    
def get_unit_dictionary(tokens):
    pass

def combine(tokens):
    '''
    Add adjacent numbers together. Return updated list.
    '''
    combined = []
    for token in tokens:
        if (len(combined) > 0 and combined[-1].replace('.', '').isdigit()
        and token.replace('.', '').isdigit()):
            if '.' in combined[-1] or '.' in token:
                combined[-1] = str(float(combined[-1]) + float(token))
            else:
                combined[-1] = str(int(combined[-1]) + int(token))
        else:
            combined.append(token)       
    return combined

def split_tokens(user_input):
    '''
    Apply delimiters to break up user input into list of strings for
    easier processing.
    '''
    token_list = []
    input_list = []
    token = ''
    previous = None
    valid_token = False
    for index, char in enumerate(user_input):
        token += char.lower()
        if index == len(user_input) - 1:
            valid_token = True
        elif (token in TEENS or
             token in TENS or
             token in LARGER or
             token in OPERATORS.values() or
             token in OTHER.values()):
            valid_token = True
        elif token in OPERATORS:
            token = OPERATORS[token]
            valid_token = True
        elif token in OTHER:
            token = OTHER[token]
            valid_token = True
        elif token in DIGITS:
            # Need to handle overlaps like "seventy" or "fourteen"
            try:
                if ((token + 'teen' in TEENS and
                user_input[index+1: index+5].lower() == 'teen') or
                (token + 'ty' in TENS and
                user_input[index+1: index+3].lower() == 'ty') or
                (token == 'eight' and (user_input[index+1].lower() == 'y' or
                user_input[index+1:index+4].lower() == 'een'))):
                    continue
            except IndexError:
                pass
            else:
                valid_token = True
        elif token[-1].isdigit() and not user_input[index+1].isdigit():
             valid_token = True
        else:
            for d in DELIMETERS:
                if d in token:
                    # String slicing to remove delimiter at the end
                    token = token[:-(len(d))]
                    if len(token):
                        valid_token = True
                        break
        if valid_token:
            input_list.append(token)
            token = word_to_number(token)
            add_token(token_list, token, previous)
            previous = token
            token = ''
            valid_token = False
    valid = verify_input(input_list)
    if not valid: return []
    return token_list
    
def verify_input(input_list):
    '''
    Check user input to verify the following:
    * No consecutive numbers consisting of digits
    * Any number that is larger than the preceding number must begin with "1", followed exclusively by at least 2 zeroes
    * No overlap of places in a decreasing sequence of numbers ie:
        "480 77" is bad
        "400 77" and "480 7" are both fine
    * Any number containing ten cannot precede a smaller number ie "410 three" is a no go
    * Ignore the above when the numbers follow a decimal point
    '''
    decimal = False
    num = ''
    prev_num = ''
    for index, token in enumerate(input_list[1:], start=1):
        num = word_to_number(token)
        prev_num = word_to_number(input_list[index-1])
        if token == '.': decimal = True
        if not decimal:
            # First we look at tokens before they are converted to numerical form to ensure that they aren't both digit-based
            if token.replace('.', '').isdigit() and input_list[index-1].replace('.', '').isdigit():
                return False
             # Now we look at the numerical form
            if num.replace('.', '').isdigit():
                # if this token and the preceding token are numbers:
                if prev_num.replace('.', '').isdigit():
                    if float(num) == float(prev_num):
                        return False
                    elif float(prev_num) < float(num):
                        if re.match(r'100+$', num) is None: return False
                    elif float(prev_num) > float(num):
                        if len(prev_num) < 2: return False
                        if prev_num[-2] == '1': return False
                        for z in zip(reversed(prev_num), reversed(num)):
                            if z.count('0') == 0: return False
            else:
                decimal = False
    return True

def word_to_number(token):
    for group in NUMBERS:
        if token in group:
            return group[token]
    return token

def add_token(token_list, token, previous):
    if (token == '-' and (len(token_list) < 1 or
                          token_list[-1] == '(' or
                          token_list[-1] in OPERATORS or
                          token_list[-1] in OPERATORS.values())):
        token_list.append('#')
        return
    # Convert ** to ^ for Reverse Polish Notation
    if token == '*' and previous == '*':
        token_list[-1] = '^'
    else:
        try:
            if token_list[-1].isdigit() and token == '.':
                token_list[-1] += '.'
                return
        except IndexError:
            pass
        if (len(token_list) >= 1 and token_list[-1].count('.') == 1 and
        token_list[-1].replace('.', '').isdigit() and token.isdigit()):
            # if the decimal place for token is less than the previous number and all
            # of the matching digits on the previous token are zeros, then we merge our
            # current decimal value with the larger preceding one
            s = token_list[-1].split('.')
            if len(s[1]) > len(token) and s[1][-len(token):].count('0') >= len(token):
                prev = list(s[1])
                start = -len(token)
                for i in range(start, 0, 1):
                    prev[i] = token[i-start]
                s[1] = ''.join(prev)
            else:
                # otherwise we append
                s[1] += token
            token_list[-1] = '.'.join(s)
        else: 
            try:
                if previous != None and float(token) > float(previous):
                    if '.' in token or '.' in previous:
                        token_list[-1] = str(float(token_list[-1]) * float(token))
                    else:
                        token_list[-1] = str(int(token_list[-1]) * int(token))
                elif previous != None and float(previous) < 100 and float(token)< float(previous):
                    if '.' in token or '.' in previous:
                        token_list[-1] = str(float(token_list[-1]) + float(token))
                    else:
                        token_list[-1] = str(int(token_list[-1]) + int(token))
                else:
                    token_list.append(token)
            except ValueError:
                token_list.append(token)
            