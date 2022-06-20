from tkinter import *
from tkinter import messagebox




class Interface:
    def __init__(self):
        self.__start_tk__()
        self.__start_main_menu__()

    def __start_tk__(self):
        self.root = Tk()
        self.root.resizable(width=False, height=False) # Lock window size
        # root.geometry("720x720")
        self.root.geometry("400x400") # Set size

    def __start_main_menu__(self):

        self.startButton = Button(text="Start",command=self.run)
        self.peopleTextBox = Text(self.root,height=1,width=5)
        self.restaurantTextBox = Text(self.root,height=1,width=5)
        self.distributorTextBox = Text(self.root,height=1,width=5)
        self.peopleLabel = Label(self.root,text="Number of people")
        self.restaurantLabel = Label(self.root,text="Number of restaurants")
        self.distributorLabel = Label(self.root,text="Number of distributors")
        self.restartButton = Button(text = "Restart",command = self.__restart__)


        self.peopleTextBox.insert(INSERT,"2000")
        self.restaurantTextBox.insert(INSERT,"100")
        self.distributorTextBox.insert(INSERT,"300")

        
        self.startButton.place(x=20,y=100)
        self.peopleTextBox.place(x=160,y=20)
        self.restaurantTextBox.place(x=160,y=40)
        self.distributorTextBox.place(x=160,y=60)
        self.peopleLabel.place(x=20,y=20)
        self.restaurantLabel.place(x=20,y=40)
        self.distributorLabel.place(x=20,y=60)
        self.restartButton.place(x=80,y=100)

    def run(self):
        people = self.peopleTextBox.get(1.0, "end-1c")
        restaurants = self.restaurantTextBox.get(1.0, "end-1c")
        distributors = self.distributorTextBox.get(1.0, "end-1c")

        try:
            self.people = int(people)
            self.restaurants = int(restaurants)
            self.distributors = int(distributors)
        except:
            messagebox.showinfo("Error","Error:All values must be integers")
            print("Error: All values must be integers")
            return
        self.__start__pygame__()

    def __start__pygame__(self):
        print("Starting pygame...")

    def __restart__(self):
        self.root.destroy()
        self.__start_tk__()
        self.__start_main_menu__()
        

if __name__ == "__main__":
    
    I = Interface()

    I.root.mainloop()