# -----------------------------------------------------------------------------
# calculator.py
#
# A simple arithmetic calculator.
#
# Code adapted from example at https://www.dabeaz.com/ply/example.html
# -----------------------------------------------------------------------------
import ply.lex as lex
import ply.yacc as yacc

from bluserver.exceptions import (
    CalculatorLexicalException,
    CalculatorSyntacticalException,
)


#
# Lexer
#

tokens = (
    'NUMBER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    )

# Tokens

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    # logger.exception("Illegal character '%s'" % t.value[0])
    raise CalculatorLexicalException("Illegal character '%s'" % t.value[0])

#
# Parser
#


# Precedence rules for the arithmetic operators
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    )


def p_program(p):
    """program : expression"""
    p[0] = p[1]


def p_program_empty(p):
    """program : empty"""
    p[0] = ''


def p_expression_binop(p):
    """expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression"""
    if p[2] == '+'  : p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]


def p_expression_number(p):
    """expression : NUMBER"""
    p[0] = p[1]


def p_empty(p):
    """empty :"""
    pass


def p_error(p):
    # logger.exception('Syntax error')
    raise CalculatorSyntacticalException('Syntax error')
    # "Illegal character '%s'" % t.value[0] if p is not none


# Build the lexer
lex.lex()


# Build the parser and exposes as calculation
calculate = yacc.yacc().parse

