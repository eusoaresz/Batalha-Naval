import random
import time
import os
from colorama import Fore, Style, just_fix_windows_console

# Habilita suporte a cores ANSI no console Windows (PowerShell/VS Code Terminal)
just_fix_windows_console()

temp = "🦣🦣🐪🐪🐯🐯🦓🦓🐢🐢🐋🐋🦜🦜🐧🐧"
figuras = list(temp)   # converte a string para lista
def carregar_ranking():
    dados = []
    if os.path.isfile("ranking.txt"):
        with open("ranking.txt", "r", encoding="utf-8") as arq:
            dados = arq.readlines()
    return dados

def menu_principal():
    while True:
        os.system("cls")
        print("=" * 40)
        print("||----------{BATALHA NAVAL}-----------||")
        print("=" * 40)
        print("||1 - Iniciar jogo                    ||")
        print("||2 - Ver ranking                     ||")
        print("||3 - Ver Regras                      ||")
        print("||4 - Finalizar                       ||")
        print("=" * 40)
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            jogar()
            input("\nPressione Enter para voltar ao menu...")
        elif opcao == "2":
            os.system("cls")
            mostrar_ranking()
            input("\nPressione Enter para voltar ao menu...")
        elif opcao == "3":
            os.system("cls")
            print("Regras do Jogo:")
            print("- O objetivo é afundar a frota adversária (posicionada em uma grade 10x10)")
            print("- antes que a sua seja destruída.")
            print("- Cada jogador tem seus navios escondidos na horizontal/vertical")
            print("- Os jogadores alternam tiros por coordenadas (ex: A-5),")
            print("- vencendo quem afundar todos os navios inimigos primeiro.")
            input("\nPressione Enter para voltar ao menu...")
        elif opcao == "4":
            print("Encerrando...")
            break
        else:
            print("Opção inválida.")
            time.sleep(1)

def jogar():
    print("=" * 40)
    print("-----------=VAMOS A BATALHA=-----------")
    print("=" * 40)
    print("||1 - Jogar contra o computador       ||")
    print("||2 - Jogar contra outro jogador      ||")
    print("||3 - Voltar ao menu                  ||")

    escolha = input("\nEscolha uma opção: ").strip()
    if escolha == "1":
        jogador = "Computador"
    elif escolha == "2":
        jogador1 = input("\nNome do Jogador 1: ")
        jogador2 = input("Nome do Jogador 2: ")
    else:
        return
    
    pontos = 0
    linhas = 10
    colunas = 10
    letras_linhas = "ABCDEFGHIJ"

    figuras_disponiveis = list(temp)
    jogo = []
    apostas = []

    def preenche_matriz():
        for i in range(linhas):
            jogo.append([])
            apostas.append([])
            for _ in range(colunas):
                jogo[i].append(random.choice(figuras_disponiveis))
                apostas[i].append("🌊")

    def mostra_tabuleiro():
        os.system("cls")
        print("   1   2   3   4   5   6   7   8   9  10")
        for i in range(linhas):
            print(letras_linhas[i], end="")
            for j in range(colunas):
                print(f" {jogo[i][j]} ", end="")
            print("\n")
        print("Memorize a posição dos bichos no tabuleiro...")
        time.sleep(2)

        print("Contagem Regressiva: ", end="")
        for i in range(10, 0, -1):
            print(i, end=" ", flush=True)
            time.sleep(1)

    def mostra_apostas():
        os.system("cls")
        print("   1   2   3   4   5   6   7   8   9  10")
        for i in range(linhas):
            print(letras_linhas[i], end="")
            for j in range(colunas):
                print(f" {apostas[i][j]} ", end="")
            print("\n")

    def faz_aposta(num):
        while True:
            mostra_apostas()
            posicao = input(f"{num}ª Coordenada (ex: A1, B7, J10): ").strip().upper()
            if len(posicao) < 2 or len(posicao) > 3 or not posicao[0].isalpha() or not posicao[1:].isdigit():
                print("Informe no formato letra+número (A1 até J10)")
                time.sleep(2)
                continue
            x = ord(posicao[0]) - ord("A")
            y = int(posicao[1:]) - 1
            try:
                if apostas[x][y] == "🌊":
                    apostas[x][y] = jogo[x][y]
                    break
                else:
                    print("Coordenada já apostada. Tente outra")
                    time.sleep(2)
            except IndexError:
                print("Coordenada inválida. Repita")
                time.sleep(2)
        return x, y

    def verifica_tabuleiro():
        faltam = 0
        for i in range(linhas):
            for j in range(colunas):
                if apostas[i][j] == "🌊":
                    faltam += 1
        return faltam

    preenche_matriz()
    mostra_tabuleiro()

    tempo_inicial = time.time()

    while True:
        x1, y1 = faz_aposta(1)
        x2, y2 = faz_aposta(2)
        mostra_apostas()

        if apostas[x1][y1] == apostas[x2][y2]:
            print("Você acertou 😀")
            pontos += 10
            contador = verifica_tabuleiro()
            if contador == 0:
                print("Parabéns! Você venceu! 🎉🎉")
                break
            else:
                print(f"Falta Descobrir: {contador // 2} bicho(s)")
            time.sleep(2)
        else:
            print("Você Errou 🥺")
            pontos -= 5
            time.sleep(2)
            apostas[x1][y1] = "🌊"
            apostas[x2][y2] = "🌊"
            continuar = input("Continuar (S/N): ").upper()
            if continuar == "N":
                break

    tempo_final = time.time()
    duracao = int(tempo_final - tempo_inicial)

    print(f"\n\nJogador: {jogador}")
    print(f"Total de Pontos: {pontos}")
    print(f"Duração do Jogo: {duracao} segundos")

    salvar_resultado(jogador, pontos, duracao)
    mostrar_ranking(jogador, pontos, duracao)

def mostrar_ranking(jogador_atual=None, pontos_atual=None, duracao_atual=None):
    dados = carregar_ranking()
    ranking_valido = []
    linhas_invalidas = 0

    for linha in dados:
        partes = linha.strip().split(";")
        if len(partes) != 3:
            linhas_invalidas += 1
            continue
        nome = partes[0].strip()
        try:
            pontos = int(partes[1])
            duracao = int(partes[2])
        except ValueError:
            linhas_invalidas += 1
            continue
        ranking_valido.append((nome, pontos, duracao))

    ranking = sorted(ranking_valido, key=lambda x: (x[1], x[2] * -1), reverse=True)

    print()
    print("=" * 43)
    print(Fore.YELLOW + "---------< RANKING DOS JOGADORES >---------" + Style.RESET_ALL)
    print("=" * 43)
    print(Fore.CYAN + "Nº Nome do Jogador.........: Pontos Tempo.:" + Style.RESET_ALL)

    if not ranking:
        print("Nenhum jogador no ranking ainda.")
        return

    posicao = 0
    for nome, pontos, duracao in ranking:
        posicao += 1
        texto = f"{posicao:2d} {nome:25s}   {pontos:2d}   {duracao:3d} seg"
        if nome == jogador_atual and pontos == pontos_atual and duracao == duracao_atual:
            print(Fore.RED + texto + Style.RESET_ALL)
        else:
            print(texto)

    if linhas_invalidas > 0:
        print(f"\nAviso: {linhas_invalidas} linha(s) inválida(s) no ranking foram ignoradas.")


def salvar_resultado(jogador, pontos, duracao):
    with open("ranking.txt", "a", encoding="utf-8") as arq:
        arq.write(f"{jogador};{pontos};{duracao}\n")


if __name__ == "__main__":
    menu_principal()