# graph_tab.py
import matplotlib.pyplot as plt
from database import get_connection

def get_student_gpa_progress(name):
    """
    Returns list of tuples (date, gpa) ordered by id ascending for the given name.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT date, gpa FROM records WHERE name = ? ORDER BY id ASC", (name,))
        data = cursor.fetchall()
        conn.close()
        return data
    except Exception as e:
        print("Graph fetch error:", e)
        return []

def plot_gpa(name):
    """
    Plot GPA for a student. Returns (True, None) on success, (None, error_message) on failure.
    """
    if not name or str(name).strip() == "":
        return None, "Student name cannot be empty"

    data = get_student_gpa_progress(name.strip())
    if not data:
        return None, "No record found for this student."

    dates = [d[0] for d in data]
    gpas = [float(d[1]) for d in data]

    try:
        plt.figure(figsize=(8, 4.5))
        plt.plot(dates, gpas, marker='o', linestyle='-', linewidth=2)
        plt.title(f"GPA Progress of {name}")
        plt.xlabel("Date")
        plt.ylabel("GPA")
        plt.ylim(0, max(10, max(gpas) + 1))  # reasonable y-axis
        plt.xticks(rotation=45, ha='right')
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        return True, None
    except Exception as e:
        return None, f"Plotting error: {e}"
