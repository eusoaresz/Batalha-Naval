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

    linhas = 10
    colunas = 10
    letras_linhas = "ABCDEFGHIJ"

    def cria_tabuleiro_agua():
        return [["🌊" for _ in range(colunas)] for _ in range(linhas)]

    def posiciona_frota(tabuleiro):
        orientacoes = ["H", "H", "V", "V"]
        random.shuffle(orientacoes)

        for indice, (navio, tamanho) in enumerate(frota):
            orientacao = orientacoes[indice]
            colocado = False

            while not colocado:
                x = random.randint(0, linhas - 1)
                y = random.randint(0, colunas - 1)

                if orientacao == "H":
                    if y + tamanho <= colunas and all(tabuleiro[x][y + k] == "🌊" for k in range(tamanho)):
                        for k in range(tamanho):
                            tabuleiro[x][y + k] = navio
                        colocado = True
                else:
                    if x + tamanho <= linhas and all(tabuleiro[x + k][y] == "🌊" for k in range(tamanho)):
                        for k in range(tamanho):
                            tabuleiro[x + k][y] = navio
                        colocado = True

    def mostra_tabuleiro_tiros(tabuleiro_tiros, titulo=None):
        os.system("cls")
        if titulo:
            print(titulo)
            print()
        print("   1   2   3   4   5   6   7   8   9  10")
        for i in range(linhas):
            print(letras_linhas[i], end="")
            for j in range(colunas):
                print(f" {tabuleiro_tiros[i][j]} ", end="")
            print("\n")

    def ler_coordenada(tabuleiro_tiros, nome_jogador=None):
        while True:
            titulo = f"Vez de {nome_jogador} | Ataque a frota inimiga" if nome_jogador else "Ataque a frota inimiga"
            mostra_tabuleiro_tiros(tabuleiro_tiros, titulo)
            posicao = input("Coordenada de tiro (ex: A1, B7, J10): ").strip().upper()
            if len(posicao) < 2 or len(posicao) > 3 or not posicao[0].isalpha() or not posicao[1:].isdigit():
                print("Informe no formato letra+número (A1 até J10)")
                time.sleep(1.5)
                continue

            x = ord(posicao[0]) - ord("A")
            y = int(posicao[1:]) - 1

            if x < 0 or x >= linhas or y < 0 or y >= colunas:
                print("Coordenada fora do tabuleiro. Repita.")
                time.sleep(1.5)
                continue

            if tabuleiro_tiros[x][y] != "🌊":
                print("Coordenada já utilizada. Tente outra.")
                time.sleep(1.5)
                continue

            return x, y

    total_setores_navio = sum(tamanho for _, tamanho in frota)
    tempo_inicial = time.time()

    if modo_dois_jogadores:
        tabuleiros_frota = [cria_tabuleiro_agua(), cria_tabuleiro_agua()]
        tabuleiros_tiros = [cria_tabuleiro_agua(), cria_tabuleiro_agua()]
        acertos_em_cada_frota = [0, 0]

        posiciona_frota(tabuleiros_frota[0])
        posiciona_frota(tabuleiros_frota[1])

        turno = 0
        while True:
            atacante = turno % 2
            defensor = 1 - atacante

            x, y = ler_coordenada(tabuleiros_tiros[atacante], jogadores[atacante])

            if tabuleiros_frota[defensor][x][y] != "🌊":
                tabuleiros_tiros[atacante][x][y] = "💥"
                acertos_em_cada_frota[defensor] += 1
                pontos_jogadores[atacante] += 10
                print(Fore.GREEN + "Acertou um navio inimigo! 💥" + Style.RESET_ALL)
            else:
                tabuleiros_tiros[atacante][x][y] = "❌"
                pontos_jogadores[atacante] -= 5
                print(Fore.RED + "Tiro na água! ❌" + Style.RESET_ALL)

            restantes = total_setores_navio - acertos_em_cada_frota[defensor]
            print(f"Setores restantes da frota inimiga: {restantes}")

            if acertos_em_cada_frota[defensor] == total_setores_navio:
                print(f"\n{jogadores[atacante]} venceu a batalha! 🏆")
                break

            input("\nPressione Enter para passar o turno...")
            turno += 1

        tempo_final = time.time()
        duracao = int(tempo_final - tempo_inicial)
        print(f"\n\nPlayer1 ({jogadores[0]}): {pontos_jogadores[0]} pontos")
        print(f"Player2 ({jogadores[1]}): {pontos_jogadores[1]} pontos")
        print(f"Duração do Jogo: {duracao} segundos")

        salvar_resultado(jogadores[0], pontos_jogadores[0], duracao)
        salvar_resultado(jogadores[1], pontos_jogadores[1], duracao)
        mostrar_ranking()
    else:
        tabuleiro_frota = cria_tabuleiro_agua()
        tabuleiro_tiros = cria_tabuleiro_agua()
        pontos = 0
        acertos = 0

        posiciona_frota(tabuleiro_frota)
        mostra_tabuleiro_tiros(tabuleiro_tiros, "A batalha começou! Escolha a primeira coordenada de tiro.")
        time.sleep(1)

        while True:
            x, y = ler_coordenada(tabuleiro_tiros)

            if tabuleiro_frota[x][y] != "🌊":
                tabuleiro_tiros[x][y] = "💥"
                acertos += 1
                pontos += 10
                print(Fore.GREEN + "Acertou um navio! 💥" + Style.RESET_ALL)
            else:
                tabuleiro_tiros[x][y] = "❌"
                pontos -= 5
                print(Fore.RED + "Tiro na água! ❌" + Style.RESET_ALL)

            restantes = total_setores_navio - acertos
            print(f"Setores de navio restantes: {restantes}")

            if acertos == total_setores_navio:
                print(Fore.YELLOW + "Parabéns! Você afundou toda a frota inimiga! 🎉🎉" + Style.RESET_ALL)
                break

            continuar = input("Continuar batalha (S/N): ").strip().upper()
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