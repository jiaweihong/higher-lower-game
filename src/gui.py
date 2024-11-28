import customtkinter as ctk
from game import HigherLowerGame, Card, Rank, Constant, Deck
from game import Constant as GameConstant
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
        self.geometry("600x600")

        self.menuFrame = MenuFrame(self)
        self.gameFrame = GameFrame(self)
        self.endFrame = EndFrame(self)

        self.currentFrame: ctk.CTkFrame = self.menuFrame
        
        # Show menu frame initially
        self.showFrame(self.menuFrame)
    
    def showFrame(self, frameToShow: ctk.CTkFrame):
        if self.currentFrame == self.menuFrame or self.currentFrame == self.endFrame:
            self.currentFrame.pack_forget() 
        elif self.currentFrame == self.gameFrame: 
            self.currentFrame.grid_forget() 

        if frameToShow == self.menuFrame or frameToShow == self.endFrame:
            frameToShow.pack(expand=True, fill="both")  
        elif frameToShow == self.gameFrame: 
            frameToShow.grid()  
        
        if hasattr(frameToShow, "updateUi"):
            frameToShow.updateUi()

        self.currentFrame = frameToShow

class GameFrame(ctk.CTkFrame):
    def __init__(self, master: HigherLowerApp):
        super().__init__(master)
        self.master: HigherLowerApp = master
        self.game: HigherLowerGame = self.master.game

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
    
        # Info Frame
        self.infoFrame = ctk.CTkFrame(self)
        self.infoFrame.grid(
            row=0, 
            column=0, 
            columnspan=2, 
            pady=20, 
            sticky="nsew"
        )

        self.numCardsRemainingLabel = ctk.CTkLabel(
            self.infoFrame, 
            text=None, 
            font=("Arial", 16)
        )
        self.numCardsRemainingLabel.pack()

        self.scoreLabel = ctk.CTkLabel(
            self.infoFrame, 
            text=f"Score: {self.game.score}", 
            font=("Arial", 16)
        )
        self.scoreLabel.pack()

        self.rodmanCountLabel = ctk.CTkLabel(
            self.infoFrame, 
            text=None, 
            font=("Arial", 16)
        )
        self.rodmanCountLabel.pack()

        self.mjRoundLabel = ctk.CTkLabel(
            self.infoFrame, 
            text=None, 
            font=("Arial", 16)
        )
        self.mjRoundLabel.pack()

        # Deck and Current Card Frame
        self.currentCardFrame = ctk.CTkFrame(self)
        self.currentCardFrame.grid(
            row=1, 
            column=0, 
            padx=20, 
            ipadx=20
        )

        self.deckFrame = ctk.CTkFrame(self)
        self.deckFrame.grid(
            row=1, 
            column=1, 
            padx=20, 
            ipadx=20
        )

        self.deckLabel = ctk.CTkLabel(
            self.deckFrame, 
            text="Deck", 
            compound="bottom", 
            font=("Arial", 20)
        )
        self.deckLabel.pack(pady=20) 

        self.currentCardLabel = ctk.CTkLabel(
            self.currentCardFrame, 
            text="Current Card", 
            compound="bottom", 
            font=("Arial", 20)
        )
        self.currentCardLabel.pack(pady=20) 

        # Buttons Frame
        self.btnFrame = ctk.CTkFrame(self)
        self.btnFrame.grid(
            row=2, 
            column=0, 
            columnspan=2, 
            pady=10, 
            sticky="nsew"
        )

        self.higherBtn = ctk.CTkButton(
            self.btnFrame, 
            text="Higher", 
            command=self.onHigherBtnClick
        )
        self.higherBtn.pack(side="left", padx=20)

        self.lowerBtn = ctk.CTkButton(
            self.btnFrame, 
            text="Lower", 
            command=self.onLowerBtnClick
        )
        self.lowerBtn.pack(side="right", padx=20)

    def showSpecialCardPopup(self, card: Card): 
        popup = ctk.CTkToplevel(self)
        popup.title("Special Card Received")
        popup.geometry("500x450")

        desc = ""
        if card.rank == Rank.MJ:
            desc = f"You have received the special {card.getName()} card.\n\n Guess the next 8 cards in the following sequence (R, R, R, W, W, R, R, R) corresponding to the Bulls Winning Sequence from 1991-98, where R means you correctly guessed it and W means you 'wrongly' guessed it, to win 10 bonus points"
        elif card.rank == Rank.RODMAN:
            desc = f"You have received the special {card.getName()} card.\n\n On the next card you get wrong, it will be rebounded by Rodman, giving you a 2nd chance to win double points!"

        descLabel = ctk.CTkLabel(
            popup,
            text=desc,
            wraplength=400,
            font=("Arial", 14),
        )
        descLabel.pack(pady=10) 

        cardLabel = ctk.CTkLabel(
            popup,
            image=self.getImage(card)
        )
        cardLabel.pack(pady=20) 

        # Button to close the popup
        closeBtn = ctk.CTkButton(
            popup, 
            text="Close", 
            command=popup.destroy
        )
        closeBtn.pack(pady=10)
        
        # Freeze main window until the popup is closed
        popup.grab_set()
        self.master.wait_window(popup)
    
    def onHigherBtnClick(self):
        nextCard: Card = self.game.deck.seeTopCard()

        if self.game.isNextCardMj(nextCard):
            self.showSpecialCardPopup(nextCard)
        elif self.game.isNextCardRodman(nextCard):
            self.showSpecialCardPopup(nextCard)

        isPlayNextRound: bool = self.game.playRound(isUserInputHigher=False)

        if isPlayNextRound:
            self.updateUi()
        else:
            self.master.showFrame(self.master.endFrame)
            
    def onLowerBtnClick(self):
        nextCard: Card = self.game.deck.seeTopCard()
        if self.game.isNextCardMj(nextCard):
            self.showSpecialCardPopup(nextCard)
        elif self.game.isNextCardRodman(nextCard):
            self.showSpecialCardPopup(nextCard)

        isPlayNextRound: bool = self.game.playRound(isUserInputHigher=False)

        if isPlayNextRound:
            self.updateUi()
        else:
            self.master.showFrame(self.master.endFrame)

    def updateUi(self):
        self.currentCardLabel.configure(image=self.getImage(self.game.currentCard))
        self.scoreLabel.configure(text=f"Score: {self.game.score}")
        self.deckLabel.configure(image=self.getImage(self.master.game.deck.seeTopCard()) if self.master.menuFrame.isIsdpOn.get() else self.getBackOfCard())

        rodmanText = f"Available Rodman Cards: {self.master.game.currentRodmanCards}" if self.game.isBullsEdition else f"Available Rodman Cards: N/A"
        self.rodmanCountLabel.configure(text=rodmanText)

        mjText = f"Current MJ Round: {self.game.currentMjRound}/{len(GameConstant.MJ_WINNING_SEQUENCE.value)}" if self.game.isBullsEdition and self.game.isMjActivated else f"Current MJ Round: N/A"
        self.mjRoundLabel.configure(text=mjText)
        self.numCardsRemainingLabel.configure(text=f"Normal Cards Remaining: {self.game.getNumRemainingNormalCards()}")

    
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

        self.menuTitleLabel = ctk.CTkLabel(
            self, 
            text="Higher Lower Game (Chicago Bulls Edition)", 
            font=("Arial", 24, "bold")
        )
        self.menuTitleLabel.pack(pady=20)

        self.rulesLabel = ctk.CTkLabel(
            self, 
            text="Game Rules: \n1. Rule one description.\n2. Rule two description.\n3. Rule three description.", 
            justify="left", 
            font=("Arial", 14)
        )
        self.rulesLabel.pack(pady=10)
        
        self.isBullsEditionOn = ctk.BooleanVar(value=False)
        self.bullsCheckbox = ctk.CTkCheckBox(
            self, 
            text="Enable Special Edition", 
            variable=self.isBullsEditionOn
        )
        self.bullsCheckbox.pack(pady=10)

        # Isdp == I See Dead People (Warcraft 3 cheat code)
        self.isIsdpOn = ctk.BooleanVar(value=False)
        self.isIsdpCheckbox = ctk.CTkCheckBox(
            self, 
            text="Enable True Sight (preview next card)", 
            variable=self.isIsdpOn
        )
        self.isIsdpCheckbox.pack(pady=10)

        self.startBtn = ctk.CTkButton(
            self, 
            text="Start Game", 
            command=self.startGame
        )
        self.startBtn.pack(pady=20)

    def startGame(self):
        self.game.configureSpecialEdition(self.isBullsEditionOn.get())
        self.game.startGame()
        
        self.master.showFrame(self.master.gameFrame)


class EndFrame(ctk.CTkFrame):
    def __init__(self, master: HigherLowerGame):
        super().__init__(master)

        self.master: HigherLowerGame = master 
        self.game: HigherLowerGame = self.master.game

        # Title label
        self.endTitleLabel = ctk.CTkLabel(
            self, 
            text="Game Over! Thank you for playing!", 
            font=("Arial", 24, "bold")
        )
        self.endTitleLabel.pack(pady=20)

        # Final score label
        self.scoreLabel = ctk.CTkLabel(
            self, 
            text=f"Your Final Score: {self.game.score}", 
            font=("Arial", 18)
        )
        self.scoreLabel.pack(pady=10)

        # Close game button
        self.closeBtn = ctk.CTkButton(
            self, 
            text="Close Game", 
            command=self.closeGame
        )

        self.closeBtn.pack(pady=10)

    def closeGame(self):
        self.master.destroy()

    def updateUi(self):
        self.scoreLabel.configure(text=f"Your Final Score: {self.game.score}")

if __name__ == "__main__":
    game = HigherLowerGame()
    app = HigherLowerApp(game)
    app.mainloop()