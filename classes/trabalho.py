import re

class Processo(object):
    arrivalTime = -1
    priority = -1
    processorTime = -1
    Mbytes = -1
    impressoras = -1
    scanners = -1
    modems = -1
    CDs = -1
    tInicio = -1
    tTotalProcesso = -1
    tTotalSuspenso = -1
    estado = -1

    def __init__(self, arrivalTime, priority, processorTime, Mbytes, impressoras, scanners, modems, CDs, tInicio, tTotalProcesso, tTotalSuspenso, estado):
        self.arrivalTime = arrivalTime
        self.priority = priority
        self.processorTime = processorTime
        self.Mbytes = Mbytes
        self.impressoras = impressoras
        self.scanners = scanners
        self.modems = modems
        self.CDs = CDs
        self.tInicio = tInicio
        self.tTotalProcesso = tTotalProcesso
        self.tTotalSuspenso = tTotalSuspenso
        self.estado = estado

    def __str__(self):
        string = "Tempo de chegada : " + str(self.arrivalTime) + "\n" + "Prioridade: " + str(self.priority)
        return string

def faz_processo(arrivalTime, priority, processorTime, Mbytes, impressoras, scanners, modems, CDs, tInicio, tTotalProcesso, tTotalSuspenso, estado):
    processo = Processo(arrivalTime, priority, processorTime, Mbytes, impressoras, scanners, modems, CDs, tInicio, tTotalProcesso, tTotalSuspenso, estado)
    return processo

file = open('processos.txt', 'r')
processos = []

for line in file:
        separador = re.compile("^\s+|\s*,\s*|\s+$")
        processoAtual = [x for x in separador.split(line) if x]
        novo = faz_processo(processoAtual[0], processoAtual[1], processoAtual[2], processoAtual[3], processoAtual[4], processoAtual[5], processoAtual[6], processoAtual[7], 0, 0, 0, 0)
        processos.append(novo)

print(processos[0])