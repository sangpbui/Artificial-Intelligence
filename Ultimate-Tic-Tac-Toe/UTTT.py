'''
Jeremy Falloon
Shannon Marshall
Sang Bui
Stephanie Parkhurst

Ultimate Tic Tac Toe

Main File. Run the program with the command: python UTTT.py <option number> 
Run this command without the option number to see the different setups.

Comments with our initials are explaining the original code. Other comments are code we modified and/or added. 
Unless mentioned otherwise, all functionality was used. 

'''

import sys
import random
import signal
import pdb
from PlayerAI import PlayerAI

#list of xnums and onums
XMovesList = set()
OMovesList = set()

# SM - Timer handler, helper function
class TimedOutExc(Exception):
        pass

def handler(signum, frame):
    # SM - print 'Signal handler called with signal', signum
    raise TimedOutExc()

#Calculates the next move
# old_move[0] is the row and old_move[1] is the column
def calc_blocks_allowed(old_move):
                blocks_allowed = []
                if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
				## top left board
				blocks_allowed = [0]
		elif old_move[0] % 3 == 0 and old_move[1] in [2, 5, 8]:
				## top right board
				blocks_allowed = [2]
		elif old_move[0] in [2,5, 8] and old_move[1] % 3 == 0:
				## bottom left board
				blocks_allowed  = [6]
		elif old_move[0] in [2,5,8] and old_move[1] in [2,5,8]:
				### bottom right board
				blocks_allowed = [8]
		elif old_move[0] % 3 == 0 and old_move[1] in [1,4,7]:
				## upper-center block
				blocks_allowed = [1]
	
		elif old_move[0] in [1,4,7] and old_move[1] % 3 == 0:
				## middle-left block
				blocks_allowed = [3]
		
		elif old_move[0] in [2,5,8] and old_move[1] in [1,4,7]:
				## lower-center block
				blocks_allowed = [7]

		elif old_move[0] in [1,4,7] and old_move[1] in [2,5,8]:
				## middle-right block
				blocks_allowed = [5]
		elif old_move[0] in [1,4,7] and old_move[1] in [1,4,7]:
				blocks_allowed = [4]

		return blocks_allowed

#SP & SM: Human player
class Manual_player:
	def __init__(self):
		pass
	def move(self, temp_board, temp_block, old_move, flag):
		global XMovesList, OMovesList
		print 'Enter your move: <format:row column> (you\'re playing with', flag + ")"
		# SB & JF - mvp is the user input, which has 2 values.
		mvp = raw_input()
		# SB & JF - split input on space character
		mvp = mvp.split()
		# SB & JF - add move ordered pair (row, column) into the appropriate move list 
		(XMovesList if flag == 'x' else OMovesList).add((int(mvp[0]), int(mvp[1])))
		# SB & JF - return the move as an ordered pair
		return (int(mvp[0]), int(mvp[1]))
		

#SP & SM - Bot that tries to block a win in current block, else if it plays in corners, else plays random.
class Player9:	
	def __init__(self):
		pass

	def move(self,temp_board,temp_block,old_move,flag):
		print "Medium bot move"

		for_corner = [0,2,3,5,6,8]

		#SB & JF - List of permitted blocks, based on old move.
		blocks_allowed = calc_blocks_allowed(old_move)

                for i in reversed(blocks_allowed):   #SB & JF - not necessary for only 1 block for block status SP and SM
                    if temp_block[i] != '-':
                        blocks_allowed.remove(i)
    # SB & JF - Evaluation function
		return_value = gameReturnsMoveBlocksAllowed(temp_board, blocks_allowed, flag)
		return return_value
		# SP & SM - We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
		# SP & SM - cells = get_empty_out_of(temp_board, blocks_allowed,temp_block)


# SP & SM - Bot that plays randomly		
class Player2:
	def __init__(self):
		pass
	def move(self,temp_board,temp_block,old_move,flag):
		print "Easy bot move"
		for_corner = [0,2,3,5,6,8]

		# List of permitted blocks, based on old move.
		blocks_allowed  = calc_blocks_allowed(old_move)
                
                for i in reversed(blocks_allowed):
                    if temp_block[i] != '-':
                        blocks_allowed.remove(i)

                #  SP & SM - We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
		cells = get_empty_out_of(temp_board,blocks_allowed,temp_block)
		return cells[random.randrange(len(cells))]



# SP & SM - function for returning corners   
# SB & JF - returns random corner on board when all 4 corners are available
def gameCornersBlocksReturn(blocks_allowed, cornerNoncornersListForABoard, flag):
	for i in xrange(len(blocks_allowed)):
		if len(cornerNoncornersListForABoard[i][0]) is 4:
			choice = randomPrint(cornerNoncornersListForABoard,i)
			(XMovesList if flag == 'x' else OMovesList).add(choice)
			return choice
	return None

def randomPrint(cornerNoncornersListForABoard,index):
	return random.choice(cornerNoncornersListForABoard[index][0])

# SP & SM - Returns corners of each block	
def returnCorners(block):
	if block is 0:
		return [(0,0), (0,2), (2,0), (2,2)]
	elif block is 1:
		return [(0,3), (0,5), (2,3), (2,5)]
	elif block is 2:
		return [(0,6), (0,8), (2,6), (2,8)]
	elif block is 3:
		return [(3,0), (3,2), (5,0), (5,2)]
	elif block is 4:
		return [(3,3), (3,5), (5,3), (5,5)]
	elif block is 5:
		return [(3,6), (3,8), (5,6), (5,8)]
	elif block is 6:
		return [(6,0), (6,2), (8,0), (8,2)]
	elif block is 7:
		return [(6,3), (6,5), (8,3), (8,5)]
	elif block is 8:
		return [(6,6), (6,8), (8,6), (8,8)]

# SB & JF - Evaluation function for Player9
def gameReturnsMoveBlocksAllowed(temp_board, blocks_allowed, flag):	    #Will need some of this logic but not all SP and SM
	global XMovesList, OMovesList
	# SB & JF - return valid spots to be played
	cornerNoncornersListForABoard = gameCornerNonCornersBlock(blocks_allowed, True)
	# SB & JF - returns the position of winning spot of the opposing player
	vertex = gameFinishFirstForWin(temp_board, blocks_allowed, flag)
	# SB & JF - If it exists, return it so we play there and they don't win that board the next time they can play on it!
	if vertex is not None:
		return vertex
	# SB & JF - returns a corner of the current board to be played on when all 4 corners are available
	vertex = gameCornersBlocksReturn(blocks_allowed, cornerNoncornersListForABoard, flag)
	if vertex is not None:
		return vertex
	for ix in range(len(blocks_allowed)):
		marks = []
		# SB & JF - available spots to be played on current board
		avail = addFunc(cornerNoncornersListForABoard,ix)
		# SB & JF - iterates over amount of possible moves on the current board
		for gh in avail:
			nodaBoard = gameBoard([blocks_allowed[ix]])
			callfuncPlay(nodaBoard,gh,flag)
			marks.append(nodaBoard.minmaxWinnerEvaluate(flag, blocks_allowed[ix])) #piece is x or o
		bestFor = max(enumerate(marks), key = lambda x:x[1])
		for kkj in xrange(len(bestFor)):
			jre = returnBestAvail(bestFor,kkj,avail) 
			return checkForNothing(temp_board,jre,flag)
	return None

# SP & SM - Returns the spots that are not corners
def returnNonCorners(block):
	if block is 0:
		return [(0,1), (1,0), (1,1), (1,2), (2,1)]
	elif block is 1:
		return [(0,4), (1,3), (1,4), (1,5), (2,4)]
	elif block is 2:
		return [(0,7), (1,6), (1,7), (1,8), (2,7)]
	elif block is 3:
		return [(3,1), (4,0), (4,1), (4,2), (5,1)]
	elif block is 4:
		return [(3,4), (4,3), (4,4), (4,5), (5,4)]
	elif block is 5:
		return [(3,7), (4,6), (4,7), (4,8), (5,7)]
	elif block is 6:
		return [(6,1), (7,0), (7,1), (7,2), (8,1)]
	elif block is 7:
		return [(6,4), (7,3), (7,4), (7,5), (8,4)]
	elif block is 8:
		return [(6,7), (7,6), (7,7), (7,8), (8,7)]

# SP & SM - returns the list of corner and non cromer points
# SB & JF - return all valids moves of current board to be played on
def gameCornerNonCornersBlock(blocks_allowed, check):
	return_list = []
	# SB & JF - return all ordered pairs of the current block to be played on
	# SP & SM - does not rule out spots that have already been played
	for block in blocks_allowed:
		corners = []
		noncorners = []
		if block is 0:
			corners = returnCorners(block)
			noncorners = returnNonCorners(block)
		elif block is 1:
			corners = returnCorners(block)
			noncorners = returnNonCorners(block)
		elif block is 2:
			corners = returnCorners(block)
			noncorners = returnNonCorners(block)
		elif block is 3:
			corners = returnCorners(block)
			noncorners = returnNonCorners(block)
		elif block is 4:
			corners = returnCorners(block)
			noncorners = returnNonCorners(block)
		elif block is 5:
			corners = returnCorners(block)
			noncorners = returnNonCorners(block)
		elif block is 6:
			corners = returnCorners(block)
			noncorners = returnNonCorners(block)
		elif block is 7:
			corners = returnCorners(block)
			noncorners = returnNonCorners(block)
		elif block is 8:
			corners = returnCorners(block)
			noncorners = returnNonCorners(block)
		else:
			print "SOMETHING REALLY WEIRD HAPPENED"
			sys.exit(1)
		if check:
			corners = cornerscheckFuncfilter(XMovesList,OMovesList,corners,noncorners)
			noncorners = noncornerscheckFuncfilter(XMovesList,OMovesList,corners,noncorners)
		cornerNoncornersListForABoard = []
		cornerNoncornersListForABoard = appendfunccorners(cornerNoncornersListForABoard,corners)
		cornerNoncornersListForABoard = appendfuncnoncorners(cornerNoncornersListForABoard,noncorners)
		return_list.append(cornerNoncornersListForABoard)
	return return_list

### The next few functions are deprecated because our bot doesn't look at corners but kept these for code safety ###
# SB & SM - Checks corners
def cornerscheckFuncfilter(XMovesList,OMovesList,corners,noncorners):
	return filter(lambda x: x not in list(XMovesList) + list(OMovesList), corners)

# SB & SM - Checks for non-corners
def noncornerscheckFuncfilter(XMovesList,OMovesList,corners,noncorners):
	return filter(lambda x: x not in list(XMovesList) + list(OMovesList), noncorners)

# SB & SM - Appends the list of corners
def appendfunccorners(cornerNoncornersListForABoard,cornerslist):
	cornerNoncornersListForABoard.append(cornerslist)
	return cornerNoncornersListForABoard

# SB & SM - Appends the list of non-corners
def appendfuncnoncorners(cornerNoncornersListForABoard,cornerslist):
	cornerNoncornersListForABoard.append(cornerslist)
	return cornerNoncornersListForABoard
### End of deprecation ###


# SB & SM - Creates list of allowed blocks to play in
def gameReturnsMoveBlocksNegationAllowed(temp_board, block_stat, flag):
	gameListAllowedBlocksFucList = []
	for i in xrange(len(block_stat)):
		gameListAllowedBlocksFucList = appendfunc(block_stat,gameListAllowedBlocksFucList,i)
	return checkFor1(gameListAllowedBlocksFucList,temp_board,flag)

# SB & SM - Appends lists
def appendfunc(block_stat,gameListAllowedBlocksFucList,index):
	if block_stat[index] == '-':
		gameListAllowedBlocksFucList.append(index)
	return gameListAllowedBlocksFucList

# SB & SM - Checks if there are any allowed moves
def checkFor1(alloe_list,temp_board,checkFlag):
	if len(alloe_list) >= 1:
		return gameReturnsMoveBlocksAllowed(temp_board,alloe_list,checkFlag)
	else:
		return None
	
# SB & SM - Adds non-corner blocks to corner block for blocks allowed, deprecated
def addFunc(cornerNoncornersListForABoard,index):
	return cornerNoncornersListForABoard[index][0] + cornerNoncornersListForABoard[index][1]

# SB & SM - Plays the game
def callfuncPlay(nodaBoard,gh,check):
	nodaBoard.play(gh,check)

# SB & SM - Checks if the requested cell is empty
def checkForNothing(temp_board,j,flag):
	if temp_board[j[0]][j[1]] == '-':
		addRespective(flag,j)
		return j

# SP and SM - Keeps track of player's moves
def addRespective(flag,j):
	if flag == 'x':
		XMovesList.add(j)
	else:
		OMovesList.add(j)

# SB & SM - Returns available
def returnBestAvail(best,index,avail):
	return avail[best[index]]


# SP & SM - Initializes the game
def get_init_board_and_blockstatus():
	board = []
	for i in range(9):
		row = ['-']*9
		board.append(row)
	
	block_stat = ['-']*9
	return board, block_stat

#  SP & SM - Checks if player has messed with the board. Don't mess with the board that is passed to your move function. 
def verification_fails_board(board_game, temp_board_state):
	return board_game == temp_board_state	

#  SP & SM - Checks if player has messed with the block. Don't mess with the block array that is passed to your move function. 
def verification_fails_block(block_stat, temp_block_stat):
	return block_stat == temp_block_stat	

# SP & SM - Gets empty cells from the list of possible blocks. Hence gets valid moves. 
# SP & SM - id2 is columns and id1 is rows SP and SM
def get_empty_out_of(gameb, blal, block_stat):
	cells = []  # it will be list of tuples
	# SP & SM - Iterate over possible blocks and get empty cells
	for idb in blal:
		id1 = idb/3
		id2 = idb%3
		for i in range(id1*3,id1*3+3):
			for j in range(id2*3,id2*3+3):
				if gameb[i][j] == '-':
					cells.append((i,j))

	#  SP & SM - If all the possible blocks are full, you can move anywhere        #Good SP and SM
	if cells == []:
		for i in range(9):
			for j in range(9):
                                no = (i/3)*3
                                no += (j/3)
				if gameb[i][j] == '-' and block_stat[no] == '-':
					cells.append((i,j))	
	return cells
		

# SP & SM - Holds the basic board and game rules are implemented here
class gameBoard:
        # SB & SM - Initializes the board
	def __init__(self, blocks_allowed):
		self.board, temp = get_init_board_and_blockstatus()
		cornerNoncornersListForABoard = gameCornerNonCornersBlock(blocks_allowed, False)
		self.free = addFunc(cornerNoncornersListForABoard,0) 
		self.player1x = set()
		self.player2o = set()

        # SB & SM - Defines winner
	def minmaxWinnerDecide(self, block):
		for ride in dicOfWinningList[block]:
            		if ride.issubset(self.player1x):
	            		return 'e'
			if ride.issubset(self.player2o):
				return 'y'
			if len(self.player1x) + len(self.player2o) == 9:
				return 'd'
		return False

        # SB & SM - A cell is claimed by a player
	def assign(self,y,x,piece):
		self.board[y][x] = piece

        # SB & SM - The game is played
	def play(self, n, piece=None):
		global XMovesList, OMovesList
		x = n[0]
		y = n[1]
		if piece:
			self.assign(y,x,piece)
			(self.player1x if piece == 'e' else self.player2o).add(n)
			self.removeFunction(n)
		else:
			self.board[y][x] = "_"
			self.free.append(n)
			(self.player1x if n in self.player1x else self.player2o).remove(n)

        # SB & SM - Removes the game
	def removeFunction(self,n):
		self.free.remove(n)

        # SB & SM - Checks for draw
	def returnFunctionP(self,state,piece):
		return (1 if state == piece else 0 if state == 'd' else -1)

        # SB & SM - Evaluates who won
	def minmaxWinnerEvaluate(self, piece, block):
		state = self.minmaxWinnerDecide(block)
		if state:
			return self.returnFunctionP(state,piece)			
		marks = []
		opponent = "xo".replace(piece, "")
		for n in self.free:
			self.play(n, opponent)
			marks.append(0 - self.minmaxWinnerEvaluate(opponent, block))
			self.play(n)
		safest = min(marks)
		return safest


#  SP & SM - Note that even if someone has won a block, it is not abandoned. But then, there's no point winning it again!
#  SP & SM - Returns True if move is valid
def check_valid_move(game_board,block_stat, current_move, old_move):

	#  SP & SM - first we need to check whether current_move is tuple of not
	#  SP & SM - old_move is guaranteed to be correct
	
	#Error checking for user input SP and SM
	if type(current_move) is not tuple:
		return False
	
	if len(current_move) != 2:
		return False

	a = current_move[0]
	b = current_move[1]	

	if type(a) is not int or type(b) is not int:
		return False
	if a < 0 or a > 8 or b < 0 or b > 8:
		return False

	# SP & SM - Special case at start of game, any move is okay!
	if old_move[0] == -1 and old_move[1] == -1:
		return True

        # SP & SM - Deprecated code: kept for safety 
	for_corner = [0,2,3,5,6,8]

	# SP & SM - List of permitted blocks, based on old move.
	blocks_allowed  = []

	if old_move[0] in for_corner and old_move[1] in for_corner:
		
		## JF - next move is a corner move
			
			if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
				## top left board
				blocks_allowed = [0]
			elif old_move[0] % 3 == 0 and old_move[1] in [2, 5, 8]:
				## top right board
				blocks_allowed = [2]
			elif old_move[0] in [2,5, 8] and old_move[1] % 3 == 0:
				## bottom left board
				blocks_allowed  = [6]
			elif old_move[0] in [2,5,8] and old_move[1] in [2,5,8]:
				### bottom right board
				blocks_allowed = [8]
			else:
				print "SOMETHING REALLY WEIRD HAPPENED!"
				sys.exit(1)

	else:
		####  SP & SM - we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
		if old_move[0] % 3 == 0 and old_move[1] in [1,4,7]:
			## upper-center block
			blocks_allowed = [1]
	
		elif old_move[0] in [1,4,7] and old_move[1] % 3 == 0:
			## middle-left block
			blocks_allowed = [3]
		
		elif old_move[0] in [2,5,8] and old_move[1] in [1,4,7]:
			## lower-center block
			blocks_allowed = [7]

		elif old_move[0] in [1,4,7] and old_move[1] in [2,5,8]:
			## middle-right block
			blocks_allowed = [5]

		elif old_move[0] in [1,4,7] and old_move[1] in [1,4,7]:
			blocks_allowed = [4]

        # SP & SM - Check if the block is won, or completed. If so you cannot move there. 

        for i in reversed(blocks_allowed):
            	if block_stat[i] != '-':
                	blocks_allowed.remove(i)
        #  SP & SM - We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
        cells = get_empty_out_of(game_board, blocks_allowed,block_stat)#Calculates the next move
	#Checks if you made a valid move. 
        if current_move in cells:
     	    return True
        else:
    	    return False

# SP & SM - Updates the board's status and checks for draws and wins
def update_lists(game_board, block_stat, move_ret, fl):    #fl = flag SP and SM
	# SP & SM - move_ret has the move to be made, so we modify the game_board, and then check if we need to modify block_stat
	game_board[move_ret[0]][move_ret[1]] = fl

	# SP & SM - block_no calculates the current block move before the next move is decided -SM SP
	block_no = (move_ret[0]/3)*3 + move_ret[1]/3
	id1 = block_no/3     #row SP and SM
	id2 = block_no%3     #col SP and SM
	mflg = 0
	if block_stat[block_no] == '-':  #not full yet SP and SM
		if game_board[id1*3][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3+2] and game_board[id1*3+1][id2*3+1] != '-':  #checking diags SP and SM
			mflg=1
		if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3][id2*3 + 2] and game_board[id1*3+1][id2*3+1] != '-':
			mflg=1
		            ### col-wise SP and SM
                if mflg != 1:
                    for i in range(id2*3,id2*3+3):
                        if game_board[id1*3][i]==game_board[id1*3+1][i] and game_board[id1*3+1][i] == game_board[id1*3+2][i] and game_board[id1*3][i] != '-':
                                mflg = 1
                                break

                ### row-wise
		if mflg != 1:
                    for i in range(id1*3,id1*3+3):
                        if game_board[i][id2*3]==game_board[i][id2*3+1] and game_board[i][id2*3+1] == game_board[i][id2*3+2] and game_board[i][id2*3] != '-':
                                mflg = 1
                                break
	else:
	     	cornerNoncornersListForABoard = gameCornerNonCornersBlock([block_no], False)
	     	for i in cornerNoncornersListForABoard[0][0] + cornerNoncornersListForABoard[0][1]:
				 (XMovesList if block_stat[block_no] == 'x' else OMovesList).add(i)

	

	
	if mflg == 1:
		block_stat[block_no] = fl
	
        # SP & SM - check for draw on the block.
        # SP & SM - has to do with individual cells. Might be all we need and not above stuff. SP and SM

        id1 = block_no/3
	id2 = block_no%3
        cells = []
	for i in range(id1*3,id1*3+3):
	    for j in range(id2*3,id2*3+3):
		if game_board[i][j] == '-':
		    cells.append((i,j))

        if cells == [] and mflg!=1:
            block_stat[block_no] = 'd' #Draw
        return

#Updated terminal state to win by one block        
def terminal_state_reached(game_board, block_stat):
        # Check if game is won!
        bs = block_stat
        # Win with one block
        for i in range(0, len(bs)):
        	if bs[i] != '-' and bs[i] != 'd':
        		return True, 'W'
        return False, 'Continue'
  
  # JF & SP - Win with 3 blocks, kept in case we wanted to play this way      
	## Row win
	if (bs[0] == bs[1] and bs[1] == bs[2] and bs[1]!='-' and bs[1]!='d') or (bs[3]!='d' and bs[3]!='-' and bs[3] == bs[4] and bs[4] == bs[5]) or (bs[6]!='d' and bs[6]!='-' and bs[6] == bs[7] and bs[7] == bs[8]):
		print block_stat
		return True, 'W'
	## Col win
	elif (bs[0]!='d' and bs[0] == bs[3] and bs[3] == bs[6] and bs[0]!='-') or (bs[1]!='d'and bs[1] == bs[4] and bs[4] == bs[7] and bs[4]!='-') or (bs[2]!='d' and bs[2] == bs[5] and bs[5] == bs[8] and bs[5]!='-'):
		print block_stat
		return True, 'W'
	## Diag win
	elif (bs[0] == bs[4] and bs[4] == bs[8] and bs[0]!='-' and bs[0]!='d') or (bs[2] == bs[4] and bs[4] == bs[6] and bs[2]!='-' and bs[2]!='d'):
		print block_stat
		return True, 'W'
	else:
		smfl = 0
		for i in range(9):
			for j in range(9):
				if game_board[i][j] == '-' and block_stat[(i/3)*3+(j/3)] == '-':
					smfl = 1
					break
		if smfl == 1:
                        #Game is still on!
			return False, 'Continue'
		
		else:
                        #Changed scoring mechanism
                        # 1. If there is a tie, player with more boxes won, wins.
                        # 2. If no of boxes won is the same, player with more corner move, wins. 
                        point1 = 0
                        point2 = 0
                        for i in block_stat:
                            if i == 'x':
                                point1+=1
                            elif i=='o':
                                point2+=1
			if point1>point2:
				return True, 'P1'
			elif point2>point1:
				return True, 'P2'
			else:
                                point1 = 0
                                point2 = 0
                                for i in range(len(game_board)):
                                    for j in range(len(game_board[i])):
                                        if i%3!=1 and j%3!=1:
                                            if game_board[i][j] == 'x':
                                                point1+=1
                                            elif game_board[i][j]=='o':
                                                point2+=1
			        if point1>point2:
				    return True, 'P1'
			        elif point2>point1:
				    return True, 'P2'
                                else:
				    return True, 'D'	

#All 4 cases are necessary due to differing messages -SM and SP
def decide_minmaxWinnerDecide_and_get_message(player,status, message):
	if player == 'P1' and status == 'L':
		return ('P2',message)
	elif player == 'P1' and status == 'W':
		return ('P1',message)
	elif player == 'P2' and status == 'L':
		return ('P1',message)
	elif player == 'P2' and status == 'W':
		return ('P2',message)
	else:
		return ('NO ONE','DRAW')
	return

#New function added to make the output human readable and prints the winning move
def print_winner(gb, bs, old_move, winner):
        block_no = (old_move[0]/3)*3 + old_move[1]/3
        print '=========== Game Board ==========='
	for i in range(9):
		if i > 0 and i % 3 == 0:
			print
		for j in range(9):
			if j > 0 and j % 3 == 0:
				print " " + gb[i][j],
			else:
				print gb[i][j],

		print
	print "=================================="     
	print "===== Winning Block Status: " + str(block_no) + " ====" #SB & SM
	col = (block_no % 3) * 3
	row = (block_no / 3) * 3
	print "     " + str(col) + " " + str(col+1) + " " + str(col+2)
	print "   ======="
	for i in range(row, row+3):
                print str(i) + " || " + gb[i][col] + " " + gb[i][col+1] + " " + gb[i][col+2]
	print

#bn is block_num of old move
#nb is next_block
#Updated to make output human readable and shows the next block available for play
def print_lists(gb, bs, bn):
	print '=========== Game Board ==========='
	for i in range(9):
		if i > 0 and i % 3 == 0:
			print
		for j in range(9):
			if j > 0 and j % 3 == 0:
				print " " + gb[i][j],
			else:
				print gb[i][j],

		print
	print "=================================="
	nb = calc_blocks_allowed(bn)
	# Print out unique statement for first move
	if len(XMovesList) == 0 and len(OMovesList) == 0:
		print
		print "You have the first move! Play on any board."
		print
	elif bs[bn[0]] == 'W' or bs[bn[0]] == 'L':
	  print       
	  print "===== Winning Block Status: " + str(bn) + " ====" 
	  col = (bn % 3) * 3
	  row = (bn / 3) * 3
	  print "     " + str(col) + " " + str(col+1) + " " + str(col+2)
	  print "   ======="
	  for i in range(row, row+3):
		  print str(i) + " || " + gb[i][col] + " " + gb[i][col+1] + " " + gb[i][col+2]
	  print
	elif bs[nb[0]] == 'd':
	  print
	  print "This board has a draw. Play on any other board."	
	  print
	else:
		for i in range(0, len(nb)):       
			print "===== Current Block Status: " + str(nb[0]) + " ====" #SP and SM
			col = (nb[0] % 3) * 3
			row = (nb[0] / 3) * 3
			print "     " + str(col) + " " + str(col+1) + " " + str(col+2)
			print "   ======="
			for i in range(row, row+3):
				print str(i) + " || " + gb[i][col] + " " + gb[i][col+1] + " " + gb[i][col+2]
	print "=================================="
	print
	print

# SB & SM - Constructs and runs a game of Ultimate Tic-Tac-Toe
# SB & SM - Comments were made by original creator for this function
def simulate(obj1,obj2): # SP & SM - main board that calls everything
	
	# Game board is a 9x9 list, block_stat is a 1D list of 9 elements
	game_board, block_stat = get_init_board_and_blockstatus()
	
	pl1 = obj1 
	pl2 = obj2

	### basically, player with flag 'x' will start the game
	pl1_fl = 'x'
	pl2_fl = 'o'

	old_move = (-1, -1) # For the first move

	minmaxWinnerDecide = ''
	MESSAGE = ''
		
        # Make your move in 6 seconds!
        # Updated time allowed per move to 1 minute
	TIMEALLOWED = 600
	print_lists(game_board, block_stat, old_move)
	global XMovesList, OMovesList
	while(1):

		# Player1 will move
		
		temp_board_state = game_board[:]
		temp_block_stat = block_stat[:]
	
		signal.signal(signal.SIGALRM, handler)
		signal.alarm(TIMEALLOWED)
		flag_set1 = 0
		# Player1 to complete in TIMEALLOWED secs. 
		try:
			# SB & SM - Player1 attempts to make their move
                        ret_move_pl1 = pl1.move(temp_board_state, temp_block_stat, old_move, pl1_fl)
			(XMovesList if pl1_fl == 'x' else OMovesList).add(ret_move_pl1)
			if not ret_move_pl1:
				ret_move_pl1 = gameReturnsMoveBlocksNegationAllowed(temp_board_state, temp_block_stat, pl1_fl)
				(XMovesList if pl1_fl == 'x' else OMovesList).add(ret_move_pl1)
				flag_set1 = 1
				# SB & SM - If move was invalid, the winner is decided
				if not ret_move_pl1:
					minmaxWinnerDecide, MESSAGE = decide_minmaxWinnerDecide_and_get_message('', '',  'COMPLETE')	
					break
	
		except TimedOutExc as e:
			minmaxWinnerDecide, MESSAGE = decide_minmaxWinnerDecide_and_get_message('P1', 'L',   'TIMED OUT')
			break
		signal.alarm(0)
	
                #Checking if list hasn't been modified! Note: Do not make changes in the lists passed in move function!
		if not (verification_fails_board(game_board, temp_board_state) and verification_fails_block(block_stat, temp_block_stat)):
			# Player1 loses - he modified something
			minmaxWinnerDecide, MESSAGE = decide_minmaxWinnerDecide_and_get_message('P1', 'L',   'MODIFIED CONTENTS OF LISTS')
			break
		
		# Check if the move made is valid
		if not check_valid_move(game_board, block_stat,ret_move_pl1, old_move) and flag_set1 is 0:
			## Player1 loses - he made the wrong move.
			minmaxWinnerDecide, MESSAGE = decide_minmaxWinnerDecide_and_get_message('P1', 'L',   'MADE AN INVALID MOVE')
			break


		print "Player 1 made the move:", ret_move_pl1, 'with', pl1_fl

                # So if the move is valid, we update the 'game_board' and 'block_stat' lists with move of pl1
		update_lists(game_board, block_stat, ret_move_pl1, pl1_fl)	
                old_move = ret_move_pl1
                
		# Checking if the last move resulted in a terminal state
		gamestatus, mesg =  terminal_state_reached(game_board, block_stat)
		if gamestatus == True:
			minmaxWinnerDecide, MESSAGE = decide_minmaxWinnerDecide_and_get_message('P1', mesg,  'COMPLETE')
			print_winner(game_board, block_stat, old_move, mesg)
			break

		
		print_lists(game_board, block_stat, old_move)

                # Now player2 plays

                temp_board_state = game_board[:]
                temp_block_stat = block_stat[:]
		flag_set2 = 0

		signal.signal(signal.SIGALRM, handler)
		signal.alarm(TIMEALLOWED)
		try:
                	ret_move_pl2 = pl2.move(temp_board_state, temp_block_stat, old_move, pl2_fl)
			(XMovesList if pl2_fl == 'x' else OMovesList).add(ret_move_pl2)
			if not ret_move_pl2:
				ret_move_pl2 = gameReturnsMoveBlocksNegationAllowed(temp_board_state, temp_block_stat, pl2_fl)
				(XMovesList if pl2_fl == 'x' else OMovesList).add(ret_move_pl2)
				flag_set2 = 1
				if not ret_move_pl2: 
					minmaxWinnerDecide, MESSAGE = decide_minmaxWinnerDecide_and_get_message('', '',  'COMPLETE')	
					break
		except TimedOutExc as e:
			minmaxWinnerDecide, MESSAGE = decide_minmaxWinnerDecide_and_get_message('P2', 'L',   'TIMED OUT')
			break
		signal.alarm(0)

                if not (verification_fails_board(game_board, temp_board_state) and verification_fails_block(block_stat, temp_block_stat)):
			minmaxWinnerDecide, MESSAGE = decide_minmaxWinnerDecide_and_get_message('P2', 'L',   'MODIFIED CONTENTS OF LISTS')
			break
			
                if not check_valid_move(game_board, block_stat,ret_move_pl2, old_move) and flag_set2 is 0:
			minmaxWinnerDecide, MESSAGE = decide_minmaxWinnerDecide_and_get_message('P2', 'L',   'MADE AN INVALID MOVE')
			break


		print "Player 2 made the move:", ret_move_pl2, 'with', pl2_fl
                update_lists(game_board, block_stat, ret_move_pl2, pl2_fl)
		old_move = ret_move_pl2

		gamestatus, mesg =  terminal_state_reached(game_board, block_stat)
                if gamestatus == True:
			minmaxWinnerDecide, MESSAGE = decide_minmaxWinnerDecide_and_get_message('P2', mesg,  'COMPLETE' )
			print_winner(game_board, block_stat, old_move, mesg)
                        break
		print_lists(game_board, block_stat, old_move)
	# SB & SM - The game continues until a winner is decided
	print minmaxWinnerDecide + " won!"
	print MESSAGE

# SB & SM - Compares the board to winning boards
def gameFinishFirstForWin(temp_board, listblocksallow, flag):
	# SB & JF listblocksallow is the list of valid blocks to be played on
	# SB & JF - loops 9 times for first move, once otherwise
	for i in xrange(len(listblocksallow)):
		global dicOfWinningList
		global XMovesList, OMovesList
		for route in dicOfWinningList[listblocksallow[i]]:
			ride1 = listfuc(route,XMovesList,flag,OMovesList)
			ride =  listfucn(route,XMovesList,flag,OMovesList)
			if len(ride1) is 1 and ride1[0] not in list(XMovesList) + list(OMovesList):
				(XMovesList if flag == 'x' else OMovesList).add(ride1[0])
				return ride1[0]
			elif len(ride) is 1 and ride[0] not in list(XMovesList) + list(OMovesList): 
				(XMovesList if flag == 'x' else OMovesList).add(ride[0])
				return ride[0]
	return None

# SB & SM - Compares current game state against known winning boards
def listfuc(way,XMovesList,flag,OMovesList):
	return list(way - set(XMovesList if flag == 'o' else OMovesList))
# SB & SM - Same as above?
def listfucn(way,XMovesList,flag,OMovesList):
	return list(way - set(XMovesList if flag == 'x' else OMovesList))

# SB & SM - A list of all possible winning cell sets
dicOfWinningList = {
	6  : (set([(6,0), (6,1), (6,2)]), set([(7,0), (7,1), (7,2)]), set([(8,0), (8,1), (8,2)]), set([(6,0),(7,0),(8,0)]), set([(6,1),(7,1),(8,1)]), set([(6,2),(7,2),(8,2)]), set([(6,0),(7,1),(8,2)]), set([(8,0),(7,1),(6,2)])),
	1  : (set([(0,3), (0,4), (0,5)]), set([(1,3), (1,4), (1,5)]), set([(2,3), (2,4), (2,5)]), set([(0,3),(1,3),(2,3)]), set([(0,4),(1,4),(2,4)]), set([(0,5),(1,5),(2,5)]), set([(0,3),(1,4),(2,5)]), set([(2,3),(1,4),(0,5)])),
	5  : (set([(3,6), (3,7), (3,8)]), set([(4,6), (4,7), (4,8)]), set([(5,6), (5,7), (5,8)]), set([(3,6),(4,6),(5,6)]), set([(3,7),(4,7),(5,7)]), set([(3,8),(4,8),(5,8)]), set([(3,6),(4,7),(5,8)]), set([(5,6),(4,7),(3,8)])),
	2  : (set([(0,6), (0,7), (0,8)]), set([(1,6), (1,7), (1,8)]), set([(2,6), (2,7), (2,8)]), set([(0,6),(1,6),(2,6)]), set([(0,7),(1,7),(2,7)]), set([(0,8),(1,8),(2,8)]), set([(0,6),(1,7),(2,8)]), set([(2,6),(1,7),(0,8)])),
	4  : (set([(3,3), (3,4), (3,5)]), set([(4,3), (4,4), (4,5)]), set([(5,3), (5,4), (5,5)]), set([(3,3),(4,3),(5,3)]), set([(3,4),(4,4),(5,4)]), set([(3,5),(4,5),(5,5)]), set([(3,3),(4,4),(5,5)]), set([(5,3),(4,4),(3,5)])),
	7  : (set([(6,3), (6,4), (6,5)]), set([(7,3), (7,4), (7,5)]), set([(8,3), (8,4), (8,5)]), set([(6,3),(7,3),(8,3)]), set([(6,4),(7,4),(8,4)]), set([(6,5),(7,5),(8,5)]), set([(6,3),(7,4),(8,5)]), set([(8,3),(7,4),(6,5)])),
	0  : (set([(0,0), (0,1), (0,2)]), set([(1,0), (1,1), (1,2)]), set([(2,0), (2,1), (2,2)]), set([(0,0),(1,0),(2,0)]), set([(0,1),(1,1),(2,1)]), set([(0,2),(1,2),(2,2)]), set([(0,0),(1,1),(2,2)]), set([(2,0),(1,1),(0,2)])),
	3  : (set([(3,0), (3,1),(3,2)]), set([(4,0), (4,1), (4,2)]), set([(5,0), (5,1), (5,2)]), set([(3,0),(4,0),(5,0)]), set([(3,1),(4,1),(5,1)]), set([(3,2),(4,2),(5,2)]), set([(3,0),(4,1),(5,2)]), set([(5,0),(4,1),(3,2)])),
	8  : (set([(6,6), (6,7), (6,8)]), set([(7,6), (7,7), (7,8)]), set([(8,6), (8,7), (8,8)]), set([(6,6),(7,6),(8,6)]), set([(6,7),(7,7),(8,7)]), set([(6,8),(7,8),(8,8)]), set([(6,6),(7,7),(8,8)]), set([(8,6),(7,7),(6,8)]))
}

#Called from command line - This assigns players and determines who goes first
if __name__ == '__main__':
	## get game playing objects

	if len(sys.argv) != 2:
		print 'Usage: python simulator.py <option>'
		print '<option> can be 1 => Human vs. Human'
		print '                2 => Human vs. Easy'
		print '                3 => Human vs. Medium'
		print '                4 => AI vs. Human'
		print '                5 => AI vs. Easy'
		print '                6 => AI vs. Medium'
		print '                7 => Easy vs. Medium'
		sys.exit(1)
 
	obj1 = ''
	obj2 = ''
	option = sys.argv[1]

	if option == '1':
		obj1 = Manual_player()
		obj2 = Manual_player()
	elif option == '2':
		obj1 = Manual_Player()
		obj2 = Player2()
	elif option == '3':
		obj1 = Manual_player()
		obj2 = Player9()
	elif option == '4':
		obj1 = PlayerAI()
		obj2 = Manual_player()
	elif option == '5':
		obj1 = PlayerAI()
		obj2 = Player2()
	elif option == '6':
		obj1 = PlayerAI()
		obj2 = Player9()
	elif option == '7':
		obj1 = Player2()
		obj2 = Player9()
        
        # Deciding player1 / player2 after a coin toss
        # However, in the tournament, each player will get a chance to go 1st. 
        num = random.uniform(0,1)
        if num > 0.5:
		simulate(obj2, obj1)
	else:
		simulate(obj1, obj2)
