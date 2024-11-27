import customtkinter as ctk
from game import HigherLowerGame, Deck, Card
from PIL import Image, ImageTk
from enum import Enum


class Constant(Enum):
    CARD_SIZE = (150,218)

class HigherLowerApp(ctk.CTk):
    def __init__(self, game: HigherLowerGame):
        super().__init__()
        self.game: HigherLowerGame = game

        ctk.set_appearance_mode("dark")

        # Configure rows and columns for centering frames
        self.grid_rowconfigure(0, weight=1)  
        self.grid_columnconfigure(0, weight=1)

        self.title("App")
        self.geometry("900x500")

        self.menuFrame: MenuFrame = MenuFrame(self)
        self.gameFrame: GameFrame = GameFrame(self)
        self.currentFrame: ctk.CTkFrame = self.menuFrame
        
        # Show menu frame initially
        self.showFrame(self.menuFrame)
    
    def showFrame(self, frameToShow: ctk.CTkFrame):
        if self.currentFrame == self.menuFrame:
            self.currentFrame.pack_forget() 
        elif self.currentFrame == self.gameFrame: 
            self.currentFrame.grid_forget() 

        if frameToShow == self.menuFrame:
            frameToShow.pack(expand=True, fill="both")  
        elif frameToShow == self.gameFrame: 
            frameToShow.grid()  
        
        self.currentFrame = frameToShow

class GameFrame(ctk.CTkFrame):
    def __init__(self, master: HigherLowerApp):
        super().__init__(master)
        self.master: HigherLowerApp = master
        self.game: HigherLowerGame = self.master.game

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
    
        self.deckFrame = ctk.CTkFrame(self)
        self.deckFrame.grid(row=0, column=0, padx=20, ipadx=20)

        self.currentCardFrame = ctk.CTkFrame(self)
        self.currentCardFrame.grid(row=0, column=1, padx=20, ipadx=20)

        # Create labels
        self.deckLabel = ctk.CTkLabel(self.deckFrame, text="Deck", compound="top", font=("Arial", 14))
        self.deckLabel.pack(pady=20) 

        self.currentCardLabel = ctk.CTkLabel(self.currentCardFrame, text="Current Card", compound="top", font=("Arial", 14))
        self.currentCardLabel.pack(pady=20) 

        # Higher and Lower Buttons
        self.btnFrame = ctk.CTkFrame(self)
        self.btnFrame.grid(row=1, column=0, columnspan=2, pady=10, sticky="nsew")

        self.higherBtn = ctk.CTkButton(self.btnFrame, text="Higher", command=self.onHigherBtnClick)
        self.higherBtn.pack(side="left", padx=20)

        self.lowerBtn = ctk.CTkButton(self.btnFrame, text="Lower", command=self.onLowerBtnClick)
        self.lowerBtn.pack(side="right", padx=20)

        # Score Label
        self.scoreFrame = ctk.CTkFrame(self)
        self.scoreFrame.grid(row=2, column=0, columnspan=2, pady=20, sticky="nsew")

        self.scoreLabel = ctk.CTkLabel(self.scoreFrame, text=f"Score: {self.game.score}", font=("Arial", 16))
        self.scoreLabel.pack()

    def showSpecialCardPopup(self, card: Card):
        print()
        print("POPUP HERE")
        print()
        popup = ctk.CTkToplevel(self)
        popup.title("Special Card Received")
        popup.geometry("300x150")

        # Add a label to display the message
        specialCard = ctk.CTkLabel(
            popup, 
            text="You have received a special card!", 
            font=("Arial", 16),
            image=self.getImage(card)
        )
        specialCard.pack(expand=True)

        # Button to close the popup
        close_button = ctk.CTkButton(
            popup, 
            text="Close", 
            command=popup.destroy
        )
        close_button.pack(pady=10)
    
    def onHigherBtnClick(self):
        self.game.playRound(isUserInputHigher=True)
        self.updateUi()
            
    def onLowerBtnClick(self):
        self.game.playRound(isUserInputHigher=False)
        self.updateUi()

    def updateUi(self):
        self.currentCardLabel.configure(image=self.getImage(self.game.currentCard))
        self.scoreLabel.configure(text=f"Score: {self.game.score}")
        self.deckLabel.configure(image=self.getImage(self.master.game.deck.seeTopCard()) if self.master.menuFrame.isIsdpOn else self.getBackOfCard())
    
    def getImage(self, card: Card) -> ImageTk.PhotoImage:
        """
        Returns the corresponding (according to attributes) and resized image of the card
        """
        # possibly change the way you are getting the file path
        originalImg = Image.open(f"images/{card.getName()}.png")
        resizedImg = originalImg.resize(Constant.CARD_SIZE.value)
        newImg = ImageTk.PhotoImage(resizedImg)
        return newImg
    
    def getBackOfCard(self) -> ImageTk.PhotoImage:
        """
        Returns the back image of a card
        """
        # possibly change the way you are getting the file path
        originalImg = Image.open(f"images/back_of_card.png")
        resizedImg = originalImg.resize(Constant.CARD_SIZE.value)
        newImg = ImageTk.PhotoImage(resizedImg)
        return newImg
    
class MenuFrame(ctk.CTkFrame):
    def __init__(self, master: HigherLowerApp):
        super().__init__(master)
        self.master: HigherLowerApp = master
        self.game: HigherLowerGame = self.master.game

        self.menuTitleLabel = ctk.CTkLabel(self, text="Higher Lower Game (Chicago Bulls Edition)", font=("Arial", 24, "bold"))
        self.menuTitleLabel.pack(pady=20)

        self.rulesLabel = ctk.CTkLabel(self, text="Game Rules: \n1. Rule one description.\n2. Rule two description.\n3. Rule three description.", justify="left", font=("Arial", 14))
        self.rulesLabel.pack(pady=10)
        
        self.isBullsEditionOn = ctk.BooleanVar(value=False)
        self.bullsCheckbox = ctk.CTkCheckBox(self, text="Enable Special Edition", variable=self.isBullsEditionOn)
        self.bullsCheckbox.pack(pady=10)

        # Isdp == I See Dead People (Warcraft 3 cheat code)
        self.isIsdpOn = ctk.BooleanVar(value=False)
        self.isIsdpCheckbox = ctk.CTkCheckBox(self, text="Enable True Sight (preview next card)", variable=self.isIsdpOn)
        self.isIsdpCheckbox.pack(pady=10)

        self.startBtn = ctk.CTkButton(self, text="Start Game", command=self.startGame)
        self.startBtn.pack(pady=20)

    def startGame(self):
        self.game.configureSpecialEdition(self.isBullsEditionOn.get())
        self.master.showFrame(self.master.gameFrame)

        self.game.startGame()
        self.master.gameFrame.updateUi()

class EndGameFrame(ctk.CTkFrame):
    def __init__(self, master, final_score, restart_callback):
        super().__init__(master)

        self.master = master
        self.final_score = final_score  # Store the final score
        self.restart_callback = restart_callback  # Callback for restarting the game

        # Title label
        self.endTitleLabel = ctk.CTkLabel(
            self, text="Game Over!", font=("Arial", 24, "bold")
        )
        self.endTitleLabel.pack(pady=20)

        # Final score label
        self.scoreLabel = ctk.CTkLabel(
            self, 
            text=f"Your Final Score: {self.final_score}", 
            font=("Arial", 18)
        )
        self.scoreLabel.pack(pady=10)

        # Restart button
        self.restartBtn = ctk.CTkButton(
            self, 
            text="Restart Game", 
            command=self.restart_game
        )
        self.restartBtn.pack(pady=10)

if __name__ == "__main__":
    game = HigherLowerGame()
    app = HigherLowerApp(game)
    app.mainloop()