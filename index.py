import tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path


# ==========================================
# JSON DATA STORAGE
# ==========================================

DATA_FILE = Path(__file__).resolve().parent / "food_data.json"


def load_data():
    """Load food records from JSON file."""

    if not DATA_FILE.exists():
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Invalid JSON data format")

        return data

    except (json.JSONDecodeError, OSError, ValueError) as error:
        messagebox.showerror(
            "Storage Error",
            f"Unable to load food data:\n{error}"
        )
        return []


def save_data(data):
    """Save food records into JSON file."""

    try:
        temp_file = DATA_FILE.with_suffix(".tmp")

        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        temp_file.replace(DATA_FILE)
        return True

    except OSError as error:
        messagebox.showerror(
            "Storage Error",
            f"Unable to save data:\n{error}"
        )
        return False


# ==========================================
# MERGE SORT ALGORITHM
# ==========================================

def merge_sort(data):

    # Base condition
    if len(data) <= 1:
        return data

    # Divide
    mid = len(data) // 2

    left = merge_sort(data[:mid])
    right = merge_sort(data[mid:])

    # Conquer and merge
    return merge(left, right)


def merge(left, right):

    result = []

    i = 0
    j = 0

    while i < len(left) and j < len(right):

        # Descending order
        if left[i]["rating"] >= right[j]["rating"]:
            result.append(left[i])
            i += 1

        else:
            result.append(right[j])
            j += 1

    # Add remaining elements
    result.extend(left[i:])
    result.extend(right[j:])

    return result


# ==========================================
# MAIN TKINTER APPLICATION
# ==========================================

class FoodRatingApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Food Rating & Ranking System")
        self.root.geometry("850x650")
        self.root.minsize(700, 550)

        self.root.configure(bg="#F3F4F6")

        self.food_data = load_data()

        self.create_ui()
        self.refresh_table()

    # ======================================
    # CREATE USER INTERFACE
    # ======================================

    def create_ui(self):

        # Main heading
        heading = tk.Label(
            self.root,
            text="Food Rating & Ranking System",
            font=("Arial", 23, "bold"),
            bg="#F3F4F6",
            fg="#1E293B"
        )
        heading.pack(pady=(25, 5))

        subtitle = tk.Label(
            self.root,
            text="Rate food, analyze feedback and discover the best meals",
            font=("Arial", 11),
            bg="#F3F4F6",
            fg="#64748B"
        )
        subtitle.pack(pady=(0, 20))

        # Input frame
        input_frame = tk.Frame(
            self.root,
            bg="white",
            padx=20,
            pady=20
        )
        input_frame.pack(fill="x", padx=35, pady=10)

        # Food Name Label
        tk.Label(
            input_frame,
            text="Food Name",
            font=("Arial", 11, "bold"),
            bg="white"
        ).grid(row=0, column=0, sticky="w", padx=10)

        # Food Name Entry
        self.food_entry = ttk.Entry(
            input_frame,
            width=25,
            font=("Arial", 12)
        )

        self.food_entry.grid(
            row=1,
            column=0,
            padx=10,
            pady=10
        )

        # Food Name Placeholder
        self.food_entry.insert(0, "Enter food name")
        self.food_entry.configure(foreground="grey")

        self.food_entry.bind(
            "<FocusIn>",
            self.clear_name_placeholder
        )

        self.food_entry.bind(
            "<FocusOut>",
            self.add_name_placeholder
        )

        # Rating Label
        tk.Label(
            input_frame,
            text="Rating (1-5)",
            font=("Arial", 11, "bold"),
            bg="white"
        ).grid(row=0, column=1, sticky="w", padx=10)

        # Rating Dropdown
        self.rating_entry = ttk.Combobox(
            input_frame,
            values=["1", "2", "3", "4", "5"],
            width=20,
            state="readonly",
            font=("Arial", 12)
        )

        self.rating_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=10
        )

        # Rating Placeholder
        self.rating_entry.set("Enter food rating")

        # Buttons
        button_frame = tk.Frame(
            input_frame,
            bg="white"
        )

        button_frame.grid(
            row=1,
            column=2,
            padx=10
        )

        ttk.Button(
            button_frame,
            text="Add Food",
            command=self.add_food
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Clear Form",
            command=self.clear_form
        ).pack(side="left", padx=5)

        # ==================================
        # STATISTICS SECTION
        # ==================================

        stats_frame = tk.Frame(
            self.root,
            bg="#F3F4F6"
        )

        stats_frame.pack(fill="x", padx=35, pady=15)

        self.total_label = self.create_stat_card(
            stats_frame, "Total Foods", "0", 0
        )

        self.highest_label = self.create_stat_card(
            stats_frame, "Highest Rated", "-", 1
        )

        self.lowest_label = self.create_stat_card(
            stats_frame, "Lowest Rated", "-", 2
        )

        # ==================================
        # FOOD TABLE
        # ==================================

        table_frame = tk.Frame(
            self.root,
            bg="white",
            padx=15,
            pady=15
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=10
        )

        tk.Label(
            table_frame,
            text="Food Rankings",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#1E293B"
        ).pack(anchor="w", pady=(0, 15))

        columns = ("rank", "food", "rating")

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=10
        )

        self.tree.heading("rank", text="Rank")
        self.tree.heading("food", text="Food Name")
        self.tree.heading("rating", text="Rating")

        self.tree.column("rank", width=100, anchor="center")
        self.tree.column("food", width=350, anchor="center")
        self.tree.column("rating", width=150, anchor="center")

        self.tree.pack(
            fill="both",
            expand=True
        )

        # ==================================
        # ACTION BUTTONS
        # ==================================

        action_frame = tk.Frame(
            self.root,
            bg="#F3F4F6"
        )

        action_frame.pack(pady=15)

        ttk.Button(
            action_frame,
            text="Sort Ratings (Merge Sort)",
            command=self.sort_food
        ).pack(side="left", padx=10)

        ttk.Button(
            action_frame,
            text="Delete Selected",
            command=self.delete_food
        ).pack(side="left", padx=10)

        ttk.Button(
            action_frame,
            text="About Project",
            command=self.show_about_modal
        ).pack(side="left", padx=10)

        # Footer
        tk.Label(
            self.root,
            text="Developed using Python | Tkinter | JSON | Merge Sort",
            font=("Arial", 9),
            bg="#F3F4F6",
            fg="#64748B"
        ).pack(pady=10)

    # ======================================
    # INPUT PLACEHOLDER FUNCTIONS
    # ======================================

    def clear_name_placeholder(self, event):

        if self.food_entry.get() == "Enter food name":

            self.food_entry.delete(0, tk.END)
            self.food_entry.configure(foreground="black")

    def add_name_placeholder(self, event):

        if not self.food_entry.get().strip():

            self.food_entry.insert(0, "Enter food name")
            self.food_entry.configure(foreground="grey")

    # ======================================
    # ABOUT PROJECT MODAL
    # ======================================

    def show_about_modal(self):

        modal = tk.Toplevel(self.root)

        modal.title("About Project")
        modal.geometry("380x320")
        modal.resizable(False, False)

        # Center the modal relative to the main window
        self.root.update_idletasks()

        x = self.root.winfo_x() + (
            self.root.winfo_width() - 380
        ) // 2

        y = self.root.winfo_y() + (
            self.root.winfo_height() - 320
        ) // 2

        modal.geometry(f"380x320+{x}+{y}")

        modal.configure(bg="#F3F4F6")

        # Make the popup modal
        modal.transient(self.root)
        modal.grab_set()

        # Modal heading
        tk.Label(
            modal,
            text="About Project",
            font=("Arial", 20, "bold"),
            bg="#F3F4F6",
            fg="#1E293B"
        ).pack(pady=(25, 15))

        # Project information
        tk.Label(
            modal,
            text="Food Rating & Ranking System",
            font=("Arial", 14, "bold"),
            bg="#F3F4F6",
            fg="#2563EB"
        ).pack(pady=8)

        tk.Label(
            modal,
            text="Developed by: Nithin Manoj",
            font=("Arial", 11),
            bg="#F3F4F6"
        ).pack(pady=5)

        tk.Label(
            modal,
            text="Course: MCA AI & ML",
            font=("Arial", 11),
            bg="#F3F4F6"
        ).pack(pady=5)

        tk.Label(
            modal,
            text="Technologies: Python, Tkinter, JSON",
            font=("Arial", 10),
            bg="#F3F4F6"
        ).pack(pady=5)

        tk.Label(
            modal,
            text="Algorithm: Merge Sort",
            font=("Arial", 11),
            bg="#F3F4F6"
        ).pack(pady=5)

        # Close button
        ttk.Button(
            modal,
            text="Close",
            command=modal.destroy
        ).pack(pady=20)

        modal.focus_set()

    # ======================================
    # STATISTICS CARDS
    # ======================================

    def create_stat_card(self, parent, title, value, column):

        card = tk.Frame(
            parent,
            bg="white",
            padx=15,
            pady=12
        )

        card.grid(
            row=0,
            column=column,
            padx=8,
            sticky="nsew"
        )

        parent.grid_columnconfigure(column, weight=1)

        tk.Label(
            card,
            text=title,
            font=("Arial", 10),
            bg="white",
            fg="#64748B"
        ).pack()

        label = tk.Label(
            card,
            text=value,
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#2563EB"
        )

        label.pack(pady=5)

        return label

    # ======================================
    # ADD FOOD
    # ======================================

    def add_food(self):

        name = self.food_entry.get().strip()
        rating = self.rating_entry.get()

        # Validate input
        if name == "Enter food name" or not name:

            messagebox.showwarning(
                "Input Error",
                "Please enter a food name."
            )
            return

        if rating == "Enter food rating" or not rating:

            messagebox.showwarning(
                "Input Error",
                "Please select a food rating."
            )
            return

        # Prevent duplicate food names
        for item in self.food_data:

            if item["food_name"].casefold() == name.casefold():

                messagebox.showwarning(
                    "Duplicate Food",
                    "This food item already exists."
                )
                return

        food = {
            "food_name": name,
            "rating": int(rating)
        }

        self.food_data.append(food)

        if not save_data(self.food_data):
            self.food_data.pop()
            return

        self.refresh_table()
        self.clear_form()

        messagebox.showinfo(
            "Success",
            "Food rating added successfully!"
        )

    # ======================================
    # SORT FOOD USING MERGE SORT
    # ======================================

    def sort_food(self):

        if not self.food_data:

            messagebox.showwarning(
                "No Data",
                "Please add food items first."
            )
            return

        self.food_data = merge_sort(self.food_data)

        save_data(self.food_data)

        self.refresh_table()

        messagebox.showinfo(
            "Sorting Complete",
            "Food items sorted successfully using Merge Sort!"
        )

    # ======================================
    # DELETE FOOD
    # ======================================

    def delete_food(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Selection Error",
                "Please select a food item to delete."
            )
            return

        if messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this food item?"
        ):

            food_name = self.tree.item(
                selected[0], "values"
            )[1]

            # Locate and remove the actual record
            for index, item in enumerate(self.food_data):

                if item["food_name"] == food_name:

                    deleted_item = self.food_data.pop(index)

                    if not save_data(self.food_data):
                        self.food_data.insert(index, deleted_item)

                    break

            self.refresh_table()

    # ======================================
    # CLEAR INPUT FORM
    # ======================================

    def clear_form(self):

        self.food_entry.delete(0, tk.END)

        self.food_entry.insert(
            0,
            "Enter food name"
        )

        self.food_entry.configure(foreground="grey")

        self.rating_entry.set("Enter food rating")

    # ======================================
    # REFRESH TABLE AND STATISTICS
    # ======================================

    def refresh_table(self):

        # Clear existing rows
        for row in self.tree.get_children():

            self.tree.delete(row)

        # Display records
        for index, item in enumerate(self.food_data, start=1):

            self.tree.insert(
                "",
                tk.END,
                values=(
                    index,
                    item["food_name"],
                    item["rating"]
                )
            )

        # Update statistics
        total = len(self.food_data)

        self.total_label.config(text=str(total))

        if total > 0:

            highest = max(
                self.food_data,
                key=lambda x: x["rating"]
            )

            lowest = min(
                self.food_data,
                key=lambda x: x["rating"]
            )

            self.highest_label.config(
                text=f'{highest["food_name"]} ({highest["rating"]})'
            )

            self.lowest_label.config(
                text=f'{lowest["food_name"]} ({lowest["rating"]})'
            )

        else:

            self.highest_label.config(text="-")
            self.lowest_label.config(text="-")


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    root = tk.Tk()

    app = FoodRatingApp(root)

    root.mainloop()