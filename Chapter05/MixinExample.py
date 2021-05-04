"""This example shows the use of a mixin class"""

class Fruit():

  _taste = 'sweet'

  def taste(self):
    print(f'It tastes {self._taste}')

class PeelableMixin():

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._peeled = False

  def peel(self):
    self._peeled = True

  def taste(self):
    if not self._peeled:
      print('I will peel it first')
      self.peel()
    super().taste()

class Plantain(PeelableMixin, Fruit):

  _taste = 'starchy'

  def peel(self):
    print('It has a tough peel!')
    super().peel()

plantain = Plantain()
plantain.taste()
