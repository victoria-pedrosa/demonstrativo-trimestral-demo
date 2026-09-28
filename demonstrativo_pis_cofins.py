import pyautogui
import time
import os
import glob
import csv
from dotenv import load_dotenv
load_dotenv()  # lê o .env local (não vai para o GitHub)

# ================= CONFIGURAÇÕES =================
# AGORA O CAMINHO ESTÁ EXATAMENTE IGUAL AO TRIMESTRAL (G:\Meu Drive)
PASTA_DESTINO = os.getenv("PASTA_DESTINO") 

# Configuração do caminho absoluto do arquivo CSV
ARQUIVO_CSV = os.getenv("ARQUIVO_CSV_PISCOFINS")

# --- COORDENADAS ---
POS_FAVORITOS = (717, 63)
# Posição do Demonstrativo PIS e COFINS no menu
POS_DEMONSTRATIVO_PIS_COFINS = (916, 138) 
# Posição do Botão OK da tela de parâmetros
POS_OK_PIS_COFINS = (1377, 370) 

POS_ICONE_PDF = (41, 436)
POS_UNICO_PDF = (370, 427)

POS_UNIDADE_DROPDOWN = (1222, 391)
POS_UNIDADE_G = (1116, 445) 
POS_MEU_DRIVE = (771, 428) # Ajustado para o exato número do Trimestral
POS_BOTAO_OK_PASTA = (1110, 671)

POS_FECHAR_PDF = (62, 174)  
POS_FECHAR_MENU = (1432, 314) 

# Coordenada para fechar o Adobe Acrobat
POS_FECHAR_ADOBE = (1888, 20)

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5
# =================================================

def renomear_arquivo_recente(pasta, nome_novo):
    """Encontra o PDF mais recente na pasta e o renomeia. Retorna True se deu certo, False se falhou."""
    print(f"Procurando o PDF na pasta {pasta} (Aguarde 10 segundos)...")
    time.sleep(10) 
    
    arquivos_pdf = glob.glob(os.path.join(pasta, '*.[pP][dD][fF]'))
    if not arquivos_pdf:
        print("ERRO: Nenhum PDF encontrado na pasta de destino.")
        return False

    arquivo_mais_recente = max(arquivos_pdf, key=os.path.getctime)
    caminho_novo = os.path.join(pasta, nome_novo)

    try:
        if os.path.exists(caminho_novo):
            os.remove(caminho_novo)
            
        os.rename(arquivo_mais_recente, caminho_novo)
        print(f"Sucesso! Arquivo renomeado para: {nome_novo}")
        return True
    except Exception as e:
        print(f"Erro ao renomear o arquivo: {e}")
        return False

def atualizar_csv(linhas):
    """Reescreve o arquivo CSV com os status atualizados."""
    try:
        # Mantendo o delimiter=',' para o PISCOFINS.csv
        with open(ARQUIVO_CSV, 'w', newline='', encoding='utf-8') as csvfile:
            escritor = csv.writer(csvfile, delimiter=',')
            escritor.writerows(linhas)
    except Exception as e:
        print(f"Erro ao salvar o CSV: {e}")

# ================= LEITURA DO CSV =================
linhas_csv = []
try:
    with open(ARQUIVO_CSV, newline='', encoding='utf-8-sig') as csvfile:
        # Delimitador correto por vírgula para ler a planilha
        leitor = csv.reader(csvfile, delimiter=',')
        for linha in leitor:
            linhas_csv.append(linha)
except FileNotFoundError:
    print(f"ERRO: O arquivo CSV não foi encontrado no caminho: {ARQUIVO_CSV}")
    exit()

if len(linhas_csv) <= 1:
    print("Nenhuma empresa encontrada no CSV.")
    exit()

print(f"Foram encontradas {len(linhas_csv)-1} empresas na planilha.")
print("Iniciando automação em 5 segundos. Deixe o sistema contábil maximizado.")
time.sleep(5)

# ================= FLUXO DE AUTOMAÇÃO (LOOP) =================

# Começa do índice 1 para pular o cabeçalho
for i in range(1, len(linhas_csv)):
    linha_atual = linhas_csv[i]
    
    if len(linha_atual) < 2:
        continue
        
    codigo_dominio = linha_atual[1].strip()
    
    if not codigo_dominio.isdigit():
        continue
        
    # Pula se já estiver feito
    if len(linha_atual) >= 3 and linha_atual[2].strip().upper() == "OK":
        print(f"Empresa {codigo_dominio} já foi feita. Pulando...")
        continue

    print(f"\n-----------------------------------------")
    print(f"Iniciando processamento da empresa: {codigo_dominio}")
    
    # Nome final exatamente como você pediu
    nome_final = f"Demonstrativo EFD PIS e COFINS 042026_{codigo_dominio}.pdf"

    # 1. Trocar de Empresa
    pyautogui.press('f8')
    time.sleep(1.5) 
    pyautogui.write(codigo_dominio)
    time.sleep(0.5)
    pyautogui.press('enter') 
    time.sleep(8) 

    # 2. Menu Favoritos -> Demonstrativos PIS e COFINS
    pyautogui.click(POS_FAVORITOS)
    time.sleep(1.5)
    pyautogui.click(POS_DEMONSTRATIVO_PIS_COFINS)
    time.sleep(3) 

    # 3. Tela de parâmetros -> Clicar em OK
    pyautogui.click(POS_OK_PIS_COFINS)
    print("Aguardando o relatório ser gerado (20 segundos)...")
    time.sleep(20) 

    # 4. Tela de Apuração -> Gerar PDF
    pyautogui.click(POS_ICONE_PDF)
    time.sleep(1.5)
    pyautogui.click(POS_UNICO_PDF)
    time.sleep(4) 

    # 5. Selecionar Diretório (Procurar Pasta) e Salvar
    pyautogui.click(POS_UNIDADE_DROPDOWN)
    time.sleep(1)
    pyautogui.click(POS_UNIDADE_G)
    time.sleep(2.5) 
    pyautogui.click(POS_MEU_DRIVE)
    time.sleep(1)
    pyautogui.click(POS_BOTAO_OK_PASTA)

    # 6. Fechar Adobe PRIMEIRO para liberar o arquivo
    print("Aguardando o Adobe abrir completamente (20 segundos)...")
    time.sleep(25)
    print("Fechando o Adobe Acrobat...")
    pyautogui.click(POS_FECHAR_ADOBE)
    time.sleep(4)

    # 7. Renomear o arquivo DEPOIS de fechar o Adobe
    print("Iniciando renomeação do arquivo...")
    sucesso = renomear_arquivo_recente(PASTA_DESTINO, nome_final)

    # 8. Voltar para o sistema e fechar as janelas internas do Domínio
    print("Fechando telas do Domínio...")
    pyautogui.click(POS_FECHAR_PDF)
    time.sleep(1.5)
    pyautogui.click(POS_FECHAR_MENU)
    time.sleep(2)
    
    # 9. Atualizar o CSV com o resultado
    while len(linha_atual) < 3:
        linha_atual.append("")
        
    if sucesso:
        linha_atual[2] = "OK"
    else:
        linha_atual[2] = "ERRO"
        
    atualizar_csv(linhas_csv)

print("\nAutomação finalizada com sucesso! A planilha foi atualizada.")