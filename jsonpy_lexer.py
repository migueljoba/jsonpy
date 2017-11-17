# -*-encoding: utf-8 -*-

"""
Analizador Léxico
Curso: Compiladores y Lenguajes de Bajo de Nivel, 2ndo Sem, 2017
TAREA 1 - Analisis Léxico

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

class CaracterInvalido(Exception):
    pass

class TokenInvalido(Exception):
    pass

class ArchivoException(Exception):
    pass

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

    def __init__(self, complex=None, lexema=''):
        self.complex = complex
        self.lexema = lexema

    def __str__(self):
        return u'%s -> %s' % (self.complex, self.lexema)

    def alimentar_lexema(self, c):
        """ formamos el lexema anexando un caracter """
        self.lexema = self.lexema + c
        return self.lexema

    def ungetc(self):
        return self.lexema[-1:]


def siguiente_token(f, num_linea=1):

    token = Token()

    c = f.read(1)

    if not c:
        token.alimentar_lexema(c)
        token.complex = 'EOF'
        return token, num_linea

    # no es EOF. Comenzar a evaluar cada caracter
    if c in [' ', '\t']:

        while c in [' ', '\t']:
            # eliminar espacios en blanco e incrementar numero de tabs
            c = f.read(1)

        else:
            f.seek(f.tell() - 1)

        token = None

    elif c in ['\r', '\n']:
        while c in ['\r', '\n']:

            if c == '\n':
                num_linea += 1

            c = f.read(1)

        else:
            if not c:
                token.complex = 'EOF'
                return token, num_linea

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

        # necesariamente, el token debe ser 'número'
        token.complex = 'numero'

        estados_de_aceptacion = [1, 4, 5]
        caracteres_esperados = ['\b', '\f', '\n', '\r', '\r', '\t',
                                ' ', ']', '}', ',']

        estado = 0

        f.seek(f.tell() - 1)

        while True:
            c = f.read(1)

            if estado == 0:
                if c.isdigit():
                    estado = 1

                else:
                    break

            elif estado == 1:
                if c.isdigit():
                    estado = 1

                elif c == '.':
                    estado = 2

                elif c in ['e', 'E']:
                    estado = 3

                else:
                    break

            elif estado == 2:
                if c.isdigit():
                    estado = 4

                else:
                    break

            elif estado == 3:
                if c.isdigit():
                    estado = 5

                elif c in ['-', '+']:
                    estado = 6

                else:
                    break

            elif estado == 4:
                if c.isdigit():
                    estado = 4

                elif c in ['e', 'E']:
                    estado = 3

                else:
                    break

            elif estado == 5:
                if c.isdigit():
                    estado = 5

                else:
                    break

            elif estado == 6:
                if c.isdigit():
                    estado = 5

                else:
                    break

            token.alimentar_lexema(c)

        if estado in estados_de_aceptacion and c in caracteres_esperados:
            token.complex = 'numero'
            f.seek(f.tell() - 1)

        else:
            CaracterInvalido()

    return token, num_linea


def lexer(argv):
    if len(argv) < 2:
        raise ArchivoException(u'Debe pasar como parámetro el nombre del archivo fuente.')

    archivo_in = argv[1]
    if not os.path.isfile(archivo_in):
        raise ArchivoException(u'No se encuentra el archivo \'%s\'' % archivo_in)

    else:
        print u'Escaneando el archivo \'%s\'' % archivo_in

        archivo_out_nombre = 'output.txt'
        # archivo_out = open(archivo_out_nombre, 'wb')

        with open(archivo_in, 'rb') as f_in:

            num_linea = 1
            prev_num_linea = 1

            tokens = []

            while True:
                try:
                    token, num_linea = siguiente_token(f_in, num_linea)
                except CaracterInvalido:
                    print u'Caracter invalido. Linea %s ' % num_linea

                if token is not None:

                    if token.complex == 'EOF':
                        # print u'FIN. Archivo de salida: \'%s\'' % archivo_out_nombre
                        break

                    # escritura en archivo de salida, considerando el numero de linea
                    if num_linea > prev_num_linea:
                        append_char = '\n' * (num_linea - prev_num_linea)
                        prev_num_linea = num_linea

                    else:
                        append_char = ' '

                    tipo_token = TABLA_SIMBOLOS.get(token.complex, '')

                    tokens.append(tipo_token)

                    # archivo_out.write(append_char + tipo_token)

            return tokens

if __name__ == '__main__':
    lexer(sys.argv)


