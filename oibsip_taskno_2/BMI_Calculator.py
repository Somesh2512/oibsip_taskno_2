# Name :- Somesh Ramdas Jatti
# Task 2 :- BMI Calculator

from tkinter import *
from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkEntry, CTkOptionMenu, CTkFont, set_appearance_mode, set_default_color_theme
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import threading
import numpy as np

# Custom theme settings
set_appearance_mode("System")
set_default_color_theme("dark-blue")


class BMIIndex(CTk):
    def __init__(self):
        CTk.__init__(self)

        self.height_feet = None
        self.weight_kilos = None
        self.bmi = None
        self.bmi_history = []

        # Title
        self.title("Body Mass Index Calculator")
        self.geometry('640x410')
        self.resizable(False, False)
        self.grid()


        # Create multiple frames
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame_left = CTkFrame(master=self, width=180, corner_radius=0)
        frame_left.grid(row=0, column=0, sticky="nswe")

        frame_right = CTkFrame(master=self)
        frame_right.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)



        # Labels
        label_left = CTkLabel(master=frame_left, text="BMI Calculator",
                              font=CTkFont(weight="bold", size=18,  family="Georgia"),
                              justify="left")
        label_left.place(relx=0.5, rely=0.15, anchor="center")

        label_right_01 = CTkLabel(master=frame_right, text="Enter your height in feet: ",
                                  font=CTkFont(size=13 ,  family="Georgia"),
                                  justify="left")
        label_right_01.place(relx=0.5, rely=0.07, anchor="center")

        label_right_02 = CTkLabel(master=frame_right, text="Enter your weight in kG: ",
                                  font=CTkFont(size=13 ,  family="Georgia"),
                                  justify="left")
        label_right_02.place(relx=0.5, rely=0.35, anchor="center")

        label_right_03 = CTkLabel(master=frame_right, text="Your Body Mass Index is: ",
                                  font=CTkFont(size=13 ,family="Georgia"),
                                  justify="left")
        label_right_03.place(relx=0.5, rely=0.63, anchor="center")

        label_right_04 = CTkLabel(master=frame_right, text="According to the BMI, You are ",
                                  font=CTkFont(size=13 , family="Georgia"),
                                  justify="left")
        label_right_04.place(relx=0.5, rely=0.8, anchor="center")

        self.label_right_05 = CTkLabel(master=frame_right, text="",
                                       font=CTkFont(size=13 , family="Georgia"),
                                       justify="left")
        self.label_right_05.place(relx=0.75, rely=0.8, anchor="center")

        # Button
        button_right = CTkButton(master=frame_right, text="Calculate", command=self.display_bmi , font=("Georgia" ,14))
        button_right.place(relx=0.5, rely=0.9, anchor="center")

        # Text inside the textbox
        self.entry_right_01 = CTkEntry(master=frame_right, width=180, height=30,
                                       placeholder_text="Your height in Feet",
                                       font=CTkFont(size=12 , family="Georgia"))
        self.entry_right_01.pack(pady=40, padx=10)

        self.entry_right_02 = CTkEntry(master=frame_right, width=180, height=30,
                                       placeholder_text="Your weight in KG",
                                       font=CTkFont(size=12 , family="Georgia"))
        self.entry_right_02.pack(pady=40, padx=10)

        self.entry_right_03 = CTkEntry(master=frame_right, width=180, height=30,
                                       font=CTkFont(size=12 ,family="Georgia"))
        self.entry_right_03.pack(pady=40, padx=10)

        # Appearances
        self.appearance_mode_label = CTkLabel(master=frame_left, text="Appearance Mode:" , font=("Georgia" ,14 , "bold"))
        self.appearance_mode_label.grid(row=1, column=0, padx=10, pady=(10, 0))
        self.appearance_mode_label.place(relx=0.5, rely=0.27, anchor="center")
        self.appearance_mode_optionmenu = CTkOptionMenu(master=frame_left,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode_event)
        self.appearance_mode_optionmenu.grid(row=2, column=0, padx=10, pady=(10, 10))
        self.appearance_mode_optionmenu.place(relx=0.5, rely=0.35, anchor="center")

        # History button
        history_button = CTkButton(master=frame_left, text="Show History", command=self.show_history)
        history_button.grid(row=3, column=0, padx=10, pady=(10, 10))
        history_button.place(relx=0.5, rely=0.45, anchor="center")


        # Load BMI history
        self.load_bmi_history()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        set_appearance_mode(new_appearance_mode)

    def bmi_calculate(self):
        try:
            self.bmi = self.weight_kilos / ((self.height_feet * 0.3048) ** 2)
        except ValueError:
            self.bmi = "Invalid input!"

    def display_bmi(self):
        try:
            self.height_feet = float(self.entry_right_01.get())
            self.weight_kilos = float(self.entry_right_02.get())
        except ValueError:
            self.entry_right_03.delete(0, END)
            self.entry_right_03.insert(END, "Invalid input")
        self.bmi_calculate()
        self.entry_right_03.delete(0, END)
        self.entry_right_03.insert(END, f"BMI: {self.bmi:.2f}")
        result_status = self.get_status()
        self.label_right_05.configure(text=result_status)
        self.bmi_history.append(self.bmi)
        self.save_bmi_history()  # Save the updated history


    def get_status(self):
        if self.bmi is None:
            return " "

        elif self.bmi < 16:
            return "anorexic"

        elif self.bmi < 18.5:
            return "underweight"

        elif self.bmi < 25:
            return "healthy"

        elif self.bmi < 30:
            return "overweight"

        else:
            return "obese"

    def show_history(self):
        if not self.bmi_history:
            return

        # Create a new window for displaying BMI history
        history_window = Toplevel(self)
        history_window.title("BMI History")

        # Display BMI history as text
        history_text = Text(history_window, height=10, width=40, font=("Courier New", 12))
        history_text.pack()

        def insert_bmi_text():
            for i, bmi in enumerate(self.bmi_history, start=1):
                history_text.insert(INSERT, f"Measurement {i}: BMI = {bmi}\n")

        history_window.after_idle(insert_bmi_text)


        plt.figure()
        plt.plot(range(1, len(self.bmi_history) + 1), self.bmi_history)
        plt.xlabel("Measurement")
        plt.ylabel("BMI Value")
        plt.title("BMI History")
        plt.grid(True)
        plt.savefig("bmi_history.png")

        img = Image.open("bmi_history.png")
        photo = ImageTk.PhotoImage(img)
        img_label = Label(history_window, image=photo)
        img_label.image = photo
        img_label.pack()

    def save_bmi_history(self, filename="bmi_history.txt"):
        with open(filename, "w") as file:
            for bmi in self.bmi_history:
                file.write(str(bmi) + "\n")

    def load_bmi_history(self, filename="bmi_history.txt"):
        self.bmi_history = []
        try:
            with open(filename, "r") as file:
                for line in file:
                    self.bmi_history.append(float(line.strip()))
        except FileNotFoundError:
            pass

    def on_window_close(self):
        # Clear the BMI history
        self.bmi_history = []
        self.save_bmi_history()
        self.destroy()

    def load_bmi_history(self, filename="bmi_history.txt"):
        self.bmi_history = []
        try:
            with open(filename, "r") as file:
                for line in file:
                    self.bmi_history.append(float(line.strip()))
        except FileNotFoundError:
            pass

    def bind_close_event(self):
        # Bind the close event to the on_window_close function
        self.protocol("WM_DELETE_WINDOW", self.on_window_close)


if __name__ == "__main__":
    bmi_index = BMIIndex()
    bmi_index.bind_close_event()
    bmi_index.mainloop()