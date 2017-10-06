from tkinter import *
import socket
import threading
import queue
HOST = '127.0.0.1'
PORT = 80
username=""
class parteGrafica:
	def __init__(self,master=None):
		self.master = master
		self.fila = queue.Queue()
		self.primeiroContainer = Frame(master)
		self.primeiroContainer.pack()

		self.segundoContainer = Frame(master)
		self.segundoContainer.pack()

		self.terceiroContainer = Frame(master)
		self.terceiroContainer.pack()

		self.quartoContainer = Frame(master)
		self.quartoContainer.pack()

		self.titulo = Label(self.primeiroContainer,text="Cliente UDP")
		self.titulo.pack()

		self.scrollbary = Scrollbar(self.segundoContainer, orient="vertical")
		self.scrollbary.pack(side=RIGHT, fill=Y)

		self.textwid = Text(self.segundoContainer,yscrollcommand=self.scrollbary.set)
		self.textwid.config(state=DISABLED)
		self.textwid.pack()

		self.scrollbary.config(command=self.textwid.yview)

		self.mensagem = Entry(self.terceiroContainer)
		self.mensagem.bind("<Return>",self.noenter)
		self.mensagem.pack()

		self.botao = Button(self.quartoContainer,text="Enviar",command=self.enviar)
		self.botao.pack()

		self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.udp.setblocking(False)
		self.dest=(HOST,PORT)
		self.udp.sendto(("msg").encode(),self.dest)
		self.udp.sendto(("").encode(),self.dest)
		self.udp.sendto(username.encode(),self.dest)
		self.thread1 = threading.Thread(target=self.work)
		self.thread1.start()

	def noenter(self,event):
		self.enviar()

	def enviar(self):
		self.fila.put(self.mensagem.get())
		self.mensagem.delete(0,'end')

	def work(self):
		while True:
			try:
				self.msgr,self.srv = self.udp.recvfrom(1024)
				self.rmt,self.svr2 = self.udp.recvfrom(1024)
				if self.msgr.decode() != "":
					self.textwid.config(state=NORMAL)
					self.textwid.insert(END,self.msgr.decode() + "\n" + self.rmt.decode() + "\n")
					self.textwid.config(state=DISABLED)

			except:
				pass
			try:
				if not self.fila.empty():
					self.msg = str(self.fila.get())
				else :
					self.msg = ""

				if self.msg != "":
					self.textwid.config(state=NORMAL)
					self.textwid.tag_config("m", justify='right')
					self.textwid.insert(END,self.msg + "\n" + username + "\n", "m")
					self.textwid.config(state=DISABLED)
					self.stats = "msg"
					self.udp.sendto(self.stats.encode(),self.dest)
					self.udp.sendto(self.msg.encode(),self.dest)
					self.udp.sendto(username.encode(),self.dest)
					
			except :
				pass
		self.udp.close()


