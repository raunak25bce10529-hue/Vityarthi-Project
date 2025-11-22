import tkinter as tk
from tkinter import ttk, messagebox
from backend import calculate_gpa, get_records, clear_all_records
from graph_tab import plot_gpa


app = tk.Tk()
app.title("GPA / CGPA Calculator")
app.geometry("700x500")
app.configure(bg="#0d1117")

style = ttk.Style(app)
style.theme_use("clam")
style.configure("TLabel", background="#0d1117", foreground="white", font=("Segoe UI", 11))
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
style.configure("TNotebook", background="#0d1117")
style.configure("TFrame", background="#0d1117")

# ---------------- ANIMATION FUNCTION ----------------
def fade_in(window):
    for i in range(0, 11):
        window.attributes('-alpha', i/10)
        window.update()
        window.after(30)

app.attributes('-alpha', 0.0)
fade_in(app)

# ---------------- TABS ----------------
tabs = ttk.Notebook(app)
tabs.pack(expand=1, fill='both')

tab1 = ttk.Frame(tabs)
tab2 = ttk.Frame(tabs)

tabs.add(tab1, text='GPA Calculator')
tabs.add(tab2, text='History')

tab3 = ttk.Frame(tabs)
tabs.add(tab3, text='GPA Graph 📈')


# ---------------- FUNCTIONS ----------------
def handle_calculate():
    name = name_entry.get()
    course = course_entry.get()
    credits = credits_entry.get().split(',')
    grades = grades_entry.get().split(',')

    gpa, error = calculate_gpa(name, course, credits, grades)

    if error:
        messagebox.showerror("Error", error)
    else:
        result_label.config(text=f"GPA: {gpa}")
        load_data()

def load_data():
    for row in tree.get_children():
        tree.delete(row)

    records = get_records()
    for record in records:
        tree.insert('', tk.END, values=record)

# ---------------- TAB 1 UI ----------------

heading = ttk.Label(tab1, text="GPA CALCULATOR", font=("Segoe UI", 16, "bold"))
heading.pack(pady=10)

form = ttk.Frame(tab1)
form.pack(pady=20)

labels = ["Student Name", "Course Name", "Credits (comma separated)", "Grades (comma separated)"]
entries = []

for i, text in enumerate(labels):
    label = ttk.Label(form, text=text)
    label.grid(row=i, column=0, padx=10, pady=10, sticky='w')

    entry = ttk.Entry(form, width=40)
    entry.grid(row=i, column=1, padx=10, pady=10)
    entries.append(entry)

name_entry, course_entry, credits_entry, grades_entry = entries

calc_btn = ttk.Button(tab1, text="Calculate GPA", command=handle_calculate)
calc_btn.pack(pady=10)

result_label = ttk.Label(tab1, text="GPA: --", font=("Segoe UI", 14, "bold"))
result_label.pack(pady=15)

# ---------------- TAB 2 UI ----------------

columns = ("Date", "Name", "Course", "GPA")
tree = ttk.Treeview(tab2, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor='center', width=150)

tree.pack(expand=1, fill='both', padx=10, pady=10)

load_data()

tree.pack(expand=1, fill="both", padx=10, pady=10)

# ---------------- TAB 3 (GRAPH) UI ----------------

graph_heading = ttk.Label(tab3, text="GPA PROGRESS GRAPH", font=("Segoe UI", 14, "bold"))
graph_heading.pack(pady=15)

graph_frame = ttk.Frame(tab3)
graph_frame.pack(pady=20)

graph_label = ttk.Label(graph_frame, text="Enter Student Name:")
graph_label.grid(row=0, column=0, padx=10, pady=10)

graph_entry = ttk.Entry(graph_frame, width=30)
graph_entry.grid(row=0, column=1, padx=10, pady=10)

def show_graph():
    name = graph_entry.get()

    if not name:
        messagebox.showwarning("Input Needed", "Please enter student name")
        return

    status, error = plot_gpa(name)

    if error:
        messagebox.showerror("Error", error)

graph_btn = ttk.Button(tab3, text="Show GPA Graph", command=show_graph)
graph_btn.pack(pady=10)

# ---------- CLEAR HISTORY BUTTON ----------

def clear_history():
    answer = messagebox.askyesno(
        "Confirm Delete",
        "⚠ Are you sure you want to delete ALL records?\nThis action cannot be undone."
    )

    if answer:
        success, error = clear_all_records()

        if success:
            load_data()
            messagebox.showinfo("Cleared", "All records have been deleted.")
        else:
            messagebox.showerror("Error", error)

clear_btn = ttk.Button(tab2, text="Clear History", command=clear_history)
clear_btn.pack(pady=10)



# ---------------- RUN APP ----------------
app.mainloop()
