import random

class Board:
	def __init__(self):
		self.fields = [Field(n) for n in range(10)] # ignore index 0
		
	def copy(self):
		b = Board()
		b.fields = [f.copy() for f in self.fields]
		return b
	
	def addPreMark(self, letter, num, pos1, pos2):
		self.fields[pos1].addPreMark(PreMark(letter, num, pos1, pos2))
		self.fields[pos2].addPreMark(PreMark(letter, num, pos2, pos1))
	
	def addFinMark(self, letter, pos):
		self.fields[pos].addFinMark(FinMark(letter, pos))
		
	def hasWon(self, letter):
		bo = self.realBoard()
		return ((bo[7] == le and bo[8] == le and bo[9] == le) or # across the top

		(bo[4] == le and bo[5] == le and bo[6] == le) or # across the middle

		(bo[1] == le and bo[2] == le and bo[3] == le) or # across the bottom

		(bo[7] == le and bo[4] == le and bo[1] == le) or # down the left side

		(bo[8] == le and bo[5] == le and bo[2] == le) or # down the middle

		(bo[9] == le and bo[6] == le and bo[3] == le) or # down the right side

		(bo[7] == le and bo[5] == le and bo[3] == le) or # diagonal

		(bo[9] == le and bo[5] == le and bo[1] == le)) # diagonal

	def realBoard(self): # returns only the "real" board, i.e. measured fields
		bo = [' '] * 10
		for f in self.fields:
			for m in f.contents:
				if isinstance(m, FinMark):		
					bo[f.num] = m.letter
		return bo
		
	def printBoard(self):
		for f in self.fields:
			print("Field" + str(f.num))
			print(f.fieldToString())
			
	def isSpaceFree(self, move):
		# Return true if the passed move is free on the passed board.
		board = self.realBoard()
		return board[move] == ' '

	def getListOfMoves(self):
		listOfMoves = []
		for move in range(1, 10):
			if self.isSpaceFree(board, move):
				listOfMoves.append(move)
		return listOfMoves
		
	def makeSteps(self, currentFieldNum, initialFieldNum):
		#print("Standing in {0}".format(currentFieldNum))
		for m in self.fields[currentFieldNum].contents:
			#print("Found mark {0}{1}".format(m.letter, m.num))
			if isinstance(m, FinMark):
				continue
			nextNum = m.otherpos
			#print("Transition to {0}".format(nextNum))
			self.fields[currentFieldNum].deletePreMark_(m.letter, m.num)
			self.fields[nextNum].deletePreMark_(m.letter, m.num)
			#self.printBoard()
			if nextNum == initialFieldNum:
				#print("Success! at {0}".format(initialFieldNum))
				return initialFieldNum
			else:
				return self.makeSteps(nextNum, initialFieldNum)
		
	def findCycle(self, markStartingFrom):		
		copyBoard = self.copy()
		if copyBoard.makeSteps(markStartingFrom, markStartingFrom):
			return True
	
	def collapse(self, markletter, marknum, collapseAt, collapseNotAt):
		currentField = self.fields[collapseAt]
		otherField = self.fields[collapseNotAt]
		print("Deleting premark {0}{1}".format(markletter, str(marknum)))
		currentField.deletePreMark_(markletter, marknum)
		otherField.deletePreMark_(markletter, marknum)
		listOfMarks = list(currentField.contents)
		print("inserting final mark {0} at {1}".format(markletter, collapseAt))
		currentField.addFinMark(FinMark(markletter, collapseAt))
		for markToBeReplaced in listOfMarks:
			m = markToBeReplaced
			if isinstance(m, FinMark):
				continue
			print("has also mark {0}{1}".format(m.letter, str(m.num)))
		for markToBeReplaced in listOfMarks:
			m = markToBeReplaced
			if isinstance(m, FinMark):
				continue
			self.collapse(m.letter, m.num, m.otherpos, m.pos)
				
		
class Field:
	def __init__(self, num):
		self.contents = []
		self.num = num
		
	def copy(self):
		f = Field(self.num)
		for m in self.contents:
			f.contents.append(m.copy())
		return f
		
	def addPreMark(self, pmark):
		if self.num != pmark.pos:
			print("Error: Wrong Mark position")
			return
		self.contents.append(pmark)
		
	def addFinMark(self, fmark):
		if self.num != fmark.pos:
			print("Error: Wrong Final Mark position")
			return
		self.contents.append(fmark)
	
	def deletePreMark(self, pmark):
		if pmark in self.contents:
			v.remove(pmark)
		else:
			print("Error: Pre Mark not in Field")
			
	def deletePreMark_(self, letter, num):
		for m in self.contents:
			if isinstance(m, PreMark):
				if m.num == num and m.letter == letter:
					self.contents.remove(m)
	
	def deleteFinMark(self, fmark):
		if fmark in self.contents:
			self.contents.remove(fmark)
		else:
			print("Error: Final Mark not in Field")
			
	def fieldToString(self):
		for m in self.contents:
			if isinstance(m, FinMark):
				return m.letter
		# so apparently there is no final mark
		s = ""
		for m in self.contents:
			s += (m.letter + str(m.num) + ", ")
		return s
			
class PreMark:
	def __init__(self, letter, num, pos, otherpos):
		self.letter = letter
		self.num = num
		self.pos = pos
		self.otherpos = otherpos
	def copy(self):
		pm = PreMark(self.letter, self.num, self.pos, self.otherpos)
		return pm
		
class FinMark:
	def __init__(self, letter, pos):
		self.letter = letter
		self.pos = pos
	def copy(self):
		fm = FinMark(self.letter, self.pos)
		return fm
		
b = Board()
b.addPreMark('X', 1, 2, 4)
b.addPreMark('O', 4, 2, 6)
b.addPreMark('O', 2, 2, 5)
b.addPreMark('X', 3, 4, 5)
b.printBoard()
b2 = b.copy()
print(b2.makeSteps(2, 2))
print(b.realBoard())

"""def drawBoard(board):
		# This function prints out the board that it was passed.
      # "board" is a list of 10 strings representing the board (ignore index 0)
		print('   |   |')
		print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
		print('   |   |')
		print('-----------')
		print('   |   |')
		print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
		print('   |   |')
		print('-----------')
		print('   |   |')
		print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
		print('   |   |')
		
def drawField(field):		
		return"""
