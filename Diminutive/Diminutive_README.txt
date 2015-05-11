Diminutive Combat Engine Users Guide:

###########################################################

1) What is Diminutive?:
The Diminutive Combat Engine, or simply Diminutive, is designed to simulate combat between arbitrary numbers of soldiers under D&D like rules.  This system is based of the rules described by Jesse Birmingham and the name is an homage to MASSIVE (Multiple Agent Simulation System in Virtual Environment), the software that produced the battles in The Lord of the Rings Movies.

###########################################################

2) Diminutive Features:
Diminutive allows for the creation of groups of units as well as a means for them to interact in a combat setting with each other as well as player characters.

###########################################################

3) Diminutive Use:
Currently Diminutive is a simple extension of the Python interpreter.  As such it is run from within a interactive Python shell such as IDLE or a terminal.
To load Diminutive type "from Diminutive import *" when you see the prompt (it looks like '>>>' ).  Now you have the full suite of tools Diminutive offers you.  Now lets take a look at these tools.

   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   3A) Groups:
   The fundamental element in Diminutive is the Group.  A Group is a simply a group of soldiers.  They are defined by certain parameters like the number of soldiers in the group,  their HP, their AC, their modifiers, the damage they can deal, and their name.  The certain values can be represented as "expressions".  An example of an expression could be that each soldier can do "1 + 1d6" points of damage.  The "1 + 1d6" is an expression.

   A quick note on dice:  Dice are expressed here in a particular notation.  1d6 would be entered in as (1|d|6),  this notation may be a bit longer than standard D&D style dice notation, however you are completely free to roll ANY type of dice you can imagine, such as a 1d13 (that's (1|d|13) in our notation).  To gain familiarity with this notation I suggest playing with it in the Dungeon Masters Desktop Calculator.

   So let's make a group by a quick example.  Jesse wants a group of 10 soldiers with 5+(2|d|2) HP, 14 AC, 1+(1|d|3) Damage, +1 modifier to magic resistance, +1 attack bonus, +1 miscellaneous modifier that effects all their actions, will attempt to flee if their HP is between 1 and (1|d|2), and is named "The Red Dragoons".  We would make this group as follows.

   First decide what to name this group instance in the compiler.  Let's name the group after the player who controls is for simplicity.  Now at the prompt ('>>>' type the following:
      Jesse = Group( 10, "5+(2|d|2)", 14, "1+(1|d|3)", 1, 1, 1, "1|d|2", "The Red Dragoons")
   Congratulations, you now have a group of soldiers at your command.
   
      -----------------------------------------------------
      3A.1) Properties of a Group:
      The following are properties of a group and can be accessed or changed via the interpreter.  At the prompt type:
      Group_Name.property
      To see it's value.  You can also change these values as follows:
      Group_Name.property = new_value_or_expression
      
         __________________________________________________
         3A.1.a) The property list
         num_of_soldiers    # Number of soldiers in this group
         initial_solders    # Initial number of soldiers
         unit_ac            # The unit's armor class.  Used to avoid physical damage from combat. Effects unit vs. unit interaction
         magic_mod          # Units resistance to magic Effects player vs. group action via magic
         atk_mod            # Effects the ability of unit's to land a physical attack.
         misc_mod           # Modifies all saves, resistances, etc.
         dmg_expression     # Describes the damage each soldier can deal
         group_name         # The name of the group
         losses             # Losses sustained
         flee_expression    # Condition against soldiers current HP to see if he attempts to flees combat

   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   3B) Combat:
   For basic inter-unit combat of course we will need another group.  I'll make the same group basically for an example:
       Kevin = Group( 10, "5+(2|d|2)", 14, "1+(1|d|3)", 1, 1, 1, "1|d|2", "The Protectors")

   Now that we have two groups we can have them attack each other, sneak attack each other, Fire volley's at each other, or fight to the death.  Let's start with Jesse sneak attacking Kevin.  A sneak attack is defined here as the first group attacks the second, but the second may not counter attack.  At the prompt we would type:

   Sneak_Atk( Jesse, Kevin)

   The |s| operator is shorthand notation for the Sneak_Atk function above.  Both are equivalent. We could have entered "Jesse |s| Kevin" and had the same effect as above.
   We will see that Diminutive will output the status of the Group that was sneak attacked.

   Jesse could also launch a volley of arrows from an archer unit called Jesse_Archers at Kevin's unit in a in a similar way:

   Volley( Jesse_Archers, Kevin)

   Jesse_Archers |v| is the shorthand notation for this.  A Volley attack is exactly the same as a sneak attack, it's just called a volley.

   Of course we could have the two units engage each other in combat.  To do this have their player controllers roll initiative for the group and whoever's higher goes first.  Let's say Kevin beats Jesse's initiative so his group gets to attack first, and then Jesse's group gets to counter attack.  We would do this as follows:

   Combat(Kevin, Jesse)

   Or Kevin |c| Jesse in our shorthand.

   Finally you can have the two units fight until only one units remains on the field.  That would be done as follows:

   Mortal_Combat( Kevin, Jessse)

   Or Kevin |MC| Jesse

   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   3C) Magic:
   As a player character you can perform magic upon your soldiers, and so can your adversaries!  Magic can effect any property of  a group via the direct assignment mentioned in 3A.1.  Such assignment effects all members of the group are applicable.  The only direct modifications that cannot be made with any effect to a group is the num_of_soldiers, initial_soldiers, and losses.  Other properties such as the HP expression can also be changed, but will have no effect so it is not included.
   
   Arcane Magic can also be used to inflict damage on a group, and Divine Magic can be used to restore HP to a group or to an individual.  Both healing and damaging magics are access via a few functions.
   
      -----------------------------------------------------
      3C.1) Group HP effects:
      There is one function which handles HP changes to groups, HP_Change.  It can be invoked with an effect, an optional resistance, and an optional multiplier.
      The effect can be a number, a roll, or any combination.  Example: 1+1d3 points healing would be "1+(1|d|3)", 1+1d3 point damage could be either "-1-(1|d|3)" or you could use the multiplier, but only if you also include a resistance.  The resistance is the difficulty of resisting the spell's effects.  The multiplier argument simply multiplies the effect by this value.
      
      To call this function on the group Jesse just type the following at the prompt (>>>):
      
      Jesse.HP_change(effect, resistance, multiplier) 
      
      -----------------------------------------------------
      3C.2) Single Unit HP effects:
      Similarly to the Group HP effect method there is one function which handles HP changes to individual units chosen at random, HP_Change_unit.  It can be invoked with an effect, an optional resistance, and an optional multiplier.  The effect can be a number, a roll, or any combination.  Example: 1+1d3 points healing would be "1+(1|d|3)", 1+1d3 point damage could be either "-1-(1|d|3)" or you could use the multiplier, but only if you also include a resistance.  The resistance is the difficulty of resisting the spell's effects.  The multiplier argument simply multiplies the effect by this value.
      
      To call this function on the group Jesse just type the following at the prompt (>>>):
      
      Jesse.HP_change_unit(effect, resistance, multiplier) 
            
      -----------------------------------------------------
      3C.3) Group Instant Death Effects:
      The Kill function will impose an instant death effect against a group of units.  It's called with only an optional resistance to save against.
      Example:
      
      Jesse.Kill() # Kills all the units in this group
      Jesse.Kill(14) # Kills all units that do not make the spell resistance of 14
      
      -----------------------------------------------------
      3C.4) Single Unit Instant Death Effects:
      The Kill_unit function will impose an instant death effect against a single random unit in a group.  It's called with only an optional resistance to save against.
      Example:
      
      Jesse.Kill_unit() # Kills a random unit in this group
      Jesse.Kill_unit(14) # Kills a random unit that does not make the spell resistance of 14
      
