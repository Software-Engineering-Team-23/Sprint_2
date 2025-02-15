import tkinter as tk
from tkinter import messagebox, simpledialog
import sql
from udp import udp_sender
from udp import IP

class firstScreen:
    def __init__(self, window):
        window.title("Entry Terminal")
        window.geometry("800x700")
        window.configure(bg="black")
        self.player_entries = {}  # Key-value dictionary with key=ID_entry and value=name_label

        title = tk.Label(window, text="Edit Game", bg="blue", fg="white", font=("Arial", 27, "bold"))
        title.pack()

        main_frame = tk.Frame(window, bg="gray")
        main_frame.pack(expand=True, fill=tk.BOTH, padx=200, pady=40)

        red_frame = tk.Frame(main_frame, bg="red", width=500, height=900)
        red_frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.make_red_rows(red_frame, "red", 20)

        green_frame = tk.Frame(main_frame, bg="green", width=500, height=900)
        green_frame.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.make_green_rows(green_frame, "green", 20)

        button_frame = tk.Frame(main_frame, bg="gray", width=200, height=300, highlightbackground="black", highlightthickness=4)
        button_frame.pack(pady=5, padx=5)
        button_frame.pack_propagate(False)

        button = tk.Button(button_frame, text="F1 Edit Game", bg="black", fg="white", width=100)
        button.pack(padx=5, pady=5)
        button = tk.Button(button_frame, text="F3 Start Game", bg="black", fg="white", width=100)
        button.pack(padx=5, pady=5)
        button = tk.Button(button_frame, text="F8 View Game", bg="black", fg="white", width=100)
        button.pack(padx=5, pady=5)
        button = tk.Button(button_frame, text="F11 Change Network", bg="black", fg="white", width=100, command=self.change_network)
        button.pack(padx=5, pady=5)
        button = tk.Button(button_frame, text="F12 Clear Game", bg="black", fg="white", width=100, command=self.clear_game)
        button.pack(padx=5, pady=5)

    def change_network(self):
        new_network = simpledialog.askstring("Input", "Enter new network")
        IP = new_network
        print("The new network is:", IP)

    def clear_game(self):
        sql.delete_table("players")  # clearing all SQL player data
        sql.create_table()
        print("Cleared game successfully")

        for entry, name_label in self.player_entries.items():
            entry.delete(0, tk.END)
            name_label.config(text="")

    def make_red_rows(self, frame, bg_color, num_rows):
         #Making labels for ID, equipment ID
        row_frame = tk.Frame(frame, bg=bg_color)
        row_frame.pack(fill=tk.X, padx=5, pady=1)
        label = tk.Label(row_frame, text=f"       Equipment ID", bg=bg_color, font=("Helvetica", 14, "bold"))
        label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        label = tk.Label(row_frame, text=f"Codename", bg=bg_color, font=("Helvetica", 14, "bold"))
        label.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)

        for row in range(num_rows):
            row_frame = tk.Frame(frame, bg=bg_color)
            row_frame.pack(fill=tk.X, padx=5, pady=1)

            label = tk.Label(row_frame, text=f"{row}", bg=bg_color, font=("Helvetica", 20))
            label.pack(side=tk.LEFT, padx=5)

            entry_left = tk.Entry(row_frame, bg="white", fg="black")
            entry_left.field_type = "integer"
            entry_left.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

            name_label = tk.Label(row_frame, bg="white", fg="black")
            self.player_entries[entry_left] = name_label
            name_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

            entry_left.bind("<Return>", lambda event, e=entry_left, r=row: self.submit(e, r))

    def make_green_rows(self, frame, bg_color, num_rows):
             #Making labels for ID, equipment ID
            row_frame = tk.Frame(frame, bg=bg_color)
            row_frame.pack(fill=tk.X, padx=5, pady=1)
            label = tk.Label(row_frame, text=f"       Equipment ID", bg=bg_color, font=("Helvetica", 14, "bold"))
            label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            label = tk.Label(row_frame, text=f"Codename", bg=bg_color, font=("Helvetica", 14, "bold"))
            label.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)

            for row in range(num_rows, num_rows+20):
                row_frame = tk.Frame(frame, bg=bg_color)
                row_frame.pack(fill=tk.X, padx=5, pady=1)

                label = tk.Label(row_frame, text=f"{row}", bg=bg_color, font=("Helvetica", 20))
                label.pack(side=tk.LEFT, padx=5)

                entry_left = tk.Entry(row_frame, bg="white", fg="black")
                entry_left.field_type = "integer"
                entry_left.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

                name_label = tk.Label(row_frame, bg="white", fg="black")
                self.player_entries[entry_left] = name_label
                name_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

                entry_left.bind("<Return>", lambda event, e=entry_left, r=row: self.submit(e, r))
    

    def submit(self, entry, row_number):
        value = entry.get().strip()
        try:
            if value == "":
                self.player_entries[entry].config(text="")
                return
            value = int(value)
        except ValueError:
            messagebox.showerror("Error", "Invalid submission. Enter an integer ID")
            return

        print(f"\nSubmitted ID: {value} (Row {row_number})")
        udp_sender(value)

        players = sql.fetch_players()
        existing_rows = [data[2] for data in players]
        existing_codenames = [data[1] for data in players]

        if row_number in existing_rows:
            try:
                codename = existing_codenames[existing_rows.index(row_number)]
                print(f"Row {row_number} already assigned to '{codename}'")
                messagebox.showinfo("Info", f"Player ID {row_number} already assigned to '{codename}'")
                self.player_entries[entry].config(text=codename)
            except Exception as e:
                print("Error fetching codename: ", e)
        else:
            try:
                print(f"Row {row_number} not found.")
                while True:
                    new_codename = simpledialog.askstring("Input", "Enter new codename")
                    if new_codename and new_codename not in existing_codenames:
                        sql.create_player(player_id=row_number, codename=new_codename)
                        messagebox.showinfo("Info", f"Player ID {row_number} assigned to '{new_codename}'")
                        self.player_entries[entry].config(text=new_codename)
                        break
                    else:
                        messagebox.showerror("Error", "Invalid or duplicate codename")
            except Exception as e:
                print("Error creating new player entry: ", e)

        sql.fetch_players()

window = tk.Tk()
gui = firstScreen(window)
window.mainloop()
