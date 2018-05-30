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

NOVO = 0
PRONTO = 1
EXECUTANDO = 2
BLOQUEADO = 3
SUSPENSO = 4
TERMINADO = 5

class Sistema():
    # Construtor da classe.
    def __init__(self, totalRam=8192, totalImp=2, totalScn=1, totalMdm=1, totalCd=2):
        self.__totalRAM = totalRam
        self.__tempoAtual = 0
        self.__ramUsada = 0
        self.__matrizES = []
        for i in range(4): self.__matrizES.append([])

        # Variáveis para controle que nao serão alteradas após instanciamento da classe.
        self.maxImp = totalImp
        self.maxScn = totalScn
        self.maxMdm = totalMdm
        self.maxCd = totalCd

        self.maximos = [totalImp, totalScn, totalMdm, totalCd]

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

    #Atualiza os tempos totais de duração de todos os processos já submetidos e carrega em RAM processos novos que
    #possam ser carregados::
    def atualizaProcessos(self, esc):
        for pr in self.listaBloqueados: pr.incrementaTempoTotal(1)
        for pr in self.listaSuspensos: pr.incrementaTempoTotal(1)
        for fila in esc.filas[:]:
            for pr in fila[:]:
                pr.incrementaTempoTotal(1)
                if (pr.pegaEstado() == pr.BLOQUEADO):
                    if pr not in self.listaBloqueados:
                        esc.filas[pr.pegaPrioridade()].remove(pr)
                        self.listaBloqueados.append(pr)
                if (pr.pegaEstado() == pr.SUSPENSO):
                    if pr not in self.listaSuspensos:
                        esc.filas[pr.pegaPrioridade()].remove(pr)
                        self.listaSuspensos.append(pr)
                self.atualizaEstado(pr, esc)
        return

    #Executa um processo, ordenando que o escalonador orquestre a execução do mesmo:
    def executa(self, esc):
        self.atualizaProcessos(esc)
        proc = self.escolheProcesso(esc)
        #print("Entrou no executa() " + str(proc))
        time.sleep(0.3)
        if (proc != None):
            if (proc.pegaEstado() == proc.EXECUTANDO): proc = esc.escalona(proc, self.__tempoAtual)
            if (proc.pegaEstado() == proc.PRONTO):
                #self.listaProntos.remove(proc)
                proc.setaEstado(proc.EXECUTANDO)
                proc.setaTempoInicio(self.__tempoAtual)
                self.listaExecutando.append(proc)
                proc = esc.escalona(proc, self.__tempoAtual)
            if (proc.pegaEstado() == proc.TERMINADO):
                print("Processo " + proc.pegaId() + " terminado\n")
                self.listaExecutando.remove(proc)
                self.desalocaES(proc)
                self.desalocaMemoria(proc)
                proc.setaTempoFim(self.__tempoAtual)
                esc.filas[proc.pegaPrioridade()].remove(proc)
                #self.listaTerminados.append(proc)
        self.__tempoAtual += 1
        return

    #Escolhe um processo para execução:
    def escolheProcesso(self, esc):
        for i in range(len(esc.filas)):
            if (len(esc.filas[i]) > 0):
                if (esc.filas[i][0].pegaId() == "U-4"):
                    print(esc.filas[i][0])
                    break
                if (esc.filas[i][0].pegaEstado() == esc.filas[i][0].PRONTO) or \
                    (esc.filas[i][0].pegaEstado() == esc.filas[i][0].EXECUTANDO): return esc.filas[i][0]
        #for i in range(len(esc.filas)): esc.imprimeFila(esc.filas[i], i)
        return None

    #Atualiza o estado de um processo conforme suas demandas por RAM e E/S são atendidas num dado momento.
    def atualizaEstado(self, pr, esc):
        if (pr.pegaEstado() == pr.BLOQUEADO): self.alocaESEReorganiza(pr, esc)
        if (pr.pegaEstado() == pr.SUSPENSO) or (pr.pegaEstado() == pr.NOVO):
            self.alocaMemoria(pr)
            if (pr.ramFoiAlocada()): self.alocaESEReorganiza(pr, esc)
            if (pr.pegaEstado() == pr.NOVO) and (not pr.ramFoiAlocada()):  # Nesse caso, o processo não pôde ser alocado em RAM e algum processo (provavelmente mais antigo)
                # deve ser suspenso para que o novo processo pronto seja alocado.
                for bloq in self.listaBloqueados[:]:
                    if (bloq.pegaMemoriaOcupada() >= pr.pegaMemoriaOcupada()):
                        #self.listaBloqueados.remove(bloq)
                        self.desalocaMemoria(bloq)
                        bloq.setaEstado(bloq.SUSPENSO)
                        #self.listaSuspensos.append(bloq)
                        self.alocaMemoria(pr)
                        if (pr.ramFoiAlocada()): self.alocaESEReorganiza(pr, esc)
                        break
        return pr

    #Ordena a alocação de dispositivos E/S a um processo e a transferência desse processo entre filas de prioridade.
    def alocaESEReorganiza(self, processo, esc):
        if (processo.pegaEstado() == processo.SUSPENSO): self.listaSuspensos.remove(processo)
        self.requisitaES(processo)
        if (processo.esFoiAlocada()):
            if (processo.pegaEstado() == processo.BLOQUEADO): self.listaBloqueados.remove(processo)
            processo.setaEstado(processo.PRONTO)
            #self.listaProntos.append(processo)
            esc.filas[processo.pegaPrioridade()].append(processo)
        else:
            if (processo.pegaEstado() != processo.BLOQUEADO):
                processo.setaEstado(processo.BLOQUEADO)
                #self.listaBloqueados.append(processo)
                esc.filas[processo.pegaPrioridade()].remove(processo)

    # Aloca memória RAM a um processo.
    def alocaMemoria(self, processo):
        if (not processo.ramFoiAlocada()):
            if (processo.pegaEstado() == processo.NOVO) or (processo.pegaEstado() == processo.SUSPENSO):
                if (processo.pegaMemoriaOcupada() + self.__ramUsada) <= self.__totalRAM:
                    self.__ramUsada += processo.pegaMemoriaOcupada()
                    processo.setaEstadoAlocacaoRam(True)
                    return True, processo
            print("Erro ao tentar alocar RAM: processo " + processo.pegaId())
            return False, processo

    # Operação simétrica à anterior.
    def desalocaMemoria(self, processo):
        if (processo.ramFoiAlocada()):
            if (processo.pegaEstado() == processo.TERMINADO) or (processo.pegaEstado() == processo.BLOQUEADO):
                if ((self.__ramUsada - processo.pegaMemoriaOcupada()) >= 0):
                    self.__ramUsada -= processo.pegaMemoriaOcupada()
                    processo.setaEstadoAlocacaoRam(False)
                    return True, processo
            # Executar método do Escalonador para trocar o processo de listas (acredito).
                else:
                    #print("Erro ao tentar desalocar RAM: processo " + processo.pegaId())
                    return False, processo
            else: return False, processo

    # Aloca recursos de E/S de um processo:
    def requisitaES(self, processo):
        if (not processo.esFoiAlocada()):
            listaES = processo.pegaNumDePerifericos()
            #print("Lista E/S do processo " + processo.pegaId()) #print(listaES)
            if (processo.pegaEstado() == processo.NOVO) or (processo.pegaEstado() == processo.SUSPENSO) or \
                    (processo.pegaEstado() == processo.BLOQUEADO):
                #for i in range(len(self.__matrizES)):
                for i in range(len(self.__matrizES[:])):
                    if (listaES[i] != 0):
                        if ((len(self.__matrizES[i]) + listaES[i]) <= (self.maximos[i])):
                            for j in range(listaES[i]): self.__matrizES[i].append(processo.pegaId() + "_" + str(j))
                        else:
                            print("Erro em requisição de E/S: processo " + processo.pegaId())
                            return False, processo
                processo.setaEstadoAlocacaoES(True)
                return True, processo

    # Desaloca recursos de E/S de um processo:
    def desalocaES(self, processo):
        if (processo.esFoiAlocada()):
            listaES = processo.pegaNumDePerifericos()
            if (processo.pegaEstado() == processo.TERMINADO):
                    #for i in range(len(self.__matrizES)):
                    for i in range(len(self.__matrizES[:])):
                        if (listaES[i] != 0):
                            for j in range(listaES[i]):
                                if (processo.pegaId() + "_" + str(j)) in self.__matrizES[i]:
                                    self.__matrizES[i].remove(processo.pegaId() + "_" + str(j))
                    processo.setaEstadoAlocacaoES(False)
                    return True, processo
            print("Erro em desalocação de E/S: processo " + processo.pegaId())
            return False, processo

    #Retorna a qtd. de dispositivos E/S livres:
    def dispositivosESLivres(self, cod):
        if cod == IMP: return (self.maxImp - (len(self.__matrizES[IMP])))
        elif cod == SCN: return (self.maxScn - (len(self.__matrizES[SCN])))
        elif cod == MDM: return (self.maxMdm - (len(self.__matrizES[MDM])))
        else: return (self.maxCd - (len(self.__matrizES[CD])))

    #Retorna a qtd. de RAM livre:
    def pegaMemoriaLivre(self):
        return self.__totalRAM - self.__ramUsada

    #Retorna o tempo atual do sistema:
    def pegaTempoAtual(self):
        return self.__tempoAtual