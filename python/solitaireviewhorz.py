from cardmodel import Card
from solitairemodel import SolitaireModel

class SolitaireView:
  def __init__(self, model):
    self.model = model

  def draw(self):
    # get data from model
    stock = self.model.getStock()
    waste = self.model.getWaste()
    foundation = []
    for i in range(4):
      foundation.append(self.model.getFoundation(i))
    tableau = []
    for i in range(7):
      tableau.append(self.model.getTableau(i))

    # stock
    print "stock: %s" % (len(stock) and "X" or "(empty)")

    # waste
    print "waste: %s" % (self.fullStack(waste[-3:]))

    # foundations
    for i in range(4):
      print "f%d: %s" % (i, len(foundation[i]) and \
          self.card(foundation[i][-1] or "(empty)"))

    # tableau
    for i in range(7):
      print "t%d: %s" % (i, self.fullStack(tableau[i]))

    # won
    print "won: %s" % (self.model.isGameWon())

  def help(self):
    print("Available commands:")
    print("   help       => print help")
    print("   quit       => end game")
    print("   new        => new game")
    print("   deal       => deal cards from stock to waste")
    print("   stock      => move waste cards back to empty stock")
    print("   flip tx    => flip top card on tableau tx")
    print("   card stack => move card to stack (fx or tx)")

  def dealFailed(self):
    print "DEAL FAILED"

  def stockFailed(self):
    print "STOCK FAILED"

  def unknownCommand(self):
    print "UNKNOWN COMMAND"

  def gameWon(self):
    print "GAME WON!"

  def fullStack(self, stack):
    if len(stack):
      cards = []
      for c in stack:
        cards.append(self.model.isCardFaceUp(c) and self.card(c) or "X")
      return " ".join(cards)
    else:
      return "(empty)"

  def card(self, card):
    suits = {Card.SPADES:"S",
             Card.CLUBS:"C",
             Card.HEARTS:"H",
             Card.DIAMONDS:"D"}
    ranks = {Card.ACE:"A",
             Card.TWO:"2",
             Card.THREE:"3",
             Card.FOUR:"4",
             Card.FIVE:"5",
             Card.SIX:"6",
             Card.SEVEN:"7",
             Card.EIGHT:"8",
             Card.NINE:"9",
             Card.TEN:"10",
             Card.JACK:"J",
             Card.QUEEN:"Q",
             Card.KING:"K"}

    return ranks[card.rank] + suits[card.suit]

