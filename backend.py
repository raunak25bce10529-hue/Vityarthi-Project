# backend.py
from datetime import datetime
from database import get_connection, create_table

# ensure table exists on import
create_table()

def _to_number_list(value):
    """
    Convert a list or comma-separated string into list of floats.
    Returns (list_of_floats, None) on success or (None, error_message) on failure.
    """
    if value is None:
        return None, "Input is empty"

    if isinstance(value, (list, tuple)):
        items = value
    else:
        # coerce to str and split by comma
        if not isinstance(value, str):
            value = str(value)
        items = [s.strip() for s in value.split(",") if s.strip() != ""]

    if len(items) == 0:
        return None, "No items provided"

    nums = []
    for i, it in enumerate(items):
        try:
            n = float(it)
            nums.append(n)
        except ValueError:
            return None, f"Item #{i+1} ('{it}') is not a number"

    return nums, None


def calculate_gpa(name, course, credits, grades):
    """
    Calculate GPA (weighted average) and save to DB.
    Returns (gpa, None) on success or (None, error_message) on failure.
    """
    if not name or str(name).strip() == "":
        return None, "Student name cannot be empty"
    if not course or str(course).strip() == "":
        return None, "Course name cannot be empty"

    credit_list, err = _to_number_list(credits)
    if err:
        return None, f"Credits error: {err}"

    grade_list, err = _to_number_list(grades)
    if err:
        return None, f"Grades error: {err}"

    if len(credit_list) != len(grade_list):
        return None, "Credits and grades counts do not match"

    total_credits = sum(credit_list)
    if total_credits == 0:
        return None, "Total credits cannot be zero"

    total_points = sum(c * g for c, g in zip(credit_list, grade_list))
    gpa = round(total_points / total_credits, 2)

    try:
        save_to_db(
            name=str(name).strip(),
            course=str(course).strip(),
            credits=credit_list,
            grades=grade_list,
            gpa=gpa
        )
    except Exception as e:
        # Computation succeeded but save failed
        return gpa, f"Computed GPA but failed to save to DB: {e}"

    return gpa, None


def save_to_db(name, course, credits, grades, gpa):
    """
    Save record to the unified table 'records'.
    credits and grades are lists of numbers.
    """
    conn = get_connection()
    cursor = conn.cursor()

    date_str = datetime.now().strftime("%d-%m-%Y")
    credits_str = ",".join(str(int(c)) if float(c).is_integer() else str(c) for c in credits)
    grades_str = ",".join(str(int(g)) if float(g).is_integer() else str(g) for g in grades)

    cursor.execute("""
        INSERT INTO records (date, name, course, credits, grades, gpa)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date_str, name, course, credits_str, grades_str, float(gpa)))

    conn.commit()
    conn.close()


def get_records():
    """
    Returns list of tuples (date, name, course, gpa)
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT date, name, course, gpa FROM records ORDER BY id ASC")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception:
        return []


def clear_all_records():
    """
    Delete all rows from records.
    Returns (True, None) on success, (False, error_message) on failure.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM records")
        conn.commit()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)


# optional small test runner
if __name__ == "__main__":
    tests = [
        ("Raunak Sharma", "B.Tech - CSE", "4,4,3,3,2", "9,8,8,7,9"),
        ("Raunak Sharma", "B.Tech - CSE", [4,4,3,3,2], [6,7,7,6,8]),
    ]
    for name, course, cr, gr in tests:
        gpa, err = calculate_gpa(name, course, cr, gr)
        if err:
            print("ERROR:", err)
        else:
            print(f"{name} GPA = {gpa}")

