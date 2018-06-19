from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.properties import StringProperty,ObjectProperty,ListProperty,NumericProperty
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from random import choice


class Manager(ScreenManager):
    #th manager that manges the screens
    def __init__(self,**opt):
        super(Manager,self).__init__(**opt)
        Clock.schedule_once(self.switch,10)
    def switch(self,dt):
        self.switch_to(PlayerNumber(),direction="right")
class MyButton(Button):
    # A Subclass of the button class
    value=StringProperty("")
    def __init__(self,**opt):
        super(MyButton,self).__init__(**opt)
class MyLabel(Label):
    #a subclass of the label class
    image=StringProperty("")
    def __init__(self,**opt):
        super(MyLabel,self).__init__(**opt)
class ContinuePopUp(Popup):
    def __init__(self,**opt):
        super(ContinuePopUp,self).__init__(**opt)

class Splash(Screen):
    def __init__(self,**opt):
        super(Splash,self).__init__(**opt)
class Cell(Button):
    #the cells' indices stored as properties
    index=ListProperty([])
    
    def __init__(self,**opt):
        super(Cell,self).__init__(**opt)
        

class PlayerDetail(Screen):
    #the screen for the player to edit their details
    players=StringProperty("")
    entry_layout=ObjectProperty(None)
    label=ObjectProperty(None)
    sec=ObjectProperty(None)
    player1_name=ObjectProperty(None)
    def __init__(self,**opt):
        super(PlayerDetail,self).__init__(**opt)
        self.bind(on_pre_enter=self.player_type)
    def player_type(self,*args):
        #the method dat validates the number of players
        if self.players=="1":
            self.sec.text="CPU"
            self.entry_layout.remove_widget(self.entry_layout.children[1])
            self.entry_layout.add_widget(self.label,1)
        elif self.players=="2":
            self.sec.text="Player 2"
            self.player2_name=TextInput(size_hint=(0.6,1),hint_text="Player 2",multiline=False)
            self.entry_layout.remove_widget(self.entry_layout.children[1])
            self.entry_layout.add_widget(self.player2_name,1)
    def set_name(self,*args):
        #getting the input texts
        #checking if the textinputs are empty then player1 or player2
        #will be used
        if self.player1_name.text=="":
            GameScreen.player1_name="PLAYER 1"
        else:
            GameScreen.player1_name=self.player1_name.text.upper()
        if self.players=="1":
            GameScreen.player2_name="CPU"    
        else:
            if self.player2_name.text=="":
                GameScreen.player2_name="PLAYER 2"
            else:
                GameScreen.player2_name=self.player2_name.text.upper()
            
    
            


class PlayerNumber(Screen):
    #the screen for choosing the number of players
    def __init__(self,**opt):
        super(PlayerNumber,self).__init__(**opt)
    def choose_player_number(self,widget):
        PlayerDetail.players=widget.value
        print(PlayerDetail.players)

        

class GameScreen(Screen):
    #the main game screen
    player1_name=StringProperty("")
    player2_name=StringProperty("")
    draw_text="DRAW"
    player1_value="X"
    player2_value="O"
    color=[0,0,1,1]
    layout=ObjectProperty(None)
    board=ObjectProperty(None)
    player1=ObjectProperty(None)
    player2=ObjectProperty(None)
    draw=ObjectProperty(None)
    player1_score=NumericProperty(0)
    player2_score=NumericProperty(0)
    draw_score=NumericProperty(0)
    round_counter=0
    computer=True
    move={"O":"X","X":"O"}

    board_list=[["","",""],
                ["","",""],
                ["","",""]]
    board_gui=[["","",""],
               ["","",""],
               ["","",""]]
    def __init__(self,**opt):
        super(GameScreen,self).__init__(**opt)
        #binding the screens to different methods
        self.bind(on_enter=self.set_player_name)
        self.bind(on_enter=self.display_board)
        self.bind(on_leave=self.clear_cells)

    def set_player_name(self,*args):
        #setting the name of the players on the game screen with initialised scores i.e. 0
        self.player1.text=self.player1_name+": "+" 0 "
        
        self.player2.text=self.player2_name+": "+" 0 "
        self.draw.text=self.draw_text+": "+" 0 "
    def display_board(self,*args):
        #the event that checks evry seconds if the game has gotten to the end state
        Clock.schedule_interval(self.checkgame,0.1)
        #method that displays the tictactoe board
        #adding buttons to the grid
        for i in range(3):
            for j in range(3):
                #a subclass of the button class
                cell=Cell(index=[i,j],background_down="images/cell_back.jpg",
                          background_normal="images/cell_back.jpg")
                cell.bind(on_press=self.play)
                #adding the button cells to the grid
                self.board.add_widget(cell)
                #adding the buttoncells to the board_gui
                #for individual control of each button
                self.board_gui[i][j]=cell
    def clear_cells(self,*args):
        #removing the cells when leaving
        self.board.clear_widgets()
        #stopping the event that checks if the game is in an end state
        Clock.unschedule(self.checkgame)
        #setting the scores back to 0s
        self.player1_score=0
        self.player2_score=0
        self.draw_score=0

    def play(self,widget):
        #getting the row of the button
        i=widget.index[0]
        #getting the column of the button
        j=widget.index[1]
        if widget.text=="" and not(self.checker(self.board_list)[0]):
           
            widget.text=self.player1_value
            #updating the board_list
            self.board_list[i][j]=self.player1_value

            #checking if numbers of players is 1 or 2
            if PlayerDetail.players=="1":
                #if the number of players is 1 thats when the computer will play
                #and the color of play will always be blue
                Clock.schedule_once(self.computer_play,0.1)
                widget.color=[0,0,1,1]
            elif PlayerDetail.players=="2":
                #changing colors if 2 players blue and green
                widget.color=self.color
                if self.color==[0,0,1,1]: self.color=[0,1,0,1]
                else: self.color=[0,0,1,1]
                #changing values of players
                self.player1_value=self.move[self.player1_value]
                #checking for the state of the game after every play
                self.checkgame()
            #print(self.board_list)

    def computer_play(self,*args):
        #the method for the computer play
        val=self.minimax(self.board_list,self.player2_value)
        #print(val)
        
        #checking if the state is not a winning state b4
        #generating the computer move
        if len(val[1])==2:
            #computer move's row
            i=val[1][0]
            #computer move's column
            j=val[1][1]
            #computer play
            #the computer will play the opposite value of player1's value
            self.board_gui[i][j].text=self.move[self.player1_value]
            self.board_gui[i][j].color=[0,1,0,1]
            self.board_list[i][j]=self.move[self.player1_value]
    def checkgame(self,*args):
        #checking the state of the game
        state=self.checker(self.board_list)

        if state[0]:
            self.round_counter+=1#incrementing the round counter
            print("round_counter",self.round_counter)
            #checking if the winner is the x player
           # #when the game gets to the end state the popup pops up to know if
            #the players wants to continue

           #the function of the round counter is to know whom to score when the players values
           #had changed
            if state[1]==1:
                
                if (self.round_counter%2)!=0:
                    print("player X has won")
                    self.player1_score+=1
                    self.player1.text=self.player1_name +":  "+  str(self.player1_score)
                    #displaying the popup
                    self.popup()
                    
                else:
                    print("player X has won")
                    self.player2_score+=1
                    self.player2.text=self.player2_name+":  "+  str(self.player2_score)
                    #displaying the popup
                    self.popup()
                    
            #checking if the winner is the o player
            elif state[1]==-1:
                
                #checking if the winner of the round is player O
                #it should now check if player1 or player2 is O
                if (self.round_counter%2)!=0:
                    print("player O has won")
                    self.player2_score+=1
                    self.player2.text=self.player2_name+": "+  str(self.player2_score)
                    #displaying the popup
                    self.popup()
                else:
                    print("player O has won")
                    self.player1_score+=1
                    self.player1.text=self.player1_name+": "+  str(self.player1_score)
                    #displaying the popup
                    self.popup()
        else:#checking if none of the cells is empty
            empty_state=True
            for i in self.board_list:
                for j in i:
                    if j=="":
                        empty_state=False
            if empty_state==True:
                #that is none of the cells is empty
                print("draw")
                self.round_counter+=1#incrementing the round counter if draw occurs
                self.draw_score+=1
                self.draw.text=self.draw_text+": "+ str(self.draw_score)
                #displaying the popup
                self.popup()
                
                
        
    def checker(self,game):
        #rowise
        for i in game:
            if len(set(i))==1 and ("" not in i):
                #checking if the winner is X or O 
                if "X" in i: return True,1
                else: return True,-1
        #column wise
        index=0
        for i in range(3):
            column=[]
            for j in range(3):
                column.append(game[j][index])
            if len(set(column))==1 and "" not in column:
                #checking if the winner is X or O
                if "X" in column: return True,1
                else: return True,-1

            index+=1
        #diagonals
        if game[0][0]==game[2][2]==game[1][1] and game[2][2]!="":
            #checking if the winner is X or O
            if "X" in game[2][2]: return True,1
            else: return True,-1
            
        if game[0][2]==game[1][1]==game[2][0] and game[0][2]!="":
            #checking if the winner is X or O
            if "X" in game[0][2]: return True,1
            else: return True,-1
        #not in a win state
        return False,-1
        
    def minimax(self,game,player):
        #method that predicts the next move for the computer
        #checking if all cells are empty i.e that is the computer is playing first
        empty=True#initialising the empty to be true
        for i in game:
            for j in i:
                if j!="":
                    empty=False#if a cell is not empty the should be false
        if empty==True:
            #randomising play if the cells are empty i.e. that is the computer is playing first
            x=choice([0,1,2])
            y=choice([0,1,2])
            if player=="X": return (1,[x,y])
            else: return (-1,[x,y])
        #changing the value of assumed player values
        nextplayer="X" if player== "O" else "O"
        #checking if we are in a winning state
        if self.checker(game)[0]:
            if player is "X": return (-1,[-1],)
            else: return (1,[-1],)
        #if the game is not in a winning state
        #initialisng the variable that stores the result
        results=[]
        #checking for draw
        empty_cells=0
        for i in game:
            for j in i:
                if j=="":
                    empty_cells+=1
        if empty_cells==0:#means no cell is empty
            return (0,[-1])
        
        #getting the indices of the empty cells
        empty_indices=[]
        for i in range(3):
            for j in range(3):
                if game[i][j]=="":
                    empty_indices.append([i,j])
        #optimizing the play on the empty cells
        for i in empty_indices:
            game[i[0]][i[1]]=player
            returned_result,move=self.minimax(game,nextplayer)
            results.append(returned_result)
            game[i[0]][i[1]]=""
        if player=="X":
            #maximising the gain i.e. returning the best play for the computer
            #if playing as X
            maxi=max(results)
            return (maxi,empty_indices[results.index(maxi)])
        else:
            #minimizing the gaini.e. returning the best play for the computer
            #if playing as O
            mini=min(results)
            return (mini,empty_indices[results.index(mini)])
    def reset(self):
        #clearing all the plays
        #counting the number of plays the human made and that of the computer
        self.touches_count=0#human play
        self.non_touches_count=0#computer play
        for i in range(3):
            for j in range(3):
                

                if self.computer==True:#if computer did not play first
                    if self.board_list[i][j]=="X":
                        self.touches_count+=1
                    elif self.board_list[i][j]=="O":
                        self.non_touches_count+=1
                self.board_list[i][j]=""#clearing the board list
                self.board_gui[i][j].text=""#clearing all cells
                    
                
        if self.computer:

            #if the computer did not play first
            self.player2_value=self.move[self.player2_value]
            self.player1_value=self.move[self.player1_value]
            if self.non_touches_count<self.touches_count:
                self.computer_play()
            self.computer=False#hanging the value computer to false
            
        else:#if the computer play first
            self.computer=True
            self.player2_value=self.move[self.player2_value]
            self.player1_value=self.move[self.player1_value]
    def popup(self):
        #asking if user or users wish to continue
        self.add_widget(ContinuePopUp())
        #unscheduling the event that checks the state of the game
        Clock.unschedule(self.checkgame)

class Tictactoe(App):
    #the tictactoe app
    title="Cv TicTacToe"
    
    def build(self):
        self.icon="images/icon.jpg"
        return Manager()


Tictactoe().run()
