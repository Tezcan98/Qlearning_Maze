import random 
import numpy as np
class Maze:
    M=0
    N=0
    maze=[]
    intro=0
    engel=0
    def __init__(self,M,N):
       self.M = M
       self.N = N 
       self.maze = [0] * self.N  # labirent haritası ilklendirmesi
       for i in range(0,self.N):
           self.maze[i] = [0] * self.M 
       
        
    def Frame_Creater(self):  # kullanıcı harita oluşturma ekranında çerçevelerde kutu olur
        for i in range(0,(self.M)):
            for j in range(0,(self.N)):
              if i==0 or i==self.M-1 or j==0 or j==self.N-1:
                self.maze[j][i]=1 
    
    def Random_Creater(self):  #rastgele harita oluşturmada 4x1lik kutular oluşturulur
        self.Frame_Creater()
         
        for j in range(0,10): 
            yon=random.randint(1,2)
            rx=random.randint(0,self.M-4)
            ry=random.randint(0,self.N-4)  
            if yon==1: 
                self.maze[ry][rx]=1
                self.maze[ry][rx+1]=1
                self.maze[ry][rx+2]=1
                self.maze[ry][rx+3]=1
            elif yon==2: 
                self.maze[ry][rx]=1
                self.maze[ry+1][rx]=1
                self.maze[ry+2][rx]=1
                self.maze[ry+3][rx]=1     
        
    def draw(self,display_surf,image_surf,olusturucu): #ekran gösterimi
       bx = 0
       by = 0 
       for i in range(0,int(self.N)*int(self.M)): 
           if self.maze[by][bx] == 1:
               display_surf.blit(image_surf,( bx * 50 , by * 50)) 
                   
           bx = bx + 1
           if bx > self.M-1:
               bx = 0 
               by = by+1  