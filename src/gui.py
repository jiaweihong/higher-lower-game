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
        self.grid_rowconfigure(0, weight=1)  # Center vertically
        self.grid_columnconfigure(0, weight=1)

        self.title("App")
        self.geometry("900x500")

        self.menuFrame = MenuFrame(self)
        self.gameFrame = GameFrame(self)
        self.currentFrame = self.menuFrame
        
        # Show menu frame initially
        self.showFrame(self.menuFrame)
    
    def showFrame(self, frameToShow: ctk.CTkFrame):
        print(f"current frame {self.currentFrame.winfo_manager()}")
        if self.currentFrame == self.menuFrame:
            self.currentFrame.pack_forget() 
        elif self.currentFrame == self.gameFrame: 
            self.currentFrame.grid_forget() 

        print(f"to show frame {frameToShow.winfo_manager()}")

        if frameToShow == self.menuFrame:
            frameToShow.pack(expand=True, fill="both")  
        elif frameToShow == self.gameFrame: 
            frameToShow.grid()  
        
        self.currentFrame = frameToShow

class GameFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
    
        deckFrame = ctk.CTkFrame(self)
        deckFrame.grid(row=0, column=0, padx=20, ipadx=20)

        currentCardFrame = ctk.CTkFrame(self)
        currentCardFrame.grid(row=0, column=1, padx=20, ipadx=20)

        # Create labels
        deckLabel = ctk.CTkLabel(deckFrame, text="Deck", compound="top", font=("Arial", 14))
        deckLabel.pack(pady=20) 

        currentCardLabel = ctk.CTkLabel(currentCardFrame, text="Current Card", compound="top", font=("Arial", 14))
        currentCardLabel.pack(pady=20) 
    
    def getImage(self, card: Card) -> ImageTk.PhotoImage:
        """
        Returns a the corresponding (according to attributes) and resized image of the card
        """
        # possibly change the way you are getting the file path
        originalImg = Image.open(f"images/{card.getName()}.png")
        resizedImg = originalImg.resize(Constant.CARD_SIZE)
        newImg = ImageTk.PhotoImage(resizedImg)
        return newImg
    
    def getBackOfCard(self) -> ImageTk.PhotoImage:
        """
        Returns the corresponding (according to attributes) and resized image of the card
        """
        # possibly change the way you are getting the file path
        originalImg = Image.open(f"images/back_of_card.png")
        resizedImg = originalImg.resize(Constant.CARD_SIZE)
        newImg = ImageTk.PhotoImage(resizedImg)
        return newImg
    
class MenuFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.menuTitleLabel = ctk.CTkLabel(self, text="Higher Lower Game (Chicago Bulls Edition)", font=("Arial", 24, "bold"))
        self.menuTitleLabel.pack(pady=20)

        self.rulesLabel = ctk.CTkLabel(self, text="Game Rules: \n1. Rule one description.\n2. Rule two description.\n3. Rule three description.", justify="left", font=("Arial", 14))
        self.rulesLabel.pack(pady=10)
        
        self.isBullsEditionOn = ctk.BooleanVar(value=False)
        self.bullsCheckbox = ctk.CTkCheckBox(self, text="Enable Special Edition", variable=self.isBullsEditionOn)
        self.bullsCheckbox.pack(pady=10)

        self.startBtn = ctk.CTkButton(self, text="Start Game", command=self.startGame)
        self.startBtn.pack(pady=20)

    def startGame(self):
        self.master.game.configureSpecialEdition(self.isBullsEditionOn.get())
        self.master.showFrame(self.master.gameFrame)

if __name__ == "__main__":
    # creating the game, does not create the deck, deck is only created after user presses startGame
    game = HigherLowerGame()
    app = HigherLowerApp(game)
    app.mainloop()