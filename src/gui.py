import customtkinter as ctk
from .game import HigherLowerGame, Card, Rank, Constant as GameConstant
from PIL import Image, ImageTk
from enum import Enum
import os


class Settings(Enum):
    CARD_SIZE = (150,218)
    COLOUR_MODE = "dark"
    WINDOW_TITLE = "Card Game"

class HigherLowerApp(ctk.CTk):
    def __init__(self, game: HigherLowerGame):
        super().__init__()
        self.game: HigherLowerGame = game

        ctk.set_appearance_mode(Settings.COLOUR_MODE.value)

        # Configure rows and columns for centering frames
        self.grid_rowconfigure(0, weight=1)  
        self.grid_columnconfigure(0, weight=1)

        self.title(Settings.WINDOW_TITLE.value)

        # initialises all frames
        self.menuFrame = MenuFrame(self)
        self.gameFrame = GameFrame(self)
        self.endFrame = EndFrame(self)

        self.currentFrame: ctk.CTkFrame = self.menuFrame
        
        # Show menu frame initially
        self.showFrame(self.menuFrame)
    
    def showFrame(self, frameToShow: ctk.CTkFrame):
        self.currentFrame.grid_forget() 
        frameToShow.grid(padx=40, pady=50)  
        
        if hasattr(frameToShow, "updateUi"):
            frameToShow.updateUi()

        self.currentFrame = frameToShow

class GameFrame(ctk.CTkFrame):
    def __init__(self, master: HigherLowerApp):
        super().__init__(master)
        self.master: HigherLowerApp = master
        self.game: HigherLowerGame = self.master.game

        self.configure(fg_color="transparent")

        # Info Frame
        # some of these text values are set to None since value is unknown until user decides on which edition to play
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
        )

        self.higherBtn = ctk.CTkButton(
            self.btnFrame, 
            text="Higher", 
            command=self.onHigherBtnClick
        )
        self.higherBtn.grid(row=0, column=0, padx=20)

        self.lowerBtn = ctk.CTkButton(
            self.btnFrame, 
            text="Lower", 
            command=self.onLowerBtnClick
        )
        self.lowerBtn.grid(row=0, column=1, padx=20)

    def showSpecialCardPopup(self, card: Card): 
        popup = ctk.CTkToplevel(self)
        popup.title("Special Card Received")

        popup.grid_rowconfigure(0, weight=1)
        popup.grid_columnconfigure(0, weight=1)

        frame = ctk.CTkFrame(popup)
        frame.grid(padx=40, pady=50)

        desc = ""
        if card.rank == Rank.MJ:
            desc = f"You have received the special {card.getName()} card.\n\n Goal: Guess the next 8 cards in the following sequence: \n(W, W, W, L, L, W, W, W)\n\n to win 10 bonus points!"
        elif card.rank == Rank.RODMAN:
            desc = f"You have received the special {card.getName()} card. Get a 2nd chance on the next card you get wrong!\n\n"

        descLabel = ctk.CTkLabel(
            frame,
            text=desc,
            wraplength=400,
            font=("Arial", 14),
        )
        descLabel.grid(pady=10, padx=20) 

        cardLabel = ctk.CTkLabel(
            frame,
            text=None,
            image=self.getImage(card)
        )
        cardLabel.grid(pady=20) 

        closeBtn = ctk.CTkButton(
            frame, 
            text="Close", 
            command=popup.destroy
        )
        closeBtn.grid(pady=10)
        
        # Freeze main window until the popup is closed
        popup.grab_set()
        self.master.wait_window(popup)
    
    def onHigherBtnClick(self):
        nextCard: Card = self.game.deck.seeTopCard()

        if self.game.isNextCardMj(nextCard):
            self.showSpecialCardPopup(nextCard)
        elif self.game.isNextCardRodman(nextCard):
            self.showSpecialCardPopup(nextCard)

        isPlayNextRound: bool = self.game.playRound(isUserInputHigher=True)

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
        Returns the corresponding resized image of a card
        """
        scriptDir = os.path.dirname(os.path.abspath(__file__))
        imagePath = os.path.join(scriptDir, "images", f"{card.getName()}.png")

        originalImg = Image.open(imagePath)
        resizedImg = originalImg.resize(Settings.CARD_SIZE.value)
        newImg = ImageTk.PhotoImage(resizedImg)
        return newImg
    
    def getBackOfCard(self) -> ImageTk.PhotoImage:
        """
        Returns the back image of a card
        """
        scriptDir = os.path.dirname(os.path.abspath(__file__))
        imagePath = os.path.join(scriptDir, "images", "back_of_card.png")
        
        originalImg = Image.open(imagePath)
        resizedImg = originalImg.resize(Settings.CARD_SIZE.value)
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
        self.menuTitleLabel.grid(pady=20)


        self.rulesLabel = ctk.CTkLabel(
            self, 
            text="How To Play:", 
            font=("Arial", 16, "bold")
        )
        self.rulesLabel.grid()
        self.rulesLabel = ctk.CTkLabel(
            self, 
            text=f"""
                1. You are given a card and you need to guess if the next card in the deck is higher or lower. Guessing wrongly will end the game.\n
                2. The ascending order (weakest -> strongest) of card rank is: 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, A.\n
                3. If the card rank is the same, then game will compare by suit. The ascending order of suit is: diamond, clubs, hearts, and spades\n
                4. Enabling special edition will add {GameConstant.NUM_MJ_CARDS.value} MJ and {GameConstant.NUM_RODMAN_CARDS.value} Rodman cards into the deck.\n
                5. Drawing the MJ card activates a special round where you need to guess the next 8 cards in the following sequence: (W, W, W, L, L, W, W, W) 
                    where 'W' means you want to correctly guessed it and 'L' means you want to 'wrongly' guessed it. If succesful, win 10 bonus points.\n
                6. Note that during the MJ Round, any rodman cards received during this special round will not count towards the win / loss sequence but will\n 
                    still be kept. As soon as your sequence does not match prefined sequence, you will immediately exit the MJ round\n
                7. Drawing a Rodman card means that on the next card you get wrong, it will activate, giving you a 2nd chance to win double points!\n
            """, 
            justify="left", 
            wraplength=1200,
            font=("Arial", 14),
            padx=30
        )
        self.rulesLabel.grid()


        self.optionsLabel = ctk.CTkLabel(
            self, 
            text="Special Options:", 
            font=("Arial", 16, "bold")
        )
        self.optionsLabel.grid()

        self.isBullsEditionOn = ctk.BooleanVar(value=False)
        self.bullsCheckbox = ctk.CTkCheckBox(
            self, 
            text="Enable Special Edition", 
            variable=self.isBullsEditionOn
        )
        self.bullsCheckbox.grid(pady=10)

        # Isdp == I See Dead People (Warcraft 3 cheat code)
        self.isIsdpOn = ctk.BooleanVar(value=False)
        self.isIsdpCheckbox = ctk.CTkCheckBox(
            self, 
            text="Enable True Sight (preview next card)", 
            variable=self.isIsdpOn
        )
        self.isIsdpCheckbox.grid(pady=10)

        self.startBtn = ctk.CTkButton(
            self, 
            text="Start Game", 
            command=self.startGame
        )
        self.startBtn.grid(pady=20)

    def startGame(self):
        self.game.configureSpecialEdition(self.isBullsEditionOn.get())
        self.game.startGame()
        
        self.master.showFrame(self.master.gameFrame)

class EndFrame(ctk.CTkFrame):
    def __init__(self, master: HigherLowerGame):
        super().__init__(master)

        self.master: HigherLowerGame = master 
        self.game: HigherLowerGame = self.master.game

        self.endTitleLabel = ctk.CTkLabel(
            self, 
            text="Game Over! Thank you for playing!", 
            font=("Arial", 24, "bold")
        )
        self.endTitleLabel.grid(pady=20, padx=20)

        self.scoreLabel = ctk.CTkLabel(
            self, 
            text=f"Your Final Score: {self.game.score}", 
            font=("Arial", 18)
        )
        self.scoreLabel.grid(pady=10)

        self.closeBtn = ctk.CTkButton(
            self, 
            text="Close Game", 
            command=self.closeGame
        )

        self.closeBtn.grid(pady=20)

    def closeGame(self):
        """
        Closes the application
        """
        self.master.destroy()

    def updateUi(self):
        self.scoreLabel.configure(text=f"Your Final Score: {self.game.score}")
