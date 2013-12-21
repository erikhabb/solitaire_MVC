from solitairemodel import SolitaireModel
# from solitaireviewhorz import SolitaireView
from solitaireviewvert import SolitaireView
from cardmodel import Card

class SolitaireController:
  def __init__(self):
    self.model = SolitaireModel()
    self.view = SolitaireView(self.model)
    self.model.newGame()

    # build dictionary of text to cards
    self.cards = {r[0]+s[0]: Card(s[1], r[1])
        for s in (
          ('S', Card.SPADES),
          ('C', Card.CLUBS),
          ('H', Card.HEARTS),
          ('D', Card.DIAMONDS))
        for r in (
          ('A', Card.ACE),
          ('2', Card.TWO),
          ('3', Card.THREE),
          ('4', Card.FOUR),
          ('5', Card.FIVE),
          ('6', Card.SIX),
          ('7', Card.SEVEN),
          ('8', Card.EIGHT),
          ('9', Card.NINE),
          ('10', Card.TEN),
          ('J', Card.JACK),
          ('Q', Card.QUEEN),
          ('K', Card.KING))}

    while not self.model.isGameWon():
      self.view.draw()
      cmd = raw_input("move> ").split(" ")

      # acceptable input:
      # "help" => print commands
      # "quit" => end game
      # "deal" => deal cards from stock to waste
      # "stock" => move waste cards back to stock
      # "flip tx" => flip top card on tableau tx
      # "card stack" => move card to stack (fx, tx)
      unknownCommand = False
      if (cmd[0] == "help"):
        self.view.help()
      elif (cmd[0] == "quit"):
        break
      elif (cmd[0] == "new"):
        self.model.newGame()
      elif (cmd[0] == "deal"):
        if self.model.canDealCard():
          self.model.didDealCard()
        else:
          self.view.dealFailed()
      elif (cmd[0] == "stock"):
        if self.model.canMoveWasteCardsIntoStock():
          self.model.didMoveWasteCardsIntoStock()
        else:
          self.view.stockFailed()
      elif (len(cmd) == 2):
        unknownCommand = True
        if (cmd[0] == "flip"):
          if (cmd[1][0] == "t"):
            try:
              index = int(cmd[1][1])
              if self.model.canFlipCardOnTableau(index):
                self.model.didFlipCardOnTableau(index)
                unknownCommand = False
            except:
              pass
        elif ((cmd[1][0] == "f") or (cmd[1][0] == "t")):
          unknownCommand = True
          # is cmd[1] len 2 and ends in number?
          try:
            if (len(cmd[1]) == 2 and int(cmd[1][1]) in range(7)):
              # does card exist
              if (cmd[0] in self.cards):
                index = int(cmd[1][1])
                card = self.cards[cmd[0]]
                foundation = True if cmd[1][0] == "f" else False

                if foundation:
                  if self.model.canDropCardOnFoundation(index, card):
                    self.model.didDropCardOnFoundation(index, card)
                    unknownCommand = False
                else:
                  if self.model.canDropCardOnTableau(index, card):
                    self.model.didDropCardOnTableau(index, card)
                    unknownCommand = False
          except:
            pass
      else:
        unknownCommand = True

      if (unknownCommand == True):
        self.view.unknownCommand()

    if self.model.isGameWon():
      self.view.draw()
      self.view.gameWon()

if __name__ == "__main__":
  controller = SolitaireController()

