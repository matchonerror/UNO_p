# from enum import Enum
# class Colors(Enum):
#     RED = 1
#     BLUE = 2
#     GREEN = 3
#     YELLOW = 4
# class Value(Enum):
#     ZERO = 0
#     ONE = 1
#     TWO = 2
#     THREE = 3
#     FOUR = 4
#     FIVE = 5
#     SIX = 6
#     SEVEN = 7
#     EIGHT = 8
#     NINE = 9
#     SKIP = "Skip"
#     REVERSE = "Reverse"
#     DRAW_TWO = "Draw Two"
#     DRAW_FOUR = "Draw Four"
#
# class Card:
#     def __init__(self,colors,value):
#         self.colors = colors
#         self.value = value
#     def __repr__(self):
#         return 'Card '+str(self.colors.name)+' '+str(self.value.name)
#
#     # Without .name it will appear like Colors.RED instead of RED
#
#   def match(self,other_card):
#         '''Check if 2 card are match or not (color or values)'''
#         return self.colors==other_card.colors or self.value==other_card.value
#
#
#
# class SkipCard(Card):
#     ''' Skip the turn '''
#     def __init__(self,colors,index_player, direction):
#         super().__init__(colors,'Skip')
#         self.index_player=index_player
#         self.direction = direction
#     def action(self):
#         self.index_player+=self.direction
#         return "Next player is skipped!"
# class ReverseCard(Card):
#     def __init__(self,colors,direction):
#         super().__init__(colors,value='Reverse')
#         self.direction=direction
#     def action(self):
#         self.direction*=-1
#         return "Reverse the play direction"
#
# class Draw_two(Card):
#     def __init__(self,colors,id_g):
#         super().__init__(colors,value='Draw TWo')
#         self.id_g=
#     def action(self):
#

from enum import Enum

class Color(Enum):
    RED = "Red"
    YELLOW = "Yellow"
    GREEN = "Green"
    BLUE = "Blue"
    WILD = 'Wild'
class Rank(Enum):
    ZERO = "0"
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    SKIP = "Skip"
    REVERSE = "Reverse"
    DRAW_TWO = "Draw2"
    WILD = "Wild"
    DRAW_FOUR = "Draw4"

class CardType(Enum):
    NUMBER = "Number"
    ACTION = "Action"

class Card:
    def __init__(self, color: Color, rank: Rank, card_type: CardType):
        self.color = color
        self.rank = rank
        self.card_type = card_type

    def __str__(self):
        return f"{self.color.value} {self.rank.value} ({self.card_type.value})"