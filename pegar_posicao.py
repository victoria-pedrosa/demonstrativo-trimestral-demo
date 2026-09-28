import pyautogui
import time
import sys

print("======================================================")
print("🔍 CAPTURA DE COORDENADAS DO MOUSE")
print("Mova o mouse até o botão desejado e anote os valores.")
print("Para parar a execução, pressione Ctrl + C.")
print("======================================================\n")

try:
    while True:
        # Pega a posição atual do mouse
        x, y = pyautogui.position()
        
        # Imprime a posição atualizando na mesma linha para não poluir a tela
        sys.stdout.write(f"\rPosição atual do mouse: X: {x:>4} | Y: {y:>4}")
        sys.stdout.flush()
        
        time.sleep(0.1) # Atualiza bem rápido (10 vezes por segundo)
        
except KeyboardInterrupt:
    print("\n\n✅ Captura finalizada pelo usuário.")