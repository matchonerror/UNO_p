import tkinter as tk
from tkinter import messagebox
from game_UNO import Game


class UnoGameGUI(tk.Tk):
    def __init__(self, player_names):
        super().__init__()
        self.title("UNO Game")
        self.geometry("800x600")
        self.game = Game(player_names)

        self.create_widgets()
        self.update_ui()

    def create_widgets(self):
        # Discard Pile Section
        self.discard_frame = tk.Frame(self)
        self.discard_frame.pack(pady=10)

        self.discard_label = tk.Label(self.discard_frame, text="Discard Pile: ")
        self.discard_label.pack(side="left", padx=5)

        self.top_card_label = tk.Label(self.discard_frame, text="Top Card: None", font=("Arial", 16))
        self.top_card_label.pack(side="left", padx=5)

        # Player Information Section
        self.player_frame = tk.Frame(self)
        self.player_frame.pack(pady=10)

        self.player_labels = []
        for player in self.game.players:
            lbl = tk.Label(self.player_frame, text=f"{player.name}: 7 cards", font=("Arial", 12))
            lbl.pack(anchor="w")
            self.player_labels.append(lbl)

        # Action Section
        self.action_frame = tk.Frame(self)
        self.action_frame.pack(pady=20)

        # Card Selection
        self.card_label = tk.Label(self.action_frame, text="Select Card:")
        self.card_label.grid(row=0, column=0, padx=5)

        self.card_dropdown = tk.StringVar(self)
        self.card_menu = tk.OptionMenu(self.action_frame, self.card_dropdown, "None")
        self.card_menu.grid(row=0, column=1, padx=5)

        # Action Buttons
        self.play_button = tk.Button(self.action_frame, text="Play Card", command=self.play_card)
        self.play_button.grid(row=1, column=0, columnspan=2, pady=5)

        self.draw_button = tk.Button(self.action_frame, text="Draw Card", command=self.draw_card)
        self.draw_button.grid(row=2, column=0, columnspan=2, pady=5)

        self.skip_button = tk.Button(self.action_frame, text="Skip Turn", command=self.skip_turn)
        self.skip_button.grid(row=3, column=0, columnspan=2, pady=5)

    def update_ui(self):
        # Update Top Card
        top_card = self.game.discard_pile[-1] if self.game.discard_pile else "None"
        self.top_card_label.config(text=f"Top Card: {top_card}")

        # Update Player Info
        for idx, player in enumerate(self.game.players):
            self.player_labels[idx].config(text=f"{player.name}: {player.hand.nb_of_cards()} cards")

        # Update Dropdown for Human Player
        if self.game.players[self.game.current_player].name == "Player":
            self.card_dropdown.set("None")
            menu = self.card_menu["menu"]
            menu.delete(0, "end")
            cards = self.game.players[self.game.current_player].hand.cards
            for card in cards:
                menu.add_command(label=str(card), command=lambda value=card: self.card_dropdown.set(value))

    def play_card(self):
        messagebox.showinfo('Notification','Play_card clicked')

        current_player = self.game.players[self.game.current_player]
        if current_player.name != "Player":
            messagebox.showerror("Error", "It is not your turn!")
            return

        selected_card_name = self.card_dropdown.get()
        if selected_card_name == "None":
            messagebox.showerror("Error", "Please select a card.")
            return

        # Find the selected card in the player's hand
        selected_card = next((card for card in current_player.hand.cards if str(card) == selected_card_name), None)
        if not selected_card:
            messagebox.showerror("Error", "Selected card not found in hand.")
            return

        # Check if the selected card is playable
        top_card = self.game.discard_pile[-1]
        if self.game.single_card_check(top_card, selected_card):
            # Play the card
            current_player.play_card(current_player.hand.cards.index(selected_card), self.game.discard_pile)
            self.game.handle_special_card(selected_card, current_player)
            self.game.next_player()
            self.update_ui()
            self.check_game_over()
            self.pc_turns()
        else:
            messagebox.showerror("Error", "This card cannot be played. Try a different one.")


    def draw_card(self):
        current_player = self.game.players[self.game.current_player]
        if current_player.name != "Player":
            messagebox.showerror("Error", "It is not your turn!")
            return

        card = current_player.draw_card(self.game.deck)
        if card:
            messagebox.showinfo("Draw Card", f"You drew: {card}")
        else:
            messagebox.showwarning("Warning", "The deck is empty!")
        self.update_ui()

    def skip_turn(self):
        current_player = self.game.players[self.game.current_player]
        if current_player.name != "Player":
            messagebox.showerror("Error", "It is not your turn!")
            return

        self.game.next_player()
        self.update_ui()
        self.pc_turns()

    def pc_turns(self):
        while self.game.players[self.game.current_player].name != "Player" and self.game.playing:
            current_player = self.game.players[self.game.current_player]
            top_card = self.game.discard_pile[-1]

            for i, card in enumerate(current_player.hand.cards):
                if self.game.single_card_check(top_card, card):
                    current_player.play_card(i, self.game.discard_pile)
                    self.game.handle_special_card(card, current_player)
                    break
            else:
                card = current_player.draw_card(self.game.deck)
                if card and self.game.single_card_check(top_card, card):
                    current_player.play_card(current_player.hand.cards.index(card), self.game.discard_pile)

            self.game.next_player()
            self.update_ui()
            self.check_game_over()

    def check_game_over(self):
        if not self.game.playing:
            winner = self.game.players[self.game.current_player].name
            messagebox.showinfo("Game Over", f"Congratulations! {winner} has won!")
            self.quit()


if __name__ == "__main__":
    player_names = ["Player", "PC1", "PC2"]
    app = UnoGameGUI(player_names)
    app.mainloop()