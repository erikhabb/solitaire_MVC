from cardmodel import Card
import random

class SolitaireModel:
  class OutOfRangeError(Exception): pass

  def __init__(self):
    pass

  def newGame(self):
    """Reshuffle and deal cards to start a new game."""

    self.foundation = [[], [], [], []]
    self.tableau = [[], [], [], [], [], [], []]
    self.stock = []
    self.waste = []
    self.faceUp = []

    # add cards to stock
    for suit in Card.suits:
      for rank in Card.ranks:
        self.stock.append(Card(suit, rank))

    # shuffle stock
    random.shuffle(self.stock)

    # deal cards to tableaus
    for i in range(7):
      for j in range(i, 7):
        self.tableau[j].append(self.stock.pop())
        # set top card in tableau face up
        if i == j:
          self.faceUp.append(self.tableau[j][-1])

    pass

  def isGameWon(self):
    """All cards have successfully reached a foundation stack."""
    won = True
    for i in range(4):
      if len(self.foundation[i]) != 13:
        won = False
        break

    return won

  def isCardFaceUp(self, card):
    """Is the given card face up?"""
    return card in self.faceUp

  def getStock(self):
    """Get the face down cards in stock."""
    return list(self.stock)
    pass

  def getWaste(self):
    """Get the top face up card from waste."""
    return list(self.waste)
    pass

  def getFoundation(self, index):
    """Get the cards on foundation 0 <= index < 3."""
    if (index >= 0 and index < len(self.foundation)):
      return list(self.foundation[index])
    else:
      raise self.OutOfRangeError, "index out of range"

  def canDropCardOnFoundation(self, index, card):
    """Can the given card be dropped on the indexth foundation?"""
    if (index >= 0 and index < len(self.foundation)):
      # card must be:
      # - face up
      # - on the end of a tableau or waste, or be an ACE on a foundation
      # - ACE if foundation is empty
      # - rank + 1 of same suit if foundation is not empty
      return self.isCardFaceUp(card) and \
        (any(card == self.tableau[i][-1] for i in range(7) \
             if len(self.tableau[i]) != 0) or \
         (len(self.waste) != 0 and card == self.waste[-1]) or \
         (card.rank == Card.ACE and \
           any(card == self.foundation[i][-1] for i in range(4) \
               if i != index and len(self.foundation[i]) != 0))) and \
        ((len(self.foundation[index]) == 0 and card.rank == Card.ACE) or \
         (len(self.foundation[index]) != 0 and \
          card.suit == self.foundation[index][-1].suit and \
          card.rank == self.foundation[index][-1].rank + 1))
    else:
      raise self.OutOfRangeError, "index out of range"

  def didDropCardOnFoundation(self, index, card):
    """Given card was dropped on the indexth foundation."""
    if (self.canDropCardOnFoundation(index, card)):
      # find card
      # on tableau?
      for i in range(7):
        if (len(self.tableau[i]) != 0 and card == self.tableau[i][-1]):
          self.tableau[i].remove(card)
          break
      # on waste?
      if (len(self.waste) != 0 and card == self.waste[-1]):
        self.waste.remove(card)
      # on foundation?
      for i in range(4):
        if (len(self.foundation[i]) != 0 and card == self.foundation[i][-1]):
          self.foundation[i].remove(card)
          break

      # put card on foundation
      self.foundation[index].append(card)
    else:
      raise self.OutOfRangeError, "index out of range"

  def canFlipCardOnTableau(self, index):
    """Can card flipped from face-down to face-up on the indexth tableau?"""
    if (index >= 0 and index < len(self.tableau)):
      # tableau must be non-empty and last card must be face down
      return (len(self.tableau[index]) != 0 and
          self.isCardFaceUp(self.tableau[index][-1]) == False)
    else:
      raise self.OutOfRangeError, "index out of range"

  def didFlipCardOnTableau(self, index):
    """Card was flipped from face-down to face-up on the indexth tableau."""
    if (index >= 0 and index < len(self.tableau)):
      if self.canFlipCardOnTableau(index):
        self.faceUp.append(self.tableau[index][-1])
    else:
      raise self.OutOfRangeError, "index out of range"

  def getTableau(self, index):
    """Get the cards on tableau index 0 <= index < 7."""
    if (index >= 0 and index < len(self.tableau)):
      return list(self.tableau[index])
    else:
      raise self.OutOfRangeError, "index out of range"

  def canDropCardOnTableau(self, index, card):
    """Can the given card be dropped on the indexth tableau?"""
    if (index >= 0 and index < len(self.tableau)):
      # card must be:
      # - face up
      # - in a tableau, or on the end of waste or foundation
      # - king on empty tableau
      # - rank - 1 of opposite color of top of tableau if tableau is not empty
      return self.isCardFaceUp(card) and \
        ((card in self.tableau[i] for i in range(7) if i != index) or \
         (len(self.waste) != 0 and card == self.waste[-1]) or \
         (card in self.foundation[i][-1] for i in range(4) \
          if len(self.foundation[i]) != 0)) and \
        (len(self.tableau[index]) == 0 and card.rank == Card.KING) or \
        (len(self.tableau[index]) != 0 and \
         ((card.rank == self.tableau[index][-1].rank - 1) and \
          card.color != self.tableau[index][-1].color))
    else:
      raise self.OutOfRangeError, "index out of range"

  def didDropCardOnTableau(self, index, card):
    """Given card was dropped on the indexth tableau."""
    if (self.canDropCardOnTableau(index, card)):
      stack = [card]
      # find card
      # on tableau?
      for i in range(7):
        if (card in self.tableau[i]):
          # TODO: move entire stack
          card_index = self.tableau[i].index(card)
          stack = list(self.tableau[i][card_index:])
          del self.tableau[i][card_index:]
          break
      # on waste?
      if (len(self.waste) != 0 and card == self.waste[-1]):
        self.waste.remove(card)
      # on foundation?
      for i in range(4):
        if (len(self.foundation[i]) != 0 and card == self.foundation[i][-1]):
          self.foundation[i].remove(card)
          break

      # put stack on tableau
      self.tableau[index].extend(stack)
    else:
      raise self.OutOfRangeError, "index out of range"

  def canDealCard(self):
    """Can user move top cards from stock to waste?"""
    return len(self.stock) != 0

  def didDealCard(self):
    """Top cards were dealt from stock to waste."""
    if self.canDealCard():
      for i in range(min(len(self.stock), 3)):
        self.waste.append(self.stock.pop())
        self.faceUp.append(self.waste[-1])
    else:
      raise self.OutOfRangeError, "stock empty"

  def canMoveWasteCardsIntoStock(self):
    """Can user move all waste cards back into stock?"""
    return len(self.stock) == 0 and len(self.waste) != 0

  def didMoveWasteCardsIntoStock(self):
    """User moved all waste cards back into stock."""
    self.stock = self.waste
    self.stock.reverse()
    self.waste = []
    for i in self.stock:
      self.faceUp.remove(i)
    pass

