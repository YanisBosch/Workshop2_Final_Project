import random
import numpy as np

class playfield:
    def __init__(self,size,numbombs,seed):
        self.size = size                    #size of one side of the square arena
        self.numbombs = numbombs            #number of bombs to play with
        self.seed = seed                    #fix seed for repeatability
        self.bombs = [[0 for x in range(self.size)] for y in range(self.size)]          #"b" = bomb, number = number of adjacent bombs
        self.playfield = [["h" for x in range(self.size)] for y in range(self.size)]    #"f" = flag, "n" = show number, "h" = hidden
        self.flagnum = 0                    #to limit total available number of flags

    def __str__(self):
        spaces = len(str(self.size))+1      #variable used for clean printing of the arena
        res = (spaces)*" "                  #fill upper corner of print
        for j in range(self.size):  
            res += str(j) + (spaces-len(str(j)))*" "        #add column numbers
        res += "\n"                     
        for i in range(self.size):
            res += str(i) + (spaces-len(str(i)))*" "        #add row number
            for j in range(self.size):                      #based on the values of playfield we print the values accordingly
                if self.playfield[i][j] == "f":             #if a flag was placed we show "F"
                    res += "F" + (spaces-1)* " "            
                elif self.playfield[i][j] == "n":           #if spot is uncovered we show the number of neighbour bombs
                    res += str(self.bombs[i][j]) + (spaces-1)* " "
                else:
                    res += "x" + (spaces-1)* " "            #if the spot is not uncovered and not flagged we just show an X
            res += "\n"
        return(res)

    def place_bombs(self):
        random.seed(self.seed)
        bombs = [[0 for x in range(self.size)] for y in range(self.size)]   #b = bomb, number = number of bombs next to square
        free = [[x,y] for x in range(self.size) for y in range(self.size)]  #coordinates where no bombs were placed
        for i in range(self.numbombs):
            ind = random.randrange(len(free))                               #pick random set of coordinates from the free ones
            bomb = free[ind]                                                
            bombs[bomb[0]][bomb[1]] = "b"                                   #at the chosen index place a bomb
            free.remove(bomb)                                               #remove coordinates where bomb was placed from the free array
        self.bombs = bombs
    
    def neighbour_slots(self,i,j):
        neighbours = [(min([max([i+x,0]),self.size-1]),min([max([j+y,0]),self.size-1])) for x in [-1,0,1] for y in [-1,0,1]]
        #list of coordinates of all neighbours of [i,j], where we limit ourselves to values in [0,self.size-1]
        neighbours = np.unique(neighbours,axis=0).tolist()      #remove any duplicates
        neighbours.remove([i,j])                                #remove the point [i,j] as it is not a neighbour of itself
        return(neighbours)

    def count_bombs_one(self,i:int,j:int):
        neighbours = self.neighbour_slots(i,j)
        return([self.bombs[x[0]][x[1]] for x in neighbours].count("b"))     #return number of neighbours = "b"
    
    def count_bombs_all(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.bombs[i][j] != "b":                     #if not a bomb replace the entry in bombs with the number of 
                                                                #neighbouring bombs
                    self.bombs[i][j] = self.count_bombs_one(i,j)

    def initialise_game(self):
        self.place_bombs()
        self.count_bombs_all()

    def update_playfield(self,i,j):
        #print("[" + str(i) + ";" + str(j) + "]")
        if self.playfield[i][j] == "h":
            self.playfield[i][j] = "n"
            if self.bombs[i][j] == 0:
                for ind in self.neighbour_slots(i,j):
                    self.update_playfield(ind[0],ind[1])

    def check_win(self,i,j):
        """i,j = last move, makes computations easier"""
        #STEP 1: CHECK IF ANY BOMBS WERE CLICKED
        if (self.bombs[i][j] == "b") and (self.playfield[i][j] == "n"):
            return("lost")
        else:
            winbyflag = True
            winbyuncover = True
            for l in range(self.size):
                for m in range(self.size):
                    if (self.bombs[l][m] == "b" and self.playfield[l][m] != "f"):
                        winbyflag = False
                    if (self.bombs[l][m] != "b" and self.playfield[l][m] != "n"):
                        winbyuncover = False
            if winbyflag or winbyuncover:
                return("win")
            else:
                return("continue")

    def play_game(self):
        spaces = len(str(self.size))+1
        print("After each round please choose first whether to place a flag or check, and then input the row and column number when prompted. \nType exit at any time to exit the game.")
        print("You will win if you place a flag on each bomb, or discover all spots without bombs. You can place at most " +str(self.numbombs) + " flags.")
        print("There are " + str(self.numbombs) + " bombs to be found.")
        done = False
        while not done:

            #INPUT TO KNOW WHETHER TO CHECK FOR BOMBS OR PLACE FLAG

            while True:
                corf = input("Please select 1 to check for bombs or 2 to place a flag \n")
                if corf == "1" or corf == "2":      #if input is correct we keep on going
                    break
                elif corf == "exit":                #we add a break if the player wants to stop, and set done to True to finish loop
                    done = True
                    break
                else:
                    print("Incorrect input, please try again.")     #Else prompt player to retry and go through loop again

            print("\n" + "-"*(spaces*(self.size+1)-1) + "\n")              #For readability
            
            if corf == "exit":                      #break again to exit second loop
                break

            #--------------

            #INPUT TO KNOW WHICH ROW TO CHECK

            while True:
                try:
                    i = input("Please input a row number between 0 and " + str(self.size-1) + " \n")
                    if i == "exit":             
                        done = True                 #we add a break if the player wants to stop, and set done to True to finish loop
                        break
                    else:
                        i = int(i)                      #tries to convert i to integer
                    if i >= 0 and i <= self.size-1:     #if i is also in the right range we break and keep on going
                        break
                    else:
                        print("Number not within specified range, please try again.")       #else prompt to retry
                except:
                    print("Specified input was not an integer, please try again.")          #else prompt to retry

            if i == "exit":                             #break again to exit second loop
                break

            #--------------

            #INPUT TO KNOW WHICH COLUMN TO CHECK

            print("\n" + "-"*(spaces*(self.size+1)-1) + "\n")

            while True:
                try:
                    j = input("Please input a column number between 0 and " + str(self.size-1) + " \n")
                    if j == "exit":                     #we add a break if the player wants to stop, and set done to True to finish loop
                        done = True
                        break
                    else:
                        j = int(j)                      #tries to convert j to integer
                    if j >= 0 and j <= self.size-1:     #if j is also in the right range we break and keep on going
                        break
                    else:
                        print("Number not within specified range, please try again.")        #else prompt to retry
                except:
                    print("Specified input was not an integer, please try again.")           #else prompt to retry

            if j == "exit":                             #break again to exit second loop
                break

            #--------------

            #UPDATE GAME STATUS ACCORDINGLY

            if corf == "1":

                self.update_playfield(i,j)
            elif corf == "2":
                if self.playfield[i][j] == "f":             #if there is already a flag remove it
                    self.playfield[i][j] = "n"
                    self.flagnum -= 1                       #update flag number counter
                elif self.playfield[i][j] != "n":           #else if there is no number there place a flag
                    if self.flagnum < self.numbombs:        #if there are not too many flags place one
                        self.playfield[i][j] = "f"  
                        self.flagnum += 1                   #update flag number counter
                    else:
                        print("You cannot place any more flags.")

            res = self.check_win(i,j)

            #--------------

            #PRINT GAME STATUS FOR PLAYER TO SEE

            print("\n" + "-"*(spaces*(self.size+1)-1) + "\n")
            print(self)
            print("-"*(spaces*(self.size+1)-1) + "\n")

            #--------------

            if res == "win":
                print("CONGRATS, YOU WON!")
                done = True
            elif res == "lost":
                print("SORRY, YOU LOST:(")
                done = True

        print("THANK YOU FOR PLAYING!")

print(np.version.version)

def main(size,numbombs,seed):
    size = max([min([50,size]),1])
    numbombs = max([numbombs,1])
    pf = playfield(size,numbombs,seed)
    pf.initialise_game()
    pf.play_game()

main(15,15,420)