'''
Natural language calculator by Evan Fredericksen
'''

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
    raw_token_list = split_tokens(user_input)
    # Convert alphabetic strings to corresponding digits
    token_list = alphabetic_to_digit(raw_token_list)
    merge_decimals(token_list)
    combined_token_list = combine(token_list)
    print(combined_token_list)
    processed_input = ''.join(combined_token_list)
    try:
        evaluation = eval(processed_input)
    except:
        evaluation = None
    return processed_input, evaluation
    
def merge_decimals(tokens):
    '''
    Merge numbers following a decimal into the preceding number. Use a zero
    if there is no preceding number.
    '''
    i = 0
    while i < len(tokens) - 1:
        if tokens[i] == '.':
            decimals = ''
            while i+1 < len(tokens) and tokens[i+1].isdigit():
                decimals += tokens[i+1]
                del tokens[i+1]
            if i > 0 and tokens[i-1].isdigit():
                tokens[i-1] += '.{0}'.format(decimals)
                del tokens[i]
                i -= 1
            else:
                tokens[i] = '0.{0}'.format(decimals)
        i += 1

def alphabetic_to_digit(raw_tokens):
    '''
    Convert alphabetic number representations into digits.
    '''
    token_list = []
    for token in raw_tokens:
        for group in NUMBERS:
            if token in group:
                token_list.append(group[token])
                break
        else:
            token_list.append(token)
    return token_list
    
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
    for index, char in enumerate(user_input):
        token += char.lower()
        if token in DIGITS:
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
                token_list.append(token)
                token = ''
        elif token in TEENS or token in TENS or token in LARGER:
            token_list.append(token)
            token = ''
        elif token in TERMS:
           token_list.append(token)
           token = ''
        elif token[:-1].replace('.', '').isdigit() and not token[-1].isdigit() and token[-1] != '.':
            token_list.append(token[:-1])
            token = token[-1]
        elif not token[:-1].replace('.', '').isdigit() and (token[-1].isdigit() or token[-1] == '.'):
            token_list.append(token[:-1])
            token = token[-1]   
        else:
            for k, v in OPERATORS.items():
                if token in (k, v):
                   token_list.append(v)
                   token = ''
                   break               
        for d in DELIMETERS:
            if d in token:
                # String slicing to remove delimiter at the end
                token = token[:-(len(d))]
                if len(token):
                    token_list.append(token)
                    token = ''
                    break
            elif index == len(user_input) - 1 and len(token):
                token_list.append(token)
                token = ''
                break
    return token_list