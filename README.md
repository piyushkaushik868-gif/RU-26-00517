# Student Attendance Manager

**PS No.:** 17
**Language:** Python 3.14
**Concepts used:** Lists, Dictionaries, Functions, File Handling

## Problem Statement

A menu-driven console application to add students, mark daily attendance as present or absent, view each student's attendance percentage, and list students below the 75% requirement. All data is saved to a file.

## Features

1. **Add student**: adds a student with a unique roll number (starts with 0 held, 0 attended).
2. **Mark attendance**: marks a student Present (`P`) or Absent (`A`) for one class.
3. **View percentage**: shows a student's attendance percentage.
4. **Shortage list**: shows students below 75% and confirms those who meet the requirement.
5. **Exit**.

## Data Storage

Each student is a dictionary stored in a list:

```python
{"roll": "101", "name": "Aman", "held": 4, "attended": 3}
```

Data is loaded from `attendance.txt` when the program starts and saved after every change. File format, one student per line:

```
roll|name|held|attended
```

## Validation

- Roll numbers must be unique and non-empty.
- An unknown roll number prints `Roll number <roll> not found.`
- Attendance status must be `P` or `A`, otherwise `Invalid status. Enter P or A.`
- Division by zero is avoided when no classes have been held.

## How to Run

```bash
python attendance.py
```

Requires Python 3. No external libraries are needed.

## Test Cases

Delete `attendance.txt` before starting. The test cases run in order on the same records.

| # | Type | Input | Expected Output |
|---|------|-------|-----------------|
| 1 | Normal | Option 1, Roll `101`, Name `Aman` | `Student added: 101 \| Aman \| Held: 0 \| Attended: 0` |
| 2 | Boundary | Option 3, Roll `101` (no classes held) | `Aman: Attendance 0.00% (no classes held yet)` |
| 3a | Invalid | Option 2, Roll `999` | `Roll number 999 not found.` |
| 3b | Invalid | Option 2, Roll `101`, Status `X` | `Invalid status. Enter P or A.` |
| 4 | Different valid | 101 Aman (4 held, 3 attended), 102 Riya (4 held, 2 attended), Option 4 | `Below 75%: 102 \| Riya \| 50.00%` and `Aman (75.00%) meets the requirement.` |

## Sample Run

```
--- Student Attendance Manager ---
1. Add student
2. Mark attendance
3. View attendance percentage
4. Shortage list (below 75%)
5. Exit
Choose an option: 1
Roll: 101
Name: Aman
Student added: 101 | Aman | Held: 0 | Attended: 0
```

## Project Files

- `attendance.py`: main program
- `attendance.txt`: data file (created automatically)
- `README.md`: project documentation

## Author

Piyush Kaushik
