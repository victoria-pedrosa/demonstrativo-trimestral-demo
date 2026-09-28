import pyautogui
import time
import os
import glob
import csv
from dotenv import load_dotenv
load_dotenv()  # lê o .env local (não vai para o GitHub)

# ================= CONFIGURAÇÕES =================
# AGORA APONTANDO PARA A UNIDADE CORRETA (G:)
PASTA_DESTINO = os.getenv("PASTA_DESTINO") 

# Configuração do caminho absoluto do arquivo CSV
ARQUIVO_CSV = os.getenv("ARQUIVO_CSV_TRIMESTRAL")

# --- COORDENADAS ---
POS_FAVORITOS = (717, 63)
POS_DEMONSTRATIVOS = (780, 93)

POS_BOTAO_NENHUM = (1135, 815)
POS_LINHA_CSLL = (914, 391)
POS_LINHA_IRPJ = (923, 411)
POS_BOTAO_OK_IMPOSTOS = (1378, 335)

POS_ICONE_PDF = (41, 436)
POS_UNICO_PDF = (370, 427)

POS_UNIDADE_DROPDOWN = (1222, 391)
# Garanta que essa coordenada clica na unidade G: na lista do sistema!
POS_UNIDADE_G = (1116, 445) 
POS_MEU_DRIVE = (766, 451)
POS_BOTAO_OK_PASTA = (1110, 671)

POS_FECHAR_PDF = (62, 174)  
POS_FECHAR_MENU = (1371, 373) 

# Coordenada para fechar o Adobe Acrobat
POS_FECHAR_ADOBE = (1888, 20)

# Medida de segurança: mova o mouse para qualquer canto da tela para abortar o script
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5
# =================================================

def renomear_arquivo_recente(pasta, nome_novo):
    """Encontra o PDF mais recente na pasta e o renomeia."""
    print(f"Procurando o PDF na pasta {pasta} (Aguarde 10 segundos)...")
    time.sleep(10) 
    
    # Busca por .pdf ou .PDF para evitar erros
    arquivos_pdf = glob.glob(os.path.join(pasta, '*.[pP][dD][fF]'))
    if not arquivos_pdf:
        print("ERRO: Nenhum PDF encontrado na pasta de destino.")
        return

    arquivo_mais_recente = max(arquivos_pdf, key=os.path.getctime)
    caminho_novo = os.path.join(pasta, nome_novo)

    try:
        if os.path.exists(caminho_novo):
            os.remove(caminho_novo)
            
        os.rename(arquivo_mais_recente, caminho_novo)
        print(f"Sucesso! Arquivo renomeado para: {nome_novo}")
    except Exception as e:
        print(f"Erro ao renomear o arquivo: {e}")

# ================= LEITURA DO CSV =================
lista_empresas = []
try:
    with open(ARQUIVO_CSV, newline='', encoding='utf-8-sig') as csvfile:
        leitor = csv.reader(csvfile, delimiter=',')
        next(leitor, None) 
        for linha in leitor:
            if len(linha) >= 2:
                codigo = linha[1].strip()
                if codigo.isdigit(): 
                    lista_empresas.append(codigo)
except FileNotFoundError:
    print(f"ERRO: O arquivo CSV não foi encontrado no caminho especificado: {ARQUIVO_CSV}")
    exit()

if not lista_empresas:
    print("Nenhuma empresa encontrada no CSV.")
    exit()

print(f"Foram encontradas {len(lista_empresas)} empresas.")
print("Iniciando automação em 5 segundos. Deixe o sistema contábil maximizado.")
time.sleep(5)

# ================= FLUXO DE AUTOMAÇÃO (LOOP) =================

for codigo_dominio in lista_empresas:
    print(f"\n-----------------------------------------")
    print(f"Iniciando processamento da empresa: {codigo_dominio}")
    
    nome_final = f"Demonstrativo Trimestral_{codigo_dominio}.pdf"

    # 1. Trocar de Empresa
    pyautogui.press('f8')
    time.sleep(1.5) 
    pyautogui.write(codigo_dominio)
    time.sleep(0.5)
    pyautogui.press('enter') 
    time.sleep(8) 

    # 2. Menu Favoritos -> Demonstrativos
    pyautogui.click(POS_FAVORITOS)
    time.sleep(1.5)
    pyautogui.click(POS_DEMONSTRATIVOS)
    time.sleep(5) 

    # 3. Seleção de Impostos (IRPJ e CSLL)
    pyautogui.click(POS_BOTAO_NENHUM)
    time.sleep(0.5)
    pyautogui.click(POS_LINHA_CSLL)
    pyautogui.click(POS_LINHA_IRPJ)
    pyautogui.click(POS_BOTAO_OK_IMPOSTOS)
    
    print("Aguardando o relatório ser gerado (15 segundos)...")
    time.sleep(15) 

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

    # 6. Fechar Adobe PRIMEIRO para liberar o arquivo para renomear
    print("Aguardando o Adobe abrir completamente (15 segundos)...")
    time.sleep(15)
    print("Fechando o Adobe Acrobat...")
    pyautogui.click(POS_FECHAR_ADOBE)
    time.sleep(4)

    # 7. Renomear o arquivo DEPOIS de fechar o Adobe
    print("Iniciando renomeação do arquivo...")
    renomear_arquivo_recente(PASTA_DESTINO, nome_final)

    # 8. Voltar para o sistema e fechar as janelas internas do Domínio
    print("Fechando telas do Domínio...")
    pyautogui.click(POS_FECHAR_PDF)
    time.sleep(1.5)
    pyautogui.click(POS_FECHAR_MENU)
    time.sleep(2)

print("\nAutomação finalizada com sucesso!")