from classes.Despachante import *
from classes.Sistema import *
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
        self.arq = "processos.txt"
        self.desp = Despachante(self.arq)
        self.esc = Escalonador(self.desp.pegafTempoReal(), self.desp.pegafUsuarioP1(), self.desp.pegafUsuarioP2(), self.desp.pegafUsuarioP3())
        self.sist = Sistema()

        #1º container
        self.widget1 = Frame(master)
        self.widget1["pady"] = 20
        self.widget1.pack()

        #Botão de escolher o arquivo de processos no PC
        self.escolherArq = Button(self.widget1, text='Escolher Arquivo', command=self.escolherArq)
        self.escolherArq["font"] = ("Arial", "10")
        self.escolherArq.pack()

        #Botão que inicia a execução do sistema
        self.executar = Button(self.widget1, text="Escalonar Processos")
        self.executar["font"] = ("Arial", "10")
        self.executar.bind("<Button-1>", self.escalonarProcessos)
        self.executar.pack()

        #Texto para exibir o arquivo que está sendo executado no momento
        self.avisoExe = Label(self.widget1,text="")
        self.avisoExe["font"] = ("Arial", "10")
        self.avisoExe.pack()

        #Label que mostra o processo que está sendo executado
        self.pAtual = Label(self.widget1, text="Processo Atual: "+str(self.esc.pAtual))
        self.pAtual["font"] = ("Arial", "10")
        self.pAtual.pack()

        #Botão para fechar o sistema
        self.sair = Button(self.widget1)
        self.sair["text"] = "Sair"
        self.sair["font"] = ("Calibri", "10")
        self.sair["width"] = 5
        self.sair["command"] = root.destroy
        self.sair.pack(side=RIGHT)

        #2º container
        self.estatisticasDoSistema = Frame(master)
        self.estatisticasDoSistema.pack()

        #Funções relacinadas a exibição da memória usada
        self.mem = Label(self.estatisticasDoSistema, text="Memória disponível: "+
                                                          str(self.sist.pegaRamUsada())+"MB usados de "+
                                                          str(self.sist.pegaTotalRam())+"MB")
        self.mem["font"] = ("Arial", "10")
        self.mem.pack()

        #Função para ter a barra vermelha ao completar 100%
        self.style = ttk.Style()
        self.style.theme_use('classic')
        self.style.configure("red.Horizontal.TProgressbar", background='red')

        self.memBar = ttk.Progressbar(self.estatisticasDoSistema, orient ="horizontal",length = 200, mode ="determinate")
        self.memBar["maximum"] = 8192
        self.memBar["value"] = self.sist.pegaRamUsada()
        self.memBar.pack()

        #Funções para mostrar as oscilaões das variáveis do sistema
        self.tempo = Label(self.estatisticasDoSistema, text="Tempo percorrido: "+str(self.esc.tAtual))
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

    #função relacionada ao botão escolherArquivo
    def escolherArq(self):
        self.arq = fileChooser()    #abre a busca de arquivos do sistema
        self.desp = Despachante(self.arq)   #cria o despachante após escolher o arquivo

    #função relacionada ao botão de executar o sistema
    def escalonarProcessos(self, event):
        self.avisoExe["text"] = "Executando " + self.arq + "..." #Mostra o arquivo que está sendo executado
        self.desp.submeteProcesso() #cria as filas de processo
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

        #atualizador da barra
        self.memBar["value"] = self.sist.pegaRamUsada()
        if (self.memBar["value"] >= 8192):
            self.memBar["style"] = "red.Horizontal.TProgressbar"
        if (self.memBar["value"] < 8192):
            self.memBar["style"] = ""

        #executa uma iteração do escalonamento
        if (self.executando): self.sist.executa(self.esc)
        root.update()
        root.after(100, self.atualizaDados)

#funçoes para o funcionamento e criação da janela
root = Tk()
app = EscDeProcessos(root)
root.title("Escalonador de Processos v0.01")
app.atualizaDados()
root.mainloop()