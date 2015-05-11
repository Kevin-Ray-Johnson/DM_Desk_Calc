#!/usr/bin/python
from __future__ import division  # Give me "real" division

# Buffer for the log/editor window and internal message passing.
messages = """
The Diminutive Combat Engine is used to model groups of soldiers in a D&D style combat system.
Based off of a statistical battle model.

Author:
Kevin.Ray.Johnson@gmail.com

Released under the GNU GPL with all freedoms 
and limitation therein.

All donations are, of course, appreciated ;-)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

# The dice we shall roll.    
def dice(n, sides):
   from random import randrange  # For the dice
   global messages
   rtn_val = 0
   for i in range(int(n)):
      roll = randrange(sides) + 1
      messages += '\n' + 'Rolling a d' + str(sides) + '. Rolled: ' + str(roll)
      rtn_val += roll
   return rtn_val

# For the creation of the |d| operator.  Use the Infix class imported above
from Infix import Infix   # Lets us make binary infix style operators
d = Infix(dice)


# A group of units      
class Group:
   def __init__(self, num_of_soldiers, hp_expression, unit_ac, dmg_expression, magic_mod, atk_mod, misc_mod, flee_expression, group_name):
      # Make a new company of soldiers...
      self.soldiers = []                        # List of soldiers ready to fight
      self.fled = []                            # List of soldiers who have attempted to flee from combat
      for i in range(num_of_soldiers):                        # Number of soldiers in the group
         self.soldiers.append(eval(str(hp_expression)))       # The staring HP of a soldier
      self.num_of_soldiers = num_of_soldiers    # Number of soldiers in this group
      self.initial_solders = num_of_soldiers    # Initial number of soldiers
      self.unit_ac = unit_ac                    # The unit's armor class.  Used to avoid physical damage from combat. Effects unit vs. unit interaction
      self.magic_mod = magic_mod                # Units resistance to magic Effects player vs. group action via magic
      self.atk_mod = atk_mod                    # Effects the ability of unit's to land a physical attack.
      self.misc_mod = misc_mod                  # Modifies all saves, resistances, etc.
      self.dmg_expression= dmg_expression       # Describes the damage each soldier can deal
      self.group_name = group_name              # The name of the group
      self.losses = 0                           # Losses sustained
      self.flee_expression = flee_expression    # Condition against soldiers current HP to see if he attempts to flees combat

   def Print(self):  # Print out the groups stats
      print self.group_name + ' status:'
      print "# of soldiers ready = " + str(len(self.soldiers)) + '\t(' + str(100*len(self.soldiers)/self.initial_solders) + '%)'
      for i in range(len(self.soldiers)):
         print "\tSoldier # " + str(i+1) + ".  HP = " + str(self.soldiers[i])
      if len(self.fled) > 0:
         print "# of soldiers who attempted to flee = " + str(len(self.fled)) + "\t(" + str(100*len(self.fled)/self.initial_solders) + '%)'
         for i in range(len(self.fled)):
            print "\tSoldier # " + str(i+1) + ".  HP = " + str(self.fled[i])
      print "Losses = " + str(self.losses) + '\t(' + str(100 * self.losses / self.initial_solders) + '%)'
      print "AC = " + str(self.unit_ac)
      print "DMG = " + str(self.dmg_expression)
      print "Magic resist = " + str(self.magic_mod)
      print "ATK modifier = " + str(self.atk_mod)
      print "Misc modifier = " + str(self.misc_mod)
      print "Flee criteria = " + str(self.flee_expression)
               
   def HP_Change(self, effect, resistance=None, multiplier=1):  #Change all units HP by by some amount. Multiplier multiplies the resulting damage (-1 == hurt, 1 == heal)
      for i in range(len(self.soldiers)): # For all the soldiers
         amount = multiplier*(eval(str(effect)))   # Calculate HP change
         if resistance: # Check if they may resist
            if ((self.magic_mod + self.misc_mod + (1|d|20)) <= resistance ):  # Trow resistance
               print "Soldier " + str(i+1) + " changed HP by " + str(amount)
               self.soldiers[i] += amount # Apply change to HP
         else:
            self.soldiers[i] += amount # Apply change to HP
      self.Eval_group()
      print '\n'
      self.Print()
      print '\n'
      
   def HP_Change_unit(self, effect, resistance=None, multiplier=1):  #Change single units HP.
      unit = (1|d|len(self.soldiers)) - 1 # Pick a soldier at random
      amount = multiplier*(eval(str(effect)))   # Calculate HP change
      if resistance: # Check if they may resist
         if ((self.magic_mod + self.misc_mod + (1|d|20)) <= resistance ):  # Trow resistance
            print "Soldier " + str(unit) + " changed HP by " + str(amount)
            self.soldiers[unit] += amount # adjust their HP
         else:
            print "No effect, the soldier saved himself."
      else:
         print "Soldier " + str(unit) + " changed HP by " + str(amount)
         self.soldiers[unit] += amount
      self.Eval_group()
      print '\n'
      self.Print()
      print '\n'
      
   def Kill(self, resistance=None):    # Kill effect against a group!
      for i in range(len(self.soldiers)): # For all the soldiers
         if resistance: # Check if they may resist
            if ((self.magic_mod + self.misc_mod + (1|d|20)) <= resistance ):  # Trow resistance
               print "Soldier " + str(i+1) + " has suffered an instant death effect!"
               self.soldiers[i] = 0
            else:
               print "No effect. Soldier " + str(i+1) + " saved himself."
         else:
            print "Soldier " + str(unit) + " has suffered an instant death effect!"
            self.soldiers[unit] = 0
      self.Eval_group()
      
   
   def Kill_unit(self, resistance=None):  # Kill effect on a random soldier
      unit = (1|d|len(self.soldiers)) - 1 # Pick a soldier at random
      if resistance: # Check if they may resist
         if ((self.magic_mod + self.misc_mod + (1|d|20)) <= resistance ):  # Trow resistance
            print "Soldier " + str(unit) + " has suffered an instant death effect!"
            self.soldiers[unit] = 0
         else:
            print "No effect, the soldier saved himself."
      else:
         print "Soldier " + str(unit) + " has suffered an instant death effect!"
         self.soldiers[unit] = 0
      self.Eval_group()
      
   def Attacked(self, number_of_atkrs, atkr_mod, dmg_expression, over_mod=0, Display=True):   # Describes getting attacked by another group
      if len(self.soldiers) <= 0:
         print self.group_name + ' is defeated.  It has no soldiers left to fight.'
         self.num_of_soldiers = 0
      else:
         for i in range(number_of_atkrs): # For all the attackers
            dmg = eval(str(dmg_expression))  # The damage to be dealt to a soldier
            if i < len(self.soldiers):   # They pair off 1-1
               if (((1|d|20) + atkr_mod) >= (self.unit_ac + self.misc_mod)):  # and try to attack
                  if Display:
                     print "A soldier took " + str(dmg) + " damage from an attack"
                  self.soldiers[i] -= dmg   # and if successful they do damage
            else:
               if (((1|d|20) + atkr_mod - over_mod) >= (self.unit_ac + self.misc_mod)):   # The excess try to attack, but at a penalty
                  if Display:
                     print "A soldier took " + str(dmg) + " damage from an extra's attack"
                  self.soldiers[(i-len(self.soldiers))%len(self.soldiers)] -= dmg   # and if successful they do damage
         self.Eval_group(Display) # Update the soldier's roster and see who fled as a result of this attack.
               
   def Eval_group(self, Display=True):  # Update the soldier's roster and see who fled as a result of this attack.
      for i in range(len(self.soldiers)): # See who attempts to flee combat
         if (self.soldiers[i] <= eval(str(self.flee_expression))) & (self.soldiers[i] >= 1):   # If their HP is below the flee limit and they are alive they try to flee
            if Display:
               print "Soldier " + str(i+1) + " has tried to flee from battle with " + str(self.soldiers[i]) + " HP!"
            self.fled.append(self.soldiers[i])
            self.soldiers[i] = 0
      new_soldiers = [] # The list of soldiers who will remain after the fleeing and casualties
      for i in range(len(self.soldiers)):
         if self.soldiers[i] > 0:   # If they are here and alive they will fight
            new_soldiers.append(self.soldiers[i])
      self.soldiers = []   # Remove the old soldier roster
      for i in new_soldiers:
         self.soldiers.append(i) # And replace it with the new roster
      self.losses = self.initial_solders - len(new_soldiers) #The number of soldier no longer in combat
      self.num_of_soldiers = len(new_soldiers)
      if Display:
         print "Losses to desertion and casualties = " + str(self.losses)
         print "Soldiers ready to fight = " + str(self.num_of_soldiers)

def Basic_Atk(A, B, Display=True): # The anatomy of one group attacking another
   if A.num_of_soldiers > 0:
      if B.num_of_soldiers > 0:
         B.Attacked(A.num_of_soldiers, A.atk_mod + A.misc_mod, A.dmg_expression, 2, Display)
      else:
         B.group_name + " has no soldiers, it is defeated."
   else: 
      print A.group_name + " has no soldiers!  It cannot attack."
      
def Print_Results(A, B):
   print '---------------------------------------------------'
   print A.group_name + ' results'
   A.Print()
   print '\n' + B.group_name + ' results'
   B.Print()
   print '---------------------------------------------------'
   
def Combat(A, B, Display=True): # Group A attacks group B, then group B counter-attacks
   if Display:
      print '\n' + B.group_name + ' is under attack from ' + A.group_name + '!'
   Basic_Atk(A, B, Display)
   if Display:
      print '\n' + A.group_name + ' is under counter-attack from ' + B.group_name + '!'
   Basic_Atk(B, A, Display)
   if Display:
      Print_Results(A, B)
   
def Sneak_Atk(A, B): # Group A attacks group B.  Group B cannot counter-attack
   print '***************************************************'
   print B.group_name + ' is under a sneak attack from ' + A.group_name + '!'
   Basic_Atk(A, B)
   B.Print()
   print '***************************************************'
   
def Volley(A, B):  # Group A attacks group B.  Group B cannot counter-attack.  Relabel of Sneak_Atk for archers
   print '***************************************************'
   print B.group_name + ' takes a volley of fire from ' + A.group_name + '!'
   Basic_Atk(A, B)
   B.Print()
   print '***************************************************'
   
def Mortal_Combat(A, B):   # Fight to the death
   print '###################################################'
   print A.group_name + ' has engaged ' + B.group_name + ' in mortal combat!'
   print 'Battle will continue until only one group remains ready to fight!'
   while (A.num_of_soldiers > 0) & (B.num_of_soldiers > 0):
      Combat(A, B, False)
   print 'Battle has concluded'
   Print_Results(A, B)
   print '###################################################'
   
# Make some operators here so we can use nice shorthand for combat
c = Infix(Combat)
s = Infix(Sneak_Atk)
v = Infix(Volley)
MC = Infix(Mortal_Combat)
