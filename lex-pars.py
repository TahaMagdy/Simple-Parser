import ply.lex  as lex
import ply.yacc as yacc
import sys

flag = 0
# The Grammar {{{
# with one or more column
    # SELECT column_name, column_name
    # FROM table_name;
    # WHERE column_name operator value;

# with function AVG/SUM/MAX/MIN and ONE column
    # SELECT AVG(column_name) FROM table_name
    # WHERE column_name operator value;

# }}}

tokens = (
            'SELECT_T',
            'FROM_T',
            'WHERE_T',
            'COLUMN_FUNCTION_NAME',
            'NUMBER',
            'EQUALITY',
            'GREATER_THAN',
            'LESS_THAN',
            'AND',
            'OR',
            'NOT',
            'OPEN_B',
            'CLOSE_B',
            'COMMA',
            'PLUS',
            'MINUS',
            'TIMES',
            'DIVIDE',
            'SEMICOLON'
         )

t_SELECT_T              = r'(?i)\bSELECT\b'
t_FROM_T                = r'(?i)\bFROM\b'
t_WHERE_T               = r'(?i)\bWHERE\b'
t_COLUMN_FUNCTION_NAME  = r'(?!SELECT|FROM|WHERE)(\b[A-Za-z_][A-Za-z_0-9]+|\*\b)'
t_NUMBER                = r'\b\d+\b'
t_EQUALITY              = r'\='
t_GREATER_THAN          = r'\>'
t_LESS_THAN             = r'\<'
t_AND                   = r'\&&'
t_OR                    = r'\|\|'
t_NOT                   = r'\!'
t_OPEN_B                = r'\('
t_CLOSE_B               = r'\)'
t_COMMA                 = r'\,'
t_SEMICOLON             = r'\;'
t_PLUS                  = r'\+'
t_MINUS                 = r'-'
t_TIMES                 = r'\*'
t_DIVIDE                = r'/'
t_ignore                = r' '

def t_error(obj):
    print ( "Invalid Tokens" )
    obj.lexer.skip(1)

lexer = lex.lex()

# TEST
line = 'SeLeCT * fROM Database WHErE  dsad = 12;'
#line = 'SeLeCT col1, col2, col3 fROM Database WHErE  dsad = 1 * 5652;'
#line = 'SeLeCT AGV ( Salary ) fROM Database WHErE weather >  12;'
#line = input ('')
lexer.input (line)
while True:
    sample = lexer.token()
    if not sample:
        break
    print (sample)


#
#        Parser [Grammar]
#

def p_SQLselect(p):
    '''SQLselect : SELECT_T COLUMN_FUNCTION_NAME FROM_T COLUMN_FUNCTION_NAME SEMICOLON
                 | SELECT_T TIMES  FROM_T COLUMN_FUNCTION_NAME SEMICOLON
                 | SELECT_T function FROM_T COLUMN_FUNCTION_NAME SEMICOLON 
                 | SELECT_T COLUMN_FUNCTION_NAME FROM_T COLUMN_FUNCTION_NAME WHERE_T condition SEMICOLON 
                 | SELECT_T TIMES  FROM_T COLUMN_FUNCTION_NAME WHERE_T condition SEMICOLON 
                 | SELECT_T function FROM_T COLUMN_FUNCTION_NAME WHERE_T condition SEMICOLON 
                 | SELECT_T columnlist FROM_T COLUMN_FUNCTION_NAME SEMICOLON
                 | SELECT_T columnlist FROM_T COLUMN_FUNCTION_NAME WHERE_T condition SEMICOLON
    '''


def p_condition(p):
    '''condition : COLUMN_FUNCTION_NAME EQUALITY       expression
                 | COLUMN_FUNCTION_NAME LESS_THAN      expression
                 | COLUMN_FUNCTION_NAME GREATER_THAN   expression
    '''

def p_expression(p):
    '''expression : expression PLUS         expression
                  | expression MINUS        expression
                  | expression TIMES        expression
                  | expression DIVIDE       expression
                  | expression AND          expression
                  | expression OR           expression
                  | NOT                     expression
                  | NUMBER'''

def p_function(p):
    '''function : COLUMN_FUNCTION_NAME OPEN_B COLUMN_FUNCTION_NAME CLOSE_B '''


def p_columnlist(p):
    '''
    columnlist : COLUMN_FUNCTION_NAME
               | COLUMN_FUNCTION_NAME COMMA columnlist
    '''


def p_error(p):
    global flag
    flag = 1



parser = yacc.yacc()
result = parser.parse( line )
if ( flag  is 0 ) :
    print("Built Success 0 error ")
else:
    print("Syntax error !")
