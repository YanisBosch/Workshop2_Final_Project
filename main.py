import random
import numpy as np

class playfield:
    def __init__(self,size,numbombs,seed):
        self.size = size
        self.numbombs = numbombs
        self.seed = seed
        self.bombs = [[0 for x in range(self.size)] for y in range(self.size)]      #"b" = bomb, number = number of adjacent bombs
        self.playfield = [["h" for x in range(self.size)] for y in range(self.size)]  #"f" = flag, "n" = show number, "h" = hidden

    def __str__(self):
        spaces = len(str(self.size))+1
        res = (spaces)*" "
        for j in range(self.size):
            res += str(j) + (spaces-len(str(j)))*" "
        res += "\n"
        for i in range(self.size):
            res += str(i) + (spaces-len(str(i)))*" "
            for j in range(self.size):
                if self.playfield[i][j] == "f":
                    res += "F" + (spaces-1)* " "
                elif self.playfield[i][j] == "n":
                    res += str(self.bombs[i][j]) + (spaces-1)* " "
                else:
                    res += "X" + (spaces-1)* " "
            res += "\n"
        return(res)

    def place_bombs(self):
        random.seed(self.seed)
        bombs = [[0 for x in range(self.size)] for y in range(self.size)]         #b = bomb, number = number of bombs next to square
        free = [[x,y] for x in range(self.size) for y in range(self.size)]
        for i in range(self.numbombs):
            ind = random.randrange(len(free))
            bomb = free[ind]
            bombs[bomb[0]][bomb[1]] = "b"
            free.remove(bomb)
        self.bombs = bombs
    
    def count_bombs_one(self,i:int,j:int):
        neighbours = [(min([max([i+x,0]),self.size-1]),min([max([j+y,0]),self.size-1])) for x in [-1,0,1] for y in [-1,0,1]]
        neighbours = np.unique(neighbours,axis=0).tolist()
        neighbours.remove([i,j])
        
        return([self.bombs[x[0]][x[1]] for x in neighbours].count("b"))
    
    def count_bombs_all(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.bombs[i][j] != "b":
                    self.bombs[i][j] = self.count_bombs_one(i,j)

    def initialise_game(self):
        self.place_bombs()
        self.count_bombs_all()

    def play_game(self):
        print("After each round please choose first whether to place a flag or check, and then input the row and column number when prompted \n")
        done = False
        while not done:
            while True:
                corf = input("Please select 1 to check for bombs or 2 to place a flag \n")
                if corf == "1" or corf == "2":
                    break
                else:
                    print("Incorrect input, please try again.")
            print()
            while True:
                try:
                    i = int(input("Please input a row number between 0 and " + str(self.size-1) + " \n"))
                    if i >= 0 and i <= self.size-1:
                        break
                    else:
                        print("Number not within specified range, please try again.")
                except:
                    print("Specified input was not an integer, please try again.")
            print()

            while True:
                try:
                    j = int(input("Please input a column number between 0 and " + str(self.size-1) + " \n"))
                    if j >= 0 and j <= self.size-1:
                        break
                    else:
                        print("Number not within specified range, please try again.")
                except:
                    print("Specified input was not an integer, please try again.")
            
            if corf == "1":
                self.playfield[i][j] = "n"
            elif corf == "2":
                self.playfield[i][j] = "f"
            print(self)
        
pf = playfield(15,15,420)
pf.initialise_game()
pf.play_game()


