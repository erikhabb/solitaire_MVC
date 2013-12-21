from solitairemodel import SolitaireModel
from cardmodel import Card
import unittest

class StartOfGame(unittest.TestCase):
  def setUp(self):
    # start game
    self.game = SolitaireModel()
    self.game.newGame()

  def testCorrectNewGame(self):
    self.assertEqual(self.game.isGameWon(), False)
    stock = self.game.getStock()
    self.assertEqual(len(stock), 24)
    waste = self.game.getWaste()
    self.assertEqual(len(waste), 0)
    for i in range(4):
      f = self.game.getFoundation(i)
      self.assertEqual(len(f), 0)
    for i in range(7):
      t = self.game.getTableau(i)
      self.assertEqual(len(t), i + 1)
      self.assertEqual(self.game.isCardFaceUp(t[-1]), True)
    self.assertEqual(self.game.canDealCard(), True)
    self.assertEqual(self.game.canMoveWasteCardsIntoStock(), False)

  def testStockWaste(self):
    # verify stock and waste behavior
    stock = self.game.getStock()
    self.assertEqual(len(stock), 24)
    waste = self.game.getWaste()
    self.assertEqual(len(waste), 0)
    for c in stock:
      self.assertEqual(self.game.isCardFaceUp(c), False)
    for c in waste:
      self.assertEqual(self.game.isCardFaceUp(c), True)
    initialStock = stock

    # perform multiple deals
    for i in range(8):
      self.assertEqual(self.game.canDealCard(), True)
      self.assertEqual(self.game.canMoveWasteCardsIntoStock(), False)
      self.game.didDealCard()
      stock = self.game.getStock()
      self.assertEqual(len(stock), 24 - (3*(i+1)))
      waste = self.game.getWaste()
      self.assertEqual(len(waste), 3*(i+1))
      for c in stock:
        self.assertEqual(self.game.isCardFaceUp(c), False)
      for c in waste:
        self.assertEqual(self.game.isCardFaceUp(c), True)
      self.assertEqual(stock, initialStock[0:-(3*(i+1))])
      w = initialStock[-3*(i+1):]
      w.reverse()
      self.assertEqual(waste, w)

    # should be back at the start
    self.assertEqual(self.game.canDealCard(), False)
    self.assertRaises(SolitaireModel.OutOfRangeError, self.game.didDealCard)
    self.assertEqual(self.game.canMoveWasteCardsIntoStock(), True)
    self.game.didMoveWasteCardsIntoStock()
    stock = self.game.getStock()
    self.assertEqual(len(stock), 24)
    self.assertEqual(stock, initialStock)
    waste = self.game.getWaste()
    self.assertEqual(len(waste), 0)
    self.assertEqual(self.game.canDealCard(), True)
    self.assertEqual(self.game.canMoveWasteCardsIntoStock(), False)
    for c in stock:
      self.assertEqual(self.game.isCardFaceUp(c), False)
    for c in waste:
      self.assertEqual(self.game.isCardFaceUp(c), True)

  def testMoveToFoundation(self):
    # keep dealing until we get an ACE on the end of a tableau
    done = False
    while (not done):
      for i in range(7):
        t = self.game.getTableau(i)
        if self.game.isCardFaceUp(t[-1]) and t[-1].rank == Card.ACE:
          # test moves to foundation
          card = t[-1]
          for j in range(4):
            self.assertEqual(self.game.canDropCardOnFoundation(j, card), True)
          # move card to all foundations
          for j in range(4):
            self.game.didDropCardOnFoundation(j, card)
            f = self.game.getFoundation(j)
            self.assertEqual(len(f), 1)
            self.assertEqual(card, f[-1])
            # try moving to other foundations
            for k in range(4):
              self.assertEqual(self.game.canDropCardOnFoundation(k, card),
                  False if j == k else True)

          done = True
          break
      if not done:
        # deal again
        self.game.newGame()

  def testOutOfRange(self):
    self.assertRaises(SolitaireModel.OutOfRangeError, self.game.getFoundation, -1)
    self.assertRaises(SolitaireModel.OutOfRangeError, self.game.getFoundation, 4)
    self.assertRaises(SolitaireModel.OutOfRangeError, self.game.getTableau, -1)
    self.assertRaises(SolitaireModel.OutOfRangeError, self.game.getTableau, 7)
    t = self.game.getTableau(0)
    self.assertEqual(len(t), 1)
    self.assertRaises(SolitaireModel.OutOfRangeError,
        self.game.canDropCardOnFoundation, -1, t[0])
    self.assertRaises(SolitaireModel.OutOfRangeError,
        self.game.canDropCardOnFoundation, 4, t[0])
    self.assertRaises(SolitaireModel.OutOfRangeError,
        self.game.didDropCardOnFoundation, -1, t[0])
    self.assertRaises(SolitaireModel.OutOfRangeError,
        self.game.didDropCardOnFoundation, 4, t[0])
    self.assertRaises(SolitaireModel.OutOfRangeError,
        self.game.canFlipCardOnTableau, -1)
    self.assertRaises(SolitaireModel.OutOfRangeError,
        self.game.canFlipCardOnTableau, -7)

if __name__ == "__main__":
  unittest.main()

