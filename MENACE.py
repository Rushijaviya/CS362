import numpy as np
import random
import json

def saveToJson(data):
  with open('train.json', 'w') as outfile:
    json.dump(data.__dict__, outfile)

class MenacePlayer:
    def __init__(self):
        self.matchboxes = {}
        self.num_win = 0
        self.num_draw = 0
        self.num_lose = 0
    
    def save(self):
      saveToJson(self)

def ValidMove(board,move):
  if move >= 0 and move <=8 and board[move] == " ":
    return True
  else :
    return False

def getEmptySpaces(currentState):
  count=[]
  for i in range(len(currentState)):
    if currentState[i] == ' ':
      count.append(i)
  return np.array(count)

def printBoard(board):
        print("\n 0 | 1 | 2     %s | %s | %s\n"
               "---+---+---   ---+---+---\n"
               " 3 | 4 | 5     %s | %s | %s\n"
               "---+---+---   ---+---+---\n"
               " 6 | 7 | 8     %s | %s | %s" % (board[0], board[1], board[2],
                                                board[3], board[4], board[5],
                                                board[6], board[7], board[8]))

# Check if Player 1 wins return +10
# Check if Player 2 wins return -10
# Check if it is draw return 0
# otherwise return -1

def isGameOver(currentState):
  state=currentState.copy()

  # check for Horizontal win
  for i in range(0,7,3) :
    if (state[i] == state[i + 1] == state[i + 2]):
      if (state[i]=='X'):
        return 10
      elif (state[i]=='O'):
        return -10

  # check vertical win
  for i in range(0,3):
    if (state[i] == state[i + 3] == state[i + 6]):
      if (state[i]=='X'):
        return 10
      elif (state[i]=='O'):
        return -10

  #check diagonal win
  if (state[0] == state[4] == state[8]) :
    if (state[0]=='X'):
        return 10
    elif (state[0]=='O'):
        return -10
  if (state[2] == state[4] == state[6]):
    if ( state[2]=='X'):
        return 10
    elif (state[2]=='O'):
        return -10

  # Check if it is a draw
  if len(getEmptySpaces(state)) == 0:
    return 0

  return -1

def GetMove(board,player=None):
  if player:
    board=''.join(board)
    if board not in player.matchboxes:
      new_beads = [index for index, value in enumerate(board) if value == ' ']
      player.matchboxes[board] = new_beads * ((len(new_beads) + 2) // 2)
    
    beads = player.matchboxes[board]
    if len(beads):
      bead = random.choice(beads)
      player.moves_played.append((board, bead))
    else:
      bead = -1
    return bead
  else :
    while True:
      move=int(input("Enter your move : "))
      if ValidMove(board,move):
        return move
      else:
        print("Invalid Input")

def SetMenaceData(player,result):
  if result == "win" :
    for (board, bead) in player.moves_played:
      player.matchboxes[board].extend([bead, bead, bead])
    player.num_win += 1
  elif result == "lose" :
    for (board, bead) in player.moves_played:
      matchbox = player.matchboxes[board]
      del matchbox[matchbox.index(bead)]
    player.num_lose += 1
  elif result == "draw" :
    for (board, bead) in player.moves_played:
      player.matchboxes[board].append(bead)
    player.num_draw += 1

  player.save()

def TrainMenace(player1,player2):
  for i in range(0,1000):
    player1.moves_played=[]
    player2.moves_played=[]
    board=np.array([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
    while isGameOver(board) == -1 : 
      move=GetMove(board,player1)
      board[move]="O"
      move=GetMove(board,player2)
      board[move]="X"
    points=isGameOver(board)
    if points == 10:
      SetMenaceData(firstPlayer,"win")
    elif points == -10:
      SetMenaceData(firstPlayer,"lose")
    elif points == 0:
      SetMenaceData(firstPlayer,"draw")

firstPlayer=MenacePlayer()

try :
  f=open('train.json')
  content=f.read()
  if len(content) > 0:
    savedData=json.load(open('train.json'))
    firstPlayer.matchboxes=savedData["matchboxes"]
    firstPlayer.num_win=savedData["num_win"]
    firstPlayer.num_lose=savedData["num_lose"]
    firstPlayer.num_draw=savedData["num_draw"]
  else:
      raise Exception("")
except:
  # train data for 1000 values here
  print("No Pre Game exist")
  print("Please wait till we train")
  secondPlayer=MenacePlayer()
  TrainMenace(firstPlayer,secondPlayer)

board=np.array([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
printBoard(board)

choice = input("Would you like to go first? (Y/N)")
firstPlayer.moves_played=[]
if choice.lower() == 'y' or choice.lower()=='yes':
  print("You are O")
  printBoard(board)
  while isGameOver(board) == -1 : 
    move=GetMove(board)
    board[move]="O"
    printBoard(board)
    if isGameOver(board) != -1:
      break
    move=GetMove(board,firstPlayer)
    board[move]="X"
    printBoard(board)
    print("\nMENACE moved : ",move)
  # if you win -10 is returned
  # if you lose 10 is returned
  # if it is a draw 0 is returned
  points=isGameOver(board)
  if points == 10:
    SetMenaceData(firstPlayer,"win")
    print("Better luck next time! You have lost")
  elif points == -10:
    SetMenaceData(firstPlayer,"lose")
    print("congratulation! You have won")    
  elif points == 0:
    SetMenaceData(firstPlayer,"draw")
    print("That's draw!")
else : 
  print("You are X")
  printBoard(board)
  while isGameOver(board) == -1 : 
    move=GetMove(board,firstPlayer)
    board[move]="O"
    printBoard(board)
    print("\nMENACE moved : ",move)
    if isGameOver(board) != -1:
      break
    move=GetMove(board)
    board[move]="X"
    printBoard(board)
  
  # if you win 10 is returned
  # if you lose -10 is returned
  # if it is a draw 0 is returned
  points=isGameOver(board)
  if points == -10:
    SetMenaceData(firstPlayer,"win")
    print("Better luck next time! You have lost")          
  elif points == 10:
    SetMenaceData(firstPlayer,"lose")
    print("congratulation! You have won")  
  elif points == 0:
    SetMenaceData(firstPlayer,"draw")
    print("That's draw!")