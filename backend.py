from datetime import datetime
from database import get_connection, create_table

# Always ensure table exists
create_table()

def calculate_gpa(name, course, credits, grades):

    if not name or not course:
        return None, "Name & Course cannot be empty"

    try:
        credits = [float(c) for c in credits]
        grades = [float(g) for g in grades]

        if len(credits) != len(grades):
            return None, "Credits and Grades count must match"

        total_points = sum(c * g for c, g in zip(credits, grades))
        total_credits = sum(credits)

        if total_credits == 0:
            return None, "Total credits cannot be zero"

        gpa = round(total_points / total_credits, 2)

        save_to_db(name, course, credits, grades, gpa)

        return gpa, None

    except ValueError:
        return None, "Only numbers are allowed"


def save_to_db(name, course, credits, grades, gpa):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO records(date, name, course, credits, grades, gpa)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().strftime("%d-%m-%Y"),
            name,
            course,
            ",".join(map(str, credits)),
            ",".join(map(str, grades)),
            gpa
        ))

        conn.commit()
        conn.close()

    except Exception as e:
        print("Database Error:", e)


def get_records():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT date, name, course, gpa FROM records")
        data = cursor.fetchall()

        conn.close()
        return data

    except Exception as e:
        print("Fetch Error:", e)
        return []
    
def clear_all_records():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM records")
        conn.commit()
        conn.close()

        return True, None

    except Exception as e:
        return False, str(e)

