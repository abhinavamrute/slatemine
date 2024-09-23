import tkinter as tk
from tkinter import font, Scale
import random

class MinesGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Mines-inspired Game")
        self.master.geometry("400x550")
        self.master.configure(bg='#2C3E50')
        
        self.mode = None
        self.tiles = []
        self.tile_states = []
        self.game_active = False
        self.first_click_done = False
        self.clicks = 0
        self.click_limit = 1

        self.create_widgets()

    def create_widgets(self):
        button_font = font.Font(family="Helvetica", size=12, weight="bold")

        control_frame = tk.Frame(self.master, bg='#2C3E50')
        control_frame.pack(pady=10)

        self.win_button = tk.Button(control_frame, text="WIN", command=lambda: self.set_mode("WIN"),
                                    bg='#27AE60', fg='white', font=button_font, width=10)
        self.win_button.grid(row=0, column=0, padx=5)
        
        self.lose_button = tk.Button(control_frame, text="LOSE", command=lambda: self.set_mode("LOSE"),
                                     bg='#C0392B', fg='white', font=button_font, width=10)
        self.lose_button.grid(row=0, column=1, padx=5)

        self.play_button = tk.Button(control_frame, text="PLAY", command=self.start_game,
                                     bg='#3498DB', fg='white', font=button_font, width=10, state=tk.DISABLED)
        self.play_button.grid(row=0, column=2, padx=5)

        self.slider_label = tk.Label(self.master, text="Select Number of Clicks (1-5):", bg='#2C3E50', fg='white', font=button_font)
        self.slider_label.pack(pady=10)

        self.click_slider = Scale(self.master, from_=1, to=5, orient=tk.HORIZONTAL, length=300, bg='#2C3E50', fg='white', 
                                  highlightbackground='#2C3E50', command=self.update_click_limit)
        self.click_slider.pack()

        self.tile_frame = tk.Frame(self.master, bg='#2C3E50')
        self.tile_frame.pack()

        for i in range(5):
            for j in range(5):
                tile = tk.Button(self.tile_frame, width=5, height=2, bg="#34495E", 
                                 command=lambda x=i, y=j: self.click_tile(x, y),
                                 state=tk.DISABLED)
                tile.grid(row=i, column=j, padx=2, pady=2)
                self.tiles.append(tile)

    def update_click_limit(self, val):
        self.click_limit = int(val)

    def set_mode(self, mode):
        self.mode = mode
        self.win_button.config(relief=tk.RAISED if mode != "WIN" else tk.SUNKEN)
        self.lose_button.config(relief=tk.RAISED if mode != "LOSE" else tk.SUNKEN)
        self.play_button.config(state=tk.NORMAL)

    def start_game(self):
        self.game_active = True
        self.first_click_done = False
        self.clicks = 0
        self.generate_tile_states()
        for tile in self.tiles:
            tile.config(bg="#34495E", state=tk.NORMAL)
        self.play_button.config(state=tk.DISABLED)

    def generate_tile_states(self):
        # 20 green tiles and 5 red tiles
        self.tile_states = ['green'] * 20 + ['red'] * 5
        random.shuffle(self.tile_states)

    def click_tile(self, x, y):
        if not self.game_active or self.clicks >= self.click_limit:
            return

        index = x * 5 + y
        self.clicks += 1

        if self.mode == "WIN":
            # In WIN mode, force every clicked tile to be green
            self.force_tile_color(index, 'green')

        elif self.mode == "LOSE":
            # In LOSE mode, if this is the nth click, the tile should be red
            if self.clicks == self.click_limit:
                self.force_tile_color(index, 'red')
            else:
                # Other clicks before the nth should be green
                self.force_tile_color(index, 'green')

        self.reveal_tile(self.tiles[index], self.tile_states[index])

        if self.clicks == self.click_limit or self.mode == "LOSE" and self.tile_states[index] == 'red':
            self.reveal_all_tiles()
            self.end_game()

    def force_tile_color(self, index, color):
        """Ensure the nth clicked tile has a specific color (green or red) and shuffle the rest."""
        if self.tile_states[index] == color:
            return
        if color == 'green':
            swap_index = self.tile_states.index('green')
        else:
            swap_index = self.tile_states.index('red')
        
        self.tile_states[index], self.tile_states[swap_index] = self.tile_states[swap_index], self.tile_states[index]

    def reveal_tile(self, tile, state):
        tile.config(bg=state, state=tk.DISABLED)

    def reveal_all_tiles(self):
        for i, (tile, state) in enumerate(zip(self.tiles, self.tile_states)):
            self.master.after(i * 50, lambda t=tile, s=state: self.reveal_tile(t, s))

    def end_game(self):
        self.game_active = False
        self.play_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    game = MinesGame(root)
    root.mainloop()
