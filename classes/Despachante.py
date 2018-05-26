import re, random  # biblioteca p/ tratar das strings
from classes import Processo as proc

# from classes.Processo import *

class Despachante():
    def __init__(self, arqProcessos):
        self.fEntrada = []
        self.fTempoReal = []
        self.fUsuarioP1 = []
        self.fUsuarioP2 = []
        self.fUsuarioP3 = []
        # abre o arquivo e cria a lista de entrada que é igual ao arquivo
        self.file = open(arqProcessos, 'r')
        self.leArq()

    def leArq(self):
        # copia o arquivo p/ a lista
        for line in self.file:
            # separa a string recebida do arquivo para envia-la p/ lista
            separador = re.compile("^\s+|\s*,\s*|\s+$")
            processoAtual = [x for x in separador.split(line) if x]
            print(processoAtual)
            novo = proc.Processo(int(processoAtual[0]), int(processoAtual[1]), int(processoAtual[2]), int(processoAtual[3]),
                           int(processoAtual[4]), int(processoAtual[5]), int(processoAtual[6]), int(processoAtual[7]),
                            0, 0, 0, 0)
            self.fEntrada.append(novo)

    # def leArq(self):
    #     # copia o arquivo p/ a lista
    #     for line in self.file:
    #         # separa a string recebida do arquivo para envia-la p/ lista
    #         separador = re.compile("^\s+|\s*,\s*|\s+$")
    #         processoAtual = [x for x in separador.split(line) if x]
    #         print(processoAtual)
    #         novo = proc.Processo(int(processoAtual[0]), int(processoAtual[1]), int(processoAtual[2]), int(processoAtual[3]),
    #                        int(processoAtual[4]), int(processoAtual[5]), int(processoAtual[6]), int(processoAtual[7]),
    #                         0, 0, 0, 0)
    #         if self.verificaProcesso(novo): self.fEntrada.append(novo)
    #     self.criaID(self.fEntrada)

    #atualizado pra funcionar com "listaPerifericos"
    def verificaProcesso(self, processo):
        if ((processo.pegaMemoriaOcupada() > 8192) or (processo.listaPerifericos[0] > 2) or (processo.listaPerifericos[1] > 1) or
            (processo.listaPerifericos[2] > 1) or (processo.listaPerifericos[3] > 2) or (processo.pegaMemoriaOcupada() < 0) or
            (processo.listaPerifericos[0] < 0) or (processo.listaPerifericos[1] < 0) or (processo.listaPerifericos[2] < 0)
            or (processo.listaPerifericos[3] < 0)):
            return False
        return True

    def criaID(self, fEntrada):
        cont1, cont2 = 1, 1
        for i in range(fEntrada.__len__()):
            if fEntrada[i].priority == 0:
                fEntrada[i].id = 'T' + str(cont1)
                cont1 += 1
            else:
                fEntrada[i].id = 'U' + str(cont2)
                cont2 += 1

    # def submeteProcesso(self):
    #     #cria os IDs antes, durante a submissao fica mais complicado
    #     self.criaID(self.fEntrada)
    #     for i in self.fEntrada:
    #         if (self.verificaProcesso(i)):
    #             if (i.priority == 0):
    #                 self.fTempoReal.append(i)
    #             elif (i.priority == 1):
    #                 self.fUsuarioP1.append(i)
    #             elif (i.priority == 2):
    #                 self.fUsuarioP2.append(i)
    #             elif (i.priority == 3):
    #                 self.fUsuarioP3.append(i)
    #         else:
    #             print("PROCESSO INVÁLIDO")

    def submeteProcesso(self):
        self.criaID(self.fEntrada)
        for i in self.fEntrada:
            if (self.verificaProcesso(i)):
                if (i.priority == 0):
                    self.fTempoReal.append(i)
                elif (i.priority == 1):
                    self.fUsuarioP1.append(i)
                elif (i.priority == 2):
                    self.fUsuarioP2.append(i)
                elif (i.priority == 3):
                    self.fUsuarioP3.append(i)
        self.fTempoReal.sort(key=lambda x: x.arrivalTime)
        for i in range(len(self.fTempoReal)):
            print("ordem:", i, self.fTempoReal[i].pegaId())
        self.fTempoReal.sort(key=lambda x: x.arrivalTime)
        for i in range(len(self.fTempoReal)):
            print("ordem:", i, self.fTempoReal[i].pegaId())
        self.fTempoReal.sort(key=lambda x: x.arrivalTime)
        for i in range(len(self.fTempoReal)):
            print("ordem:", i, self.fTempoReal[i].pegaId())

    # def submeteProcesso(self, tempo):
    #     self.criaID(self.fEntrada)
    #     for i in self.fEntrada:
    #         if (i.arrivalTime == tempo):
    #             if (i.priority == 0):
    #                 self.fTempoReal.append(self.fEntrada.pop(0))
    #             elif (i.priority == 1):
    #                 self.fUsuarioP1.append(self.fEntrada.pop(0))
    #             elif (i.priority == 2):
    #                 self.fUsuarioP2.append(self.fEntrada.pop(0))
    #             elif (i.priority == 3):
    #                 self.fUsuarioP3.append(self.fEntrada.pop(0))
    #         else:
    #             break

    def pegafTempoReal(self):
        return self.fTempoReal

    def pegafUsuarioP1(self):
        return self.fUsuarioP1

    def pegafUsuarioP2(self):
        return self.fUsuarioP2

    def pegafUsuarioP3(self):
        return self.fUsuarioP3
