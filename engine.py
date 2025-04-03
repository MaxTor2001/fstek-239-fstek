import tkinter as tk
import os
from tkinter import messagebox
from PIL import Image, ImageTk

# Assuming these dictionaries are defined elsewhere
from ubi_fstec import threats
from comparison_ubi import threats1
from security_239 import information_security_measures, measures1, measures2, measures3

# Set for collecting unique security measures
unique_measures = set()

# Define the order for sorting
order = [
    "IAF.0",
    "IAF.1",
    "IAF.2",
    "IAF.3",
    "UPD",
    "OPS",
    "ZNI",
    "AUD",
    "AVZ",
    "SOV",
    "OCL",
    "ODT",
    "ZTS",
    "ZIS",
    "INC",
    "UKF",
    "OPO",
    "PLN",
    "DNS",
    "IPO",
    "ANZ",
    "ZSV",
]


def save_results():
    selected_threats = [threat for threat, var in checkboxes.items() if var.get() == 1]
    with open("result.txt", "w", encoding="utf-8") as file:
        for key, value in threats1.items():  # Iterate over threats1 dictionary
            if key in selected_threats and value:  # Check selected threat
                threats_list = value.split(",")
                if key in threats:  # Check existence in threats
                    threat_value = threats[key]  # Get value from the threats dictionary
                    file.write(f"{key}: {threat_value}:\n")  # Output both values
                for threat in threats_list:
                    if threat in information_security_measures:
                        unique_measures.add(
                            information_security_measures[threat]
                        )  # Collect unique measures
                        file.write(
                            f"  - {information_security_measures[threat]}\n"
                        )  # Write measure

        # Write unique security measures sorted according to 'order'
        file.write("\nНеобходимо реализовать следующие меры ИБ:\n")
        sorted_measures = sorted(
            unique_measures,
            key=lambda x: order.index(x) if x in order else float("inf"),
        )
        for measure in sorted_measures:
            file.write(f"  - {measure}\n")

        # Check measures for each category
        for i, measures in enumerate([measures1, measures2, measures3], start=1):
            file.write(
                f"\nДля реализации требований ИБ по {i}-ой категории не хватает следующих мер ИБ:\n"
            )
            for measure in measures.values():
                if measure not in unique_measures:
                    file.write(f"  - {measure}\n")

    messagebox.showinfo("Success", "Results saved to result.txt")


def select_all():
    for var in checkboxes.values():
        var.set(1)  # Check all


# Initialize Tkinter window
root = tk.Tk()
photo = tk.PhotoImage(file="bezopasnost.png")
root.iconphoto(False, photo)
root.title("Реализация УБИ мерами 239 приказа ФСТЭК")
root.geometry("800x600+250+250")
root.config(bg="#808080")
root.resizable(False, False)

print("Current Working Directory:", os.getcwd())


# Create a canvas for scrolling
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)
canvas = tk.Canvas(frame)
scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)

# Create checkboxes for the threats
checkboxes = {}  # Initialize checkboxes dictionary


def wrap_text(text, max_length=80):
    """Wraps the text to ensure lines do not exceed max_length and are left-aligned."""
    if len(text) <= max_length:
        return text
    else:
        # Split the text into words and construct lines
        lines = []
        words = text.split(" ")
        current_line = ""

        for word in words:
            if len(current_line) + len(word) + (1 if current_line else 0) <= max_length:
                # If the current line can accommodate the word, add it
                current_line += (
                    " " + word if current_line else word
                )  # Add with a space only if not empty
            else:
                # If the line is too long, start a new line
                lines.append(
                    current_line
                )  # Add the current line without leading spaces
                current_line = word  # Start a new current_line with the next word

        if current_line:  # Add any remaining text
            lines.append(current_line)  # Add the final line

        return "\n".join(lines)  # Join lines with newline characters


# Assuming threats is a dictionary where keys are threat names and values are their descriptions or values
for threat, value in threats.items():  # Use items() to get both key and value
    var = tk.IntVar()  # Create an IntVar for each threat
    checkboxes[threat] = var  # Store the IntVar in the checkboxes dictionary

    # Combine threat and value, then wrap text
    display_text = wrap_text(f"{threat}: {value}")  # Wrap the text if too long
    cb = tk.Checkbutton(
        scrollable_frame, text=display_text, variable=var
    )  # Display the wrapped text
    cb.pack(anchor="w")  # Pack the Checkbutton into the UI

# Create buttons
select_all_button = tk.Button(root, text="Выбрать все 222 УБИ", command=select_all)
select_all_button.pack(pady=5)


save_button = tk.Button(
    root, text="Сохранить результаты в текущем каталоге", command=save_results
)
save_button.pack(pady=10)

root.mainloop()
