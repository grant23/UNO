from cards import get_cards 
from cards import get_cards_bool
import os
import sys
import time
import random

import socket
import threading
import pickle

bind_ip = "127.0.0.1"
bind_port = 11235

##card setting##
uno_card = []
uno_card_bool = []

uno_card = get_cards()
uno_card_bool = get_cards_bool()

total_cards = len(uno_card)

player_id = 0

turn = 0
card_count = 0
draw_num  = 0
reverse_gate = 0
wild_color = ""

#print(uno_card)
#print(uno_card_bool)
####

##player setting##
now_add_player = 0
player_num = 3
player = []
player_init = []
####

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
server.bind((bind_ip,bind_port))

server.listen(5)
	
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
		
	if(player_id == 0):
		print("choose color(r,y,b,g):")
		re = input()
	else:
		request = client_socket.recv(1024)
		re = request .decode('ascii')
		print("[*] Received:" + re)	
	
	color = re
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
			
			content = str(player_id)
			co = content.encode('ascii')
			client_socket.send(co)
			
			wild_color = set_wild_color()
		if(card == "wild"):
			
			content = str(player_id)
			co = content.encode('ascii')
			client_socket.send(co)
			
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
			content =str(player_id)
			co = content.encode('ascii')
			client_socket.send(co)
			
			wild_color = set_wild_color()
			return 1
		
		if(card == "wild"):
			
			content = str(player_id)
			co = content.encode('ascii')
			client_socket.send(co)
			
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
		content = str(player_id)
		co = content.encode('ascii')
		client_socket.send(co)
		
		wild_color = set_wild_color()
		return 1
	elif(card == "wdraw4"):
			
		content = str(player_id)
		co = content.encode('ascii')
		client_socket.send(co)
		
		wild_color = set_wild_color()
		return 1
	
	return 0
		
	
def handle_client(client_socket,ipadd,portadd):
	global now_add_player
	global player_id
	global player_init 
	global turn
	global card_count
	global wild_color
	global draw_num
	global reverse_gate
	global player_num
	global player
	
	
	ID = now_add_player
		
	content = "ID"
	co = content.encode('ascii')
	client_socket.send(co)
	
	time.sleep(1)
	
	content = str(now_add_player)
	co = content.encode('ascii')
	client_socket.send(co)
	
	time.sleep(1)
	
	while True:
		
		print("waiting game start!!")		

		while True:
			if(now_add_player != player_num):
				print("Game Start!")
				content = "Game Start!"
				co = content.encode('ascii')
				client_socket.send(co)
				time.sleep(1)
				break;
		##uno start##
		##deal##
		
		for i in range(player_num):
			player_init = deal(player_init, 7)
			player.append(player_init)
			player_init = []
			
			if(i == 0):
				print("player" + str(i))
				print(player[i])
			
			elif(i == ID):
				content = "card_list"
				co = content.encode('ascii')
				client_socket.send(co)
				time.sleep(1)
				
				data = pickle.dumps(player[i])
				client_socket.send(data)
				time.sleep(1)
		##play##
		pre_card = ""

		while(True):
			print("")
			print("============================================")
			print("")
			player_id = turn % player_num
			print("player"+ str(player_id) + "'s turn")
			
			content = str(player_id)
			co = content.encode('ascii')
			client_socket.send(co)
			time.sleep(1)
						
			if(player_id == 0 ):
				print(player[player_id])
	
			elif(player_id == ID):
				data = pickle.dumps(player_id)
				client_socket.send(data)
				time.sleep(1)
				
			#print("card_count:" + str(card_count))
			if(card_count == 4):
				card_count = 0
				pre_card = ""
			
			if(pre_card != ""):
				if(player_id == 0 ):
					print("Last Card: " + pre_card)
				elif(player_id == ID):
					content = str(pre_card)
					co = content.encode('ascii')
					client_socket.send(co)
					time.sleep(1)
								
			check = check_all_card(player[player_id], pre_card)
			
			if(player_id == ID):
				content = str(check)
				co = content.encode('ascii')
				client_socket.send(co)
			
			else:
				pass
			
			time.sleep(2)
			#####
			if(check == 7):
				card_count = card_count + 1
				pre_card = "e" + pre_card
				
				if(player_id == 0):
					print("player" + str(player_id) + " is draw " + str(draw_num) + " cards this turn")
				elif(player_id == ID):
					content = str(draw_num)
					co = content.encode('ascii')
					client_socket.send(co)
					time.sleep(1)
					
				player[player_id] = deal(player[player_id], draw_num)
				if(player_id == 0):
					print(player[player_id])
				elif(player_id == ID):
					data = pickle.dumps(player_id)
					client_socket.send(data)
					time.sleep(1)
				
			elif(check == 6):
				card_count = card_count + 1
				if(player_id == 0):
					print("play draw card or draw(" + str(draw_num) + " cards )")
				elif(player_id == ID):
					content =str(draw_num)
					co = content.encode('ascii')
					client_socket.send(co)
					
				if(player_id == 0):
					re = input()
				else:
					request = client_socket.recv(1024)
					re = request .decode('ascii')
					print("[*] Received:" + re)	
				
				card_id = re
		
				if(card_id == "draw"):
					pre_card = "e" + pre_card
					print("player" + str(player_id) + " is draw " + str(draw_num) + " cards this turn")
					
					player[player_id] = deal(player[player_id], draw_num)
					if(player_id == 0):
						print(player[player_id])
					elif(player_id == ID):
						data = pickle.dumps(player_id)
						client_socket.send(data)
						time.sleep(1)
					pass
				else:
					while(True):
						if(player_id != 0):
							content = str(check_single_card(player[player_id], card_id, pre_card))
							co = content.encode('ascii')
							client_socket.send(co)
						
						if(check_single_card(player[player_id], card_id, pre_card) == 1):
														
							wild_color = set_wild_color()
							card_id = int(card_id)
							pre_card = wild_color + "draw4"
							
							if(player_id == 0):
								print("player" + str(player_id) + " play " + pre_card)
							elif(player_id == ID):
								content = pre_card
								co = content.encode('ascii')
								client_socket.send(co)
								time.sleep(1)
							
							break;
						else:
							if(player_id == 0):
								print("please play a draw4 card")
																		
							if(player_id == 0):
								re = input()
							else:
								request = client_socket.recv(1024)
								re = request .decode('ascii')
								print("[*] Received:" + re)	
								
							card_id = re
			elif(check == 5):
				card_count = card_count + 1
				pre_card = "e" + pre_card
				
				if(player_id == 0):
					print("player" + str(player_id) + " is draw " + str(draw_num) + " cards this turn")
				elif(player_id == ID):
					content = str(draw_num)
					co = content.encode('ascii')
					client_socket.send(co)
					time.sleep(1)
				
				player[player_id] = deal(player[player_id], draw_num)
				if(player_id == 0):
					print(player[player_id])
				elif(player_id == ID):
					data = pickle.dumps(player_id)
					client_socket.send(data)
					time.sleep(1)
						
			elif(check == 4):
				card_count = card_count + 1
				if(player_id == 0):
					print("play draw card or draw(" + str(draw_num) + " cards )")
				elif(player_id == ID):
					content = str(draw_num) 
					co = content.encode('ascii')
					client_socket.send(co)
					time.sleep(1)
					
				if(player_id == 0):
					re = input()
				else:
					request = client_socket.recv(1024)
					re = request .decode('ascii')
				
				card_id = re
		
				if(card_id == "draw"):
					pre_card = "e" + pre_card
					if(player_id == 0):
						print("player" + str(player_id) + " is draw " + str(draw_num) + " cards this turn")
					elif(player_id == ID):
						content = str(draw_num)
						co = content.encode('ascii')
						client_socket.send(co)
						time.sleep(1)
					
					player[player_id] = deal(player[player_id], draw_num)
					if(player_id == 0):
						print(player[player_id])
					elif(player_id == ID):
						data = pickle.dumps(player_id)
						client_socket.send(data)
						time.sleep(1)
					pass
				else:
					while(True):
						if(player_id != 0):
							content = check_single_card(player[player_id], card_id, pre_card)
							co = content.encode('ascii')
							client_socket.send(co)
						
						if(check_single_card(player[player_id], card_id, pre_card) == 1):
							card_id = int(card_id)
							pre_card = player[player_id][card_id]
							if(player_id == 0):
								print("player" + str(player_id) + " play " + pre_card)
							elif(player_id == ID):
								content = "player" + str(player_id) + " play " + pre_card
								co = content.encode('ascii')
								client_socket.send(co)
							
							break;
						else:
							if(player_id == 0):
								print("please play a draw card")
							elif(player_id == ID):
								content = "please play a draw card"
								co = content.encode('ascii')
								client_socket.send(co)
							
							if(player_id == 0):
								re = input()
							else:
								request = client_socket.recv(1024)
								re = request .decode('ascii')
								print("[*] Received:" + re)	
							
							card_id = re		
		
			elif(check == 3):
				card_count = card_count + 1
				pre_card = "e" + pre_card
				
				if(player_id == 0):
					print("player" + str(player_id) + " is skipped this turn")
				elif(player_id == ID):
					content = "player" + str(player_id) + " is skipped this turn"
					co = content.encode('ascii')
					client_socket.send(co)
				
			elif(check == 2):
				card_count = card_count + 1
				if(player_id == 0):
					print("play skip card or skip")
				elif(player_id == ID):
					content = "play skip card or skip"
					co = content.encode('ascii')
					client_socket.send(co)
				
				if(player_id == 0):
					re = input()
				else:
					request = client_socket.recv(1024)
					re = request .decode('ascii')
					print("[*] Received:" + re)	
				
				card_id = re
				
				if(card_id == "skip"):
					pre_card = "e" + pre_card
					if(player_id == 0):
						print("player" + str(player_id) + " is skipped this turn")
					elif(player_id == ID):
						content = "player" + str(player_id) + " is skipped this turn"
						co = content.encode('ascii')
						client_socket.send(co)
					pass
				
				else:
					while(True):
						if(check_single_card(player[player_id], card_id, pre_card) == 1):
							card_id = int(card_id)
							pre_card = player[player_id][card_id]
							
							if(player_id == 0):
								print("player" + str(player_id) + " play " + pre_card)
							elif(player_id == ID):
								content = "player" + str(player_id) + " play " + pre_card
								co = content.encode('ascii')
								client_socket.send(co)
							
							break;
						else:
							if(player_id == 0):
								print("please play a skip card")
							elif(player_id == ID):
								content = "please play a skip card"
								co = content.encode('ascii')
								client_socket.send(co)
				
			elif(check == 1):
				card_count = card_count + 1
				while(True):
					if(pre_card == ""):
						if(player_id == 0):
							print("play one card")
						elif(player_id == ID):
							content = "play one card"
							co = content.encode('ascii')
							client_socket.send(co)
					else:
						if(player_id == 0):
							print("play one card / draw")
						elif(player_id == ID):
							content = "play one card / draw"
							co = content.encode('ascii')
							client_socket.send(co)
								
					if(player_id == 0):
						re = input()
					elif(player_id == ID):
						request = client_socket.recv(1024)
						re = request .decode('ascii')
						print("[*] Received:" + re)	
					
					card_id = re
					
					if(card_id == "draw" and pre_card != ""):
						player[player_id] = deal(player[player_id], 1)
						l = len(player[player_id]) -1
						
						if(player_id == 0):
							print("you got " + player[player_id][l])
						elif(player_id == ID):	
							content = "you got " + player[player_id][l]
							co = content.encode('ascii')
							client_socket.send(co)
												
							data = pickle.dumps(player[player_id])
							client_socket.send(data)
						
						if(player_id == 0):
							print("play one card / pass")
						elif(player_id == ID):
							content = "play one card / pass"
							co = content.encode('ascii')
							client_socket.send(co)
							
						if(player_id == 0):
							re = input()
						else:
							request = client_socket.recv(1024)
							re = request .decode('ascii')
							print("[*] Received:" + re)	

						card_id = re
						if(card_id == "pass"):
							break;
						else:
							while(True):
								card_id = int(card_id)
								if(check_single_card(player[player_id], card_id, pre_card) == 1):
									pre_card = player[player_id][card_id] 
									play_card(player[player_id], card_id)
									
									if(player_id == 0):
										print("player" + str(player_id) + " play " + pre_card)
									elif(player_id == ID):
										content = "player" + str(player_id) + " play " + pre_card
										co = content.encode('ascii')
										client_socket.send(co)
									
									break;
									
								else:
									if(player_id == 0):
										print("you can not play this card, play another card.")
									elif(player_id == ID):
										content = "you can not play this card, play another card."
										co = content.encode('ascii')
										client_socket.send(co)
														
									if(player_id == 0):
										re = input()
									else:
										request = client_socket.recv(1024)
										re = request .decode('ascii')
										print("[*] Received:" + re)	
									
									card_id = re
							break;
					elif(card_id == "draw" and pre_card == ""):
						if(player_id == 0):
							print("you can not do this, play one card:")
						elif(player_id == ID):
							content = "you can not do this, play one card:"
							co = content.encode('ascii')
							client_socket.send(co)
						
					else:
						while(True):
							card_id = int(card_id)
							if(check_single_card(player[player_id], card_id, pre_card) == 1):
								pre_card = player[player_id][card_id] 
								play_card(player[player_id], card_id)
								if(player_id == 0):
									print("player" + str(player_id) + " play " + pre_card)
								elif(player_id == ID):
									content = "player" + str(player_id) + " play " + pre_card
									co = content.encode('ascii')
									client_socket.send(co)
								
								break;
								
							else:
								if(player_id == 0):
									print("you can not play this card, play another card.")
								elif(player_id == ID):
									content = "you can not play this card, play another card."
									co = content.encode('ascii')
									client_socket.send(co)
								
								if(player_id == 0):
									re = input()
								else:
									request = client_socket.recv(1024)
									re = request .decode('ascii')
									print("[*] Received:" + re)	
								
								card_id = re
						break;
				
			elif(check == 0):
				card_count = card_count + 1
				if(player_id == 0):
					print("no card can play, draw a card.")
				elif(player_id == ID):
					content = "no card can play, draw a card."
					co = content.encode('ascii')
					client_socket.send(co)
	
				player[player_id] = deal(player[player_id], 1)
				check = check_all_card(player[player_id], pre_card)
				if(check == 1):
					l = len(player[player_id]) -1
					if(player_id == 0):
						print("you got " + player[player_id][l] + ", play this card ?(y/n):")
					elif(player_id == ID):
						content = "you got " + player[player_id][l] + ", play this card ?(y/n):"
						co = content.encode('ascii')
						client_socket.send(co)
					
					if(player_id == 0):
						print(player[player_id])
					elif(player_id == ID):
						data = pickle.dumps(player[player_id])
						client_socket.send(data)
					
					if(player_id == 0):
						re = input()
					else:
						request = client_socket.recv(1024)
						re = request .decode('ascii')
						print("[*] Received:" + re)	
			
					card_id = re
					if(card_id == "y"):
						check_single_card(player[player_id], l, pre_card)
						pre_card = player[player_id][l] 
						play_card(player[player_id], l)
	
						if(player_id == 0):
							print("player" + str(player_id) + " play " + pre_card)
						elif(player_id == ID):	
							content = "player" + str(player_id) + " play " + pre_card
							co = content.encode('ascii')
							client_socket.send(co)
	
					else:
						pass
			
			
			if(check_winner(player[player_id]) == 1):
				if(player_id == 0):
					print("player" + str(player_id) + " win!")
				elif(player_id == ID):
					content = "player" + str(player_id) + " win!"
					co = content.encode('ascii')
					client_socket.send(co)
				break;
		
			if(pre_card == "wild"):
				pre_card = "e" + wild_color + "*"
			
			if(pre_card[1:] == "draw4"):
				pre_card = wild_color + "draw4"
				draw_num = draw_num + 4
		
			if(reverse_gate == 0):
				turn = turn + 1
			else:
				turn = turn -1
		
while True:
	
	client_socket,addr = server.accept()
	print("[*] Accept connection from:"+ addr[0] +":" + str(addr[1]))
	
	now_add_player = now_add_player + 1
		
	client_handler = threading.Thread(target=handle_client,args=(client_socket,addr[0],addr[1],))
	client_handler.start()