#Import
from Tkinter import *
from random import shuffle
import Pmw
import tkMessageBox
import time
import Image, ImageTk, PngImagePlugin
import gettext, os, sys
from copy import copy


############Constants###############
passe=0 #=1 when the player pass
numplayer=-1 #n?of the player playing, 0->you
# =-1 at the beginning, for the player 0 receive the effects of the first card
sens=1
color=None
map_height=700
map_width=map_height
card_height=map_height/5
card_width=card_height*2/3
espacecarte=card_width/3
cartebord=card_height/3
cartebord2=espacecarte
nbcolor=4
NumberOfPlayer=[2,3,4]
HandcardNumer=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
cardset='classic'
flagPioche=0


#######Define the fonctions#######

def callback():
    """Show a window at the end"""
    if tkMessageBox.askokcancel(_("Quit"),_("Do you want to quit this program?")):
        fen1.destroy()

class Carte:
    """Card class"""
    def __init__(self,carte,player=0,x=map_width/2+espacecarte,y=map_height/2-card_height/2):
        self.x=x
        self.y=y
        self.player=player
        self.carte=carte
        color=carte[1]
        if not player: # True , to see the card of the others players
            if self.carte[0] in ['jok','+4']:
                dir="./"+cardset+"/"+self.carte[0]+".png"
            else:
                dir="./"+cardset+"/"+self.carte[0]+"-"+self.carte[1]+".png"
        else:
            dir="./"+cardset+"/back.png"
        try:
            self.img=Image.open(dir)
        except:
            tkMessageBox.showinfo(_('Error'),_("Fail to read Image Files."))
        self.img=self.img.resize((card_width,card_height),Image.ANTIALIAS)
        self.card_width=card_width
        self.card_height=card_height
        self.rot=90*player
        if player%2==1:
            self.card_width,self.card_height=self.card_height,self.card_width
        self.img=self.img.rotate(self.rot)
        self.im=ImageTk.PhotoImage(self.img)
        self.image=can1.create_image(x,y,image=self.im)


    def coord(self,coordx,coordy,mouv=False):
        can1.tkraise(self.image)
        self.x2=self.x
        self.y2=self.y
        self.x=coordx
        self.y=coordy
        step=20
        if mouv:
            for var in xrange(step):
                var+=1.
                self.xtemp=(var/step)*self.x+((step-var)/step)*self.x2
                self.ytemp=(var/step)*self.y+((step-var)/step)*self.y2
                can1.coords(self.image,self.xtemp+self.card_width/2,self.ytemp+self.card_height/2)
                can1.update()
                time.sleep(0.01)#define the speed of the moving
        can1.coords(self.image,coordx+self.card_width/2,coordy+self.card_height/2)

    def place(self,player,num,mouv=False):
        if player == 0:
            self.x=num*espacecarte+cartebord
            self.y=map_height-self.card_height-cartebord2
            self.coord(num*espacecarte+cartebord,map_height-self.card_height-cartebord2,mouv)
        if player == 1:
            self.x=cartebord2
            self.y=cartebord+num*espacecarte
            self.coord(cartebord2,cartebord+num*espacecarte,mouv)
        if player == 2:
            self.x=map_width-card_height-num*espacecarte-cartebord
            self.y=cartebord2
            self.coord(map_width-card_height-num*espacecarte-cartebord,cartebord2,mouv)
        if player == 3:
            self.x=map_width-card_height-cartebord2
            self.y=map_height-card_width-cartebord-num*espacecarte
            self.coord(map_width-card_height-cartebord2,map_height-card_width-cartebord-num*espacecarte,mouv)

    def play(self):
        self.card_width=card_width
        self.card_height=card_height
        self.suppr()
        if self.carte[0] in ['jok','+4']:
            dir="./"+cardset+"/"+self.carte[0]+".png"
        else:
            dir="./"+cardset+"/"+self.carte[0]+"-"+self.carte[1]+".png"
        self.img=Image.open(dir)
        self.img=self.img.resize((card_width,card_height),Image.ANTIALIAS)
        self.im=ImageTk.PhotoImage(self.img)
        self.image=can1.create_image(self.x,self.y,image=self.im)
        self.coord(map_width/2-card_width,map_height/2-card_height/2,True)

    def suppr(self):
        can1.delete(self.image)

def start():
    """Start game window"""
    global box1,box2,entry,fen,logcheck,logvar,PlayerName
    fen=Toplevel()
    fen.title(_('New game'))
    box1=Pmw.ComboBox(fen, labelpos=NW, label_text=_('Number of players :'), scrolledlist_items=NumberOfPlayer)
    box1.pack()
    box1.selectitem(2)
    box2=Pmw.ComboBox(fen, labelpos=NW, label_text=_('\nNumber of cards for each player :'), scrolledlist_items=HandcardNumer)
    box2.pack()
    box2.selectitem(6)
    Label(fen, text=_("\nYour name :")).pack()
    entry=Entry(fen)
    entry.pack()
    PlayerName=str(entry.get())
    logvar=IntVar()
    logcheck=Checkbutton(fen,text=_("log the actions"), variable=logvar)
    logcheck.pack()
    botton=Button(fen, text=_('Ok'), command=valider)
    botton.pack()
    fen.transient(fen1)

def abotton():
    tkMessageBox.showinfo(_('Abotton'), _(u"Python UNO project") )

#Main window
fen1=Tk()
fen1.title(_(u'UNO'))
can1=Canvas(fen1,bg='dark green', width=map_width, height=map_height)
can1.pack(fill=BOTH, expand=1)
action="<Button-1>" # <Double-Button-1>
can1.bind(action, pointeur)
frame=Frame(fen1)
botton1=Button(fen1,text=_('Draw'),font=18, command=jpioche, state=DISABLED)
botton2=Button(fen1,text=_('Pass'),font=18, command=jpasse, state=DISABLED)
botton1.pack(side=LEFT, fill=BOTH, expand=1)
botton2.pack(side=LEFT, fill=BOTH, expand=1)
frame.pack(expand=1, side=BOTTOM)
###info=Label(frame)
###info.pack(side=RIGHT)

#Menu
menu=Menu(fen1)
fen1.config(menu=menu)
game=Menu(menu)
menu.add_cascade(label=_('Game'), menu=game)
game.add_command(label=_('New game'), command=start)
game.add_separator()
game.add_command(label=_('Quit'), command=callback)

help=Menu(menu)
menu.add_cascade(label=_('Help'), menu=help)
help.add_separator()
help.add_command(label=_('Abotton...'), command=abotton)

#End of the program
fen1.protocol("WM_DELETE_WINDOW", callback)
