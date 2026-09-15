import tkinter as tk
from tkinter import messagebox
from datetime import date
import csv
import os


RECORDS_FILE = "study_records.csv"
GOAL_FILE = "weekly_goal.txt"
REPORT_FILE = "study_report.txt"


# =========================
# File Management
# =========================

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


def load_records():
    create_file_if_needed()

    with open(
        RECORDS_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)
        return list(reader)


def save_records(records):
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


def get_next_session_number():
    records = load_records()

    if not records:
        return 1

    numbers = [
        int(record["session_number"])
        for record in records
    ]

    return max(numbers) + 1


# =========================
# Weekly Goal
# =========================

def get_weekly_goal():

    if not os.path.exists(GOAL_FILE):
        return 0

    try:

        with open(
            GOAL_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return float(file.read().strip())

    except ValueError:
        return 0


def save_weekly_goal(goal):

    with open(
        GOAL_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(str(goal))


# =========================
# Add Study Session
# =========================

def add_study_session():

    form_window = tk.Toplevel(window)

    form_window.title(
        "Add Study Session"
    )

    form_window.geometry(
        "450x650"
    )

    form_window.configure(
        bg="#F5F7FA"
    )

    tk.Label(
        form_window,
        text="Add Study Session 📚",
        bg="#F5F7FA",
        fg="#2C3E50",
        font=("Arial", 20, "bold")
    ).pack(pady=15)

    def create_label(text):

        tk.Label(
            form_window,
            text=text,
            bg="#F5F7FA",
            fg="#2C3E50",
            font=("Arial", 11, "bold")
        ).pack(pady=3)

    create_label("Your Name")

    name_entry = tk.Entry(
        form_window,
        font=("Arial", 12),
        width=30
    )

    name_entry.pack(pady=3)

    create_label("Subject")

    subject_entry = tk.Entry(
        form_window,
        font=("Arial", 12),
        width=30
    )

    subject_entry.pack(pady=3)

    create_label("Today's Study Hours")

    hours_entry = tk.Entry(
        form_window,
        font=("Arial", 12),
        width=30
    )

    hours_entry.pack(pady=3)

    create_label("Days Studied This Week")

    days_entry = tk.Entry(
        form_window,
        font=("Arial", 12),
        width=30
    )

    days_entry.pack(pady=3)

    create_label("Weekly Study Hours")

    weekly_hours_entry = tk.Entry(
        form_window,
        font=("Arial", 12),
        width=30
    )

    weekly_hours_entry.pack(pady=3)

    create_label("Weekly Study Goal 🎯")

    goal_entry = tk.Entry(
        form_window,
        font=("Arial", 12),
        width=30
    )

    goal_entry.pack(pady=3)

    old_goal = get_weekly_goal()

    if old_goal > 0:

        goal_entry.insert(
            0,
            str(old_goal)
        )

    result_label = tk.Label(
        form_window,
        text="",
        bg="#F5F7FA",
        fg="#2C3E50",
        font=("Arial", 10, "bold"),
        wraplength=380
    )

    result_label.pack(pady=10)

    def save_study_session():

        name = name_entry.get().strip()
        subject = subject_entry.get().strip()

        if not name or not subject:

            result_label.config(
                text="Please fill in your name and subject."
            )

            return

        try:

            hours = float(
                hours_entry.get()
            )

            days = int(
                days_entry.get()
            )

            weekly_hours = float(
                weekly_hours_entry.get()
            )

            weekly_goal = float(
                goal_entry.get()
            )

        except ValueError:

            result_label.config(
                text="Please enter valid numbers."
            )

            return

        if hours < 0:

            result_label.config(
                text="Study hours cannot be negative."
            )

            return

        if days <= 0:

            result_label.config(
                text="Days studied must be greater than 0."
            )

            return

        if weekly_hours < 0:

            result_label.config(
                text="Weekly hours cannot be negative."
            )

            return

        if weekly_goal <= 0:

            result_label.config(
                text="Weekly goal must be greater than 0."
            )

            return

        weekly_average = round(
            weekly_hours / days,
            2
        )

        if hours >= 3:

            study_message = (
                "Excellent study session! 🌟"
            )

        elif hours >= 2:

            study_message = (
                "Good job! Keep going! 💪"
            )

        else:

            study_message = (
                "Try to study a little more next time! 📚"
            )

        save_weekly_goal(
            weekly_goal
        )

        session_number = get_next_session_number()

        today = date.today()

        records = load_records()

        records.append({

            "session_number": str(
                session_number
            ),

            "date": str(today),

            "subject": subject,

            "daily_hours": str(
                hours
            ),

            "weekly_hours": str(
                weekly_hours
            )
        })

        save_records(records)

        result_label.config(

            text=
            f"Saved successfully! ⭐\n\n"
            f"{study_message}\n"
            f"Weekly average: "
            f"{weekly_average} hours/day\n"
            f"Weekly goal: "
            f"{weekly_goal} hours"

        )

        name_entry.delete(
            0,
            tk.END
        )

        subject_entry.delete(
            0,
            tk.END
        )

        hours_entry.delete(
            0,
            tk.END
        )

        days_entry.delete(
            0,
            tk.END
        )

        weekly_hours_entry.delete(
            0,
            tk.END
        )

    tk.Button(

        form_window,

        text="Save Study Session",

        font=("Arial", 13, "bold"),

        width=22,

        bg="#DCE6F1",

        fg="#2C3E50",

        command=save_study_session

    ).pack(pady=10)


# =========================
# Dashboard
# =========================

def show_dashboard():

    dashboard_window = tk.Toplevel(
        window
    )

    dashboard_window.title(
        "Dashboard"
    )

    dashboard_window.geometry(
        "850x720"
    )

    dashboard_window.configure(
        bg="#F5F7FA"
    )

    tk.Label(

        dashboard_window,

        text="Study Dashboard 📊",

        font=("Arial", 24, "bold"),

        bg="#F5F7FA",

        fg="#2C3E50"

    ).pack(pady=15)

    tk.Label(

        dashboard_window,

        text="Your study progress at a glance",

        font=("Arial", 12),

        bg="#F5F7FA",

        fg="#2C3E50"

    ).pack(pady=3)

    records = load_records()

    if not records:

        tk.Label(

            dashboard_window,

            text="No study data available yet.",

            font=("Arial", 13),

            bg="#F5F7FA",

            fg="#2C3E50"

        ).pack(pady=50)

        return

    total_sessions = len(
        records
    )

    total_hours = round(
        sum(
            float(record["daily_hours"])
            for record in records
        ),
        2
    )

    weekly_hours = round(
        sum(
            float(record["weekly_hours"])
            for record in records
        ),
        2
    )

    average_hours = round(
        total_hours / total_sessions,
        2
    )

    weekly_goal = get_weekly_goal()

    if weekly_goal > 0:

        progress = round(
            (weekly_hours / weekly_goal) * 100,
            1
        )

        remaining_hours = max(
            round(
                weekly_goal - weekly_hours,
                2
            ),
            0
        )

    else:

        progress = 0
        remaining_hours = 0

    progress_display = min(
        progress,
        100
    )

    cards_frame = tk.Frame(
        dashboard_window,
        bg="#F5F7FA"
    )

    cards_frame.pack(
        pady=15
    )

    def create_card(
        row,
        column,
        icon,
        title,
        value
    ):

        card = tk.Frame(

            cards_frame,

            bg="#DCE6F1",

            width=185,

            height=125

        )

        card.grid(

            row=row,

            column=column,

            padx=8,

            pady=8

        )

        card.pack_propagate(
            False
        )

        tk.Label(

            card,

            text=icon,

            font=("Arial", 22),

            bg="#DCE6F1"

        ).pack(
            pady=(8, 2)
        )

        tk.Label(

            card,

            text=title,

            font=("Arial", 10, "bold"),

            bg="#DCE6F1",

            fg="#2C3E50"

        ).pack()

        tk.Label(

            card,

            text=value,

            font=("Arial", 18, "bold"),

            bg="#DCE6F1",

            fg="#2C3E50"

        ).pack(
            pady=3
        )

    create_card(
        0,
        0,
        "📚",
        "Sessions",
        str(total_sessions)
    )

    create_card(
        0,
        1,
        "⏱️",
        "Total Hours",
        f"{total_hours} h"
    )

    create_card(
        0,
        2,
        "📊",
        "Average",
        f"{average_hours} h"
    )

    create_card(
        0,
        3,
        "🗓️",
        "Weekly Hours",
        f"{weekly_hours} h"
    )

    create_card(
        1,
        1,
        "🎯",
        "Weekly Goal",
        f"{weekly_goal} h"
    )

    create_card(
        1,
        2,
        "📈",
        "Goal Progress",
        f"{progress}%"
    )

    create_card(
        1,
        3,
        "⏳",
        "Remaining",
        f"{remaining_hours} h"
    )

    # Progress bar

    progress_frame = tk.Frame(

        dashboard_window,

        bg="#F5F7FA"

    )

    progress_frame.pack(

        fill="x",

        padx=60,

        pady=10

    )

    tk.Label(

        progress_frame,

        text="Weekly Goal Progress 🎯",

        font=("Arial", 15, "bold"),

        bg="#F5F7FA",

        fg="#2C3E50"

    ).pack(pady=5)

    background = tk.Frame(

        progress_frame,

        bg="#DCE6F1",

        height=30

    )

    background.pack(

        fill="x",

        pady=8

    )

    background.pack_propagate(
        False
    )

    progress_bar = tk.Frame(

        background,

        bg="#2C3E50"

    )

    progress_bar.place(

        x=0,

        y=0,

        relheight=1,

        relwidth=progress_display / 100

    )

    tk.Label(

        progress_frame,

        text=f"{progress}% completed",

        font=("Arial", 11, "bold"),

        bg="#F5F7FA",

        fg="#2C3E50"

    ).pack()

    # Study insight

    if average_hours >= 3:

        insight = (
            "🌟 Excellent! You are maintaining "
            "a strong study routine."
        )

    elif average_hours >= 2:

        insight = (
            "💪 Good progress! Keep building "
            "your study consistency."
        )

    else:

        insight = (
            "📚 Try increasing your study time "
            "gradually."
        )

    tk.Label(

        dashboard_window,

        text=insight,

        font=("Arial", 12, "bold"),

        bg="#F5F7FA",

        fg="#2C3E50",

        wraplength=700

    ).pack(pady=12)

    def edit_weekly_goal():

        goal_window = tk.Toplevel(
            dashboard_window
        )

        goal_window.title(
            "Edit Weekly Goal"
        )

        goal_window.geometry(
            "400x250"
        )

        goal_window.configure(
            bg="#F5F7FA"
        )

        tk.Label(

            goal_window,

            text="Edit Weekly Goal 🎯",

            font=("Arial", 20, "bold"),

            bg="#F5F7FA",

            fg="#2C3E50"

        ).pack(pady=20)

        tk.Label(

            goal_window,

            text="Enter your new weekly goal:",

            font=("Arial", 12),

            bg="#F5F7FA",

            fg="#2C3E50"

        ).pack()

        goal_entry = tk.Entry(

            goal_window,

            font=("Arial", 13),

            width=20

        )

        goal_entry.pack(
            pady=10
        )

        goal_entry.insert(
            0,
            str(get_weekly_goal())
        )

        def save_new_goal():

            try:

                new_goal = float(
                    goal_entry.get()
                )

                if new_goal <= 0:

                    messagebox.showerror(
                        "Invalid Goal",
                        "Goal must be greater than 0."
                    )

                    return

                save_weekly_goal(
                    new_goal
                )

                goal_window.destroy()

                dashboard_window.destroy()

                show_dashboard()

            except ValueError:

                messagebox.showerror(
                    "Invalid Goal",
                    "Please enter a valid number."
                )

        tk.Button(

            goal_window,

            text="Save New Goal",

            font=("Arial", 12, "bold"),

            width=20,

            bg="#DCE6F1",

            command=save_new_goal

        ).pack(pady=10)

    tk.Button(

        dashboard_window,

        text="Edit Weekly Goal 🎯",

        font=("Arial", 12, "bold"),

        width=23,

        bg="#DCE6F1",

        command=edit_weekly_goal

    ).pack(pady=8)

    tk.Button(

        dashboard_window,

        text="Export Study Report 📄",

        font=("Arial", 12, "bold"),

        width=23,

        bg="#DCE6F1",

        command=export_report

    ).pack(pady=5)


# =========================
# View Records + Search + Sort
# =========================

def view_study_records():

    records_window = tk.Toplevel(
        window
    )

    records_window.title(
        "Study Records"
    )

    records_window.geometry(
        "700x570"
    )

    records_window.configure(
        bg="#F5F7FA"
    )

    tk.Label(

        records_window,

        text="Your Study Records 📚",

        font=("Arial", 20, "bold"),

        bg="#F5F7FA",

        fg="#2C3E50"

    ).pack(pady=12)

    search_frame = tk.Frame(

        records_window,

        bg="#F5F7FA"

    )

    search_frame.pack(
        fill="x",
        padx=25,
        pady=5
    )

    tk.Label(

        search_frame,

        text="Search 🔎",

        font=("Arial", 11, "bold"),

        bg="#F5F7FA",

        fg="#2C3E50"

    ).pack(
        side="left"
    )

    search_entry = tk.Entry(

        search_frame,

        font=("Arial", 11),

        width=28

    )

    search_entry.pack(
        side="left",
        padx=8
    )

    tk.Label(

        search_frame,

        text="Sort:",

        font=("Arial", 11, "bold"),

        bg="#F5F7FA",

        fg="#2C3E50"

    ).pack(
        side="left"
    )

    sort_var = tk.StringVar()

    sort_var.set(
        "Newest"
    )

    sort_menu = tk.OptionMenu(

        search_frame,

        sort_var,

        "Newest",
        "Oldest",
        "Most Hours",
        "Least Hours"

    )

    sort_menu.config(
        font=("Arial", 10)
    )

    sort_menu.pack(
        side="left",
        padx=5
    )

    records = load_records()

    records_frame = tk.Frame(

        records_window,

        bg="#F5F7FA"

    )

    records_frame.pack(

        fill="both",

        expand=True,

        padx=20,

        pady=10

    )

    canvas = tk.Canvas(

        records_frame,

        bg="#F5F7FA",

        highlightthickness=0

    )

    scrollbar = tk.Scrollbar(

        records_frame,

        orient="vertical",

        command=canvas.yview

    )

    scrollable_frame = tk.Frame(

        canvas,

        bg="#F5F7FA"

    )

    canvas.create_window(

        (0, 0),

        window=scrollable_frame,

        anchor="nw"

    )

    canvas.configure(

        yscrollcommand=scrollbar.set

    )

    canvas.pack(

        side="left",

        fill="both",

        expand=True

    )

    scrollbar.pack(

        side="right",

        fill="y"

    )

    def display_records():

        for widget in scrollable_frame.winfo_children():

            widget.destroy()

        search_text = (

            search_entry.get()
            .strip()
            .lower()
        )

        filtered_records = [

            record

            for record in records

            if (

                not search_text

                or search_text
                in record["subject"].lower()

                or search_text
                in record["date"].lower()

                or search_text
                in record["session_number"].lower()

            )

        ]

        selected_sort = sort_var.get()

        if selected_sort == "Newest":

            filtered_records.sort(
                key=lambda x: x["date"],
                reverse=True
            )

        elif selected_sort == "Oldest":

            filtered_records.sort(
                key=lambda x: x["date"]
            )

        elif selected_sort == "Most Hours":

            filtered_records.sort(
                key=lambda x: float(
                    x["daily_hours"]
                ),
                reverse=True
            )

        elif selected_sort == "Least Hours":

            filtered_records.sort(
                key=lambda x: float(
                    x["daily_hours"]
                )
            )

        if not filtered_records:

            tk.Label(

                scrollable_frame,

                text="No matching records found.",

                bg="#F5F7FA",

                fg="#2C3E50",

                font=("Arial", 12, "bold")

            ).pack(pady=25)

        else:

            for record in filtered_records:

                record_text = (

                    f"Session #{record['session_number']} | "

                    f"{record['date']} | "

                    f"{record['subject']} | "

                    f"{record['daily_hours']} hours"

                )

                tk.Label(

                    scrollable_frame,

                    text=record_text,

                    bg="#DCE6F1",

                    fg="#2C3E50",

                    font=("Arial", 11),

                    anchor="w",

                    width=75

                ).pack(

                    pady=4,

                    padx=5

                )

        scrollable_frame.update_idletasks()

        canvas.configure(

            scrollregion=canvas.bbox("all")

        )

    search_entry.bind(
        "<KeyRelease>",
        lambda event: display_records()
    )

    sort_var.trace_add(
        "write",
        lambda *args: display_records()
    )

    display_records()


# =========================
# Edit Study Session
# =========================

def edit_study_session():

    edit_window = tk.Toplevel(
        window
    )

    edit_window.title(
        "Edit Study Session"
    )

    edit_window.geometry(
        "650x500"
    )

    edit_window.configure(
        bg="#F5F7FA"
    )

    tk.Label(

        edit_window,

        text="Edit Study Session ✏️",

        font=("Arial", 20, "bold"),

        bg="#F5F7FA",

        fg="#2C3E50"

    ).pack(pady=20)

    records = load_records()

    if not records:

        tk.Label(

            edit_window,

            text="No study records found.",

            font=("Arial", 12),

            bg="#F5F7FA"

        ).pack(pady=30)

        return

    tk.Label(

        edit_window,

        text="Select a session to edit:",

        font=("Arial", 12),

        bg="#F5F7FA"

    ).pack(pady=5)

    list_frame = tk.Frame(

        edit_window,

        bg="#F5F7FA"

    )

    list_frame.pack(

        fill="both",

        expand=True,

        padx=25,

        pady=10

    )

    listbox = tk.Listbox(

        list_frame,

        font=("Arial", 12),

        height=10

    )

    scrollbar = tk.Scrollbar(

        list_frame,

        orient="vertical",

        command=listbox.yview

    )

    listbox.configure(
        yscrollcommand=scrollbar.set
    )

    listbox.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    for record in records:

        listbox.insert(

            tk.END,

            f"Session #{record['session_number']} | "
            f"{record['date']} | "
            f"{record['subject']} | "
            f"{record['daily_hours']} hours"

        )

    def open_edit_form():

        selected = listbox.curselection()

        if not selected:

            messagebox.showwarning(

                "Select Session",

                "Please select a study session first."

            )

            return

        index = selected[0]

        selected_record = records[index]

        form_window = tk.Toplevel(
            edit_window
        )

        form_window.title(
            "Edit Session"
        )

        form_window.geometry(
            "450x400"
        )

        form_window.configure(
            bg="#F5F7FA"
        )

        tk.Label(

            form_window,

            text="Edit Study Session ✏️",

            font=("Arial", 20, "bold"),

            bg="#F5F7FA",

            fg="#2C3E50"

        ).pack(pady=15)

        tk.Label(

            form_window,

            text="Subject",

            font=("Arial", 12, "bold"),

            bg="#F5F7FA"

        ).pack(pady=5)

        subject_entry = tk.Entry(

            form_window,

            font=("Arial", 12),

            width=30

        )

        subject_entry.pack(pady=5)

        subject_entry.insert(
            0,
            selected_record["subject"]
        )

        tk.Label(

            form_window,

            text="Today's Study Hours",

            font=("Arial", 12, "bold"),

            bg="#F5F7FA"

        ).pack(pady=5)

        hours_entry = tk.Entry(

            form_window,

            font=("Arial", 12),

            width=30

        )

        hours_entry.pack(pady=5)

        hours_entry.insert(
            0,
            selected_record["daily_hours"]
        )

        tk.Label(

            form_window,

            text="Weekly Study Hours",

            font=("Arial", 12, "bold"),

            bg="#F5F7FA"

        ).pack(pady=5)

        weekly_entry = tk.Entry(

            form_window,

            font=("Arial", 12),

            width=30

        )

        weekly_entry.pack(pady=5)

        weekly_entry.insert(
            0,
            selected_record["weekly_hours"]
        )

        def save_edit():

            subject = subject_entry.get().strip()

            if not subject:

                messagebox.showerror(
                    "Invalid Subject",
                    "Subject cannot be empty."
                )

                return

            try:

                hours = float(
                    hours_entry.get()
                )

                weekly_hours = float(
                    weekly_entry.get()
                )

            except ValueError:

                messagebox.showerror(
                    "Invalid Number",
                    "Please enter valid numbers."
                )

                return

            if hours < 0 or weekly_hours < 0:

                messagebox.showerror(
                    "Invalid Number",
                    "Hours cannot be negative."
                )

                return

            selected_record["subject"] = subject

            selected_record["daily_hours"] = str(
                hours
            )

            selected_record["weekly_hours"] = str(
                weekly_hours
            )

            save_records(
                records
            )

            messagebox.showinfo(
                "Updated",
                "Study session updated successfully! ⭐"
            )

            form_window.destroy()

            edit_window.destroy()

        tk.Button(

            form_window,

            text="Save Changes",

            font=("Arial", 13, "bold"),

            width=22,

            bg="#DCE6F1",

            command=save_edit

        ).pack(pady=20)

    tk.Button(

        edit_window,

        text="Edit Selected Session ✏️",

        font=("Arial", 13, "bold"),

        width=25,

        bg="#DCE6F1",

        command=open_edit_form

    ).pack(pady=15)


# =========================
# Delete Study Session
# =========================

def delete_study_record():

    delete_window = tk.Toplevel(
        window
    )

    delete_window.title(
        "Delete Study Record"
    )

    delete_window.geometry(
        "600x450"
    )

    delete_window.configure(
        bg="#F5F7FA"
    )

    tk.Label(

        delete_window,

        text="Delete Study Record 🗑️",

        font=("Arial", 20, "bold"),

        bg="#F5F7FA",

        fg="#2C3E50"

    ).pack(pady=20)

    records = load_records()

    if not records:

        tk.Label(

            delete_window,

            text="No study records found.",

            font=("Arial", 12),

            bg="#F5F7FA"

        ).pack(pady=30)

        return

    list_frame = tk.Frame(

        delete_window,

        bg="#F5F7FA"

    )

    list_frame.pack(

        fill="both",

        expand=True,

        padx=25,

        pady=10

    )

    listbox = tk.Listbox(

        list_frame,

        font=("Arial", 12),

        height=10

    )

    scrollbar = tk.Scrollbar(

        list_frame,

        orient="vertical",

        command=listbox.yview

    )

    listbox.configure(
        yscrollcommand=scrollbar.set
    )

    listbox.pack(

        side="left",

        fill="both",

        expand=True

    )

    scrollbar.pack(

        side="right",

        fill="y"

    )

    for record in records:

        listbox.insert(

            tk.END,

            f"Session #{record['session_number']} | "
            f"{record['date']} | "
            f"{record['subject']} | "
            f"{record['daily_hours']} hours"

        )

    def delete_selected():

        selected = listbox.curselection()

        if not selected:

            messagebox.showwarning(

                "Select Session",

                "Please select a study session first."

            )

            return

        index = selected[0]

        deleted = records[index]

        confirm = messagebox.askyesno(

            "Confirm Delete",

            f"Delete Session #{deleted['session_number']}?"

        )

        if not confirm:
            return

        records.pop(index)

        save_records(
            records
        )

        listbox.delete(
            index
        )

        messagebox.showinfo(

            "Deleted",

            "Study session deleted successfully! 🗑️"

        )

    tk.Button(

        delete_window,

        text="Delete Selected Session",

        font=("Arial", 13, "bold"),

        width=25,

        bg="#DCE6F1",

        command=delete_selected

    ).pack(pady=15)


# =========================
# Export Report
# =========================

def export_report():

    records = load_records()

    if not records:

        messagebox.showwarning(

            "No Data",

            "There are no study records to export."

        )

        return

    total_sessions = len(
        records
    )

    total_hours = round(

        sum(
            float(record["daily_hours"])
            for record in records
        ),

        2

    )

    average_hours = round(

        total_hours /
        total_sessions,

        2

    )

    weekly_hours = round(

        sum(
            float(record["weekly_hours"])
            for record in records
        ),

        2

    )

    weekly_goal = get_weekly_goal()

    if weekly_goal > 0:

        progress = round(

            (weekly_hours / weekly_goal)
            * 100,

            1

        )

    else:

        progress = 0

    with open(

        REPORT_FILE,

        "w",

        encoding="utf-8"

    ) as file:

        file.write(
            "SMART STUDY TRACKER REPORT\n"
        )

        file.write(
            "===========================\n\n"
        )

        file.write(
            f"Report Date: {date.today()}\n\n"
        )

        file.write(
            f"Total Sessions: {total_sessions}\n"
        )

        file.write(
            f"Total Study Hours: {total_hours}\n"
        )

        file.write(
            f"Average Study Hours: {average_hours}\n"
        )

        file.write(
            f"Weekly Hours: {weekly_hours}\n"
        )

        file.write(
            f"Weekly Goal: {weekly_goal}\n"
        )

        file.write(
            f"Goal Progress: {progress}%\n\n"
        )

        file.write(
            "STUDY SESSIONS\n"
        )

        file.write(
            "--------------\n"
        )

        for record in records:

            file.write(

                f"Session #{record['session_number']} | "
                f"{record['date']} | "
                f"{record['subject']} | "
                f"{record['daily_hours']} hours\n"

            )

    messagebox.showinfo(

        "Report Exported",

        f"Study report saved as:\n{REPORT_FILE}"

    )


# =========================
# Main Window
# =========================

window = tk.Tk()

window.title(
    "Smart Study Tracker"
)

window.geometry(
    "600x720"
)

window.configure(
    bg="#F5F7FA"
)

tk.Label(

    window,

    text="Smart Study Tracker 📚",

    font=("Arial", 28, "bold"),

    bg="#F5F7FA",

    fg="#2C3E50"

).pack(pady=35)

tk.Label(

    window,

    text="Track your study. Build your progress.",

    font=("Arial", 14),

    bg="#F5F7FA",

    fg="#2C3E50"

).pack(pady=5)


def create_main_button(
    text,
    command
):

    tk.Button(

        window,

        text=text,

        font=("Arial", 15, "bold"),

        width=24,

        bg="#DCE6F1",

        fg="#2C3E50",

        command=command

    ).pack(pady=7)


create_main_button(
    "Add Study Session",
    add_study_session
)

create_main_button(
    "View Study Records 🔎",
    view_study_records
)

create_main_button(
    "Edit Study Session ✏️",
    edit_study_session
)

create_main_button(
    "Dashboard 📊",
    show_dashboard
)

create_main_button(
    "Delete Study Record 🗑️",
    delete_study_record
)

create_main_button(
    "Export Study Report 📄",
    export_report
)

create_main_button(
    "Exit",
    window.destroy
)


window.mainloop()