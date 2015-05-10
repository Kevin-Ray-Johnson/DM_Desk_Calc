#!/usr/bin/python

from __future__ import division  # Give me "real" division

welcome = """
A desktop calculator for the DM.  Fully featured d20 arithmetic system.  
Includes |d| operator to do unusual rolls.  For example, how would you 
roll a 1d27 ?  It's just 1|d|27.  It's easy. 

The |d| operator is your standard dice notation.  It takes the number, 
from any calculation, on the left and rolls that many dice with a 
number of sides on it's right.

To demonstrate, lets roll 2d4 to decide how many d6 to roll.  It's just 
2|d|4|d|6.  To get the sum of 2d4 and 1d6 it's (2|d|4)+(1|d|6).  
To roll 1 die with 3+1d5 sides you just 1|d|3+(1|d|5).

The [d20] button will clear the display and give the result of rolling 1|d|20.

The possible rolls are endless, so keep on rollin'

Author:
Kevin.Ray.Johnson@gmail.com
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

# Version: 1
#  To-Do:
#     Keyboard key-bindings


from random import randrange  # For the dice
from Tkinter import Text, Scrollbar, Button, Tk, Frame, DISABLED, RIGHT, VERTICAL, NORMAL, END, NSEW, N, S, E, W        # Minimum for the GUI
import sys  # For sys stream stuff
import tkFileDialog  # For saving files

messages = welcome  # A string used to keep messages until they can be displayed, or written to a file

# The dice we shall roll.    
def dice(n, sides):
   global messages
   rtn_val = 0
   for i in range(int(n)):
      roll = randrange(sides) + 1
      messages += '\n' + 'Rolling a d' + str(sides) + '. Rolled: ' + str(roll)
      rtn_val += roll
   return rtn_val

# For the creation of the |d| operator...
# Thanks to Ferdinand Jamitzky
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/384122
class Infix(object):
   def __init__(self, function):
      self.function = function
   def __ror__(self, other):
      return Infix(lambda x: self.function(other, x))
   def __or__(self, other):
      return self.function(other)
   def __rlshift__(self, other):
      return Infix(lambda x, self=self, other=other: self.function(other, x))
   def __rshift__(self, other):
      return self.function(other)
   def __call__(self, value1, value2):
       return self.function(value1, value2)
# Now we define the |d| operator that will give us dice rolls!
d = Infix(dice)

# The calculator & GUI
class Calculator(Frame):
   def __init__(self, parent):
      Frame.__init__(self, parent)
      self.font_size=8
      self.make_window()

   def make_window(self):
      
      # The keypad looks like so, less the '=' button below and the display above
      rows = 7
      cols = 4
      the_buttons = [['|d|2', '|d|4', '|d|6', '|d|8'],
                     ['|d|10', '|d|12', '|d|20', '|d|100'],
                     ['1', '2', '3', '+'],
                     ['4', '5', '6', '-'],
                     ['7', '8', '9', '*'],
                     ['(', '0', ')', '/'],
                     ['|d|', '<-', 'Clr', '.']]
      
      # Now we make them fill everything out..
      for r in range(rows+2):
         self.rowconfigure(r, weight=1)
      for c in range(cols):
         self.columnconfigure(c, weight=1)  
      
      # Set the display in the GUI
      self.display=Text(self, fg='black', bg='white', font=('', 2*self.font_size, ''), height=1, width=20, state=DISABLED)
      self.display.grid(column=0, row=0, columnspan=4, sticky=NSEW)
                     
      # Now for the buttons              
      self.buttons = []
      for row_list in the_buttons:
         for btn in row_list:
            if btn == '<-':
               self.buttons.append(Button(self, text=btn, font=('', `self.font_size`, ''), command=self.backspace))
               self.buttons[-1].bind(self.backspace)  # Button binding, not key binding!
            elif btn == 'Clr':
               self.buttons.append(Button(self, text=btn, font=('', `self.font_size`, ''), command=self.clear))
               self.buttons[-1].bind(self.clear) # Button binding, not key binding!
            else:    
               self.buttons.append(Button(self, font=('', `self.font_size`, ''), text=btn))
               self.buttons[-1].bind('<1>', self.buttonCB)  # Button binding, not key binding!
      
      # Now we place them
      for r in range(rows):
         for c in range(cols):
            self.buttons[r*cols + c].grid(row = r + 1, column = c,  sticky=NSEW)
      
      # And now the equals button
      self.eq_button=Button(self, text='=', font=('', `self.font_size`, ''), command=self.equals)
      self.fast_d20_button=Button(self, text='[d20]', font=('', `self.font_size`, ''), command=self.fast_d20)
      self.eq_button.grid(row=rows+1, column=0, columnspan=3, stick=NSEW)
      self.fast_d20_button.grid(row=rows+1, column=3, stick=NSEW)

   def fast_d20 (self):
      global messages
      ans=1|d|20
      messages += '\n\nCalculation:\n1|d|20'
      self.display.config(state=NORMAL)
      self.display.delete(1.0, END)
      self.display.insert(1.0, ans)
      self.display.config(state=DISABLED)
      messages += '\n' + 'Result = ' + str(ans)
      messages += '\n' + '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'

   def buttonCB(self, event):
      val=event.widget.cget('text')
      self.display.config(state=NORMAL)
      self.display.insert(END, val)
      self.display.config(state=DISABLED)

   def equals(self):
      if self.display.get(1.0, END):
         global messages
         ans=eval(self.display.get(1.0, END))  # Use eval() to take the "program" in the display and run it through the interpreter.
         messages += '\n' + '\nCalculation:\n' + self.display.get(1.0, END)
         self.display.config(state=NORMAL)
         self.display.delete(1.0, END)
         self.display.insert(1.0, ans)
         self.display.config(state=DISABLED)
         messages += '\n' + 'Result = ' + str(ans)
         messages += '\n' + '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'

   def clear(self):
      self.display.config(state=NORMAL)
      self.display.delete(1.0, END)
      self.display.config(state=DISABLED)

   def backspace(self):
      self.display.config(state=NORMAL)
      line = str(self.display.get(1.0, END))[0:-2]
      self.display.delete(1.0, END)
      self.display.insert(1.0, line)
      self.display.config(state=DISABLED)
      
# A test window with scroll bar.
class Scratch (Frame):
   def __init__(self, parent):
      Frame.__init__(self, parent)
      self.txt_box = Text (self, bg='white', fg='black', font=('', 12, ''))
      self.sc_bar = Scrollbar ( self, orient=VERTICAL)
      self.txt_box['yscrollcommand'] = self.sc_bar.set
      self.sc_bar['command'] = self.txt_box.yview
      self.save_button = Button(self, text="Save Transcript", command=self.save_text)
      self.clear_button = Button(self, text="Clear Text", command=self.clear_text)
      self.rowconfigure(0, weight=1)
      self.columnconfigure(0, weight=1)
      self.txt_box.grid(row=0, column=0, columnspan=2, sticky=NSEW)
      self.sc_bar.grid(row=0, column=2, stick=N+S)
      self.save_button.grid(row=1, column=0, sticky=E+W)
      self.clear_button.grid(row=1, column=1, sticky=E+W)
      self.prnt_stuff()

   def prnt_stuff (self):
      global messages
      Update_per_sec = 4
      if '' != messages:
         self.txt_box.insert(END, messages)
         messages = ''
         self.txt_box.yview(END)
      self.after(int(1000/Update_per_sec), self.prnt_stuff)   # run approximately Update_per_sec times per second
   
   def clear_text (self):
      self.txt_box.delete(1.0, END)
      
   def save_text (self):
      global messages 
      outfile = tkFileDialog.asksaveasfilename(title="Save transcript as...")
      save_file = open(outfile, 'w')
      save_file.write(self.txt_box.get(1.0, END))
      messages += '\nTranscrips saved as: ' + outfile + '\n'
       
# If called as main program...
if __name__ == '__main__':
   win1 = Tk()
   win2 = Tk()
   win1.title('DM\'s Desk Calculator')
   win2.title('DM\'s Rolls & Notes')
   
   calc = Calculator(win1)
   log = Scratch(win2)
   
   win1.rowconfigure(0, weight=1)
   win1.columnconfigure(0, weight=1)  
   win2.rowconfigure(0, weight=1)
   win2.columnconfigure(0, weight=1)  
   
   calc.grid(row=0, column=0, sticky=NSEW)
   log.grid(row=0, column=0, sticky=NSEW)

   win1.mainloop()
   win2.mainloop()
