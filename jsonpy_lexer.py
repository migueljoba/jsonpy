# -*-encoding: utf-8 -*-

"""
Analizador Léxico
Curso: Compiladores y Lenguajes de Bajo de Nivel, 2ndo Sem, 2016
TAREA 1 - Analisis Lexico

Descripción:
Implementar un analizador lexico que reconozca tokens
para un archivo fuente tipo JSONML

El código es una adaptación del fuente original
en el repo https://github.com/jpaciello/compiladores
"""

import os
import sys

TABLA_SIMBOLOS = {
    'literal': 'LITERAL_CADENA',
    'numero': 'LITERAL_NUM',
    '{': 'L_LLAVE',
    '}': 'R_LLAVE',
    ',': 'COMA',
    ':': 'DOS_PUNTOS',
    '[': 'L_CORCHETE',
    ']': 'R_CORCHETE',
    'true': 'PR_TRUE',
    'TRUE': 'PR_TRUE',
    'false': 'PR_FALSE',
    'FALSE': 'PR_FALSE',
    '': 'EOF',
}


class Entrada():
    def __init__(self, complex, lexema):
        self.complex = complex
        self.lexema = lexema


class Token():
    """ Un token está formado por:
        - Componente léxico:
            Const, relación, identificador, número, literal,
            palabras reservadas

        - Lexema:
            El valor del componente léxico, como ser "Hola mundo" el lexema
            para un LITERAL

        - Patrón:
            No se implementará para esta tarea. Es la regla que genera la
            secuencia de caracteres para el token --> REGEX
    """

    def __init__(self, complex=None, entrada=None, lexema=''):
        self.complex = complex
        self.entrada = entrada  # no se para que sirve
        self.lexema = lexema

    def __str__(self):
        return u'%s -> %s' % (self.complex, self.lexema)

    def alimentar_lexema(self, c):
        """ formamos el lexema anexando un caracter """
        self.lexema = self.lexema + c
        return self.lexema

    def ungetc(self):
        return self.lexema[-1:]


def siguiente_token(f):
    i = 0
    acepto = False
    estado = 0

    token = Token()

    c = f.read(1)

    if not c:
        token.alimentar_lexema(c)
        token.complex = 'EOF'
        return token

    # no es EOF. Comenzar a evaluar cada caracter
    if c in [' ', '\t']:

        while c in[' ', '\t']:
            # eliminar espacios en blanco e incrementar numero de tabs
            # print "Es algo de tab o espacio en blanco"
            c = f.read(1)

        else:
            f.seek(f.tell() - 1)

        token = None

    elif c in ['\r', '\n']:
        while c in ['\r', '\n']:
            c = f.read(1)

        else:
            if not c:
                token.complex = 'EOF'
                return token

            f.seek(f.tell() - 1)

        token = None

    elif c.isalpha():
        # puede aceptarse true|TURE|false|FALSE|null|NULL
        # TODO null|NULL

        # es caracter alfabético
        # Comenzar a agrupar caracteres para buscar en la tabla
        # de variables

        while c.isalpha():
            token.alimentar_lexema(c)
            c = f.read(1)

        else:
            f.seek(f.tell() - 1)
            token.complex = token.lexema

    elif c == '"':
        token.alimentar_lexema(c)
        c = f.read(1)

        while c != '"':
            token.alimentar_lexema(c)
            c = f.read(1)

        else:
            token.alimentar_lexema(c)

        token.complex = 'literal'

    elif c == ':':
        token.alimentar_lexema(c)
        token.complex = ':'

    elif c == ',':
        token.alimentar_lexema(c)
        token.complex = ','

    elif c == '[':
        token.alimentar_lexema(c)
        token.complex = '['

    elif c == ']':
        token.alimentar_lexema(c)
        token.complex = ']'

    elif c == '{':
        token.alimentar_lexema(c)
        token.complex = '{'

    elif c == '}':
        token.alimentar_lexema(c)
        token.complex = '}'

    elif c.isdigit():
        # es caracter numérico

        estado = 1  # estado inicial
        acepto = False

        f.seek(f.tell() - 1)

        while True:
            c = f.read(1)

            if c in [',', ']', '}'] and acepto:
                f.seek(f.tell() - 1)
                break

            # Por defecto, no aceptar cada nuevo caracter
            # hasta que sea evaluado y explícitamente aceptado
            # acepto = False

            if estado == 1:
                if c.isdigit():
                    estado = 2
                    acepto = True

                else:
                    acepto = False
                    break

            elif estado == 2:
                acepto = False

                if c.isdigit():
                    estado = 2
                    acepto = True

                elif c == '.':
                    estado = 3

                elif c in ['e', 'E']:
                    estado = 5

                else:
                    # acepto = False
                    break

            elif estado == 3:
                if c.isdigit():
                    estado = 4
                    acepto = True

                else:
                    acepto = False
                    break

            elif estado == 4:
                if c.isdigit():
                    estado = 4
                    acepto = True

                elif c in ['e', 'E']:
                    estado = 5

                else:
                    acepto = False
                    break

            elif estado == 5:
                if c in ['+', '-']:
                    estado = 6

                elif c.isdigit():
                    estado = 6

                else:
                    acepto = False
                    break

            elif estado == 6:
                if c.isdigit():
                    estado = 6
                    acepto = True

                else:
                    acepto = False
                    break

            token.alimentar_lexema(c)

        if c in [ '\b', '\f', '\n', '\r', '\r', '\t', ' '] and acepto:
            # acepto = True
            f.seek(f.tell() - 1)

        if not acepto:
            print u'Caracter inesperado: %s' % c

        else:
            token.complex = 'numero'

    return token

def main(argv):

    if len(argv) < 2:
        print u'Debe pasar como parámetro el nombre del archivo fuente.'
        return

    filename = argv[1]
    if not os.path.isfile(filename):
        print u'No se encuentra el archivo \'%s\'' % filename
        return

    else:
        with open(filename, 'rb') as f:

            while True:
                token = siguiente_token(f)

                if token is not None:
                    if token.complex == 'EOF':
                        break

                    print  TABLA_SIMBOLOS.get(token.complex , '').ljust(17), token.lexema.ljust(15)


if __name__ == '__main__':
    main(sys.argv)

