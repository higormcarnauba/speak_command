import sys, subprocess, os
import controller as control

args = sys.argv

def main():
    if len(args) < 2:
        print('Erro: Nenhum comando fornecido!')
        sys.exit()
    
    cmd = args[1:]

    match cmd[0]:
        case '--python_File':
            result = control.run_python_script(cmd[1])  # Chama a função que executa o script Python 
        case _:
            result = control.read_terminal_history(cmd)  # Caso contrário, lê o histórico do terminal

if __name__ == "__main__":
    main()
