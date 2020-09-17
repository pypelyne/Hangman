import re
from random_word import RandomWords
from tkinter import Tk, Label, Button, StringVar, Entry,IntVar, messagebox, Checkbutton, Toplevel

class insertBox:
	def __init__(self,master):
		self.top=Toplevel(master)
		self.customEntry=Entry(self.top,show='*')
		self.customEntry.pack()
		self.customEntry.bind("<Return>",self.sendCustomWord)
		self.customEntry.focus()
	def sendCustomWord(self,event):
		self.customWord=self.customEntry.get()
		self.top.destroy()
class gui:
	def __init__(self,master):
		self.ranWordGen=RandomWords()
		print("check your internet connection!")
		master.title("Hangman")
		self.dashtext=StringVar()
		self.attempttext=StringVar()
		self.complicated=IntVar()



		self.dashes = Label(master, textvariable=self.dashtext)
		self.attempts=Label(master, textvariable=self.attempttext)
		self.dashes.pack()

		self.lives=IntVar()
		self.liveslabel=Label(master,textvariable=self.lives)
		self.liveslabel.pack()

		self.insert=Entry(master)
		self.insert.bind("<Return>",self.checkLetter)
		self.insert.pack()
		self.attempts.pack()
		
		self.newgame()

		self.playButton=Button(master,text="new Game",command=self.newgame)
		self.playButton.pack()
		self.quitButton=Button(master,text="quit",command=master.quit)
		self.quitButton.pack()

		self.ownwords=Checkbutton(master,text="random words",variable=self.complicated)
		self.ownwords.pack()

		self.insert.focus()

	def newgame(self):
		self.word=self.makeword()
		self.lives.set(8)
		self.updateLabel()
		self.insert.config(state='normal')
		self.attempttext.set("")
		

	def makeword(self):
		if self.complicated.get():
			try:
				retval=self.ranWordGen.get_random_word()
			except ConnectionError:
				print("no network!")
		else:
			dialogBox=insertBox(master)
			Tk.wait_window(dialogBox.top)
			retval=dialogBox.customWord
		self.guessed=[False]*len(retval)
		for i in range(len(retval)):
			if not re.compile("[a-z]").fullmatch(retval[i]):
				self.guessed[i]=True
		return retval
			

	def updateLabel(self):
		labelcontent=""
		for i in range(len(self.word)):
			labelcontent+= self.word[i] if self.guessed[i] else "_ "
		self.dashtext.set(labelcontent)
	def checkLetter(self,event):
		l=self.insert.get()
		if l in self.word:
			for s in re.finditer(l,self.word):
				for i in range(*s.span()):
					self.guessed[i]=True
				self.updateLabel()
			if all(self.guessed):
				if messagebox.askyesno(title="You were just lucky",message="Congratulations! You win! Start new game"):
					self.newgame()
				else:
					self.insert.config(state='disabled')

		else:
			self.lives.set(self.lives.get()-1)
			self.attempttext.set(self.attempttext.get()+l+" ")
			if self.lives.get()==0:
				if messagebox.askyesno(title=self.word+", you idiot!",message="You loose! Start new game?"):
					self.newgame()
				else:
					self.insert.config(state='disabled')
		self.insert.delete(0,'end')
master = Tk()
gui(master)
master.mainloop()