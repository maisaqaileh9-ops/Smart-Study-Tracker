from datetime import date
import csv
import os


RECORDS_FILE = "study_records.csv"


def get_next_session_number():
    if not os.path.exists(RECORDS_FILE):
        return 1

    try:
        with open(RECORDS_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            records = list(reader)

            if not records:
                return 1

            numbers = [int(record["session_number"]) for record in records]
            return max(numbers) + 1

    except (FileNotFoundError, ValueError, KeyError):
        return 1


def create_file_if_needed():
    if not os.path.exists(RECORDS_FILE):
        with open(RECORDS_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow([
                "session_number",
                "date",
                "subject",
                "daily_hours",
                "weekly_hours"
            ])


def add_study_session(session_number):
    print()
    print("Starting a new study session...")
    print()

    name = input("What is your name? ")

    today = date.today()

    print("Hello,", name, "! Let's start studying! 📚")

    subject = input("What subject are you studying today? ")

    print("Today's subject is:", subject)

    while True:
        hours_input = input("How many hours did you study today? ")

        try:
            hours = float(hours_input)

            if hours < 0:
                print("Please enter a positive number.")
                continue

            break

        except ValueError:
            print("Please enter a number.")

    print("Great! You studied", hours, "hours today! 📚")

    if hours >= 3:
        print("Excellent! Keep up the great work! 🌟")
    else:
        print("Good start! Try to study a little more tomorrow! 📚")

    while True:
        days_input = input("How many days did you study this week? ")

        try:
            days = int(days_input)

            if days <= 0:
                print("Please enter a number greater than 0.")
                continue

            break

        except ValueError:
            print("Please enter a whole number.")

    while True:
        weekly_hours_input = input(
            "How many hours did you study this week? "
        )

        try:
            weekly_hours = float(weekly_hours_input)

            if weekly_hours < 0:
                print("Please enter a positive number.")
                continue

            break

        except ValueError:
            print("Please enter a number.")

    weekly_average = round(weekly_hours / days, 2)

    print(
        "Your weekly average is",
        weekly_average,
        "hours per day. 📊"
    )

    if weekly_average >= 3:
        print("Excellent weekly progress! ⭐")
    elif weekly_average >= 2:
        print("Good progress! Keep improving! 💪")
    else:
        print("Try to study a little more next week! 📚")

    with open(
        RECORDS_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            session_number,
            today,
            subject,
            hours,
            weekly_hours
        ])

    print()
    print("Study record saved successfully!")
    print()

    print("--- Study Session Summary ---")
    print("Study Session #", session_number)
    print("Date:", today)
    print("Subject:", subject)
    print("Today's study hours:", hours)
    print("Weekly average:", weekly_average, "hours/day")
    print("Your study session has been added to your records!")

    print()


def view_study_records():
    print()
    print("Your Study Records")
    print("====================")

    create_file_if_needed()

    with open(
        RECORDS_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)
        records = list(reader)

    if not records:
        print("No study records found.")
        return

    for record in records:
        print()
        print("Study Session #", record["session_number"])
        print("Date:", record["date"])
        print("Subject:", record["subject"])
        print("Today's study hours:", record["daily_hours"])
        print("Weekly hours:", record["weekly_hours"])
        print("--------------------")


def delete_study_record():
    print()
    print("Delete a Study Record")
    print("====================")

    create_file_if_needed()

    with open(
        RECORDS_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)
        records = list(reader)

    if not records:
        print("No study records found.")
        return

    print("Your study records:")

    for i, record in enumerate(records, start=1):
        print(
            i,
            "- Session #",
            record["session_number"],
            "-",
            record["subject"]
        )

    try:
        record_number = int(
            input("Enter the record number you want to delete: ")
        )

    except ValueError:
        print("Please enter a valid number.")
        return

    if 1 <= record_number <= len(records):
        deleted_record = records.pop(record_number - 1)

        with open(
            RECORDS_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            fieldnames = [
                "session_number",
                "date",
                "subject",
                "daily_hours",
                "weekly_hours"
            ]

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            writer.writeheader()
            writer.writerows(records)

        print(
            "Study record #",
            deleted_record["session_number"],
            "deleted successfully!"
        )

    else:
        print("Invalid record number.")


create_file_if_needed()

session_number = get_next_session_number()


while True:

    print()
    print("===== Smart Study Tracker =====")
    print()
    print("1. Add a study session")
    print("2. View study records")
    print("3. Delete a study record")
    print("4. Exit")
    print()

    choice = input("Choose an option: ")

    if choice == "1":
        add_study_session(session_number)

        session_number += 1

    elif choice == "2":
        view_study_records()

    elif choice == "3":
        delete_study_record()

    elif choice == "4":
        print()
        print("Thank you for using Smart Study Tracker! 📚")
        break

    else:
        print()
        print("Please choose 1, 2, 3, or 4.")