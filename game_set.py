from cards import get_cards 
from cards import get_cards_bool
import time

import random

from Tkinter import *
from random import shuffle
import Pmw
import tkMessageBox
import time
import Image, ImageTk, PngImagePlugin
import gettext, os, sys
from copy import copy

##card setting##
uno_card = []
uno_card_bool = []

uno_card = get_cards()
uno_card_bool = get_cards_bool()

total_cards = len(uno_card)

turn = 0
card_count = 0
draw_num  = 0
reverse_gate = 0
wild_color = ""

#print(uno_card)
#print(uno_card_bool)
####

##player setting##
player_num = 4
player = []
player_init = []
####

###Quit game
def callback():
    """Show a window at the end"""
    if tkMessageBox.askokcancel(_("Quit"),_("Do you want to quit this program?")):
        fen1.destroy()


##deal func##
def deal(player, times):
	global uno_card
	global uno_card_bool
	global total_cards
	global draw_num
	gate = 0
	times = int(times)
		
	while(times != 0):
		times = times - 1
		gate = 0
				
		if(total_cards == 0):
			return player
		
		rand_num = random.randint(0,len(uno_card)-1)
				
		while(gate == 0):
			if(uno_card_bool[rand_num] != 1):
				player.append(uno_card[rand_num])
				uno_card_bool[rand_num] = 1
				gate = 1
				total_cards = total_cards - 1
			else:
				rand_num = random.randint(0,len(uno_card)-1)
		
	draw_num  = 0
	return player

##play_card func##
def play_card(player, card_id):
	global card_count
	card_id = int(card_id)
	pop_card = player[card_id]
	
	if(card_id < len(player) and card_id >= 0):
		player.pop(card_id)
	else:
		print("play_card() error")
	
	card_count = 0	
	return pop_card

##check_winner func##
def check_winner(player):
	if(len(player) == 0):
		return 1
	else:
		return 0
	
##wild_color func##
def set_wild_color():
	print("choose color(r,y,b,g):")
	color = input()
	return color
		
		
##check_all_card func##
def check_all_card(player, pre_card):
	
	card_id = len(player)
	re = 0
	
	if(pre_card == ""):
		re = 1
	
	else:
		while(card_id != 0):
			card_id = card_id - 1
			mycard = player[card_id]
			
			if(mycard == "wdraw4" and pre_card[1:] != "skip"):
				if(mycard == "wdraw4" and pre_card[1:]  == "draw2"):
					re = 6
					break;
					
				elif(mycard == "wdraw4" and pre_card[1:] == "draw4"):
					re = 6
					break;
				else:
					re = 1
					
			elif(mycard == "wild" and pre_card[1:] != "skip" and pre_card[1:] != "draw2" and pre_card[1:] != "draw4"):
				re = 1
							
			elif(pre_card[0:1] == "e"):
				if(pre_card[1:2] == mycard[0:1]):
					re = 1
				elif(pre_card[2:] == mycard[1:]):
					re = 1
				
			elif(pre_card[1:] == "draw2"):
				if(pre_card[1:] == "draw2" and mycard[1:] == "draw2"):
					re = 4
				elif(re != 4):
					re = 5
			
			elif(pre_card[1:] == "draw4" and re != 6):
				re = 7
				
			elif(pre_card[1:] == "skip"):
				if(pre_card[1:] == "skip" and mycard[1:] == "skip"):
					re = 2
				elif(re != 2):
					re = 3
			elif(pre_card[0:1] == mycard[0:1]):
				re = 1
			elif(pre_card[1:] == mycard[1:]):
				re = 1
			
				
	return re

##check_single_card func
def check_single_card(player, card_id, pre_card):
	global reverse_gate
	global draw_num
	global wild_color
	
	card_id = int(card_id)
	card = player[card_id]
	
	if(pre_card == ""):
		if(card == "wdraw4"):
			wild_color = set_wild_color()
		if(card == "wild"):
			wild_color = set_wild_color()
		if(card[1:] == "reverse"):
			if(reverse_gate == 0):
				reverse_gate = 1
			else:
				reverse_gate = 0
		if(card[1:] == "draw2"):
			draw_num = draw_num + 2
		
		return 1
	
	elif(pre_card[0:1] == "e"):
		
		if(card == "wdraw4"):
			wild_color = set_wild_color()
			return 1
		
		if(card == "wild"):
			wild_color = set_wild_color()
			return 1
		
		if(pre_card[1:2] == card[0:1]):
			if(card[1:] == "reverse"):
				if(reverse_gate == 0):
					reverse_gate = 1
				else:
					reverse_gate = 0
			if(card[1:] == "draw2"):
				draw_num = draw_num + 2
			
			return 1
		
		elif(pre_card[2:] == card[1:]):
			if(card[1:] == "reverse"):
				if(reverse_gate == 0):
					reverse_gate = 1
				else:
					reverse_gate = 0
			if(card[1:] == "draw2"):
				draw_num = draw_num + 2
			
			return 1
	elif(pre_card[1:] == "draw2" and card[1:] == "draw2"):
		draw_num = draw_num + 2
		return 1
	elif(pre_card[1:] == "draw2" and card[1:] == "draw4"):
		return 1
	elif(pre_card[1:] == "draw2" and card[1:] != "draw2"):
		return 0
	elif(pre_card[1:] == "skip" and card[1:] == "skip"):
		return 1
	elif(pre_card[1:] == "skip" and card[1:] != "skip"):
		return 0
	elif(pre_card[1:] == "draw4"):
		if(card[1:] == "draw4"):
			return 1
		else:
			return 0
	elif(pre_card[0:1] == card[0:1]):
		if(card[1:] == "reverse"):
			if(reverse_gate == 0):
				reverse_gate = 1
			else:
				reverse_gate = 0
		if(card[1:] == "draw2"):
			draw_num = draw_num + 2
		return 1
	elif(pre_card[1:] == card[1:] ):
		if(card[1:] == "reverse"):
			if(reverse_gate == 0):
				reverse_gate = 1
			else:
				reverse_gate = 0
		if(card[1:] == "draw2"):
			draw_num = draw_num + 2
		return 1
	elif(card == "wild"):
		wild_color = set_wild_color()
		return 1
	elif(card == "wdraw4"):
		wild_color = set_wild_color()
		return 1
	
	return 0
	
##uno start##
##deal##

for i in range(player_num):
	player_init = deal(player_init, 7)
	player.append(player_init)
	player_init = []
	print("player" + str(i))
	print(player[i])
	
##play##
pre_card = ""

while(True):
	
#Main window
fen1=Tk()
fen1.title(_(u'UNO'))
can1=Canvas(fen1,bg='dark green', width=largeurjeu, height=hauteurjeu)
can1.pack(fill=BOTH, expand=1)
action="<Button-1>" # <Double-Button-1>
can1.bind(action, pointeur)
frame=Frame(fen1)
bout1=Button(fen1,text=_('Draw'),font=18, command=jpioche, state=DISABLED)
bout2=Button(fen1,text=_('Pass'),font=18, command=jpasse, state=DISABLED)
bout1.pack(side=LEFT, fill=BOTH, expand=1)
bout2.pack(side=LEFT, fill=BOTH, expand=1)
frame.pack(expand=1, side=BOTTOM)
info=Label(frame)
info.pack(side=RIGHT)


#Menu
menu=Menu(fen1)
fen1.config(menu=menu)
game=Menu(menu)
menu.add_cascade(label=_('Game'), menu=game)
game.add_command(label=_('New game'), command=start)
game.add_separator()
game.add_command(label=_('Quit'), command=callback)

options=Menu(menu)
menu.add_cascade(label=_('Options'),menu=options)
options.add_command(label=_('Language'), command=changeLang)

help=Menu(menu)
menu.add_cascade(label=_('Help'), menu=help)
help.add_separator()
help.add_command(label=_('About...'), command=about)



#End of the program
fen1.protocol("WM_DELETE_WINDOW", callback)

fen1.mainloop()

	print("")
	print("============================================")
	print("")
	player_id = turn % player_num
	print("player"+ str(player_id) + "'s turn")
	
	print(player[player_id])
	
	print("card_count:" + str(card_count))
	if(card_count == 4):
		card_count = 0
		pre_card = ""
	
	print(pre_card)
	check = check_all_card(player[player_id], pre_card)
	
	time.sleep(2)

	if(check == 7):
		card_count = card_count + 1
		pre_card = "e" + pre_card
		print("player" + str(player_id) + " is draw " + str(draw_num) + " cards this turn")
		player[player_id] = deal(player[player_id], draw_num)
		print(player[player_id])
		
	elif(check == 6):
		card_count = card_count + 1
		print("play draw card or draw(" + str(draw_num) + " cards )")
		card_id = input()
		
		if(card_id == "draw"):
			pre_card = "e" + pre_card
			print("player" + str(player_id) + " is draw " + str(draw_num) + " cards this turn")
			player[player_id] = deal(player[player_id], draw_num)
			print(player[player_id])
			pass
		else:
			while(True):
				if(check_single_card(player[player_id], card_id, pre_card) == 1):
					wild_color = set_wild_color()
					card_id = int(card_id)
					pre_card = wild_color + "draw4"
					print("player" + str(player_id) + " play " + pre_card)
					break;
				else:
					print("please play a draw4 card")
					card_id = input()
		
	elif(check == 5):
		card_count = card_count + 1
		pre_card = "e" + pre_card
		print("player" + str(player_id) + " is draw " + str(draw_num) + " cards this turn")
		player[player_id] = deal(player[player_id], draw_num)
		print(player[player_id])
		
	elif(check == 4):
		card_count = card_count + 1
		print("play draw card or draw(" + str(draw_num) + " cards )")
		card_id = input()
		
		if(card_id == "draw"):
			pre_card = "e" + pre_card
			print("player" + str(player_id) + " is draw " + str(draw_num) + " cards this turn")
			player[player_id] = deal(player[player_id], draw_num)
			print(player[player_id])
			pass
		else:
			while(True):
				if(check_single_card(player[player_id], card_id, pre_card) == 1):
					card_id = int(card_id)
					pre_card = player[player_id][card_id]
					print("player" + str(player_id) + " play " + pre_card)
					break;
				else:
					print("please play a draw card")
					card_id = input()		
		
	elif(check == 3):
		card_count = card_count + 1
		pre_card = "e" + pre_card
		print("player" + str(player_id) + " is skipped this turn")
				
	elif(check == 2):
		card_count = card_count + 1
		print("play skip card or skip")
		card_id = input()
		
		if(card_id == "skip"):
			pre_card = "e" + pre_card
			print("player" + str(player_id) + " is skipped this turn")
			pass
		else:
			while(True):
				if(check_single_card(player[player_id], card_id, pre_card) == 1):
					card_id = int(card_id)
					pre_card = player[player_id][card_id]
					print("player" + str(player_id) + " play " + pre_card)
					break;
				else:
					print("please play a skip card")
				
	elif(check == 1):
		card_count = card_count + 1
		while(True):
			if(pre_card == ""):
				print("play one card")
			else:
				print("play one card / draw")			
			card_id = input()
			
			if(card_id == "draw" and pre_card != ""):
				player[player_id] = deal(player[player_id], 1)
				l = len(player[player_id]) -1
				print("you got " + player[player_id][l])
				print(player[player_id])
				print("play one card / pass")
				card_id = input()
				if(card_id == "pass"):
					break;
				else:
					while(True):
						card_id = int(card_id)
						if(check_single_card(player[player_id], card_id, pre_card) == 1):
							pre_card = player[player_id][card_id] 
							play_card(player[player_id], card_id)
							print("player" + str(player_id) + " play " + pre_card)
							break;
						else:
							print("you can not play this card, play another card.")
							card_id = input()
					break;
			elif(card_id == "draw" and pre_card == ""):
				print("you can not do this, play one card:")
			else:
				while(True):
					card_id = int(card_id)
					if(check_single_card(player[player_id], card_id, pre_card) == 1):
						pre_card = player[player_id][card_id] 
						play_card(player[player_id], card_id)
						print("player" + str(player_id) + " play " + pre_card)
						break;
					else:
						print("you can not play this card, play another card.")
						card_id = input()
				break;
				
	elif(check == 0):
		card_count = card_count + 1
		print("no card can play, draw a card.")
		player[player_id] = deal(player[player_id], 1)
		print(player[player_id])
		check = check_all_card(player[player_id], pre_card)
		if(check == 1):
			l = len(player[player_id]) -1
			print("you got " + player[player_id][l] + ", play this card ?(y/n):")
			print(player[player_id])
			card_id = input()
			if(card_id == "y"):
				check_single_card(player[player_id], l, pre_card)
				pre_card = player[player_id][l] 
				play_card(player[player_id], l)
				print("player" + str(player_id) + " play " + pre_card)
			else:
				pass
			
			
	if(check_winner(player[player_id]) == 1):
		print("player" + str(player_id) + " win!")
		sys.exit(0)
		
	if(pre_card == "wild"):
		pre_card = "e" + wild_color + "*"
		
	if(pre_card[1:] == "draw4"):
		pre_card = wild_color + "draw4"
		draw_num = draw_num + 4
		
	if(reverse_gate == 0):
		turn = turn + 1
	else:
		turn = turn -1
