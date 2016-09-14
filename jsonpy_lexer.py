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

tabla_simbolos = {
    'literal': 'LITERAL_CADENA',
    '{': 'L_LLAVE',
    '}': 'R_LLAVE',
    ',': 'COMA',
    ':': 'DOS_PUNTOS',
    '[': 'L_CORCHETE',
    ']': 'R_CORCHETE',
    '': 'EOF',
}


class Entrada():
    def __init__(self, complex, lexema):
        self.complex = complex
        self.lexema = lexema
        # TODO notar que falta tipo de dato


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
        return u'%s -> %s' % (self.complex ,self.lexema)

    def alimentar_lexema(self, c):
        """ formamos el lexema anexando un caracter """
        self.lexema = self.lexema + c
        return self.lexema

    def ungetc(self):
        return self.lexema[-1:]


def init_tabla():
    pass


def init_tabla_simbolos():
    pass


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
        # eliminar espacios en blanco e incrementar numero de tabs
        print "Es algo de tab o espacio en blanco"

    elif c == '\n':
        print "Es Salto de linea"

    elif c.isalpha():
        # TODO hace falta esto? En la tarea no se especifica ID como componente léxico

        # es caracter alfabético
        # Comenzar a agrupar caracteres para buscar en la tabla
        # de variables

        # TODO aquí autómata de identificador

        while c.isalpha() or c.isdigit():
            token.alimentar_lexema(c)
            c = f.read(1)

    elif c.isdigit():
        # es caracter numérico

        # TODO aquí autómata de números
        pass

    elif c == '"':
        # TODO aquí autómata de literal

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

    return token

if __name__ == '__main__':
    init_tabla()
    init_tabla_simbolos()

    filename = 'input_test.txt'
    with open(filename) as f:
        while True:
            token = siguiente_token(f)

            print token.complex
            print tabla_simbolos.get(token.complex)

            if token.complex == 'EOF':
                break