import sys
def solution(f_in, f_out):
    variables = {}
    functions = {}
    def add(a,b):
        return a+b
    def sub(a,b):
        return a-b
    def mul(a,b):
        return a*b
    def div(a,b):
        return a/b
    def init(var):
        if 'init ' in var:
            var.remove('init ')
            var_name = var[0:var.index( )]
            var = var[var.index::]
            variables[var_name] = var[var]
if __name__ == "__main__":
    solution(sys.stdin, sys.stdout)