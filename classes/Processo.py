import random

class Processo(object):
    def __init__(self, arrivalTime, priority, processorTime, memoriaRam, impressoras, scanners, modems,
                 CDs, tInicio, tTotalProcesso, tTotalSuspenso, estado):
        self.arrivalTime = arrivalTime
        self.priority = priority
        self.processorTime = processorTime
        self.memoriaRam = memoriaRam
        self.listaPerifericos = [impressoras, scanners, modems, CDs]
        self.tInicio = tInicio
        self.tTotalProcesso = tTotalProcesso
        self.tTotalSuspenso = tTotalSuspenso
        self.estado = estado
        self.id = ""

        # Constantes de estado do processo.
        self.PRONTO = 0
        self.EXECUTANDO = 1
        self.BLOQUEADO = 2
        self.SUSPENSO = 3
        self.TERMINADO = 4

    # modelo do print de processo
    def __str__(self):
        return "Id: " + str(self.pegaId()) #+ "\n" + \
        #comentado so pra enxergar na hora de executar, senao fica confuso de ver
        # '''
        #        "Tempo de chegada: " + str(self.arrivalTime) + "\n" + \
        #        "Prioridade: " + str(self.priority) + "\n" + \
        #        "Tempo de serviço: " + str(self.processorTime) + "\n" + \
        #        "Memória consumida (MBytes): " + str(self.pegaMemoriaOcupada()) + "\n" + \
        #        "Impressoras usadas: " + str(self.listaPerifericos[0]) + "\n" + \
        #        "Scanners usados: " + str(self.listaPerifericos[1]) + "\n" + \
        #        "Modems usados: " + str(self.listaPerifericos[2]) + "\n" + \
        #        "Drivers de CD usados: " + str(self.listaPerifericos[3]) + "\n" + \
        #        "Tempo de início: " + str(self.tInicio) + "\n" + \
        #        "Tempo total do processo: " + str(self.tTotalProcesso) + "\n" + \
        #        "Tempo total suspenso: " + str(self.tTotalSuspenso) + "\n" + \
        #        "Estado atual: " + self.printEstado()
        # '''

    #printar o estado do processo, em vez de printar 0,1,2,3
    def printEstado(self):
        if (self.estado == 0):
            return "pronto\n"
        elif (self.estado == 1):
            return "executando\n"
        elif (self.estado == 2):
            return "suspenso\n"
        else:
            return "bloqueado\n"

    def pegaEstado(self):
        return self.estado

    def setaEstado(self, estado):
        self.estado = estado
        #suspesno ou bloqueado?
        if (estado == -1):
            print("Processo não está pronto\n")
        elif (estado == 0):
            print("Processo está pronto\n")

    def pegaPrioridade(self):
        return self.priority

    def setaPrioriade(self, p):
        self.priority = p

    def pegaTempoChegada(self):
        return self.arrivalTime

    def pegaMemoriaOcupada(self): return self.memoriaRam

    def setaTempoInicio(self, tInicio):
        self.tInicio = tInicio

    def setaTempoFim(self, tFim):
        self.tFim = tFim

    def pegaTempoFim(self):
        return self.tFim

    def pegaNumDePerifericos(self):
        return self.listaPerifericos

    def setaId(self, novoId):
        self.id = novoId

    def pegaId(self):
        return self.id

    # print(fEntrada[0])
