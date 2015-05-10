# Allows the creation of infix operators
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
       
# To create a binary operator just make a function that takes 2 arguments like say
# def my_add (a, b):
#    return a + b
#
# Then we get import this...
# from Infix import Infix   # Lets us make binary infix style operators
#
# Then we make the operator, lets call it p...
# p = Infix(my_add)
#
# Now to use it just put in 
# arg1 |p| arg2
