import customtkinter as ctk

class App(ctk.CTk):
    # self here allows the app to refer to itself
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")

        self.title("Higher Lower (Chicago Bulls Edition)")
        self.geometry("400x180")
        

if __name__ == "__main__":
    app = App()
    app.mainloop()