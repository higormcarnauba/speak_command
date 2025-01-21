import subprocess
import os
import pyttsx3
import threading
import keyboard

# Configuração do motor de fala
engine = pyttsx3.init()

LOG_FILE = "terminal_log.txt"
keypress_event = threading.Event()


def speak(text):
    """Faz o computador falar o texto passado."""
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Erro ao falar: {e}")

def stop_speaking():
    engine.stop()

def detect_keypress():
    """Detecta pressionamento da tecla ESC para parar a fala."""
    while not keypress_event.is_set():
        if keyboard.is_pressed('esc'):
            print("Parando a fala...")
            stop_speaking()
            keypress_event.set()  # Sinaliza que a tecla foi pressionada
            break

def keyPressed():
    keypress_event.clear()
    keypress_thread = threading.Thread(target=detect_keypress, daemon=True)
    keypress_thread.start()


def run_command_and_log(command):
    """Executa um comando no terminal e salva no log, usando subprocess."""
    with open(LOG_FILE, "w", encoding="utf-8") as log:
        log.write(f"\n> {' '.join(command)}\n")  # Salva o comando digitado

        try:
            # Executa o comando com subprocess
            result = subprocess.run(command, shell=True, capture_output=True, text=True, errors="replace")
            output = result.stdout + result.stderr

        except Exception as e:
            output = f"Erro ao executar o comando: {e}"

        log.write(output + "\n")  # Salva a saída do comando no log
        return output

def read_terminal_history(command):
    """Lê o histórico de comandos e saídas salvos no arquivo de log, executa comandos e fala o conteúdo."""
    output = run_command_and_log(command)  # Agora usa o comando passado como argumento
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8", errors="replace") as file:
            history = file.read()
            print(history)  # Exibe o histórico no terminal
            
            keyPressed()
            
            speak(history)  # Lê todo o histórico em voz alta
            return history
    else:
        history = "Nenhum histórico encontrado."
        print(history)
        speak(history)
        return history

def run_python_script(script_name):
    """Executa um arquivo Python no diretório atual e retorna a saída."""
    current_directory = os.getcwd()  # Obtém o diretório atual do terminal
    script_path = os.path.join(current_directory, script_name)
    
    keyPressed()
    
        # Verifica se o script existe
    if not os.path.exists(script_path):
        error_msg = f"Erro: O arquivo '{script_name}' não foi encontrado no diretório '{current_directory}'"
        print(error_msg)
        speak(error_msg)
        return error_msg

        # Executa o script Python e captura a saída
    result = subprocess.run(
        ["python3", script_path],  # Usa `python` (troque para `python3` se necessário)
        capture_output=True,
        text=True
    )

        # Lida com tecla ESC para parar a fala
    

        # Se for 0 a saida foi bem sucedida
    if result.returncode == 0:
        output = result.stdout.strip()
        print("Saída do script: ", output)  # Exibe a saída no terminal
        speak(output)  # Fala a saída do script
        return output
    else:
        error_msg = f"Erro ao executar o script:\n{result.stderr.strip()}"
        print(error_msg)  # Exibe o erro no terminal
        speak(error_msg)  # Fala o erro
        return error_msg