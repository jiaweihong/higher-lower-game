import customtkinter as ctk
from main import Deck

class App(ctk.CTk):
    # self here allows the app to refer to itself
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")

        self.title("Higher Lower (Chicago Bulls Edition)")
        self.geometry("900x500")

        self.deck = Deck(isBullsEdition=True)

        # Create Frames
        tableFrame = ctk.CTkFrame(self)
        tableFrame.pack(pady=20)

        deckFrame = ctk.CTkFrame(tableFrame)
        deckFrame.grid(row=0, column=0, padx=20, ipadx=20)

        currentCardFrame = ctk.CTkFrame(tableFrame)
        currentCardFrame.grid(row=0, column=1, padx=20, ipadx=20)

        # Create labels
        deckLabel = ctk.CTkLabel(deckFrame, text="Deck", font=("Arial", 14))
        deckLabel.pack(pady=20) 

        currentCardLabel = ctk.CTkLabel(currentCardFrame, text=self.deck.seeTopCard().getName(), font=("Arial", 14))
        currentCardLabel.pack(pady=20) 

        

if __name__ == "__main__":
    app = App()
    app.mainloop()