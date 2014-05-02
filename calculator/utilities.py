'''
Natural language calculator by Evan Fredericksen
'''

import re
from calculator import constants

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
    '^': '**',
    'mod': '%',
    'modulus': '%',
    '(': '(',
    ')': ')',
    'dot': '.',
    'point': '.',
    'negative': '-',
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
    # print(token_list)
    # Convert alphabetic strings to corresponding digits
    combined_token_list = combine(token_list)
    processed_input = ''.join(combined_token_list)
    try:
        evaluation = eval(processed_input)
    except:
        evaluation = None
    return processed_input, evaluation
    
def get_unit_dictionary(tokens):
    pass

def combine(tokens):
    '''
    Find the smallest number in list of token strings with a smaller
    adjacent number. Multiply that number by the sum of smaller numbers
    on the left and add that to the sum of smaller numbers on the
    right. Run recursively until no consecutive numbers remain.
    '''
    consecutive = False
    count = 0
    for t in tokens:
        if t.isdigit():
            if consecutive:
                count += 1
            consecutive = True
        else:
            consecutive = False
    # base case
    if count <= 0:
        return tokens
    else:
        smallest = None
        for index, t in enumerate(tokens):
            if t.replace('.', '').isdigit():
                if ((index > 0 and tokens[index-1].replace('.', '').isdigit() and float(tokens[index-1]) <= float(t)) or
                (index < len(tokens) - 1 and tokens[index+1].replace('.', '').isdigit() and float(tokens[index+1]) <= float(t))):
                    if smallest is None:
                        smallest = int(t)
                    elif int(t) < smallest:
                        smallest = int(t)
        index = tokens.index(str(smallest))
        right_sum = 0
        while (index < len(tokens) - 1 and tokens[index+1].replace('.', '').isdigit() and
        smallest >= float(tokens[index+1])):
            try:
                right_sum += int(tokens[index+1])
            except ValueError:
                right_sum += float(tokens[index+1])
            del tokens[index+1]
        left_sum = 0
        while (index > 0 and tokens[index-1].replace('.', '').isdigit() and
        smallest >= float(tokens[index-1])):
            try:
                left_sum += int(tokens[index-1])
            except ValueError:
                right_sum += float(tokens[index+1])
            del tokens[index-1]
            index -= 1
        if left_sum == 0:
            left_sum = 1
        tokens[index] = str(int(tokens[index]) * left_sum + right_sum)
        return combine(tokens)

def split_tokens(user_input):
    '''
    Apply delimiters to break up user input into list of strings for
    easier processing.
    '''
    token_list = []
    token = ''
    previous = None
    valid_token = False
    for index, char in enumerate(user_input):
        token += char.lower()
        if (index == len(user_input) - 1 or
            token in TEENS or
            token in TENS or
            token in LARGER or
            token in OPERATORS.values()):
            valid_token = True
        elif token in OPERATORS:
            token = OPERATORS[token]
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
            for group in NUMBERS:
                if token in group:
                    token = group[token]
                    break
            add_token(token_list, token, previous)
            previous = token
            token = ''
            valid_token = False
    return token_list
    
def add_token(token_list, token, previous):
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
            