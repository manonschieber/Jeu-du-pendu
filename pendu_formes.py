import os
from random import randint, choice
import math
from tkinter import *
from tkinter.messagebox import * 

class ZoneAffichage(Canvas):
    def __init__(self,parent,w,h):
        Canvas.__init__(self,parent,width=w, height=h, bg='white')


class FenPrincipale(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Jeu du pendu')
        
        self.__zoneAffichage = ZoneAffichage(self,500,400)
        self.__zoneAffichage.pack()
        
        #On crée les boutons principaux
        f = Frame(self)
        f.pack(side=BOTTOM, padx=5, pady=5)
        Button(f, text ='Nouvelle partie', width=15, command =
        self.nouvellePartie).pack(side=LEFT, padx = 5,pady = 5)
        Button(f, text='Quitter',width=12, command=self.destroy).pack(side=LEFT, padx=5, pady=5)   
        Button(f, text='Afficher score',width=12, command=self.affiche_score).pack(side=LEFT, padx=5, pady=5)
        Button(f, text='Historique',width=12, command=self.affiche_historique).pack(side=LEFT, padx=5, pady=5)
        Button(f, text='Réinitialiser',width=12, command=self.reinitialiser).pack(side=LEFT, padx=5, pady=5)

        #On crée les boutons du clavier
        lettres = []
        for i in range(26):
            lettres.append(chr(ord('A')+i))   #code ASCI
        
        self.__boutons=[]
        f1 = Frame(self)
        f1.pack(side=TOP, padx=5, pady=5)
        for i in range(1,27):
            bouton = MonBouton(f1,self,lettres[i-1],4)
            bouton.grid(row=(i//8),column= i%8)
            self.__boutons.append(bouton)
            bouton.config(command = bouton.cliquer)
        
        self.__nbmanques=0
        self.__mots=self.chargeMots()
        self.__mot = self.nouveauMot()  #le mot à deviner
        
        self.__motdecouvert='*'*len(self.__mot)  #ce qui a déjà été découvert
        
        self.__motaffiche = Label(self)   
        self.__motaffiche.pack(side=TOP)
        self.__motaffiche.config(text='Mot :'+self.__motdecouvert)
    
        #On attribue un fichier au joueur s'il n'existe aps déjà
        self.__joueur = input("Tapez votre nom: ")
        self.__joueur = self.__joueur.capitalize()
        if os.path.exists(self.__joueur+'.txt')==True:   #le fichier existe
            fichier = open(self.__joueur+'.txt', "r")   
        else:   #le fichier n'existe pas encore
            with open(self.__joueur+'.txt','w') as f:   #un fichier texte par joueur
                f.write(self.__joueur+"\n"+'0'+"\n"+'0'+"\n"+'0')   #joueur;score;nbpartiesgagnées;nbpartiesjouées
                f.close()
        
        self.__score = Label(self)   
        self.__score.pack(side=TOP)
            

    def nouvellePartie(self):
        self.__mot=self.nouveauMot()
        self.__motdecouvert='*'*len(self.__mot)
        self.__motaffiche.config(text='Mot :'+self.__motdecouvert)

        for i in range(1,27):
             self.__boutons[i-1].config(state='normal')    #on réactive tous les boutons
             
        self.__nbmanques=0  #le nombre d'échecs retombe à 0
        self.__zoneAffichage.delete(ALL)   #on enlève les dessins restants

        
    def nouveauMot(self):   #choisit un mot au hasard dans la liste
        l = len(self.__mots)
        n = randint(0,l-1)
        mot = self.__mots[n]
        return mot
        
    def affiche_forme(self):    #Affichage d'un bout du pendu
        liste=[[30,200,150,205],[88,40,93,200],[88,40,180,45],[175,40,180,80],[163,75,193,105],[170,90,186,140],[150,110,178,115],[178,110,205,115],[170,120,175,170],[181,120,186,170]]
        
        nb=self.__nbmanques-1
        if nb== 4: # pour la tête
            self.__zoneAffichage.create_oval(liste[nb][0],liste[nb][1],liste[nb][2],liste[nb][3],fill = "black")
            
        else: # pour les rectangles
            self.__zoneAffichage.create_rectangle(liste[nb][0],liste[nb][1],liste[nb][2],liste[nb][3],fill = "black")
      
    
    def finpartie(self):
        if self.__nbmanques==10:  #la partie est perdue
            a='Vous avez perdu, le mot était:'+self.__mot
            self.__motaffiche.config(text=a) #afficher un bout du pendu
            self.affiche_forme()
            for i in range(1,27):
                self.__boutons[i-1].config(state=DISABLED)    #on désactive tous les boutons
            
            #gestion du score
            fichier=open(self.__joueur+'.txt','r')
            text=fichier.read()
            a=(self.__mot,'échec')
            with open(self.__joueur+'.txt','w') as f:   
                f.write(str(text)+"\n"+str(a))   
                f.close()
            
            fichier = open(self.__joueur+'.txt', "r")
            text1=fichier.readline()
            text2=fichier.readline()   #score
            text3=fichier.readline()   #nbpartiesgagnées
            text4=fichier.readline()    #nbpartiesjouées
            text=fichier.read()
            
            text4=str(int(text4)+1)   #une partie jouée de plus
            text2=str(int(text3)/int(text4)*100)     #Calcul du nouveau score
            
            with open(self.__joueur+'.txt','w') as f:   
                f.write(str(text1)+str(text2)+"\n"+str(text3)+str(text4)+"\n"+str(text))   
                f.close()
            
            fichier.close()
                
        if self.__mot==self.__motdecouvert:  #la partie est gagnée
            a=self.__mot+ '-Bravo, vous avez gagné'
            self.__motaffiche.config(text=a)
            for i in range(1,27):
                self.__boutons[i-1].config(state=DISABLED)    #on désactive tous les boutons
                 
            #gestion du score
            fichier=open(self.__joueur+'.txt','r')
            text=fichier.read()
            a=(self.__mot,'victoire')
            with open(self.__joueur+'.txt','w') as f:   
                f.write(str(text)+"\n"+str(a))   
                f.close()
            
            fichier = open(self.__joueur+'.txt', "r")
            text1=fichier.readline()
            text2=fichier.readline()   #score
            text3=fichier.readline()   #nbpartiesgagnées
            text4=fichier.readline()    #nbpartiesjouées
            text=fichier.read()
            
            text4=str(int(text4)+1)   #une partie jouée de plus
            text3=str(int(text3)+1)   #une partie gagnée de plus
            text2=str(int(text3)/int(text4)*100)    #Calcul du nouveau score
            
            with open(self.__joueur+'.txt','w') as f:   
                f.write(str(text1)+str(text2)+"\n"+str(text3)+"\n"+str(text4)+"\n"+str(text))   
                f.close()
            
            fichier.close()
            
    
    def affiche_score(self):
        fichier = open(self.__joueur+'.txt', "r")
        text1=fichier.readline()
        text2=fichier.readline()   #score
        
        self.__score.config(text='Score :'+text2)
            
        
    def traitement(self,lettre):
        for i in range(len(self.__mot)):
            if lettre==self.__mot[i]:  #la lettre est bien dans le mot à un moment
                self.__motdecouvert=self.__motdecouvert[:i]+self.__mot[i]+self.__motdecouvert[i+1:]
                self.__motaffiche.config(text='Mot :'+self.__motdecouvert)
                
        if self.__mot==self.__motdecouvert:  #la partie est gagnée
            self.finpartie()
        
        elif lettre not in self.__mot :   #si la lettre n'est pas dans le mot
            self.__nbmanques += 1
            self.affiche_forme()   #alors on affiche un bout du pendu
            
            if self.__nbmanques==10:  #la partie est perdue
                self.finpartie()
                
    
    def chargeMots(self):   #on met les mots du document dans une liste
        f = open('mots.txt','r')
        s = f.read()
        l = s.split('\n')
        f.close()
        return l
        
    
    def affiche_score(self):
        fichier = open(self.__joueur+'.txt', "r")
        text1=fichier.readline()
        text2=fichier.readline()   #score
        
        self.__score.config(text='Score :'+text2)
    
    
    def affiche_historique(self):
        fichier = open(self.__joueur+'.txt', "r")
        fichier.readline()   
        fichier.readline()   
        fichier.readline()
        fichier.readline()   #on a sauté les 4 premières lignes: nom, score, parties jouées, parties gagnées 
        
        text=fichier.read()   #le fichier sans les 4 premières lignes
        print(text)   #On affiche l'historique dans la console
    
    
    def reinitialiser(self):    #on écrase le fichier du joueur
        with open(self.__joueur+'.txt','w') as f:
            f.write(self.__joueur+"\n"+'0.0'+"\n"+'0'+"\n"+'0')
    
        

class MonBouton(Button):
    def __init__(self,parent, fen, t, w):
        Button.__init__(self,master=parent,text=t,width=w)
        self.__fenetrePrincipale =fen
        self.__lettre = t
        
        
    def cliquer(self):
        self.config(state=DISABLED)   #pour désactiver le bouton quand on a cliqué dessus
        self.__fenetrePrincipale.traitement(self.__lettre)
       



if __name__ == '__main__':
    fen = FenPrincipale()
    fen.mainloop()
