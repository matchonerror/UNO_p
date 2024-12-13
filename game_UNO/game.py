import random
from game_UNO import Deck, Player, CardType,Rank,Color



class Game:
    def __init__(self, player_names):
        """
              Initialise le jeu UNO avec les noms des joueurs.
              """
        self.deck = Deck()
        self.discard_pile = []
        self.players = [Player(name) for name in player_names]
        self.current_player = 0
        self.playing = True
        self.direction=1
        self.game_over = False
        self.initialize_game()

    def initialize_game(self):
        """
                Distribue les cartes initiales aux joueurs et place la première carte sur la pile de défausse.
                """
        for player in self.players:
            for i in range(7):
                player.draw_card(self.deck)
        self.deal_initial_card()

    def deal_initial_card(self):
        """
                Distribue la première carte non-action sur la pile de défausse.
                """
        while True:
            top_card = self.deck.deal()
            if top_card is None:

                self.reshuffle_discard_pile()
                top_card = self.deck.deal()

            if top_card.card_type != CardType.ACTION:
                self.discard_pile.append(top_card)
                break
            else:
                self.discard_pile.append(top_card)
                self.deck.cards.insert(0, top_card)  # Put the action card back into the deck

    def reshuffle_discard_pile(self):
        """
              Mélange la pile de défausse et la remet dans le paquet.
              """
        # Remove the top card of the discard pile
        top_card = self.discard_pile.pop()
        # Shuffle the rest of the discard pile into the deck
        random.shuffle(self.discard_pile)
        self.deck.cards = self.discard_pile
        self.discard_pile = [top_card]
    def next_player(self):
        """
               Passe au joueur suivant en fonction de la direction du jeu.
               """
        self.current_player = (self.current_player + self.direction) % len(self.players)

    def play_turn(self):
        """
               Gère le tour du joueur actuel.
               """
        current_player = self.players[self.current_player]
        top_card = self.discard_pile[-1]

        print(f"\n{current_player.name}'s turn")
        print(f"Top card is: {top_card}")
        current_player.hand.cards_in_hand()

        if current_player.win_check():
            print(f"{current_player.name} WON!!")
            self.playing = False
            return

        if current_player.name == "Player":
            self.player_turn(current_player, top_card)
        else:
            self.pc_turn(current_player, top_card)

    def player_turn(self, player, top_card):
        """
           Gère le tour du joueur humain.
           """
        choice = input("\nHit or Pull? (h/p): ")
        if choice == 'h':
            pos = int(input('Enter index of card: '))
            card = player.hand.single_card(pos)
            if self.single_card_check(top_card, card):
                played_card = player.play_card(pos, self.discard_pile)
                self.handle_special_card(played_card, player)
            else:
                print("This card cannot be used.")
        elif choice == 'p':
            card = player.draw_card(self.deck)
            print(f"You drew: {card}")
            if not self.single_card_check(top_card, card):
                self.next_player()

    def pc_turn(self, player, top_card):
        """
               Gère le tour du joueur contrôlé par l'ordinateur.
               """
        for i, card in enumerate(player.hand.cards):
            if self.single_card_check(top_card, card):
                played_card = player.play_card(i, self.discard_pile)
                print(f"PC joue: {played_card}")
                self.handle_special_card(played_card, player)
                return
        print("PC pioche une carte")
        card = player.draw_card(self.deck)
        if self.single_card_check(top_card, card):
            print(f"PC joue: {card}")
            played_card = player.play_card(player.hand.cards.index(card), self.discard_pile)
            self.handle_special_card(played_card, player)
        else:
            self.next_player()

    def single_card_check(self, top_card, card):
        """
             Vérifie si une carte peut être jouée sur la carte du dessus de la pile de défausse.
             """
        return card.color == top_card.color or card.rank == top_card.rank or card.rank == "Wild"

    def handle_special_card(self, card, players):
        if card.rank == "Reverse":
            self.direction *= -1
            print("Direction reversed!")
        elif card.rank == "Skip":
            print("Next player's turn skipped!")
            self.next_player()
        elif card.rank == "Draw2":
            next_player = self.players[(self.current_player + 1) % len(self.players)]
            for _ in range(2):
                next_player.draw_card(self.deck)
            print(f'{next_player.name} draw 2 cards')
        elif card.rank == "Draw4":
            next_player = self.players[(self.current_player + 1) % len(self.players)]
            for _ in range(4):
                next_player.draw_card(self.deck)
            print(f'{next_player.name} draw 4 cards')
            self.set_new_color(card)
        elif card.rank == 'Wild':
            self.set_new_color(card)
    def set_new_color(self, card):
        """
               Permet au joueur de choisir une nouvelle couleur pour une carte Joker.
               """
        valid_colors=[color.value for color in Color if color != Color.WILD] #Comprehension
        new_color=input(f'Choose a new color({valid_colors}):')

        if new_color in valid_colors:
            card.color=new_color
            print(f'Card had changed to {new_color}')
        else:
            print(f'Invalid Color')
            card.color = Color.RED # Default color

    def is_over(self):
        return self.game_over

    def get_winner_name(self):
        """
               Retourne le nom du gagnant si le jeu est terminé.
               """
        if not self.game_over:
            return None
        for p in self.players:
            if len(p.hand) == 0:
                return p.name
        return None


    def start_game(self):
        """ Démarre la boucle principale du jeu.
               """
        while self.playing:
            self.play_turn()
            self.next_player()
