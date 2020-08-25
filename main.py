import os
import platform
import pygame
import time
import tkinter.messagebox
from tkinter import ttk
from tkinter import *
from maze import *
import pickle
red = (200,0,0)
green = (0,200,0)
black=(0,0,0)
bright_red = (255,0,0)
bright_green = (0,255,0)

maze=None

M=12 #x oyun harita boyutu
N=12  #y
def yazdir(T,n):
    for j in range(1,n):
        print(str(j)+"]",end="")
        for i in range(0,4):

            print(T[j][i],end="")
            if not T[j][i]=="*" and T[j][i]>=0:
                print(" ",end="")
            print(" |",end="")
        print("")
    print("________________")

class Scores:
    scores=[]
    def __init__(self):
        try:
            self.scores= pickle.load( open( "save.pkl", "rb" ) )
        except:
            print("Your First Time. Have a Good lesson")
            pickle.dump(self.scores, open("save.pkl", "wb"))
    def add(self,eps,ogrenme,N,M,obs,iterasyon):
        print(eps,ogrenme,N,M,obs,iterasyon)
        tempList = [len(self.scores)+1, eps,ogrenme,N,M,obs,iterasyon]
        self.scores.append(tempList)
        pickle.dump(self.scores, open("save.pkl", "wb"))
    def returnWithOrder(self):
        sort_as_it = sorted(self.scores, key=lambda x: x[4])
        return self.scores

class Player:
    x = 1   #oyuncu 1,1 noktasından başlar
    y = 1
    speed=1
    def moveRight(self):
        if maze.maze[self.y][self.x+1]==0:  # bir engel yoksa ilerler
            self.x = self.x + self.speed
    def moveLeft(self):
        if maze.maze[self.y][self.x-1]==0:
            self.x = self.x - self.speed
    def moveUp(self):
        if maze.maze[self.y-1][self.x]==0:
            self.y = self.y - self.speed
    def moveDown(self):
        if maze.maze[self.y+1][self.x]==0:
            self.y = self.y + self.speed

class window(object):

    epsilon=0.6
    ogrenme=0.7
    yer=[1,1]         # Oyuncunun konumu
    hedef=[7,7]
    yon=1             # Kutu oluşturucuda dikey ya da yatay olarak kutu oluşturacağı farenin topu(orta tuşu) ile değiştirilir
    skorlar=Scores()
    _display_surf = None    # Oyun alanı

    def initVals(self):
        self.start=False           # Oyun başlatır
        self.kutu_olusturucu=False # kutu oluşturucu modundaki işlemler için
        self.windowWidth = M*50
        self.windowHeight = N*50
        self.player = None
        self._block_surf=None  # Engelleri ilklendirme
        self.kisi=None         # Oyuncu ilklendirmesi
        self.kazandı=False
        self.delay=0
        self.bekle=1
        self.it=1
        self.bitti=False
        self.S=M*self.yer[1]+self.yer[0]
        self.R=None
        self.Q=None
    def py_init(self):
        self.initVals()
        self._running = True
        self.player = Player()

        self.player.x=self.yer[0]
        self.player.y=self.yer[1]
        n = M*N
        self.R = [-1] * n
        self.Q = [-1] * n
        for i in range(1,n):
            self.R[i] = [-1] * 4
        for i in range(1,n):
            self.Q[i] = [-1] * 4


    def initTables(self):
        n = M*N
        maze.maze[self.hedef[1]][self.hedef[0]]=0
        maze.maze[self.yer[1]][self.yer[0]]=0
        for i in range(1,n):
             by=i//M
             bx=i%M
             if bx>0:
                 if not maze.maze[by][bx-1]==1:     #engel yoksa odülü ayarla
                     self.R[i][0]=n-self.getMesafe(by,bx-1,self.hedef[0],self.hedef[1])              #solu
                     self.Q[i][0]=0
             if by>0:
                 if not maze.maze[by-1][bx]==1:
                     self.R[i][1]=n-self.getMesafe(by-1,bx,self.hedef[0],self.hedef[1])              #yukarı
                     self.Q[i][1]=0
             if bx<M-1:
                 if not maze.maze[by][bx+1]==1:
                     self.R[i][2]=n-self.getMesafe(by,bx+1,self.hedef[0],self.hedef[1])              #asağı
                     self.Q[i][2]=0
             if by<N-1:
                 if not maze.maze[by+1][bx]==1:
                     self.R[i][3]=n-self.getMesafe(by+1,bx,self.hedef[0],self.hedef[1])              #asağı
                     self.Q[i][3]=0
        yazdir(self.R,N*M)


        print("_____State: "+str(self.S)+"______")
        print("_____Iteration:  0______")
    def train(self):
            rand=random.random()
            print("_____Random: "+str(rand)+"______")
            if rand>self.epsilon:
                action=self.getMax(self.Q[self.S])
            else:
                action=random.randint(0,3)
                while self.R[self.S][action] == -1:
                    action=random.randint(0,3)

            S=self.S

            if action==0: # aksiyona göre hareket edilir
                self.player.moveLeft()
                self.S-=1
            if action==1:
                self.player.moveUp()
                self.S-=M
            if action==2:
                self.player.moveRight()
                self.S+=1
            if action==3:
                self.player.moveDown()
                self.S+=M

            self.Q[S][action]=self.R[S][action]+self.ogrenme*self.getMax(self.R[self.S]) #self.S= yeni state ; S=güncellenmeden önceki S

            #if self.it%100==0:
            print("_____State: "+str(self.S)+"______")
            print("_____Iteration:  "+str(self.it)+"______")
            self.it+=1

    def getMax(self,G):
        max=G[0]
        ind=-1
        for i,r in enumerate(G):
            if r>=max:
                ind=i
                max=r
        return ind


    def getMesafe(self,i,j,k,l):
        return abs((k-1)-j + (l-1)-i)


    def harita_olustur(self):  #harita oluşturma modu
        mouse = pygame.mouse.get_pos()
        x=mouse[0]//1
        y=mouse[1]//1
        if 0<x<self.windowWidth and 0<y<self.windowHeight:
            if self.yon==1: # farenin oldugu yerde kutu oluşturulacak yerler gözükür
                self._display_surf.blit(self._block_surf,(x,y-50))
                self._display_surf.blit(self._block_surf,(x+1*50,y-50))
                self._display_surf.blit(self._block_surf,(x+2*50,y-50))
                self._display_surf.blit(self._block_surf,(x+3*50,y-50))
            else:

                self._display_surf.blit(self._block_surf,(x,y))
                self._display_surf.blit(self._block_surf,(x,y-1*50))
                self._display_surf.blit(self._block_surf,(x,y-2*50))
                self._display_surf.blit(self._block_surf,(x,y-3*50))

        x=x//50
        y=y//50
        click = pygame.mouse.get_pressed()
        if click[0] == 1:   #tıklanan yere kutu yerleştirir
            x=int(mouse[0]/50)
            y=int(mouse[1]/50)
            if self.yon==1:
                maze.maze[y][x]=1
                if  x < M-2:
                    maze.maze[y][x+1]=1
                if  x < M-3:
                    maze.maze[y][x+2]=1
                if  x < M-4:
                    maze.maze[y][x+3]=1
            elif self.yon==0:
                maze.maze[y][x]=1
                if y>1:
                    maze.maze[y-1][x]=1
                if y>2:
                    maze.maze[y-2][x]=1
                if y>3:
                    maze.maze[y-3][x]=1
        if click[2]==1:
            x=int(mouse[0]/50)
            y=int(mouse[1]/50)
            maze.maze[y][x]=0

        if click[1]==1:
            if self.yon==1:
                self.yon=0
            else:
                self.yon=1
    def on_click(self,id):
        global maze
        if id==1:
            maze = Maze(M,N)
            maze.Random_Creater()
            self.start=True
            self.initTables()
        elif id==2:
            maze = Maze(M,N)
            maze.Frame_Creater()
            self.start=True
            self.kutu_olusturucu=True
        elif id==3:
            self.kutu_olusturucu=False
            self.start=True
            self.initTables()

    def btn_hover(self,x,y,w,h,color,popcolor,gameDisplay):
        mouse = pygame.mouse.get_pos()

        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(gameDisplay, popcolor,(x,y,w,h))
        else:
            pygame.draw.rect(gameDisplay, color,(x,y,w,h))

    def text_object(self,text,font,color):
        textSurface = font.render(text,True,color)
        return textSurface,textSurface.get_rect()

    def yazi_olustur(self,x,y,w,h,font_size,text,gameDisplay,color):
        smallText= pygame.font.SysFont("broadway", font_size)
        textSurf, textRect = self.text_object(text, smallText,color)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        gameDisplay.blit(textSurf, textRect)

    def button(self,x,y,w,h,text,color,popcolor,font_size,gameDisplay):
        self.btn_hover(x,y,w,h,color,popcolor,gameDisplay)
        self.yazi_olustur(x,y,w,h,font_size,text,gameDisplay,black)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        self._running = True
        pygame.display.set_caption('pygame Maze')

        self.oyuncu = pygame.image.load("player.png").convert()
        self._block_surf = pygame.image.load("block.png").convert()
        self._hedef = pygame.image.load("hedef.png").convert()
        self.image = pygame.image.load('background.jpg')

    def on_render(self):
        click= pygame.mouse.get_pressed()
        mouse=pygame.mouse.get_pos()

        if click[0]==1:
            if not self.start:      # Buttonlara onlick eklemek için koordinatları yazıldı
                btn1_x=0.1*self.windowWidth
                btn1_y=0.5*self.windowHeight
                btn1_w=self.windowWidth/3
                btn1_h=self.windowHeight/10
                btn2_x=0.6*self.windowWidth
                btn2_y=0.5*self.windowHeight
                btn2_w=self.windowWidth/3
                btn2_h=self.windowHeight/10

                if btn1_x+btn1_w > mouse[0] > btn1_x and btn1_y+btn1_h > mouse[1] > btn1_y:
                    self.on_click(1)
                elif btn2_x+btn2_w > mouse[0] > btn2_x and btn2_y+btn2_h > mouse[1] > btn2_y:
                    self.on_click(2)
            else:
                btn3_x=self.windowWidth-(self.windowHeight//4)
                btn3_y=50
                btn3_w=self.windowWidth/6
                btn3_h=self.windowHeight/15
                if btn3_x+btn3_w > mouse[0] > btn3_x and btn3_y+btn3_h> mouse[1] > btn3_y:
                    self.on_click(3)


        if not self.start:
            display_surface = pygame.display.set_mode((self.windowWidth, self.windowHeight))
            display_surface.blit(self.image, (0, 0))
            #button yerleştirme
            self.button(0.1*self.windowWidth,0.5*self.windowHeight,self.windowWidth/3,self.windowHeight/10,"Rastgele Labirent",green,bright_green,self.windowWidth//30,self._display_surf)
            self.button(0.6*self.windowWidth,0.5*self.windowHeight,self.windowWidth/3,self.windowHeight/10,"Labirent Olustur",red,bright_red,self.windowWidth//30,self._display_surf)
        else:
            self._display_surf.fill((10,10,10))
            self._display_surf.blit(self.oyuncu,(50*self.player.x,50*self.player.y))
            self._display_surf.blit(self._hedef,(self.hedef[0]*50,self.hedef[1]*50))

            if self.kutu_olusturucu:
                maze.draw(self._display_surf, self._block_surf,1)
                self.yazi_olustur(self.windowWidth/2,30,0,0,20,'Kutu olusturmak istediginiz yeri tıklayın',self._display_surf,bright_green)
                self.button(self.windowWidth-(self.windowHeight//4),50,self.windowWidth/6,self.windowHeight/15,"Baslat",bright_red,red,self.windowWidth//30,self._display_surf)
                self.harita_olustur()
            else:
                maze.draw(self._display_surf, self._block_surf,0)

                if self.kazandı:
                    self.yazi_olustur(self.windowWidth/2,self.windowHeight/2,0,0,60,"KAZANDINIZ",self._display_surf,red)

        pygame.display.flip()


    ### Gui functions
    def generate(self):
         global M,N
         self.display_surface = pygame.display.set_mode((self.windowWidth, self.windowHeight))
         self.display_surface.blit(self.image, (0, 0))
         pygame.display.flip()
         self.epsilon=float(self.areaEpsEntered.get())
         self.ogrenme=float(self.areaEntered.get())
         M=self.variablex.get()
         N=self.variabley.get()
         self.yer[0]=self.variableajanx.get()
         self.yer[1]=self.variableajany.get()
         self.hedef[0]=self.variablehedefx.get()
         self.hedef[1]=self.variablehedefy.get()

         if self.yer[0]>M-2 or self.yer[1]>N-2 or self.hedef[0]>M-2 or self.hedef[1]>N-2:
             messagebox.showinfo("HATA","Hedef oyun alanının dışına çıkıyor")
             return -1
         self.py_init()
         self.on_init()

    def change_speed(self,val):
        self.bekle=51-int(val)

    def popup(self):
        win = Toplevel()
        win.wm_title("Window")

        label = Label(win, text="Skorlar", font=("Arial",20)).grid(row=0, columnspan=2)
        cols = ('No','Epsilon', 'Öğrenme katsayısı','N','M','Engel Sayısı',"Iterasyon")
        listBox = ttk.Treeview(win, columns=cols, show='headings')
        # set column headings
        for col in cols:
            listBox.heading(col, text=col)
        listBox.grid(row=1, column=0, columnspan=8)
        tempList=self.skorlar.returnWithOrder()
        for s in self.skorlar.scores:
            listBox.insert("", "end",values=s)
        print(self.skorlar.returnWithOrder())
        Button(win, text="Close", width=15, command=lambda:win.destroy()).grid(row=4, column=1)

        win.mainloop()
    def __init__(self):
        self.py_init()
        self.root = Tk()  # Main window
        self.root.title("Q-Learning Simulation")
        self.root.iconbitmap(r'ai.ico')
        self.root.configure(background='#9b9b9b')

        # Large Frame
        self.win_frame = Frame(self.root, width=1200, height=700, highlightbackground='#595959', highlightthickness=2)

        # menu (left side)
        self.menu = Frame(self.win_frame, width=250, height=700, highlightbackground='#595959', highlightthickness=2)
        self.menu_label = Label(self.menu, text="Harita boyunu giriniz", bg='#8a8a8a', font=("Courier", "10", "bold roman"))


        self.variablex = IntVar(self.menu)
        self.variablex.set(M) # default value
        self.variabley = IntVar(self.menu)
        self.variabley.set(N) # default value
        self.options=[4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
        self.options2=[4,5,6,7,8,9,10,11,12]
        self.xx = OptionMenu(self.menu, self.variablex, *self.options)
        self.yy = OptionMenu(self.menu, self.variabley, *self.options2)
        self.hizLabel = Label(self.menu, text="Oyun hizi", bg='#8a8a8a', font=("Courier", "10", "bold roman"))

        self.ss = Scale(self.menu, from_=1, to=50,orient=HORIZONTAL,length=100,command=self.change_speed)
        self.ss.set(50)
        self.ogrnmelabel = Label(self.menu, text="Öğrenme Katsayısı", bg='#8a8a8a', font=("Courier", "10", "bold roman"))
        self.area = IntVar()
        self.area.set(self.ogrenme)
        self.areaEntered = Entry(self.menu, width = 5, textvariable = self.area)

        self.epsilonlabel = Label(self.menu, text="Epsilon Değeri", bg='#8a8a8a', font=("Courier", "10", "bold roman"))
        self.areaEps = IntVar()
        self.areaEps.set(self.epsilon)
        self.areaEpsEntered = Entry(self.menu, width = 5, textvariable = self.areaEps)

        self.ajan_label = Label(self.menu, text="Ajan Nereden başlasın", bg='#8a8a8a', font=("Courier", "10", "bold roman"))

        self.variableajanx = IntVar(self.menu)
        self.variableajanx .set(self.yer[0]) # default value
        self.variableajany = IntVar(self.menu)
        self.variableajany.set(self.yer[0]) # default value
        self.optionsx=[]
        for i in range(2,M-3):
            self.optionsx.append(i)
        self.ajanx =  OptionMenu(self.menu, self.variableajanx, *self.optionsx)
        self.optionsy=[]
        for i in range(2,N-3):
            self.optionsy.append(i)
        self.ajany =  OptionMenu(self.menu, self.variableajany, *self.optionsy)

        self.hedef_label = Label(self.menu, text="Hedef Nerede olsun", bg='#8a8a8a', font=("Courier", "10", "bold roman"))
        self.variablehedefx = IntVar(self.menu)
        self.variablehedefx .set(self.hedef[0]) # default value
        self.variablehedefy = IntVar(self.menu)
        self.variablehedefy.set(self.hedef[1]) # default value

        self.optionsx=[]
        self.optionsy=[]

        for i in range(2,16):
            self.optionsx.append(i)
        for i in range(2,10):
            self.optionsy.append(i)
        self.hedefx = OptionMenu(self.menu, self.variablehedefx, *self.optionsx)
        self.hedefy = OptionMenu(self.menu, self.variablehedefy, *self.optionsy)

        self.generateb = Button(self.menu, text="Oluştur", font="Courier", bg='#bcbcbc', activebackground='#cdcdcd',command=self.generate)

        # pygame
        self.pygame_frame = Frame(self.win_frame, width=900, height=700, highlightbackground='#595959', highlightthickness=2)
        self.embed = Frame(self.pygame_frame, width=900, height=700,)

        # Packing
        self.win_frame.pack(expand=True)
        self.win_frame.pack_propagate(0)

        self.menu.pack(side="left")
        self.menu.pack_propagate(0)
        self.menu_label.pack(ipadx=60, ipady=2)
        self.xx.pack()
        self.yy.pack()
        self.ogrnmelabel.pack(ipadx=60, ipady=2)
        self.areaEntered.pack(ipadx=60, ipady=2)
        self.epsilonlabel.pack(ipadx=60, ipady=2)
        self.areaEpsEntered.pack(ipadx=60, ipady=2)

        self.ajan_label.pack(ipadx=60, ipady=2)
        self.ajanx.pack()
        self.ajany.pack()

        self.hedef_label.pack(ipadx=60, ipady=2)
        self.hedefx.pack()
        self.hedefy.pack()
        self.generateb.pack(ipadx=20, ipady=10, pady=20)

        self.hizLabel.pack(ipadx=60, ipady=2)
        self.ss.pack()
        self.pygame_frame.pack(side="left")
        self.embed.pack()
        #This embeds the pygame window
        os.environ['SDL_WINDOWID'] = str(self.embed.winfo_id())
        system = platform.system()
        if system == "Windows":
            os.environ['SDL_VIDEODRIVER'] = 'windib'
        elif system == "Linux":
            os.environ['SDL_VIDEODRIVER'] = 'x11'

        self.root.update_idletasks()
        #Start pygame
        pygame.init()
        self.win = pygame.display.set_mode((512, 512))

        self.bg_color = (200, 155, 255)
        self.win.fill(self.bg_color)
        self.pos = 0, 0
        self.direction = 10, 10
        self.size = 40
        self.color = (0, 255, 0)

        self.on_init()
        self.root.after(10, self.update)
        self.root.mainloop()


    def update(self):
        self.on_render()   # oyun ekranı yüklenir
        self.delay+=1
        if self.start:
            if not self.kutu_olusturucu and self.delay%self.bekle==0:
                if self.S != self.hedef[1]*M+self.hedef[0]:
                    self.train()
                    print(self.epsilon,self.ogrenme)
                else:
                    engel_sayisi=0
                    for m in maze.maze:
                        engel_sayisi+=m.count(1)
                    engel_sayisi-=(2*M+2*N-4)
                    MsgBox = messagebox.askquestion ('Hedefe Ulaşıldı','Hedefe ulaşıldı, Kaydetmek ister misiniz ?',icon = 'warning')
                    if MsgBox == 'yes':
                       print(self.epsilon,self.ogrenme,N,M,engel_sayisi,self.it)
                       self.skorlar.add(self.epsilon,self.ogrenme,N,M,engel_sayisi,self.it)

                    self.generate()
                    self.root.after(1, self.update)
                    self.popup()

        pygame.event.pump()
        pygame.display.update()


        self.root.after(1, self.update)

screen = window()
