# -*-encoding: utf-8 -*-

"""
Analizador Sint[actico aplicando el algoritmo LL!
Curso: Compiladores y Lenguajes de Bajo de Nivel, 2ndo Sem, 2016
TAREA 2 - Analisis Sint[actico

"""
import os
import sys

from jsonpy_lexer import lexer, ArchivoException

# variables para diferenciar a un terminal de un no terminal.  Utilizado para comparar terminales en la pila
Term = 0
Rule = 1

# Terminales

# [
L_CORCHETE = 0
# ]
R_CORCHETE = 1
# {
L_LLAVE = 2
# }
R_LLAVE = 3
# ,
COMA = 4
# :
DOS_PUNTOS = 5
# string
LITERAL_CADENA = 6
# number
LITERAL_NUM = 7
# booleanos
PR_TRUE = 8
PR_FALSE = 9
PR_NULL = 10
# Fin de archivo
EOF = 11

# token invalido
T_INVALID = 12

# No terminales
N_JSON = 0
N_ELEMENT = 1
N_ARRAY = 2
N_ELEMENT_LIST = 3
N_ELEMENT_LIST_PRI = 4
N_OBJECT = 5
N_ATTR_LIST = 6
N_ATTR_LIST_PRI = 7
N_ATTR = 8
N_ATTR_NAME = 9
N_ATTR_VAL = 10

EMPTY = 'empty'

# Gramatica del json simple.
# Para cada produccion, definimos sus componentes en cada tupla.
# Se debe saber si el componente es terminal o no terminal con Ter y Rule, respectivamente
rules = [
    # 0 json -> element $
    [(Rule, N_ELEMENT)],
    # 1 element -> object
    [(Rule, N_OBJECT)],
    # 2 element -> array
    [(Rule, N_ARRAY)],
    # 3 array -> [ ]
    [(Term, L_CORCHETE), (Term, R_CORCHETE)],
    # 4 array -> [ element-list ]
    [(Term, L_CORCHETE), (Rule, N_ELEMENT_LIST), (Term, R_CORCHETE)],
    # 5 element-list -> element element-list-pri
    [(Rule, N_ELEMENT), (Rule, N_ELEMENT_LIST_PRI)],
    # 6 element-list-prim -> , element element-list-pri
    [(Term, COMA), (Rule, N_ELEMENT), (Rule, N_ELEMENT_LIST_PRI)],
    # 7 element-list-prim -> empty
    [(Term, EMPTY)],
    # 8 object -> { }
    [(Term, L_LLAVE), (Term, R_LLAVE)],
    # 9 object -> { attr-list }
    [(Term, L_LLAVE), (Rule, N_ATTR_LIST), (Term, R_LLAVE)],
    # 10 attr-list -> attr attr-list-pri
    [(Rule, N_ATTR), (Rule, N_ATTR_LIST_PRI)],
    # 11 attr-list-pri -> , attr attr-list-pri
    [(Term, COMA), (Rule, N_ATTR), (Rule, N_ATTR_LIST_PRI)],
    # 12 attr-list-pri -> empty
    [(Term, EMPTY)],
    # 13 attr -> attr-name : attr-value
    [(Rule, N_ATTR_NAME), (Term, DOS_PUNTOS), (Rule, N_ATTR_VAL)],
    # 14 attr-name -> string
    [(Term, LITERAL_CADENA)],
    # 15 attr-value -> element
    [(Rule, N_ELEMENT)],
    # 16 attr-value -> string
    [(Term, LITERAL_CADENA)],
    # 17 attr-value -> number
    [(Term, LITERAL_NUM)],
    # 18 attr-value -> true
    [(Term, PR_TRUE)],
    # 19 attr-value -> false
    [(Term, PR_FALSE)],
    # 20 attr-value -> null
    [(Term, PR_NULL)],
]

# Tabla de parsing
# Cada elemento de la lista representa a una fila de la tabla.
# Cada elemento de la fila representa a un terminal, ordenado asi:
# [ ] { } , : string number true false null $
#
tabla_parsing = [[0, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1],

                 [2, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1],

                 [3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],

                 [5, -1, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1],

                 [-1, -1, -1, -1, 6, -1, -1, -1, -1, -1, -1, -1],

                 [-1, -1, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1],

                 [-1, -1, -1, -1, -1, -1, 10, -1, -1, -1, -1, -1],

                 [-1, -1, -1, -1, 11, -1, -1, -1, -1, -1, -1, -1],

                 [-1, -1, -1, -1, -1, -1, 13, -1, -1, -1, -1, -1],

                 [-1, -1, -1, -1, -1, -1, 14, -1, -1, -1, -1, -1],

                 [15, -1, 15, -1, -1, -1, 16, 17, 18, 19, 20, -1],

                 ]


def complex_a_indice(lista_tokens):
    """ Funcion para transformar cadenas de los componentes lexicos
        a elementos enteros int, que deban coincidir con los
        indices de la tabla de parsing.
    """

    tokens = []

    # evalua componentes lexicos. Todos se consideran validos, ya
    # que fueron generados por el lexer (exepto cacdena vacia)
    for t in lista_tokens:
        if t == 'L_LLAVE':
            tokens.append(L_LLAVE)
        elif t == 'R_LLAVE':
            tokens.append(R_LLAVE)
        elif t == 'L_CORCHETE':
            tokens.append(L_CORCHETE)
        elif t == 'R_CORCHETE':
            tokens.append(R_CORCHETE)
        elif t == 'COMA':
            tokens.append(COMA)
        elif t == 'DOS_PUNTOS':
            tokens.append(DOS_PUNTOS)
        elif t == 'LITERAL_CADENA':
            tokens.append(LITERAL_CADENA)
        elif t == 'LITERAL_NUM':
            tokens.append(LITERAL_NUM)
        elif t == 'PR_TRUE':
            tokens.append(PR_TRUE)
        elif t == 'PR_FALSE':
            tokens.append(PR_FALSE)
        elif t.strip == '':
            # el lexer tiene bug que retorna caracter vacio. Se puede ignorar esto con seguridad.
            pass

    tokens.append(EOF)

    # print(tokens)
    return tokens


def ll1_algoritmo(lista_tokens):
    tokens = complex_a_indice(lista_tokens)

    print 'Analisis Sintactico'

    # cargamos pila con EOF y primera produccion N_JSON
    stack = [(Term, EOF), (Rule, N_JSON)]

    # indice para el token evaluado
    position = 0

    while len(stack) > 0:

        (stack_type, stack_value) = stack.pop()

        token = tokens[position]

        if stack_type == Term:  # 0
            # se encuentra terminal

            if stack_value == token:
                position += 1
                print('pop', stack_value)
                if token == EOF:
                    print 'Input aceptado'
            else:
                print 'Error de sintaxis:', token
                break

        elif stack_type == Rule:  # 1
            # se encuentra no terminal. Es una regla

            print 'Valor en pila: ', stack_value, ' token: ', token
            rule = tabla_parsing[stack_value][token]

            print 'rule: ', rule

            for r in reversed(rules[rule]):
                stack.append(r)

        print 'stack: ', stack


if __name__ == '__main__':
    try:
        # analisis lexico
        lista_tokens = lexer(sys.argv)

        # analisis sintactico
        ll1_algoritmo(lista_tokens)

    except ArchivoException as ex:
        print ex.message

    except Exception as ex:
        print u'Error inesperado: %s' % ex.message
