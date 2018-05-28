from classes import Processo as proc

# Responsável pelo escalonamento (execução, suspensão e término) de processos.
class Escalonador(object):
    def __init__(self, fTReal, fUs1, fUs2, fUs3):
        self.tAtual = 0
        self.pAtual = None
        self.totalQuantums = 2
        self.TR = 0
        self.U1 = 1
        self.U2 = 2
        self.U3 = 3
        self.filas = [fTReal, fUs1, fUs2, fUs3]

    #Responsável por escalonar um processo. Emprega "round robin" (fila de TR) e "feedback" (filas de prioridade de usuário) para isso.
    def escalona(self, p, i, tAtual):
        self.pAtual = p
        if (p.pegaEstado() == p.PRONTO):
            p.setaEstado(p.EXECUTANDO)
            p.setaTempoInicio(tAtual)
        self.tAtual = tAtual
        #Se um processo chegou a seu fim:
        if (p.pegaTempoTotal() == p.pegaTempoDeServico()):
            p.setaTempoFim(tAtual)
            p.setaEstado(p.TERMINADO) #Tem que fazer isso aqui.
            if (p.pegaPrioridade() == 0): self.filas[self.TR].pop(i)
        #Para processos de usuário (prioridades 1-3):
        else:
            #Filas de prioridade de usuário. Seguem a política de escalonanamento "feedback", usando quantum = 2.
            executarTroca = False
            if (p.pegaQuantums() == self.totalQuantums):
                p.setaQuantums(0)
                executarTroca = True
            else: p.incrementaQuantums(1)
            if (p.pegaPrioridade() == 1):
                if (executarTroca):
                    self.filas[self.U1].pop(i)
                    p.setaPrioridade(2)
                    self.filas[self.U2].append(p)  #Adiciona na próxima fila (política de feedback)
            elif (p.pegaPrioridade() == 2):
                if (executarTroca):
                    self.filas[self.U2].pop(i)
                    p.setaPrioridade(3)
                    self.filas[self.U3].append(p)
            elif (p.pegaPrioridade() == 3):
                if (executarTroca):
                    self.filas[self.U3].pop(i)
                    p.setaPrioridade(1)
                    self.filas[self.U1].append(p)
        p.incrementaTempoTotal(1)
        print(p)
        return p

    #Seleciona um determinado processo de uma das filas de prioridade conforme o parâmetro passado como índice para a função:
    def pegaProcesso(self, fila, indice):
        if fila == 0: return self.filas[self.TR][indice]
        elif fila == 1: return self.filas[self.U1][indice]
        elif fila == 1: return self.filas[self.U2][indice]
        else: return self.filas[self.U3][indice]