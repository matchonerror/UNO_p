import tkinter as tk
from tkinter import messagebox, simpledialog
from game_UNO import Game, Color, Rank

class UnoGameCanvas(tk.Tk):
    def __init__(self, player_names):
        super().__init__()
        self.title("UNO Game - Canvas Edition")
        self.geometry("800x600")
        self.game = Game(player_names)

        self.canvas = tk.Canvas(self, bg="#333333", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)  # Add a section to display all players' hands

        # Store references to drawn items for updating UI
        self.top_card_text = None
        self.player_info_texts = []
        self.play_button = None
        self.draw_button = None
        self.skip_button = None
        self.selected_card = None  # The currently selected card string
        self.hand_frame = None
        self.player_card_text_items = []
        self.hands_labels={}

        self.create_layout()
        self.update_ui()

        # Bind clicks on the canvas to handle card selections
        self.canvas.bind("<Button-1>", self.canvas_click_handler)


    def create_layout(self):
        # Draw Discard Pile label and top card text
        self.canvas.create_text(400, 50, text="Discard Pile:", font=("Arial", 14), fill="white")
        self.top_card_text = self.canvas.create_text(400, 80, text="Top Card: None", font=("Arial", 14), fill="yellow")

        # Player info section
        # We'll place them at (50, 150, 200...) and so on.
        start_y = 150
        for player in self.game.players:
            t = self.canvas.create_text(50, start_y, text=f"{player.name}: 7 cards", font=("Arial", 12), fill="white", anchor="w")
            self.player_info_texts.append(t)
            start_y += 30
            hand_label = tk.Label(self, text=f"{player.name}'s cards: ", font=("Arial", 12), bg="white")
            hand_label.pack(pady=2,anchor='w')
            self.hands_labels[player.name] = hand_label
        # Interact section (Action Buttons)
        # We'll place actions at bottom center
        y_base = 300
        # "Select Card" label
        self.canvas.create_text(400, y_base, text="Click a card below to select it", font=("Arial", 12), fill="white")

        # Play Card Button
        self.play_button = self.create_button(400, 350, "Play Card", self.play_card)
        # Draw Card Button
        self.draw_button = self.create_button(400, 400, "Draw Card", self.draw_card)


        # We'll show player's cards at the bottom (x ~200, y ~500 and onwards)
        # This will be updated dynamically in update_ui()

    def create_button(self, x, y, text, command):
        # Create a rectangle and text over it for a button
        w = 100
        h = 30
        rect_id = self.canvas.create_rectangle(x - w//2, y - h//2, x + w//2, y + h//2, fill="#444444", outline="white")
        text_id = self.canvas.create_text(x, y, text=text, font=("Arial", 12), fill="white")
        # We associate the text and rect with a callback
        self.canvas.tag_bind(rect_id, "<Button-1>", lambda e: command())
        self.canvas.tag_bind(text_id, "<Button-1>", lambda e: command())
        return (rect_id, text_id)

    def update_ui(self):
        # Update top card
        top_card = self.game.discard_pile[-1] if self.game.discard_pile else "None"

        # Update player's hand
        for player in self.game.players:
            hand_cards = [str(card) for card in player.hand.cards]  # Convert card objects to strings
            self.hands_labels[player.name].config(text=f"{player.name}'s cards: {', '.join(hand_cards)}")
        # Update player info
        for idx, player in enumerate(self.game.players):
            self.canvas.itemconfig(
                self.player_info_texts[idx],
                text=f"{player.name}: {player.hand.nb_of_cards()} cards")
            for item in self.player_card_text_items:
                self.canvas.delete(item)
            self.player_card_text_items.clear()

        # Show cards for all players
        y_start = 100
        card_per_row = 1
        current_player = self.game.players[self.game.current_player]
        if current_player.name == "Player":
            x_center = 325
            y_center = 150

            self.canvas.create_text(
               400, y_center - 40,
                text="Your Cards:",
                font=("Arial", 14),
                fill="white"
            )
            for card_idx, card in enumerate(current_player.hand.cards):
                row = card_idx // card_per_row  # Calculate which row this card is in
                col = card_idx % card_per_row  # Calculate column position
                x_pos = x_center + col * 80  # Adjust spacing between cards
                y_pos_card = y_center + row * 20  # Adjust row spacing

                card_text = str(card)
                card_id = self.canvas.create_text(
                    x_pos, y_pos_card,
                    text=card_text,
                    font=("Arial", 12),
                    fill="yellow",
                    anchor="w"
                )
                self.player_card_text_items.append(card_id)

        for idx, player in enumerate(self.game.players):
            if player.name == 'Player':
                continue
            x_start = 50
            y_pos = y_start + idx * 170
            self.canvas.create_text(
                x_start, y_pos - 20,
                text=f"{player.name}'s cards:",
                font=("Arial", 12),
                fill="white",
                anchor="w"
            )
            for card_idx, card in enumerate(player.hand.cards):
                row = card_idx // card_per_row  # Calculate which row this card is in
                col = card_idx % card_per_row  # Calculate column position
                x_pos = x_start + col * 80  # Adjust spacing between cards
                y_pos_card = y_pos + row * 20  # Adjust row spacing

                card_text = str(card)
                card_id = self.canvas.create_text(
                    x_pos, y_pos_card,
                    text=card_text,
                    font=("Arial", 10),
                    fill="yellow",
                    anchor="w"
                )
                self.player_card_text_items.append(card_id)
    def canvas_click_handler(self, event):
        # Handle clicks on the cards
        # Find all items at the clicked location
        clicked = self.canvas.find_closest(event.x, event.y)
        if clicked:
            item = clicked[0]
            # Check if this item matches a card in player's hand
            if self.game.players[self.game.current_player].name == "Player":
                current_player = self.game.players[self.game.current_player]
                # We can identify a card by comparing the drawn text with their cards
                card_text = self.canvas.itemcget(item, "text")
                if card_text and any(str(c) == card_text for c in current_player.hand.cards):
                    # Selected a card
                    self.selected_card = card_text
                    messagebox.showinfo("Card Selected", f"You selected: {self.selected_card}")

    def play_card(self):
        current_player = self.game.players[self.game.current_player]


        if not self.selected_card:
            messagebox.showerror("Error", "No card selected. Click on a card in your hand first.")
            return

        # Find the selected card in the player's hand
        matching_cards = [card for card in current_player.hand.cards if str(card) == self.selected_card]

        # Select the first matching card if it exists, otherwise None
        selected_card = matching_cards[0] if matching_cards else None

        if selected_card.color == Color.WILD or selected_card.rank == Rank.DRAW_FOUR :
            # Prompt user to select a new color
            valid_colors = [color.name for color in Color if color != Color.WILD]
            new_color = simpledialog.askstring("Wild Card", f"Choose a new color ({', '.join(valid_colors)}):")

            if new_color:
                new_color = new_color.strip().upper()
                if new_color in valid_colors:
                    selected_card.color = Color[new_color]
                    messagebox.showinfo("Color Chosen", f"Card color changed to {new_color}.")
                else:
                    messagebox.showwarning("Invalid Color", "Invalid color selected. Defaulting to RED.")
                    selected_card.color = Color.RED
            else:
                messagebox.showwarning("No Color", "No color selected. Defaulting to RED.")
                selected_card.color = Color.RED

        # Check if the selected card is playable
        top_card = self.game.discard_pile[-1] if self.game.discard_pile else None
        if self.game.single_card_check(top_card, selected_card):
            current_player.play_card(current_player.hand.cards.index(selected_card), self.game.discard_pile)
            self.handle_special_card(selected_card)
            self.game.next_player()
            self.selected_card = None  # Reset selected card after playing
            self.update_ui()
            self.check_game_over()
            self.pc_turns()
        else:
            messagebox.showerror("Error", "This card cannot be played.")

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



    def handle_special_card(self, card):
        if card.rank == "Reverse":
            self.game.direction *= -1
            messagebox.showinfo("Special Card", "Direction reversed!")
        elif card.rank == "Skip":
            messagebox.showinfo("Special Card", "Next player's turn skipped!")
            self.game.next_player()
        elif card.rank == "Draw2":
            next_player = self.game.players[(self.game.current_player + 1) % len(self.game.players)]
            for _ in range(2):
                next_player.draw_card(self.game.deck)
            messagebox.showinfo("Special Card", f"{next_player.name} drew 2 cards!")
        elif card.rank == "Draw4":
            next_player = self.game.players[(self.game.current_player + 1) % len(self.game.players)]
            for _ in range(4):
                next_player.draw_card(self.game.deck)
            messagebox.showinfo("Special Card", f"{next_player.name} drew 4 cards!")
            self.set_new_color(card)
        elif card.rank == "Wild":
            self.set_new_color(card)

    @staticmethod
    def set_new_color(self, card):
        # Ask user for color
        valid_colors = [color.name for color in Color if color != Color.WILD]
        new_color = simpledialog.askstring("Wild Card", f"Choose a new color ({', '.join(valid_colors)}):")

        if new_color:
            new_color = new_color.strip().upper()

        if new_color in valid_colors:
            card.color = Color[new_color]
            messagebox.showinfo("Color Chosen", f"The card color has changed to {new_color}")
        else:
            messagebox.showwarning("Invalid Color", "Invalid color. Defaulting to RED.")
            card.color = Color.RED

    def pc_turns(self):
        while self.game.players[self.game.current_player].name != "Player" and self.game.playing:
            current_player = self.game.players[self.game.current_player]
            top_card = self.game.discard_pile[-1] if self.game.discard_pile else None

            played = False
            for i, c in enumerate(current_player.hand.cards):
                if self.game.single_card_check(top_card, c):
                    current_player.play_card(i, self.game.discard_pile)
                    self.handle_special_card(c)
                    played = True
                    break

            if not played:
                # PC draws a card if can't play
                card = current_player.draw_card(self.game.deck)
                if card and self.game.single_card_check(top_card, card):
                    current_player.play_card(current_player.hand.cards.index(card), self.game.discard_pile)
                    self.handle_special_card(card)

            self.game.next_player()
            self.update_ui()
            self.check_game_over()

    def check_game_over(self):
        for player in self.game.players:
            if player.win_check():  # Use the win_check method to check if the player has won
                self.game.playing = False  # Stop the game
                winner = player.name  # Get the winner's name
                messagebox.showinfo("Game Over", f"Congratulations! {winner} has won!")
                self.quit()
                return  # Exit after handling the game-over logic

if __name__ == "__main__":
    player_names = ["Player", "PC1", "PC2"]
    app = UnoGameCanvas(player_names)
    app.mainloop()