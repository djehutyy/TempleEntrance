import re
import sys
from io import StringIO
from tokenize import generate_tokens, STRING, COMMENT, NAME, NUMBER, OP

class HolyCConverter:
    def __init__(self):
        self.type_map = {
            'void': 'U0',
            'int': 'I64',
            'long': 'I64',
            'float': 'F64',
            'double': 'F64',
            'char': 'U8',
            'bool': 'Bool',
            'size_t': 'U64'
        }
        
        self.func_map = {
            'printf': 'Print',
            'sprintf': 'SPrint',
            'scanf': 'Scan',
            'malloc': 'MAlloc',
            'calloc': 'CAlloc',
            'realloc': 'RAlloc',
            'free': 'Free',
            'memcpy': 'MemCpy',
            'memset': 'MemSet'
        }

    def convert_type(self, token):
        return self.type_map.get(token, token)

    def convert_function(self, token):
        return self.func_map.get(token, token)

    def tokenize(self, code):
        return list(generate_tokens(StringIO(code).readline))

    def convert_code(self, source):
        output = []
        tokens = self.tokenize(source)
        in_function = False
        in_param = False
        paren_depth = 0

        for tok in tokens:
            token_type, token_string, start, end, line = tok

            # Ignora stringhe e commenti
            if token_type in (STRING, COMMENT):
                output.append(token_string)
                continue

            # Gestione tipi di dato
            if token_type == NAME:
                # Controlla se è un tipo
                converted = self.convert_type(token_string)
                if converted != token_string:
                    output.append(converted)
                    continue
                
                # Controlla se è una funzione
                converted = self.convert_function(token_string)
                if converted != token_string:
                    output.append(converted)
                    continue

            # Gestione puntatori
            if token_string == '*' and not in_param:
                output.append('*')
                continue

            # Gestione parametri funzione
            if token_string == '(' and output[-1] == 'Main':
                in_param = True
                paren_depth = 1
                output.append('(')
                continue

            if in_param:
                if token_string == '(':
                    paren_depth += 1
                elif token_string == ')':
                    paren_depth -= 1
                    if paren_depth == 0:
                        in_param = False

            # Converti costrutti for
            if token_string == 'for':
                output.append('for')
                self.convert_for_loop(tokens, output)
                continue

            output.append(token_string)

        return ''.join(output)

    def convert_for_loop(self, tokens, output):
        paren_count = 1
        parts = ['', '', '']
        current_part = 0
        
        while paren_count > 0:
            tok = next(tokens)
            if tok.string == '(':
                paren_count += 1
            elif tok.string == ')':
                paren_count -= 1
            elif tok.string == ';':
                current_part += 1
                continue
            
            if current_part < 3:
                parts[current_part] += tok.string

        output.append(f'{parts[0]}; {parts[1]}; {parts[2]} {{')

    def preprocess(self, code):
        # Gestione include
        code = re.sub(r'#include\s*<.*?>', '#include "Sys/OS.h"', code)
        
        # Gestione define
        code = re.sub(r'#define\s+(\w+)\s*\(([^)]+)\)', 
                     r'#define \1(%\2%)', code)
        
        # Gestione cast
        code = re.sub(r'\((int|long|float|double)\)', 
                     lambda m: f'({self.type_map[m.group(1)]})', code)
        
        return code

def main():
    if len(sys.argv) < 2:
        print("Usage: python holyc_converter.py <input.c> [output.hc]")
        sys.exit(1)

    converter = HolyCConverter()
    
    with open(sys.argv[1], 'r') as f:
        code = f.read()

    code = converter.preprocess(code)
    converted = converter.convert_code(code)

    output_file = sys.argv[2] if len(sys.argv) > 2 else 'output.hc'
    
    with open(output_file, 'w') as f:
        f.write(converted)

    print(f"Converted {sys.argv[1]} to {output_file}")

if __name__ == "__main__":
    main()