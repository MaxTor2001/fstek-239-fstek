import tkinter as tk
import os
from tkinter import messagebox
from PIL import Image, ImageTk

from ubi_fstec import threats
from comparison_ubi import threats1
from security_239 import information_security_measures, measures1, measures2, measures3

unique_measures = set()

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
        for key, value in threats1.items():
            if key in selected_threats and value:
                threats_list = value.split(",")
                if key in threats:
                    threat_value = threats[key]
                    file.write(f"{key}: {threat_value}:\n")
                for threat in threats_list:
                    if threat in information_security_measures:
                        unique_measures.add(information_security_measures[threat])
                        file.write(f"  - {information_security_measures[threat]}\n")

        file.write("\nНеобходимо реализовать следующие меры ИБ:\n")
        sorted_measures = sorted(
            unique_measures,
            key=lambda x: order.index(x) if x in order else float("inf"),
        )
        for measure in sorted_measures:
            file.write(f"  - {measure}\n")

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


root = tk.Tk()
photo = tk.PhotoImage(file="bezopasnost.png")
root.iconphoto(False, photo)
root.title("Реализация УБИ мерами 239 приказа ФСТЭК")
root.geometry("1200x600+250+250")
root.config(bg="#808080")
root.resizable(False, False)

print("Current Working Directory:", os.getcwd())


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

checkboxes = {}


def wrap_text(text, max_length=220):
    """Wraps the text to ensure lines do not exceed max_length and are left-aligned."""
    if len(text) <= max_length:
        return text
    else:
        lines = []
        words = text.split(" ")
        current_line = ""

        for word in words:
            if len(current_line) + len(word) + (1 if current_line else 0) <= max_length:
                current_line += " " + word if current_line else word
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return "\n".join(lines)


for threat, value in threats.items():
    var = tk.IntVar()
    checkboxes[threat] = var

    display_text = wrap_text(f"{threat}: {value}")
    cb = tk.Checkbutton(scrollable_frame, text=display_text, variable=var)
    cb.pack(anchor="w")

select_all_button = tk.Button(root, text="Выбрать все 222 УБИ", command=select_all)
select_all_button.pack(pady=5)


save_button = tk.Button(
    root, text="Сохранить результаты в текущем каталоге", command=save_results
)
save_button.pack(pady=10)

root.mainloop()
