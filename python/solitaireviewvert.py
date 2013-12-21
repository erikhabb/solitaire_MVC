from cardmodel import Card
from solitairemodel import SolitaireModel

class SolitaireView:
  def __init__(self, model):
    self.model = model

  def draw(self):
    # get data from model
    stock = self.model.getStock()
    # limit waste to last 3 cards
    waste = self.model.getWaste()
    waste = waste[(-1*(min(3, len(waste)))):]
    foundation = []
    for i in range(4):
      foundation.append(self.model.getFoundation(i))
    tableau = []
    for i in range(7):
      tableau.append(self.model.getTableau(i))

    # print header
    print(" f0  f1  f2  f3   t0  t1  t2  t3  t4  t5  t6  STK  WST")
    print("--- --- --- ---  --- --- --- --- --- --- ---  ---  ---")

    # find longest list from foundation, tableau, stock (show only one card),
    # and waste (already reduced to max length of 3)
    longest = reduce(max,
        [reduce(max, map(len, foundation)),
         reduce(max, map(len, tableau)),
         1,
         len(waste)
        ])
    for i in range(longest):
      # build string
      st = ""
      # add foundation
      for j in range(4):
        st += '{:>3s} '.format(self.model.isCardFaceUp(foundation[j][i]) and \
                               self.card(foundation[j][i]) or "X") \
                               if len(foundation[j]) > i else " " * 4
      st += " "

      # add tableau
      for j in range(7):
        st += '{:>3s} '.format(self.model.isCardFaceUp(tableau[j][i]) and \
                               self.card(tableau[j][i]) or "X") \
                               if len(tableau[j]) > i else " " * 4
      st += " "

      # add stock.  Either X or EMP if first row
      st += '{:>3s} '.format(len(stock) and "X" or "") if i == 0 else " " * 4
      st += " "

      # add waste.  Only top 3 cards
      st += '{:>3s} '.format(self.model.isCardFaceUp(waste[i]) and \
                             self.card(waste[i]) or "X") \
                             if len(waste) > i and i < 3 else " " * 4


      print(st)

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

