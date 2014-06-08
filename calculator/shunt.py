#!/usr/bin/python

import sys

#Associativity constants for operators
LEFT_ASSOC = 0
RIGHT_ASSOC = 1

#Supported operators
OPERATORS = {
    '+' : (0, LEFT_ASSOC),
    '-' : (0, LEFT_ASSOC),
    '#' : (10, RIGHT_ASSOC),
    '*' : (5, LEFT_ASSOC),
    '/' : (5, LEFT_ASSOC),
    '%' : (5, LEFT_ASSOC),
    '^' : (10, RIGHT_ASSOC),
}

def is_operator(token):
    return token in OPERATORS

#Test the associativity type of a certain token
def is_associative(token, assoc):
    if not is_operator(token):
        raise ValueError('Invalid token: %s' % token)
    return OPERATORS[token][1] == assoc

#Compare the precedence of two tokens
def cmp_precedence(token1, token2):
    if not is_operator(token1) or not is_operator(token2):
        raise ValueError('Invalid tokens: {0} {1}'.format(token1, token2))
    return OPERATORS[token1][0] - OPERATORS[token2][0]

def infix_to_rpn(tokens):
    '''
    Implement a shunting-yard algorithm to convert tokens in infix to their
    Reverse Polish Notation equivalent. Original version:
    http://andreinc.net/2010/10/05/converting-infix-to-rpn-shunting-yard-algorithm/
    '''
    rpn = []
    stack = []
    for token in tokens:
        if is_operator(token):
            while len(stack) and is_operator(stack[-1]):
                if ((is_associative(token, LEFT_ASSOC) and
                    cmp_precedence(token, stack[-1]) <= 0) or
                    (is_associative(token, RIGHT_ASSOC) and
                    cmp_precedence(token, stack[-1]) < 0)):
                    rpn.append(stack.pop())
                    continue
                break
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while len(stack) and stack[-1] != '(':
                rpn.append(stack.pop())
            stack.pop()
        else:
            rpn.append(token)
    while len(stack):
        rpn.append(stack.pop())
    return rpn
   
def evaluate_rpn(tokens):
    '''
    Return evaluation of list of tokens in RPN form. Return None if unable to
    evaluate.
    '''
    stack = []
    for token in tokens:
        if token.replace('.', '').replace('-', '').isdigit():
            stack.append(token)
        elif token == '#':
            try:
                v = stack.pop()
                stack.append('({0})'.format(eval('-{0}'.format(v))))
            except IndexError:
                return
        else:
            try:
                v2 = stack.pop()
                v1 = stack.pop()
                if token == '^': token = '**'
                stack.append(eval('{0}{1}{2}'.format(v1, token, v2)))
            except IndexError:
                return
    if len(stack) == 1:
        return stack[0]
            