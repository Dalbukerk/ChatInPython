from tkinter import *
import socket
import threading
import sqlite3
HOST = ''
PORT = 80
class Banco():
	def __init__(self):
		self.conexao = sqlite3.connect('servidorudpgui.db')
		self.createTable()

	def createTable(self):
		c=self.conexao.cursor()

		c.execute("""create table if not exists usuarios (
					 idusuario integer primary key autoincrement ,
					 nome text,
					 usuario text,
					 senha text)""")
		self.conexao.commit()
		c.close()

class parteGrafica:
	def __init__(self,master=None):
		self.master = master
		self.running = 0
		self.primeiroContainer = Frame(master)
		self.primeiroContainer.pack()

		self.segundoContainer = Frame(master)
		self.segundoContainer.pack()

		self.terceiroContainer = Frame(master)
		self.terceiroContainer.pack()

		self.titulo = Label(self.primeiroContainer,text="Servidor UDP")
		self.titulo.pack()

		self.scrollbary = Scrollbar(master, orient="vertical")
		self.scrollbary.pack(side=RIGHT, fill=Y)

		self.textwid = Text(master,yscrollcommand=self.scrollbary.set)
		self.textwid.pack()

		self.botao = Button(master,text="Iniciar Servidor",command=self.startserver)
		self.botao.pack()

		self.udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.orig = (HOST,PORT)
		self.udp.bind(self.orig)
		self.clientes = []	


	def workserver(self):
		while self.running:
			self.stats,self.cliente = self.udp.recvfrom(1024)
			if self.stats.decode() == "login":
				
				self.user,self.cliente = self.udp.recvfrom(1024)
				self.password,self.cliente = self.udp.recvfrom(1024)
				banco = Banco()
				try:
					cursor=banco.conexao.cursor()
					ok=False;
					cursor.execute("""SELECT * FROM usuarios;""")
					for linha in cursor.fetchall():
						if linha[2] == self.user.decode():
							senhabanco=linha[3]
							ok=True
					cursor.close()

					if ok:
						if self.password.decode() == senhabanco:
							self.reply="success"
							self.udp.sendto(self.reply.encode(),self.cliente)
							self.textwid.insert(END,str(self.cliente) + " fez login\n")		
						else:
							
							self.reply="wpassword"
							self.udp.sendto(self.reply.encode(),self.cliente)
							
					else:
						self.reply="usernotfound"
						self.udp.sendto(self.reply.encode(),self.cliente)
							

				except:
					pass					
			if self.stats.decode() == "msg" :
				try:
					self.msg,self.cliente = self.udp.recvfrom(1024)
					self.rmt,self.cliente = self.udp.recvfrom(1024)
				except:
					pass
				if self.cliente not in self.clientes:
					self.clientes.append(self.cliente)
				for d in self.clientes:
					if d != self.cliente:
						self.udp.sendto(self.msg,d)
						self.udp.sendto(self.rmt,d)

			if self.stats.decode() == "signin":
			
				self.nomeC,self.cliente = self.udp.recvfrom(1024)
				self.nick,self.cliente = self.udp.recvfrom(1024)
				self.senha,self.cliente = self.udp.recvfrom(1024)
				banco = Banco()
				self.reply=""
				try:
					cursor=banco.conexao.cursor()
					cursor.execute("""SELECT * FROM usuarios;""")
					for linha in cursor.fetchall():
						if linha[2] == self.nick.decode():	
							self.reply = "useralready"
					cursor.close()
				except:
					pass

				if self.reply != "useralready":
					banco=Banco()
					try:
						cursor=banco.conexao.cursor()
						cursor.execute("insert into usuarios (nome, usuario, senha) values ('" + self.nomeC.decode() + "','" + self.nick.decode() + "','" + self.senha.decode() + "' )")
						banco.conexao.commit()
						cursor.close()
						self.reply = "ok";
					except:
						self.reply = "fail"

				self.udp.sendto(self.reply.encode(),self.cliente)	

		self.udp.close()

	def startserver(self):
		self.running = 1
		
		self.botao["text"] = "Interromper Servidor"
		self.botao["command"] = self.endserver
		self.thread1 = threading.Thread(target=self.workserver)
		self.thread1.start()
						

	def endserver(self):
		self.running = 0
		self.botao["text"] = "Iniciar Servidor"
		self.botao["command"] = self.startserver

root = Tk()
root.wm_title("Servidor")
parteGrafica(root)
root.mainloop()
root.destroy()
