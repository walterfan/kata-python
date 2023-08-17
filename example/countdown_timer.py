#!/usr/bin/env python3

import time
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from playsound import playsound

DEFAULT_MINS = 25

class PomodoroTimer:

    def __init__(self, title = "Pomodoro Timer"):
        self._root = Tk()
        self._style = ttk.Style()
        self._style.theme_use('alt')
        # Define the geometry of the window
        self._root.geometry("360x240")

        #define title
        self._root.title(title)

        # set background color
        #self._root.config(bg='green')

        # declaration of variables
        self._hour=StringVar()
        self._minute=StringVar()
        self._second=StringVar()

        self.init_ui()
        self._started = False

    def init_time(self):
        # setting the default value as 0
        self._hour.set("00")
        self._minute.set("{}".format(DEFAULT_MINS))
        self._second.set("00")

    def init_ui(self):

        self.init_time()

        # Using Entry class to take input from the user
        hour_box= Entry(
            self._root,
            width=3, 
            font=("Arial",18,""),
            textvariable=self._hour)

        hour_box.place(x=80,y=80)

        mins_box = Entry(
            self._root,
            width=3,
            font=("Arial",18,""),
            textvariable=self._minute)

        mins_box.place(x=130,y=80)

        sec_box = Entry(
            self._root,
            width=3,
            font=("Arial",18,""),
            textvariable=self._second)

        sec_box.place(x=180,y=80)


        #Create a Label
        label = Label(self._root, text= "Focus and Flow",font=('Helvetica bold', 24))
        #label.grid(column=0, row=0, padx=20, pady=20,  sticky='w')
        label.pack(pady=20)
        # button widget
        btn = Button(self._root, text='Start', bd='5', fg="green", command= self.countdown)
        btn.place(x = 80,y = 120)

        btn = Button(self._root, text='Stop', bd='5', fg="red", command= self.stop)
        btn.place(x = 160,y = 120)

    def stay_on_top(self):
        self._root.lift()
        self._root.after(2000, self.stay_on_top)

    def run(self):
        #Make the window jump above all
        self.stay_on_top()
        self._root.mainloop()


    def stop(self):
        self._started = False

        self._hour.set("{0:2d}".format(0))
        self._minute.set("{0:2d}".format(DEFAULT_MINS))
        self._second.set("{0:2d}".format(0))

    def countdown(self):
        self._started = True
        try:
            # store the user input
            user_input = int(self._hour.get())*3600 + int(self._minute.get())*60 + int(self._second.get())
        except:
            messagebox.showwarning('', 'Invalid Input!')
        while self._started and user_input >-1:
            
            # divmod(firstvalue = user_input//60, secondvalue = user_input%60)
            mins,secs = divmod(user_input,60)

            # Converting the input entered in mins or secs to hours,
            hours=0
            if mins >60:
                hours, mins = divmod(mins, 60)

            # store the value up to two decimal places
            # using the format() method
            self._hour.set("{0:2d}".format(hours))
            self._minute.set("{0:2d}".format(mins))
            self._second.set("{0:2d}".format(secs))

            # updating the GUI window
            self._root.update()
            time.sleep(1)

            # if user_input value = 0, then a messagebox pop's up
            # with a message
            if (user_input == 0):
                #messagebox.showinfo("Time Countdown", "Time Over")
                print("It is time")

            # decresing the value of temp
            # after every one sec by one

            user_input -= 1

        #exit loop and play music

        self.init_time()
        playsound('starlet.wav', block = False)

if __name__ == '__main__':
    timer = PomodoroTimer()
    timer.run()

