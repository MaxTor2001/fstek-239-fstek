import tkinter as tk
from tkinter import messagebox

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
            if key in selected_threats and value:  # Check if it's a selected threat
                threats_list = value.split(",")

                # Compare keys of threats1 with keys of threats
                if key in threats:  # Check if the key exists in the threats dictionary
                    threat_value = threats[
                        key
                    ]  # Get the value from the threats dictionary
                    file.write(f"{key}: {threat_value}:\n")  # Output both values

                for threat in threats_list:  # Iterate over each threat in the list
                    if (
                        threat in information_security_measures
                    ):  # Check against measures
                        unique_measures.add(
                            information_security_measures[threat]
                        )  # Collect unique measures
                        file.write(
                            f"  - {information_security_measures[threat]}\n"
                        )  # Write the measure

        # Write unique security measures sorted according to 'order'
        file.write("\nНеобходимо реализовать следующие меры ИБ:\n")
        sorted_measures = sorted(
            unique_measures,
            key=lambda x: order.index(x) if x in order else float("inf"),
        )

        for measure in sorted_measures:
            file.write(f"  - {measure}\n")

        # New Section: Compare unique measures to each measures category
        for i, measures in enumerate([measures1, measures2, measures3], start=1):
            file.write(
                f"\nДля реализации требований ИБ по {i}-ой категории не хватает следующих мер ИБ:\n"
            )
            sorted_missing_measures = sorted(
                measures.values(),
                key=lambda x: order.index(x) if x in order else float("inf"),
            )

            for measure in sorted_missing_measures:
                if measure not in unique_measures:
                    file.write(f"  - {measure}\n")

    messagebox.showinfo("Success", "Results saved to result.txt")


def select_all():  # New function to select all checkboxes
    for var in checkboxes.values():
        var.set(1)  # Set each variable to 1 (checked)


# Create Tkinter window
root = tk.Tk()
root.title("Select Threats")

# Setup scrollable frame
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Create a canvas for scrolling
canvas = tk.Canvas(frame)
scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

# Configure scrollbar
scrollable_frame.bind(
    "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

# Create window in canvas
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Associate scrollbar with canvas
canvas.configure(yscrollcommand=scrollbar.set)

# Create checkboxes for the threats
checkboxes = {}
for threat in threats:
    var = tk.IntVar()
    checkboxes[threat] = var
    cb = tk.Checkbutton(scrollable_frame, text=threat, variable=var)
    cb.pack(anchor="w")

# Create buttons
select_all_button = tk.Button(
    root, text="Выбрать все 222 УБИ", command=select_all
)  # New button to select all
select_all_button.pack(pady=5)  # Optional: Added padding for better UI

save_button = tk.Button(root, text="Сохранить результаты в текущем каталоге", command=save_results)
save_button.pack(pady=10)

root.mainloop()
