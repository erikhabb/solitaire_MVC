from cardmodel import Card
import unittest

class KnownValues(unittest.TestCase):
  def setUp(self):
    # build deck of legal cards
    self.knownValues = tuple((s, r, Card.RED if s in Card.red_suits else Card.BLACK)
        for s in Card.suits
        for r in Card.ranks)

  def testKnownValues(self):
    for suit, rank, color in self.knownValues:
      card = Card(suit, rank)
      self.assertEqual(suit, card.suit)
      self.assertEqual(rank, card.rank)
      self.assertEqual(color, card.color)

  def testUnknownValues(self):
    for rank in Card.ranks:
      self.assertRaises(Card.OutOfRangeError, Card, 5, rank)

    for suit in Card.suits:
      self.assertRaises(Card.OutOfRangeError, Card, suit, 14)

if __name__ == "__main__":
  unittest.main()

