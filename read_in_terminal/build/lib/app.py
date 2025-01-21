import sys, subprocess, os, pyttsx3

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# import controller as control

# args vai pegar os argumentos
# args = sys.argv
# if len(args) != 4:
#     print('Erro nos Argumentos!')
#     sys.exit()

LOG_FILE = "terminal_log.txt"
engine = pyttsx3.init()

def speak(text):
    """Faz o computador falar o texto passado."""
    engine.say(text)
    engine.runAndWait()
    
def run_command_and_log(command):
    """Executa um comando no terminal, salva no log e lê a saída com voz."""
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"\n> {command}\n")  # Salva o comando digitado

        try:
            result = subprocess.run(command, shell=True, text=True, capture_output=True, encoding="utf-8", errors="replace")
            output = result.stdout + result.stderr  # Captura stdout e stderr
        except Exception as e:
            output = f"Erro ao executar o comando: {e}"

        log.write(output + "\n")  # Salva a saída do comando
        print(output)  # Exibe a saída no terminal
        
        return output

def read_terminal_history():
    """Lê o histórico de comandos e saídas salvos no arquivo de log e os fala."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8", errors="replace") as file:
            history = file.read()
            print(history)  # Exibe o histórico no terminal
            speak(history)  # Lê todo o histórico em voz alta
            return history
    return "Nenhum histórico encontrado."

def main():
    while True:
        cmd = input("Digite um comando (ou 'exit' para sair): ")
        if cmd.lower() == "exit":
            break
        elif cmd.lower() == "rit --all" or cmd.lower() == "Read_In_Terminal --all":
            read_terminal_history()  # Lê e fala todo o histórico
        else:
            run_command_and_log(cmd)  # Executa, salva e fala o comando
            
if __name__ == "__main__":
    main()