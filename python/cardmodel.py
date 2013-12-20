class Card:
  class OutOfRangeError(Exception): pass

  SPADES = 1
  CLUBS = 2
  HEARTS = 3
  DIAMONDS = 4
  suits = (SPADES, CLUBS, HEARTS, DIAMONDS)

  ACE = 1
  TWO = 2
  THREE = 3
  FOUR = 4
  FIVE = 5
  SIX = 6
  SEVEN = 7
  EIGHT = 8
  NINE = 9
  TEN = 10
  JACK = 11
  QUEEN = 12
  KING = 13
  ranks = (ACE, TWO, THREE, FOUR, FIVE, SIX, SEVEN,
           EIGHT, NINE, TEN, JACK, QUEEN, KING)

  BLACK = 0
  RED = 1
  black_suits = (SPADES, CLUBS)
  red_suits = (DIAMONDS, HEARTS)

  def __init__(self, suit, rank):
    if (suit in self.suits and rank in self.ranks):
      self.suit = suit
      self.rank = rank
      self.color = self.RED if (suit in self.red_suits) else self.BLACK
    else:
      raise self.OutOfRangeError, "suit or rank out of range"

  def __eq__(self, other):
    return self.suit == other.suit and self.rank == other.rank

  def suit(self):
    return self.suit

  def rank(self):
    return self.rank

  def color(self):
    return self.color

