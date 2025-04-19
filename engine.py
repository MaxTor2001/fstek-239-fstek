import tkinter as tk
import os
from tkinter import messagebox

from ubi_fstec import threats
from comparison_ubi import threats1
from security_239 import information_security_measures, measures1, measures2, measures3
from PIL import Image, ImageTk

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
    selected = [t for t, v in checkboxes.items() if v.get()]
    with open("result.txt", "w", encoding="utf-8") as f:
        for key, val in threats1.items():
            if key in selected and val:
                parts = val.split(",")
                if key in threats:
                    f.write(f"{key}: {threats[key]}:\n")
                for p in parts:
                    if p in information_security_measures:
                        unique_measures.add(information_security_measures[p])
                        f.write(f"  - {information_security_measures[p]}\n")

        f.write("\nНеобходимо реализовать следующие меры ИБ:\n")
        sorted_measures = sorted(
            unique_measures,
            key=lambda x: order.index(x) if x in order else float("inf"),
        )
        for m in sorted_measures:
            f.write(f"  - {m}\n")

        for i, meas in enumerate((measures1, measures2, measures3), 1):
            f.write(
                f"\nДля реализации требований ИБ по {i}-ой категории не хватает следующих мер ИБ:\n"
            )
            for m in meas.values():
                if m not in unique_measures:
                    f.write(f"  - {m}\n")

    messagebox.showinfo("Success", "Results saved to result.txt")


def select_all():
    for var in checkboxes.values():
        var.set(1)


root = tk.Tk()
root.title("Реализация УБИ мерами 239 приказа ФСТЭК")
root.geometry("1050x600+250+250")
UNIFORM_BG = "#E8F5E9"  # Светло-зеленый
root.config(bg=UNIFORM_BG)
root.resizable(False, False)


outer = tk.Frame(root, bg="#FFEBEE")  # Светло-розовый
outer.pack(fill="both", expand=True)

canvas = tk.Canvas(outer, bg="#E0E0E0", highlightthickness=0)  # Светло-серый
scrollbar = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
scrollable = tk.Frame(canvas, bg="#E0E0E0")

scrollable.bind(
    "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

checkboxes = {}


def wrap_text(text, max_length=220):
    if len(text) <= max_length:
        return text
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) <= max_length:
            cur += (" " + w) if cur else w
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return "\n".join(lines)


for threat, val in threats.items():
    var = tk.IntVar()
    checkboxes[threat] = var
    text = wrap_text(f"{threat}: {val}")
    cb = tk.Checkbutton(
        scrollable,
        text=text,
        variable=var,
        bg="#E8F5E9",  # Светло-зеленый
        activebackground="#FFCDD2",  # Светло-красный
        selectcolor="#FFAB91",  # Персиковый
        anchor="w",
        justify="left",
        wraplength=1000,
    )
    cb.pack(fill="x", padx=5, pady=1)

btns = tk.Frame(root, bg="#FFF3E0")  # Светло-оранжевый
btns.pack(fill="x", pady=5)

tk.Button(
    btns,
    text="Выбрать все 222 УБИ",
    command=select_all,
    bg="#BCAAA4",  # Светло-коричневый
    activebackground="#FFCCBC",  # Светло-оранжевый
).pack(side="left", padx=20)
tk.Button(
    btns,
    text="Сохранить результаты в текущем каталоге",
    command=save_results,
    bg="#BCAAA4",  # Светло-коричневый
    activebackground="#FFCCBC",  # Светло-оранжевый
).pack(side="right", padx=20)

root.mainloop()
