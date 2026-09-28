# Demonstrativo Trimestral

> Projeto de portfólio de **Victória Pedrosa** (Automação, Processos e Dados). Automação desenvolvida para um escritório de contabilidade; **esta é uma versão com dados fictícios** — nomes, CNPJs, e-mails e IDs internos foram substituídos.

## Problema de negócio
Gerar os demonstrativos trimestrais e de PIS/COFINS na Domínio para cada empresa é repetitivo.

## Antes x depois
| | Antes | Depois |
|---|---|---|
| Como é feito | Geração manual do relatório empresa a empresa. | Robô gera e salva os demonstrativos a partir de uma lista. |

## Ganho
- Demonstrativos em lote.

## Tecnologias
PyAutoGUI (RPA por imagem), Python, SQLite

## Arquivos
- `demonstrativo_pis_cofins.py`
- `demonstrativo_trimestral.py`
- `pegar_posicao.py`
- `requirements.txt`

## Como rodar
1. `pip install -r requirements.txt`
2. Copie `.env.exemplo` para `.env` e preencha os caminhos.
3. Execute o script principal.

> As imagens de referência usadas pelo robô para clicar na tela (PyAutoGUI) não foram incluídas nesta versão.

## Autora
Victória Pedrosa — Product Owner do Time de IA, automação de processos contábeis e fiscais.
