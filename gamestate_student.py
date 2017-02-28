import sys, time, random, copy
from settings import *

class GameState:

    # Initializer for the Connect4 GameState
    # Board is initialized to size width*height
    def __init__(self, rows, cols):
        self.__rows  = rows         # number of rows in the board
        self.__cols = cols          # number of columns in the board
        self.__pieces = [0]*cols    # __pieces[c] = number of pieces in a column c
        self.__player = 0           # the current player to move, 0 = Player One, 1 = Player Two
        self.__board   = [[PLAYER_NONE]*cols for r in range(rows)]
        self.__last_move = 0

    # some getter functions that you probably won't need to modify
    def get_last_move(self):    return self.__last_move
    def get(self, r, c):        return self.__board[r][c]   # piece type located at (r,c)
    def cols(self):             return self.__cols          # number of columns in board
    def rows(self):             return self.__rows          # number of rows in board
    def pieces(self, col):      return self.__pieces[col]   # number of pieces in a given column
    def total_pieces(self):     return sum(self.__pieces)   # total pieces on the board
    def player_to_move(self):   return self.__player        # the player to move next

    # a move (placing a piece into a given column) is legal if the column isn't full
    def is_legal(self, move):   return move >= 0 and move < self.cols() and self.__pieces[move] < self.rows()

    # returns a list of legal moves at this state (which columns aren't full yet)
    def get_legal_moves(self):  return [i for i in range(self.cols()) if self.is_legal(i)]

        
    # performs the given move, putting the piece into the appropriate column and swapping the player
    def do_move(self, move):
        if not self.is_legal(move):
            print("DOING ILLEGAL MOVE")
            sys.exit()
        self.__board[self.pieces(move)][move] = self.player_to_move()
        self.__pieces[move] += 1
        self.__last_move = move
        self.__player = (self.__player + 1) % 2

    # undo a give move, reset the board values and number of pieces in a columns and swapping the player
    def undo_move(self, move):
        self.__board[self.pieces(move)-1][move] = PLAYER_NONE
        self.__pieces[move]= self.pieces(move) - 1
        self.__player = (self.__player + 1) % 2

    # Student TODO: Implement
    #
    #   Calculates a heuristic evaluation for the current GameState from the P.O.V. of the player to move
    #
    #   Args:
    #
    #     player (int) - The player whose POV the evaluation is from.
    #
    #   Returns:
    #
    #     value  (int) - A heuristic evaluation of the current GameState. Positive value should indicate
    #                    that the input player is winning, negative value that they are losing.
    #
    #     return values:
    #     Large positive value  = Player is winning the game (infinity if player has won)
    #     Larger negative value = Opponent is winning the game (-infinity if player has lost)
    #                             Infinity = Some large integer > non-win evaluations


    #     return values base on number ofs available four's slot for current player
    def eval(self, player):
        val = 0
        if(self.winner() == player):
            val = 1000000 - self.total_pieces()
            return val
        if(self.winner() == (player + 1)%2):
            val = -1000000
            return val
        #check available slots for current to place four pieces
        # if there are add 10 to the values
         
        for i in range(self.rows()):
            for j in range(self.cols()):
                count = 0
                for k in range(4):
                    if self.is_illegal(i, j, 0, k):
                        break
                    if (self.get(i,j+k) == player) or (self.get(i,j+k) == PLAYER_NONE):
                        count = count + 1
                    else: break
                if count == 4:
                    val = val + 10
                count = 0
                for k in range(4):
                    if self.is_illegal(i, j, k, 0):
                        break
                    if (self.get(i+k,j) == player) or (self.get(i+k,j) == PLAYER_NONE):
                        count = count + 1
                    else: break
                if count == 4:
                    val = val + 10
                count = 0
                for k in range(4):
                    if self.is_illegal(i, j, k, k):
                        break
                    if (self.get(i+k,j+k) == player) or (self.get(i+k,j+k) == PLAYER_NONE):
                        count = count + 1
                    else: break
                if count == 4:
                    val = val + 10
                count = 0
                for k in range(4):
                    if self.is_illegal(i, j, -k, k):
                        break
                    if (self.get(i-k,j+k) == player) or (self.get(i-k,j+k) == PLAYER_NONE):
                        count = count + 1
                    else: break
                if count == 4:
                    val = val + 10
        #check if opponent's pieces block the slots
        # then subtract 20 from the total value
        for i in range(self.rows()):
            for j in range(self.cols()):
                count = 0
                for k in range(4):
                    if self.is_illegal(i, j, 0, k):
                        break
                    if (self.get(i,j+k) == (player + 1)%2) or (self.get(i,j+k) == PLAYER_NONE):
                        count = count + 1
                    else: break
                if count == 4:
                    val = val - 20
                count = 0
                for k in range(4):
                    if self.is_illegal(i, j, k, 0):
                        break
                    if (self.get(i+k,j) == (player + 1)%2) or (self.get(i+k,j) == PLAYER_NONE):
                        count = count + 1
                    else: break
                if count == 4:
                    val = val - 20
                count = 0
                for k in range(4):
                    if self.is_illegal(i, j, k, k):
                        break
                    if (self.get(i+k,j+k) == (player + 1)%2) or (self.get(i+k,j+k) == PLAYER_NONE):
                        count = count + 1
                    else: break
                if count == 4:
                    val = val - 20
                count = 0
                for k in range(4):
                    if self.is_illegal(i, j, -k, k):
                        break
                    if (self.get(i-k,j+k) == (player + 1)%2) or (self.get(i-k,j+k) == PLAYER_NONE):
                        count = count + 1
                    else: break
                if count == 4:
                    val = val - 20
        return val
    # Student TODO: Implement
    # You will probably want to implement this function first and make sure it is working before anything else
    #
    #   Calculates whether or not there is a winner on the current board and returns one of the following values
    #
    #   Return PLAYER_ONE  (0) - Player One has won the game
    #   Return PLAYER_TWO  (1) - Player Two has won the game
    #   Return PLAYER_NONE (2) - There is no winner yet and the board isn't full
    #   Return DRAW        (3) - There is no winner and the board is full
    #
    #   A Player has won a connect 4 game if they have 4 pieces placed in a straight line or on a diagonal
    #   REMEMBER: The board rows and columns can be any size, make sure your checks acccount for this
    #   NOTE: Create 4 seprate loops to check win formations: horizontal, vertical, diagonal up, diagonal down
    #         Be sure to test this function extensively, if you don't detect wins correctly it will be bad
    #         Also, be sure not to check past the bounds of the board, any duplicate win checks will just
    #         end up wasting precious CPU cycles and your program will perform much worse.
    #
    def is_illegal (self, row, col, redRow, redCol ):
        if row + redRow < 0 or row + redRow >= self.rows():
            return True
        if self.get(row,col) == 2 :
            return True
        if col + redCol >= self.cols() or col + redCol < 0:
            return True
        return False

    def winner(self):
        #Player winning
        #vertical check
        vcount = 0
        originalRow = self.pieces(self.get_last_move()) -1
        for i in range(4):
            if self.is_illegal(originalRow, self.get_last_move(), -i, 0):
                break
            if self.get(originalRow,self.get_last_move()) == self.get( originalRow - i,self.get_last_move() ):
                vcount = vcount + 1
            else:
                break
        if vcount >= 4:
            return self.get(originalRow,self.get_last_move())

        #diagonalUp check
        vcount = 0
        for i in range(4):
            if self.is_illegal(originalRow, self.get_last_move(), -i, -i):
                break
            if self.get(originalRow,self.get_last_move()) == self.get(originalRow - i,self.get_last_move()-i):
                vcount = vcount + 1
            else:
                break

        if vcount >= 4:
            return self.get(originalRow,self.get_last_move())

        for i in range(1,4):
            if self.is_illegal(originalRow, self.get_last_move(), i, i):
                break
            if self.get(originalRow,self.get_last_move()) == self.get(originalRow + i,self.get_last_move() +i):
                vcount = vcount + 1
            else:
                break

        if vcount >= 4:
            return self.get(originalRow,self.get_last_move())

        #diagonal down check
        vcount = 0
        for i in range(4):
            if self.is_illegal(originalRow, self.get_last_move(), i, -i):
                break
            if self.get(originalRow,self.get_last_move()) == self.get(originalRow + i, self.get_last_move() -i):
                vcount = vcount + 1
            else:
                break
        if vcount >= 4:
            return self.get(originalRow,self.get_last_move())

        for i in range(1,4):
            if self.is_illegal(originalRow, self.get_last_move(), -i, i):
                break
            if self.get(originalRow,self.get_last_move()) == self.get(originalRow - i,self.get_last_move() +i):
                vcount = vcount + 1
            else:
                break
        if vcount >= 4:
            return self.get(originalRow,self.get_last_move())

        #horizontal check

        vcount = 0
        for i in range(4):
            if self.is_illegal(originalRow, self.get_last_move(), 0, -i):
                break
            if self.get(originalRow,self.get_last_move()) == self.get(originalRow, self.get_last_move() -i):
                vcount = vcount + 1
            else:
                break
        if vcount >= 4:
            return self.get(originalRow,self.get_last_move())

        for i in range(1,4):
            if self.is_illegal(originalRow, self.get_last_move(), 0, i):
                break
            if self.get(originalRow,self.get_last_move()) == self.get(originalRow,self.get_last_move() +i):
                vcount = vcount + 1
            else:
                break
        if vcount >= 4:
            return self.get(originalRow,self.get_last_move())

        #DRAW
        if self.total_pieces() == self.rows()*self.cols():
            return DRAW
        #NO WINNING STATE
        return PLAYER_NONE





# Student TODO: Implement this class
class Player_AlphaBeta:

    # Constructor for the Player_AlphaBeta class
    #
    # Ideally, this object should be constructed once per player, and then the get_move function will be
    # called once per turn to get the move the AI should do for a given state
    #
    # Args:
    #
    #  depth      (int) - Max depth for the AB search. If 0, no limit is used for depth
    #  time_limit (int) - Time limit (in ms) for the AB search. If 0, no limit is used for time
    #
    #  NOTE: One or both of depth or time_limit must be set to a value > 0
    #        If both are > 0, then whichever happens first will terminate the AB search
    #
    def __init__(self, max_depth, time_limit):
        self.max_depth = max_depth      # set the max depth of search
        self.time_limit = time_limit    # set the time limit (in milliseconds)
        self.best_move = -1             # record the best move found so far
        # self.current_best_move = -1
        self.arrayVals =[]

        # Add more class variables here as necessary (you will probably need more)

    def reset(self):
        self.current_best_move = -1
        self.best_move = -1
        self.arrrayVals = []

    # Student TODO: Implement this function
    #
    # This function calculates the move to be perfomed by the AI at a given state
    # This function will (ideally) call your alpha_beta recursive function from the the root node
    #
    # Args:
    #
    #   state (GameState) - The current state of the Connect4 game, with the AI next to move
    #
    # Returns:
    #
    #   move (int)        - The move the AI should do at this state. The move integer corresponds to
    #                       which column to place the next piece into (0 is the left-most column)
    #
    # NOTE: Make sure to remember the current player to move, as this is the player you are calculating
    # a move for, and will act as the maximizing player throughout your AB recusive calls
    #
    def get_move(self, state1):
        state = copy.deepcopy(state1)
        # store the time that we started calculating this move, so we can tell how much time has passed
        self.time_start = time.clock()
        # store the player that we're deciding a move for and set it as a class variable
        self.player = state.player_to_move()
        self.reset()
        # do your alpha beta (or ID-AB) search here
        self.IDAB(state)
        return self.best_move
    #check if the alpha beta search excess the maximum depth
    def is_terminal(self, state, depth):
        if self.max_depth > 0 and depth >= self.max_depth:
            return True
        return state.winner() != PLAYER_NONE
    #check if the searching time excess time limit
    def is_timeout(self,time_elapsed_ms):
        if self.time_limit == 0: return False
        if self.time_start >= 0 and time_elapsed_ms > self.time_limit: return True

    #interative deeping alpha beta funcion
    def IDAB(self, state):
        if self.max_depth != 0: max_d = self.max_depth
        else: max_d = 100
        alpha = -10000000 
        beta = 10000000
        player = True
        for i in range(1,max_d+1):
            try:
                self.max_depth = i   
                self.best_move_val = self.alpha_beta(state, 0, alpha, beta, player)
                self.best_move = self.current_best_move
            except TimeoutException as err:
                break
        return self.best_move

    # Student TODO: You might have a function like this... wink wink
    #
    # NOTE: Get Alpha-Beta with fixed search depth working first, then move to ID-AB. You should
    #       be able to use this alpha-beta function within your ID-AB calls.
    #
    def alpha_beta(self, state, depth, alpha, beta, max_player):
        self.time_elapsed_ms = (time.clock() - self.time_start)*1000
        #raise timeout Exception
        if self.is_timeout(self.time_elapsed_ms):raise TimeoutException()
        #return the a value base on the heuristic evaluation
        if self.is_terminal(state, depth):return state.eval(self.player)

        for m in state.get_legal_moves():
            state.do_move(m)
            val = self.alpha_beta(state, depth + 1, alpha, beta, not max_player)
            state.undo_move(m)
            if depth == 0:
                self.arrrayVals.append((val,m,state.total_pieces()))
            if (max_player and val > alpha):
                if depth == 0:
                    self.current_best_move = m
                alpha = val
            elif(not max_player and val < beta): beta = val
            if alpha >= beta: break

        return alpha if max_player else beta
#custom exception for timeout so the program won't catch other excpetion
class TimeoutException(Exception):
    def __init__(self):
        Exception.__init__(self) 
