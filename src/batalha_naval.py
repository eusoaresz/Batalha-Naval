import random
import time
import os
from colorama import Fore, Style, just_fix_windows_console

# Habilita suporte a cores ANSI no console Windows (PowerShell/VS Code Terminal)
just_fix_windows_console()

# Frota com tamanho real de cada navio (1, 2, 3 e 4 casas)
frota = [("🛥️", 1), ("⛴️", 2), ("🛳️", 3), ("🚢", 4)]

def carregar_ranking():
    dados = []
    if os.path.isfile("ranking.txt"):
        with open("ranking.txt", "r", encoding="utf-8") as arq:
            dados = arq.readlines()
    return dados

def menu_principal():
    while True:
        os.system("cls")
        print(Fore.BLUE + "=" * 40 + Style.RESET_ALL)
        print(Fore.YELLOW + "||" + Fore.RED + "----------{BATALHA NAVAL}-----------" + Style.RESET_ALL + Fore.YELLOW + "||")
        print(Fore.BLUE + "=" * 40 + Style.RESET_ALL)
        print(Fore.YELLOW + "||" + Fore.WHITE + "1 - Iniciar jogo                    " + Style.RESET_ALL + Fore.YELLOW + "||")
        print(Fore.YELLOW + "||" + Fore.WHITE + "2 - Ver ranking                     " + Style.RESET_ALL + Fore.YELLOW + "||")
        print(Fore.YELLOW + "||" + Fore.WHITE + "3 - Ver Regras                      " + Style.RESET_ALL + Fore.YELLOW + "||")
        print(Fore.YELLOW + "||" + Fore.WHITE + "4 - Finalizar                       " + Style.RESET_ALL + Fore.YELLOW + "||")
        print(Fore.BLUE + "=" * 40 + Style.RESET_ALL)
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            os.system("cls")
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
    print(Fore.BLUE + "=" * 40 + Style.RESET_ALL)
    print(Fore.YELLOW + "||" + Fore.RED + "----------=VAMOS A BATALHA=---------" + Style.RESET_ALL + Fore.YELLOW + "||")
    print(Fore.BLUE + "=" * 40 + Style.RESET_ALL)
    print(Fore.YELLOW + "||" + Fore.WHITE + "1 - Jogar contra o computador       " + Style.RESET_ALL + Fore.YELLOW + "||")
    print(Fore.YELLOW + "||" + Fore.WHITE + "2 - Jogar contra outro jogador      " + Style.RESET_ALL + Fore.YELLOW + "||")
    print(Fore.YELLOW + "||" + Fore.WHITE + "3 - Voltar ao menu                  " + Style.RESET_ALL + Fore.YELLOW + "||")
    print(Fore.BLUE + "=" * 40 + Style.RESET_ALL)

    escolha = input("\nEscolha uma opção: ").strip()
    modo_dois_jogadores = False
    if escolha == "1":
        jogador = "Computador"
    elif escolha == "2":
        modo_dois_jogadores = True
        jogador1 = input("\nNome do Jogador 1: ").strip() or "Player1"
        jogador2 = input("Nome do Jogador 2: ").strip() or "Player2"
        jogadores = [jogador1, jogador2]
        pontos_jogadores = [0, 0]
    else:
        return
    
    pontos = 0
    linhas = 10
    colunas = 10
    letras_linhas = "ABCDEFGHIJ"

    jogo = []
    apostas = []

    def preenche_matriz():
        for i in range(linhas):
            jogo.append([])
            apostas.append([])
            for _ in range(colunas):
                jogo[i].append("🌊")
                apostas[i].append("🌊")

        # Garante navios horizontais e verticais no tabuleiro
        orientacoes = ["H", "H", "V", "V"]
        random.shuffle(orientacoes)

        for indice, (navio, tamanho) in enumerate(frota):
            orientacao = orientacoes[indice]
            colocado = False

            while not colocado:
                x = random.randint(0, linhas - 1)
                y = random.randint(0, colunas - 1)

                if orientacao == "H":
                    if y + tamanho <= colunas and all(jogo[x][y + k] == "🌊" for k in range(tamanho)):
                        for k in range(tamanho):
                            jogo[x][y + k] = navio
                        colocado = True
                else:
                    if x + tamanho <= linhas and all(jogo[x + k][y] == "🌊" for k in range(tamanho)):
                        for k in range(tamanho):
                            jogo[x + k][y] = navio
                        colocado = True

    def mostra_apostas():
        os.system("cls")
        print("   1   2   3   4   5   6   7   8   9  10")
        for i in range(linhas):
            print(letras_linhas[i], end="")
            for j in range(colunas):
                print(f" {apostas[i][j]} ", end="")
            print("\n")

    def faz_aposta(vez_jogador=None):
        while True:
            mostra_apostas()
            if vez_jogador:
                print(f"Vez do {vez_jogador}")
            posicao = input("Coordenada de tiro (ex: A1, B7, J10): ").strip().upper()
            if len(posicao) < 2 or len(posicao) > 3 or not posicao[0].isalpha() or not posicao[1:].isdigit():
                print("Informe no formato letra+número (A1 até J10)")
                time.sleep(2)
                continue
            x = ord(posicao[0]) - ord("A")
            y = int(posicao[1:]) - 1
            try:
                if apostas[x][y] == "🌊":
                    break
                else:
                    print("Coordenada já apostada. Tente outra")
                    time.sleep(2)
            except IndexError:
                print("Coordenada inválida. Repita")
                time.sleep(2)
        return x, y

    total_setores_navio = sum(tamanho for _, tamanho in frota)
    acertos_totais = 0

    preenche_matriz()
    mostra_apostas()
    print("A batalha começou! Escolha a primeira coordenada de tiro.")
    time.sleep(1)

    tempo_inicial = time.time()
    turno = 0

    while True:
        indice_jogador = turno % 2
        vez_jogador = jogadores[indice_jogador] if modo_dois_jogadores else None

        if modo_dois_jogadores:
            x, y = faz_aposta(vez_jogador)
        else:
            x, y = faz_aposta()

        mostra_apostas()

        if jogo[x][y] != "🌊":
            apostas[x][y] = "💥"
            print("Acertou um navio! 💥")
            acertos_totais += 1
            if modo_dois_jogadores:
                pontos_jogadores[indice_jogador] += 10
            else:
                pontos += 10

            setores_restantes = total_setores_navio - acertos_totais
            if setores_restantes == 0:
                print("Parabéns! Você afundou toda a frota inimiga! 🎉🎉")
                break
            else:
                print(f"Setores de navio restantes: {setores_restantes}")
            time.sleep(2)
        else:
            apostas[x][y] = "❌"
            print("Tiro na água! ❌")
            if modo_dois_jogadores:
                pontos_jogadores[indice_jogador] -= 5
            else:
                pontos -= 5
            time.sleep(2)
            continuar = input("Continuar batalha (S/N): ").upper()
            if continuar == "N":
                break

        turno += 1

    tempo_final = time.time()
    duracao = int(tempo_final - tempo_inicial)

    if modo_dois_jogadores:
        print(f"\n\nPlayer1 ({jogadores[0]}): {pontos_jogadores[0]} pontos")
        print(f"Player2 ({jogadores[1]}): {pontos_jogadores[1]} pontos")
    else:
        print(f"\n\nJogador: {jogador}")
        print(f"Total de Pontos: {pontos}")

    print(f"Duração do Jogo: {duracao} segundos")

    if modo_dois_jogadores:
        salvar_resultado(jogadores[0], pontos_jogadores[0], duracao)
        salvar_resultado(jogadores[1], pontos_jogadores[1], duracao)
        mostrar_ranking()
    else:
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
    print(Fore.BLUE + "=" * 43 + Style.RESET_ALL)
    print(Fore.YELLOW + "---------< RANKING DOS JOGADORES >---------" + Style.RESET_ALL)
    print(Fore.BLUE + "=" * 43 + Style.RESET_ALL)
    print(Fore.MAGENTA + "Nº Nome do Jogador.........: Pontos Tempo.:" + Style.RESET_ALL)

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