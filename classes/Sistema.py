from classes import Escalonador as es
from classes import Processo as proc

# Organiza alocação e desalocação de memória e entrada/saída.

from classes.Escalonador import *
import time

# Constantes para requisição de recursos de E/S:
IMP = 0
SCN = 1
MDM = 2
CD = 3

PRONTO = 0
EXECUTANDO = 1
SUSPENSO = 2
TERMINADO = 3

class Sistema():
    # Construtor da classe.
    def __init__(self, totalRam=8192, totalImp=2, totalScn=1, totalMdm=1, totalCd=2):
        self.__totalRAM = totalRam
        self.__tempoAtual = 0
        self.__ramUsada = 0
        self.__matrizES = []
        for i in range(4): self.__matrizES.append([0])

        # Variáveis para controle que nao serão alteradas após instanciamento da classe.
        self.maxImp = totalImp
        self.maxScn = totalScn
        self.maxMdm = totalMdm
        self.maxCd = totalCd

        #Filas de estado:
        self.listaProntos = []
        self.listaExecutando = []
        self.listaBloqueados = []
        self.listaSuspensos = []
        self.listaTerminados = []

        # Variáveis para controle. Acho que poderá ser removido futuramente
        # self.totalProcessosProntos = 0
        # self.totalProcessosExecutando = 0
        # self.totalProcessosSuspensos = 0
        # self.totalProcessosTerminados = 0

    # Organiza o 'print' da classe:
    def __str__(self):
        return "RAM Livre: " + str(self.__totalRAM) + "\n" + "RAM Usada: " + str(self.__totalRAM) + "\n" + \
               "Processos Prontos: " + str(len(self.listaProntos)) + "\n" + "Processos Executando: " + \
               str(len(self.listaExecutando)) + "\n" + "Processos Suspensos: " + str(len(self.listaSuspensos)) + "\n" + \
               "Processos Terminados: " + str(len(self.listaTerminados)) + "\n"

    # Retorna a quantidade de memória RAM total:
    def pegaTotalRam(self):
        return self.__totalRAM

    # Retorna a quantidade de RAM usada atualmente:
    def pegaRamUsada(self):
        return self.__ramUsada

    #Manda um processo de uma das 4 listas para execução:
    def executa(self, esc):
        processo, pos = self.escolheProcesso(esc)
        self.__tempoAtual += 1
        time.sleep(1)
        if (processo != None):
            if (processo.pegaEstado() == processo.EXECUTANDO): processo = esc.escalona(processo, pos)
            #As linhas seguintes deve ser alterada para prever momentos em que não há como executar E/S.
            #Por enquanto ele deixa de executar um processo que não pode acessa E/S, mas deixao na memória (ou seja, bloqueia-o).

            #As linhas comentadas devem ser descomentadas quando as funcionalidades de lista de prontos, lista de bloqueados
            # e etc. form devidamente implementadas.
            if (processo.pegaEstado() == processo.PRONTO):
                ramAlocada, processo = self.alocaMemoria(processo)
                if (ramAlocada):
                    #self.listaProntos.remove(processo)
                    esAlocado, processo = self.requisitaES(processo)
                    if esAlocado:
                        processo.setaEstado(processo.EXECUTANDO)
                        #self.listaExecutando.append(processo)
                        processo = esc.escalona(processo, pos)
                    else:
                        processo.setaEstado(processo.BLOQUEADO)
                        #self.listaBloqueados.append(processo)
                        return False
            if (processo.pegaEstado() == processo.TERMINADO):
                self.desalocaES(processo)
                self.desalocaMemoria(processo)
                #self.listaExecutando.remove(processo.setaEstado(processo.EXECUTANDO))
                #self.listaTerminados.append(processo)
            return True

    #Escolhe um processo a ser executado dentre todas as listas (se houver(em)):
    def escolheProcesso(self, esc):
        escolhido = False
        pos = -1
        proc = None
        if (not escolhido) and (len(esc.fTempoReal) != 0):
            for i in range(len(esc.fTempoReal)):
                proc = esc.fTempoReal[i]
                pos = i
                if (proc.pegaTempoChegada() <= self.__tempoAtual):
                    escolhido = True
                    break
        elif (not escolhido) and (len(esc.fUsuarioP1) != 0):
            for i in range(len(esc.fUsuarioP1)):
                proc = esc.fUsuarioP1[i]
                pos = i
                if (proc.pegaTempoChegada() <= self.__tempoAtual):
                    escolhido = True
                    break
        elif (not escolhido) and (len(esc.fUsuarioP2) != 0):
            for i in range(len(esc.fUsuarioP2)):
                proc = esc.fUsuarioP1[i]
                pos = i
                if (proc.pegaTempoChegada() <= self.__tempoAtual):
                    escolhido = True
                    break
        elif (not escolhido) and (len(esc.fUsuarioP3) != 0):
            for i in range(len(esc.fUsuarioP3)):
                proc = esc.fUsuarioP1[i]
                pos = i
                if (proc.pegaTempoChegada() <= self.__tempoAtual):
                    escolhido = True
                    break
        return proc, pos

    # Aloca memória RAM a um processo.
    def alocaMemoria(self, processo):
        if (processo.pegaEstado() == processo.PRONTO):
            if (processo.pegaMemoriaOcupada() + self.__ramUsada) < self.__totalRAM:
                self.__ramUsada += processo.pegaMemoriaOcupada()
                return True, processo
            print("Erro ao tentar alocar RAM: processo " + processo.pegaId())
            return False, processo


    # Operação simétrica à anterior.
    def desalocaMemoria(self, processo):
        if (processo.pegaEstado() == 1) or (processo.pegaEstado() == processo.SUSPENSO):
                self.__ramUsada -= processo.pegaMemoriaOcupada()
                return True, processo
        # Executar método do Escalonador para trocar o processo de listas (acredito).
        else:
            print("Erro ao tentar desalocar RAM: processo " + processo.pegaId())
            return False, processo

    # Aloca recursos de E/S de um processo:
    def requisitaES(self, processo):
        listaES = processo.pegaNumDePerifericos()
        if processo.pegaEstado() == 0:
            try:
                seraBloqueado = False
                if listaES[IMP] != 0:
                    if len(self.__matrizES[IMP]) < (len(self.__matrizES[IMP]) + listaES[IMP]):
                        for i in range(listaES[IMP]): self.__matrizES[IMP].append(processo.pegaId() + "_" + str(i))
                    else:
                        seraBloqueado = True
                if listaES[SCN] != 0:
                    if len(self.__matrizES[SCN]) < (len(self.__matrizES[SCN]) + listaES[SCN]):
                        for i in range(listaES[SCN]): self.__matrizES[SCN].append(processo.pegaId() + "_" + str(i))
                    else:
                        seraBloqueado = True
                if listaES[MDM] != 0:
                    if len(self.__matrizES[MDM]) < (len(self.__matrizES[MDM]) + listaES[MDM]):
                        for i in range(listaES[MDM]): self.__matrizES[MDM].append(processo.pegaId() + "_" + str(i))
                    else:
                        seraBloqueado = True
                if listaES[CD] != 0:
                    if len(self.__matrizES[CD]) < len(self.__matrizES[CD]) + listaES[CD]:
                        for i in range(listaES[CD]): self.__matrizES[CD].append(processo.pegaId() + "_" + str(i))
                    else:
                        seraBloqueado = True
                if seraBloqueado:
                    processo.setaEstado(processo.BLOQUEADO)
                    return False, processo
                else:
                    return True, processo
            except:
                print("Erro em requisição de E/S: processo " + processo.pegaId())

    # Desaloca recursos de E/S de um processo:
    def desalocaES(self, processo):
        listaES = processo.pegaNumDePerifericos()
        if processo.pegaEstado() == processo.EXECUTANDO:
            try:
                if listaES[IMP] != 0:
                    for i in range(listaES[IMP]): self.__matrizES[IMP].remove(processo.pegaId() + "_" + str(i))
                if listaES[SCN] != 0:
                    for i in range(listaES[SCN]): self.__matrizES[SCN].remove(processo.pegaId() + "_" + str(i))
                if listaES[MDM] != 0:
                    for i in range(listaES[MDM]): self.__matrizES[MDM].remove(processo.pegaId() + "_" + str(i))
                if listaES[CD] != 0:
                    for i in range(listaES[CD]): self.__matrizES[CD].remove(processo.pegaId() + "_" + str(i))
            except:
                print("Erro em desalocação de E/S: processo " + processo.pegaId())

    #Retorna a qtd. de dispositivos E/S livres:
    def dispositivosESLivres(self, cod):
        if cod == IMP:
            return (self.maxImp - (len(self.__matrizES[IMP]) - 1))
        elif cod == SCN:
            return (self.maxScn - (len(self.__matrizES[SCN]) - 1))
        elif cod == MDM:
            return (self.maxMdm - (len(self.__matrizES[MDM]) - 1))
        else:
            return (self.maxCd - (len(self.__matrizES[CD]) - 1))

    #Retorna o tempo atual:
    def pegaTempo(self):
        return self.__tempoAtual

    #Retorna a qtd. de RAM livre:
    def pegaMemoriaLivre(self):
        return self.__totalRAM - self.__ramUsada
