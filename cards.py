def get_cards():
	#normal card, 0*1, 1~9*2, 4 colors, total 76 cards
	nr = ["r0","r1","r1","r2","r2","r3","r3","r4","r4","r5","r5","r6","r6","r7","r7","r8","r8","r9","r9"]
	ny = ["y0","y1","y1","y2","y2","y3","y3","y4","y4","y5","y5","y6","y6","y7","y7","y8","y8","y9","y9"]
	nb = ["b0","b1","b1","b2","b2","b3","b3","b4","b4","b5","b5","b6","b6","b7","b7","b8","b8","b9","b9"]
	ng = ["g0","g1","g1","g2","g2","g3","g3","g4","g4","g5","g5","g6","g6","g7","g7","g8","g8","g9","g9"]
	
	#funcation card, skip*2, reverse*2, draw two*2, 4 colors, total 24 cards
	fr = ["rskip","rskip","rreverse","rreverse","rdraw2","rdraw2"]
	fy = ["yskip","yskip","yreverse","yreverse","ydraw2","ydraw2"]
	fb = ["bskip","bskip","breverse","breverse","bdraw2","bdraw2"]
	fg = ["gskip","gskip","greverse","greverse","gdraw2","gdraw2"]
	
	#wild card, wild*4, wild draw 4*4, total 8 cards
	wild = ["wild","wild","wild","wild","wdraw4","wdraw4","wdraw4","wdraw4"]
		
	uno_card = []
	uno_card.extend(nr)
	uno_card.extend(ny)
	uno_card.extend(nb)
	uno_card.extend(ng)
	uno_card.extend(fr)
	uno_card.extend(fy)
	uno_card.extend(fb)
	uno_card.extend(fg)
	uno_card.extend(wild)
		
	return uno_card

def get_cards_bool():
	uno_card_bool = []

	for i in range(108):
		uno_card_bool.extend([0])
		
	return uno_card_bool;