"""A sample class definition"""

####################
# Class Definition #
####################

class Banana:
  """A tasty tropical fruit"""

####################
# Class Attributes #
####################

  # class variables are shared by all objects in the class
  food_group = 'fruit'
  colors = ['green', 'green-yellow', 'yellow', 'brown spotted', 'black']

######################
# Methods, instances #
######################

  # Instance methods get the object as an automatic first argument
  # We traditionally call it `self`
  def peel(self):
    """Peel the banana"""
    self.peeled = True

  def set_color(self, color):
    """Set the color of the banana"""
    if color in self.colors:
      # create instance variables by attaching them to `self`
      self.color = color
    else:
      raise ValueError(f'A banana cannot be {color}!')

  # Class methods only have access to the class, not the instance
  # The class is passed in as a first argument
  @classmethod
  def check_color(cls, color):
    """Test a color string to see if it is valid."""
    return color in cls.colors

  @classmethod
  def make_greenie(cls):
    """Create a green banana object"""
    banana = cls()
    banana.set_color('green')
    return banana

  # Static methods have no access to class or instance
  @staticmethod
  def estimate_calories(num_bananas):
    """Given `num_bananas`, estimate the number of calories"""
    return num_bananas * 105

#################
# Magic Methods #
#################

  # "Magic methods" define how our object responds to operators and built-ins
  def __str__(self):
    # "Magic Attributes" contain metadata about the object or class
    return f'A {self.color} {self.__class__.__name__}'

  # __init__ is the most important Magic Method
  def __init__(self, color='green'):

    if not self.check_color(color):
      raise ValueError(f'A {self.__class__.__name__} cannot be {color}')
    self.color = color

    # instance vars should be first declared in __init__ when possible
    self.peeled = False


#################################
# Private and Protected Members #
#################################
  __ripe_colors = ['yellow', 'brown spotted']

  def _is_ripe(self):
    """Protected method to see if the banana is ripe."""
    return self.color in self.__ripe_colors


  def can_eat(self, must_be_ripe=False):
    """Check if I can eat the banana."""
    if must_be_ripe and not self._is_ripe():
      return False
    return True

################
# Sub-classing #
################

class RedBanana(Banana):
  """Bananas of the red variety"""

  colors = ['green', 'orange', 'red', 'brown', 'black']
  botanical_name = 'red dacca'

  def set_color(self, color):
    if color not in self.colors:
      raise ValueError(f'A Red Banana cannot be {color}!')

  def peel(self):
    # Use `super()` to access the parent class methods
    super().peel()
    print('It looks like a regular banana inside!')
