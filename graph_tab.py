import matplotlib.pyplot as plt
from database import get_connection


def get_student_gpa_progress(name):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT date, gpa 
            FROM records 
            WHERE name = ? 
            ORDER BY id ASC
        """, (name,))

        data = cursor.fetchall()
        conn.close()

        return data

    except Exception as e:
        print("Graph Fetch Error:", e)
        return []


def plot_gpa(name):
    data = get_student_gpa_progress(name)

    if not data:
        return None, "No record found for this student."

    dates = [row[0] for row in data]
    gpas = [row[1] for row in data]

    plt.figure(figsize=(8, 5))
    plt.plot(dates, gpas, marker="o")
    plt.title(f"GPA Progress of {name}")
    plt.xlabel("Date / Semester")
    plt.ylabel("GPA")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    plt.show()
    return True, None
