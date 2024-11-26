import customtkinter as ctk
from main import Deck, Card
from PIL import Image, ImageTk

class App(ctk.CTk):
    # self here allows the app to refer to itself
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")

        self.title("Higher Lower (Chicago Bulls Edition)")
        self.geometry("900x500")

        self.deck: Deck = Deck(isBullsEdition=True)
        card1: Card = self.deck.drawCard()
        card2: Card= self.deck.drawCard()


        

        # Create Frames
        tableFrame = ctk.CTkFrame(self)
        tableFrame.pack(pady=20)

        deckFrame = ctk.CTkFrame(tableFrame)
        deckFrame.grid(row=0, column=0, padx=20, ipadx=20)

        currentCardFrame = ctk.CTkFrame(tableFrame)
        currentCardFrame.grid(row=0, column=1, padx=20, ipadx=20)

        # Create labels
        deckLabel = ctk.CTkLabel(deckFrame, text="Deck", compound="top", font=("Arial", 14), image=self.getBackOfCard())
        deckLabel.pack(pady=20) 

        currentCardLabel = ctk.CTkLabel(currentCardFrame, text="Current Card", compound="top", font=("Arial", 14), image=self.getImage(card2))
        currentCardLabel.pack(pady=20) 


    def getImage(self, card: Card) -> ImageTk.PhotoImage:
        """
        Returns a the corresponding (according to attributes) and resized image of the card
        """
        # possibly change the way you are getting the file path
        originalImg = Image.open(f"images/{card.getName()}.png")
        resizedImg = originalImg.resize((150,218))
        newImg = ImageTk.PhotoImage(resizedImg)
        return newImg
    
    def getBackOfCard(self) -> ImageTk.PhotoImage:
        """
        Returns a the corresponding (according to attributes) and resized image of the card
        """
        # possibly change the way you are getting the file path
        originalImg = Image.open(f"images/back_of_card.png")
        resizedImg = originalImg.resize((150,218))
        newImg = ImageTk.PhotoImage(resizedImg)
        return newImg
        

if __name__ == "__main__":
    app = App()
    app.mainloop()