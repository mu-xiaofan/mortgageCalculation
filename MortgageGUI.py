#This program is used to calculate the mortgage by taking user's input and using the formula of mortgage.
#It uses GUI to become more user friendly.
#It also uses an API to read a file and data in it to draw the corresponding chart to show the user the relationship of years and rate

import tkinter as tk
from printMeFirst import *
from Reverse import *
from tkinter import *
from tkinter import messagebox as msg
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import csv
import os

BUTTON_BG_COLOR = "blue"

#create the fields
fields = ('Loan Amount', 'Interest Rate%', 'Loan Term (Years)', "Monthly Payment",'Total Paid')

# this function will calculate the mortgage by using its function and then print out the result in a nice format
#it also checks the user's input. If it is not valid, it will give user a notification
# @parm entries:  This contains the form field on the GUI forms
# @parm operator: # @return NONE
#
def calculateMortgage(entries):
    # Review: Good use of try and except to catch exceptions.
   try:  # catch exception if inputs are invalid (float) for num1 & num2

      loanAmount = float(entries['Loan Amount'].get())  
      interestRate = float(entries['Interest Rate%'].get())
      loanTerm = float(entries['Loan Term (Years)'].get())
      # the code that printing the values of loanAmount, interestRate, and loanTerm 
      # to the console look like debugging code. It is better to delete them after development
    #   print(str(loanAmount))
    #   print(str(interestRate))
    #   print(str(loanTerm))

      # Review: Storing the warning message in a variable.
      warningMessage = 'Must be positive number > 0'
      
      if loanAmount <= 0 or interestRate <= 0 or loanTerm <= 0:
          msg.showwarning('Error: Invalid Input', warningMessage)
      else:
          monthlyPayment = loanAmount * ((interestRate/100)/12)*pow((1+((interestRate/100)/12)),loanTerm*12)/(pow((1+((interestRate/100)/12)),loanTerm*12)-1)
          totalPaid = monthlyPayment * (loanTerm * 12)
          #make field normal again so we can place value into these fields
          entries['Monthly Payment'].configure(state='normal')
          entries['Monthly Payment'].delete(0,END)
          entries['Monthly Payment'].insert(0, '$ '+format(monthlyPayment,",.2f"))
          entries['Monthly Payment'].configure(state='disabled')
          entries['Total Paid'].configure(state='normal')
          entries['Total Paid'].delete(0,END)
          entries['Total Paid'].insert(0, '$ '+format(totalPaid,",.2f"))
          entries['Total Paid'].configure(state='disabled')
   except:
       msg.showwarning('Error: Invalid Input', warningMessage)
 
# Add labels to line plots (annotation)
# zip joins x and y coordinates in pairs
# @param xlist,ylist are the lists contain the data of x and y coordinate
# Review: the name of the function should be annotationLabel instead of annatationLabel
def annotationLabel(xlist, ylist):
    count = 0 # used to only plot out annatation for every other number
    for x,y in zip(xlist,ylist):
        if (count == 2): 
            label = "{:.2f}%".format(y)
            plt.annotate(label, # this is the text
                         (x,y), # this is the point to label
                         textcoords="offset points", # how to position the text
                         xytext=(0,10), # distance from text to points (x,y)
                         rotation=90,
                         fontsize=10,
                         ha='center') # horizontal alignment can be left, right or center
            count = 0
        else:
            # Review：Code Redundancy: use count += 1 instead of count = count + 1
            count += 1



# displayChart function takes one parameter, which is the name of the file and then read the file and draw the chart using the API
# @pram fileName is the name of the file we are going to read
# @return none
def displayChart(fileName):
    FONTSIZE = 8
    # Review: checking the file exists or not.
    if not os.path.exists(fileName):  # check
        print("Error: File does not exist.")
        return  # if it not exists, return
    Axlist = []
    Aylist = []
    with open(fileName,'r') as myFile:
        plots = csv.reader (myFile, delimiter = ',')
        for row in plots:
            Axlist.append(row[0])
            Aylist.append(float(row[1]))
    Axlist = Reverse(Axlist)
    Aylist = Reverse(Aylist)
    plt.plot(Axlist,Aylist,label = 'Mortgage Rate')
    ax = plt.gca()# get current axes
    #Review: use constant FONTSIZE for setting the font size
    plt.xticks(rotation = 90, fontsize = FONTSIZE) # rotate the label 90 degree
    # only print out every other x label so it will fit
    # If remove the for loop, labels will overlap each other
    counter = 1
    for label in ax.get_xaxis().get_ticklabels():
        if (not counter%10==0) and (not counter == 1):
            label.set_visible(False)
        # Review：Code Redundancy: use counter += 1 instead of counter = counter + 1
        counter += 1
    plt.xlabel('Year', fontsize = FONTSIZE)
    plt.ylabel('Rate %')
    plt.title('Historical Mortgage Rate')
    annotationLabel(Axlist, Aylist)
    plt.legend()
    plt.show()




# this function will make a GUI form with all the fields based on
# the fields list
# @parm root:  This is the root window canvas for the GUI
# @parm fields: This list contains all the fields to be placed on the GUI
#               forms.
# @return entries: dictionary which contains the GUI form field and its value
# Review: Function names like makeform and calculateMortgage are not consistently named.
# so we change the makeform to makeForm
def makeForm(root, fields):
   entries = {}
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=22, text=field+": ", anchor='w')
      ent = Entry(row)
      ent.insert(0,"0")
      row.pack(side = TOP, fill = X, padx = 5 , pady = 5)
      lab.pack(side = LEFT)
      ent.pack(side = RIGHT, expand = YES, fill = X)
      entries[field] = ent
   return entries

# main program
if __name__ == '__main__':
   root = Tk() # create a Tk window
   root.title("Mortgage Calculator")
   root.configure(background="light blue")
  # generate GUI forms and return field/values in
  # ents dictionary
  # Review: Good use of functions like makeform and calculateMortgage, enhancing readability and reusability
   ents = makeForm(root, fields)
   # lambda is used to recontruct a new function with same function
   # name with different paramters
   #
   # We use lambda functions when we require a nameless function
   # for a short period of time. In Python, we generally use it
   # as an argument to a higher-order function (a function that
   # takes in other functions as arguments).
   # Review1: change the color settings in the GUI to constants, 
   # so that future modifications can be made by only changing this constant.
   # Review2: the arguments of the Button constructor for b1 and b2 are not in the same order.
   b1 = Button(root, text = "Calculate",bg = BUTTON_BG_COLOR,
               command=(lambda e = ents: calculateMortgage(e)))
   b1.pack(side = LEFT, padx = 5, pady = 5)
   b1.configure(foreground = "blue")
   # use fileName = "mortgageRate.txt" instead of hardcoded in displayChart
   fileName = "mortgageRate.txt"
   b2 = Button(root, text='Chart', bg = BUTTON_BG_COLOR,
               command=(lambda e = ents: displayChart(fileName)))
   b2.pack(side = LEFT, padx = 5, pady = 5)
   b4 = Button(root, text = 'Quit', command = root.destroy)
   b4.pack(side = LEFT, padx = 5, pady = 5)
   # Review: delete the unnecessary '/'
   # make Monthly Payment field readonly
   ents['Monthly Payment'].configure(
       state='readonly', font=("Arial", 14, "bold", "italic")
       )
   # make Total Paid field readonly
   ents['Total Paid'].configure(
       state='readonly', font=("Arial", 14, "bold", "italic")
       )
   
   printStuff = printMeFirst("Xiaofan Mu","CNET 142")# call printMeFirst function to get the string to print
   tbox = tk.Text(root, height=2, width=30)
   tbox.pack()
   tbox.insert(tk.END, printStuff)
   tbox.configure(state='disabled')
   root.mainloop()
