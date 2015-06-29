import socket
import threading
import os
import sys

import pickle
import time

target_host = "127.0.0.1"
target_port = 11235


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client.connect((target_host,target_port))
		
def handle_receive():
		
	response = client.recv(4096)
	re = response.decode('ascii')
		
	if(re == "ID"):
		response = client.recv(4096)
		re = response.decode('ascii')
		ID = int(re)
		
		print("Waiting Game Start!")
		
		response = client.recv(4096)
		re = response.decode('ascii')
		
		if(re == "Game Start!"):
			print("Game Start!")
		
		response = client.recv(4096)
		re = response.decode('ascii')
				
		if(re == "card_list"):
			data = client.recv(4096)
			data_list = pickle.loads(data)
			print("player" + str(ID))
			print(data_list)
		
		while(True):
			print("")
			print("============================================")
			print("")
			
			response = client.recv(4096)
			re = response.decode('ascii')
			
			print("player"+ str(re) + "'s turn")
			
			if(ID != int(re)):
				pass				
			else:
				data = client.recv(4096)
				data_list = pickle.loads(data)
				print(data_list)
				
				response = client.recv(4096)
				re = response.decode('ascii')
				print("Last Card: " + str(re))
				
				response = client.recv(4096)
				re = response.decode('ascii')
				print("Debug: check: " + str(re))
				
				if(int(re) == 7):
					response = client.recv(4096)
					re = response.decode('ascii')
					print("player" + str(ID) + " is draw " + str(re) + " cards this turn")
					
					data = client.recv(4096)
					data_list = pickle.loads(data)
					print(data_list)
										
				elif(int(re) == 6):
					response = client.recv(4096)
					re = response.decode('ascii')
					print("play draw card or draw(" + str(re) + " cards )")
					
					content = input()
					co = content.encode('ascii')
					client.send(co)
					time.sleep(1)
					
					if(content == "draw"):
						print("player" + str(player_id) + " is draw " + str(re) + " cards this turn")
						
						data = client.recv(4096)
						data_list = pickle.loads(data)
						print(data_list)
						pass
					
					else:
						while(True):
							response = client.recv(4096)
							re = response.decode('ascii')
							
							if(int(re) == 1):
								print("choose color(r,y,b,g):")
								content = input()
								co = content.encode('ascii')
								client.send(co)
								time.sleep(1)
								
								response = client.recv(4096)
								re = response.decode('ascii')
								print("player" + str(player_id) + " play " + str(re))
								
								break
								
							else:
								print("please play a draw4 card")
								content = input()
								co = content.encode('ascii')
								client.send(co)
								time.sleep(1)
							
				elif(int(re) == 5):
					response = client.recv(4096)
					re = response.decode('ascii')
					print("player" + str(ID) + " is draw " + str(re) + " cards this turn")
					
					data = client.recv(4096)
					data_list = pickle.loads(data)
					print(data_list)
					pass
				
				elif(int(re) == 4):
					response = client.recv(4096)
					re = response.decode('ascii')
					print("play draw card or draw(" + str(re) + " cards ")
					
					
					content = input()
					co = content.encode('ascii')
					client.send(co)
					time.sleep(1)
					
					if(content == "draw"):
						response = client.recv(4096)
						re = response.decode('ascii')
						print("player" + str(player_id) + " is draw " + str(re) + " cards this turn")
						data = client.recv(4096)
						data_list = pickle.loads(data)
						print(data_list)
						pass
					else:
						while(True):
							response = client.recv(4096)
							re = response.decode('ascii')
										
					pass
				elif(int(re) == 3):
					pass
				elif(int(re) == 2):
					pass
				elif(int(re) == 1):
					pass
				elif(int(re) == 0):
					pass		
			
			
		
receive_handler  = threading.Thread(target=handle_receive,args=())
receive_handler.start()	