from .Processo import Processo

class Despachante:

    def criaProcesso(tempo_chegada, prioridade, tempo_execucao, tamanho, impressora, scanner, modem, cd):

        p =  Processo(tempo_chegada, prioridade, tempo_execucao, tamanho, impressora, scanner, modem, cd)

        if (tamanho > 8192 or impressora > 2 or scanner > 1 or modem > 1 or cd > 2 or tamanho < 0 or impressora < 0 or
            scanner < 0 or modem < 0 or cd < 0):
            print ("dados invalidos.")
        else:
            if (prioridade == 0):
                fTempoReal[0].append(p)
            elif (prioridade > 1):
                tam = len(fUsuarioP1)
                for i in range (0, tam):
                    if (fUsuarioP1[i].prioridade > p.prioridade):
                        fUsuarioP1.insert(i, p)
                        break
                    if (i == tam):
                        fUsuarioP1.append(p)
            else:
                raise ValueError("Dados invalidos")



