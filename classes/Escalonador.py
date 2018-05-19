from classes import Processo as proc


# Responsável pelo escalonamento (execução, suspensão e término) de processos.
class Escalonador(object):
    def __init__(self, fTReal, fUs1, fUs2, fUs3):
        self.fTempoReal = fTReal
        self.fUsuarioP1 = fUs1
        self.fUsuarioP2 = fUs2
        self.fUsuarioP3 = fUs3
        self.tAtual = 0
        self.pAtual = "null"
        self.quantum = 2

    #Escalona um processo por um pedaço de tempo a cada vez que a função é chamada.
    def escalona(self, p, i):
        self.pAtual = p
        if (p.pegaEstado == 0):
            p.setaEstado = 1
        if (p.tInicio == 0):
            p.setaTempoInicio(self.tAtual)
        p.tTotalProcesso += 1
        self.tAtual += 1
        #Se um processo de tempo real (prioridade 0) chegou a seu fim:
        if (p.tTotalProcesso == p.processorTime):
            p.setaTempoFim(self.tAtual)
            p.setaEstado(4) #Tem que fazer isso aqui.
            if (p.pegaPrioridade() == 0): self.fTempoReal.pop(i)
        #Para processos de usuário (prioridades 1-3):
        else:
            if (p.pegaPrioridade == 1):
                self.fUsuarioP1.pop(i)
                p.setaPrioridade(2)
                if (p.tTotalProcesso != p.processorTime): self.fUsuarioP2.append(p)  #Adiciona na próxima fila (política de feedback)
            elif (p.pegaPrioridade == 2):
                self.fUsuarioP2.pop(i)
                p.setaPrioridade(3)
                if (p.tTotalProcesso != p.processorTime): self.fUsuarioP3.append(p)
            elif (p.pegaPrioridade == 3):
                self.fUsuarioP3.pop(i)
                p.setaPrioridade(1)
                if (p.tTotalProcesso != p.processorTime): self.fUsuarioP1.append(p)
        print(p)
        return p

    # def escalona(self, p):
    #     self.pAtual = p
    #     if (p.tInicio == 0):
    #         p.setaTempoInicio(self.tAtual)
    #     terminado = False
    #     p.tTotalProcesso += 1
    #     self.tAtual += 1
    #     if (p.priority == 0):
    #         if (p.tTotalProcesso == p.processorTime):
    #             p.setaTempoFim(self.tAtual)
    #             self.fTempoReal.pop(0)
    #     else:
    #         if (p.tTotalProcesso == p.processorTime):
    #             terminado = True
    #             p.setaTempoFim(self.tAtual)
    #         if (p.priority == 1):
    #             p.priority = 2
    #             self.fUsuarioP1.pop(0)
    #             if (not terminado):
    #                 self.fUsuarioP2.append(p)  # adiciona na proxima fila
    #         elif (p.priority == 2):
    #             p.priority = 3
    #             self.fUsuarioP2.pop(0)
    #             if (not terminado):
    #                 self.fUsuarioP3.append(p)
    #         elif (p.priority == 3):
    #             p.priority = 1
    #             self.fUsuarioP3.pop(0)
    #             if (not terminado):
    #                 self.fUsuarioP1.append(p)
    #     print(p)

    def pegaProcesso(self, fila, indice):
        if fila == 0: return self.fTempoReal[indice]
        elif fila == 1: return self.fUsuarioP1[indice]
        elif fila == 1: return self.fUsuarioP2[indice]
        else: return self.fUsuarioP3[indice]

    def suspende(self, p):
        return