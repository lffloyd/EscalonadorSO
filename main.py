#self.listboxTerminados.place(x=32, y=90)



from classes.Despachante import *
from classes.Sistema import *
from classes.Processo import *
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename as fileChooser

class EscDeProcessos:
    def __init__(self, master=None):
        #Tamanho da janela
        master.minsize(width=720, height=480)
        #Variavel para saber quando o programa deve iniciar
        self.executando = FALSE
        #Iniciadores das classes
        self.sist = Sistema()
        self.arq = "processos.txt"
        self.desp = Despachante(self.arq, self.sist.pegaTotalRam())
        self.esc = Escalonador(self.desp.pegafTempoReal(), self.desp.pegafUsuarioP1(), self.desp.pegafUsuarioP2(), self.desp.pegafUsuarioP3())
        self.termAux = 0
        self.pausado = FALSE

        #1º container
        self.menu = Frame(master)
        self.menu["pady"] = 5
        self.menu.pack(side=TOP)

        #Botão de escolher o arquivo de processos no PC
        self.escolherArq = Button(self.menu, text='Escolher Arquivo', command=self.escolherArq)
        self.escolherArq["font"] = ("Arial", "10")
        self.escolherArq["width"] = 15
        self.escolherArq.pack(side=LEFT)

        #Botão que inicia a execução do sistema
        self.executar = Button(self.menu, text="Escalonar Processos")
        self.executar.bind("<Button-1>", self.escalonarProcessos)
        self.executar["font"] = ("Arial", "10")
        self.executar["width"] = 15
        self.executar.pack(side=LEFT)

        self.pause = Button(self.menu, text="Pausar", command=self.pausar)
        self.pause["font"] = ("Arial", "10")
        self.pause["width"] = 15
        #self.pause.pack(side=LEFT)

        #2º container
        self.info = Frame(master)
        self.info["pady"] = 5
        self.info.pack(side=TOP)

        #Texto para exibir o arquivo que está sendo executado no momento
        self.avisoExe = Label(self.info,text="Executando null")
        self.avisoExe["font"] = ("Arial", "10")
        self.avisoExe.pack(side=TOP)

        #Label que mostra o processo que está sendo executado
        self.pAtual = Label(self.info, text=str(self.esc.pAtual))
        self.pAtual["font"] = ("Arial", "10")
        self.pAtual.pack(side=BOTTOM)

        # 3º container
        self.memInfo = Frame(master)
        self.memInfo.pack()

        #Funções relacinadas a exibição da memória usada
        self.mem = Label(self.memInfo, text="Memória disponível: "+
                                                          str(self.sist.pegaRamUsada())+"MB usados de "+
                                                          str(self.sist.pegaTotalRam())+"MB")
        self.mem["font"] = ("Arial", "10")
        self.mem.pack(side=TOP)

        #Função para ter a barra vermelha ao completar 90%
        self.style = ttk.Style()
        self.style.theme_use('classic')
        self.style.configure("red.Horizontal.TProgressbar", background='red')

        self.memBar = ttk.Progressbar(self.memInfo, orient ="horizontal",length = 200, mode ="determinate")
        self.memBar["maximum"] = 8192
        self.memBar["value"] = self.sist.pegaRamUsada()
        self.memBar.pack(side=LEFT)

        self.porcentBar = Label(self.memInfo, text=self.percentMem())
        self.porcentBar.pack(side=LEFT)

        self.listasExecutando = Label(master, text=self.listasAtuais())
        self.listasExecutando.pack()

        # 4º container
        self.estatisticasDoSistema = Frame(master)
        self.estatisticasDoSistema.pack(side=BOTTOM)

        self.terminados = Scrollbar(master)
        self.terminados.pack(side=RIGHT, fill=Y)
        self.listboxTerminados = Listbox(master, yscrollcommand=self.terminados.set)
        self.listboxTerminados.pack(side=RIGHT)
        self.terminados.config(command=self.listboxTerminados.yview)
        self.listboxTerminados.insert(END, "Processos terminados:")
        self.listboxTerminados.bind('<<ListboxSelect>>', self.CurSelet)


        #Funções para mostrar as oscilaões das variáveis do sistema
        self.tempo = Label(self.estatisticasDoSistema, text="Tempo percorrido: "+str(self.sist.pegaTempo()))
        self.tempo.pack()

        self.impDisp = Label(self.estatisticasDoSistema,
                             text="Impressoras disponíveis: " + str(self.sist.dispositivosESLivres(0)))
        self.impDisp.pack()
        self.scnDisp = Label(self.estatisticasDoSistema,
                             text="Scanners disponíveis: " + str(self.sist.dispositivosESLivres(1)))
        self.scnDisp.pack()
        self.mdmDisp = Label(self.estatisticasDoSistema,
                             text="Modems disponíveis: " + str(self.sist.dispositivosESLivres(2)))
        self.mdmDisp.pack()
        self.cdDisp = Label(self.estatisticasDoSistema,
                             text="Drives de CD disponíveis: " + str(self.sist.dispositivosESLivres(3)))
        self.cdDisp.pack()

        # Botão para fechar o sistema
        self.sair = Button(self.estatisticasDoSistema, text="Sair")
        self.sair["font"] = ("Calibri", "10")
        self.sair["width"] = 10
        self.sair["command"] = root.destroy
        self.sair.pack(side=RIGHT, pady= 10)

    def pausar(self):
        if (self.pausado == FALSE):
            root.after_cancel(AFTER)
            self.pausado = TRUE
        else:
            self.atualizaDados()
            self.pausado = FALSE

    def create_window(self, processo):
        win = Toplevel(root)
        for i in self.sist.listaTerminados:
            if(processo == i.id):
                message ="Tempo de chegada: " + str(i.arrivalTime) + "\n" + \
                "Prioridade: " + str(i.priority) + "\n" + \
                "Tempo de serviço: " + str(i.processorTime) + "\n" + \
                "Memória consumida (MBytes): " + str(i.pegaMemoriaOcupada()) + "\n" + \
                "Impressoras usadas: " + str(i.listaPerifericos[0]) + "\n" + \
                "Scanners usados: " + str(i.listaPerifericos[1]) + "\n" + \
                "Modems usados: " + str(i.listaPerifericos[2]) + "\n" + \
                "Drivers de CD usados: " + str(i.listaPerifericos[3]) + "\n" + \
                "Tempo de início: " + str(i.tInicio) + "\n" + \
                "Tempo total do processo: " + str(i.tTotalProcesso) + "\n" + \
                "Tempo total suspenso: " + str(i.tTotalSuspenso) + "\n" + \
                "Estado atual: " + i.printEstado()
                titulo = "Histórico do processo " + i.id
        Label(win, text=message).pack()
        win.iconbitmap('win.ico')
        win.title(titulo)
        Button(win, text='OK', command=win.destroy).pack()

    def CurSelet(self, evt):
        aux = self.listboxTerminados.get(self.listboxTerminados.curselection())
        if(len(aux)<=4):
            self.create_window(aux)

    def listasAtuais(self):
        texto = "Executando de Tempo real: "
        for p in self.esc.fTempoReal:
            if (p.arrivalTime <= self.sist.pegaTempo()):
                texto += str(p.pegaId()+" - ")
        texto += "\n Executando de Prioridade 1: "
        for p in self.esc.fUsuarioP1:
            if (p.arrivalTime <= self.sist.pegaTempo()):
                texto += str(p.pegaId()+" - ")
        texto += "\n Executando de Prioridade 2: "
        for p in self.esc.fUsuarioP2:
            if (p.arrivalTime <= self.sist.pegaTempo()):
                texto += str(p.pegaId()+" - ")
        texto += "\n Executando de Prioridade 3: "
        for p in self.esc.fUsuarioP3:
            if (p.arrivalTime <= self.sist.pegaTempo()):
                texto += str(p.pegaId()+" - ")
        return texto

    def addTerminados(self):
        if(len(self.sist.listaTerminados)>self.termAux):
            self.listboxTerminados.insert(END, str((self.sist.listaTerminados[self.termAux]).pegaId()))
            self.termAux += 1

    def percentMem(self):
        if (self.memBar["value"]==0):
            return "0%"
        return str(int((self.memBar["value"]/self.memBar["maximum"])*100))+"%"

    #função relacionada ao botão escolherArquivo
    def escolherArq(self):
        self.arq = fileChooser()    #abre a busca de arquivos do sistema
        self.desp = Despachante(self.arq, self.sist.pegaTotalRam())   #cria o despachante após escolher o arquivo

    #função relacionada ao botão de executar o sistema
    def escalonarProcessos(self, event):
        self.pause.pack(side=LEFT)
        self.avisoExe["text"] = "Executando " + self.arq + "..." #Mostra o arquivo que está sendo executado
        self.desp.submeteProcesso()
        #self.desp.submeteProcesso(self.sist.pegaTempoAtual()) #cria as filas de processo
        print(self.desp.fTempoReal)
        self.esc = Escalonador(self.desp.pegafTempoReal(), self.desp.pegafUsuarioP1(), self.desp.pegafUsuarioP2(), self.desp.pegafUsuarioP3())
        self.executando = TRUE

    #função que auxilia o loop principal
    def atualizaDados(self):
        #atualizadores dos textos
        self.mem["text"] = "Memória disponível: "+str(self.sist.pegaRamUsada())+"MB usados de "+\
                           str(self.sist.pegaTotalRam())+"MB"
        self.tempo["text"] = "Tempo percorrido: " + str(self.esc.tAtual or self.sist.pegaTempo()) + "s"
        self.pAtual["text"] ="Processo Atual: "+str(self.esc.pAtual)
        self.impDisp["text"] = "Impressoras disponíveis: " + str(self.sist.dispositivosESLivres(0))
        self.scnDisp["text"] = "Scanners disponíveis: " + str(self.sist.dispositivosESLivres(1))
        self.mdmDisp["text"] = "Modems disponíveis: " + str(self.sist.dispositivosESLivres(2))
        self.cdDisp["text"] = "Drives de CD disponíveis: " + str(self.sist.dispositivosESLivres(3))

        self.addTerminados()
        self.listasExecutando["text"]=self.listasAtuais()

        #atualizador da barra
        self.memBar["value"] = self.sist.pegaRamUsada()
        self.porcentBar["text"] = self.percentMem()
        if (self.memBar["value"] >= 0.9*self.sist.pegaTotalRam()):
            self.memBar["style"] = "red.Horizontal.TProgressbar"
        if (self.memBar["value"] < 0.9*self.sist.pegaTotalRam()):
            self.memBar["style"] = ""

        #executa uma iteração do escalonamento
        if (self.executando): self.sist.executa(self.esc)
        root.update()
        global AFTER
        AFTER = root.after(100, self.atualizaDados)


#funçoes para o funcionamento e criação da janela
root = Tk()
app = EscDeProcessos(root)
root.title("Escalonador de Processos v0.01")
#root.iconbitmap('win.ico')
app.atualizaDados()
root.mainloop()