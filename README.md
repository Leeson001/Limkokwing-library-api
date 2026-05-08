# Limkokwing-library-api

Limkokwing Library Digital System API
Project Description
A Python asynchronous API simulation for managing library books, borrowing, returns, and overdue tracking at Limkokwing University of Creative Technology.
Features
	•	Search books by title, author, or category
	•	Borrow and return books
	•	Track overdue books and calculate fines
	•	Supports multiple users accessing the system concurrently
Project Structure

limkokwing-library-api/
|
+-- main.py              # Core API simulation
+-- README.md            # Project documentation
+-- .gitignore           # Excludes cache and env files
+-- requirements.txt     # Dependencies
+-- docs/
    +-- api_design.md    # Endpoint documentation


How to Run
Make sure you have Python 3.10 or higher installed.

python main.py


API Endpoints



|Method|Endpoint|Purpose            |
|------|--------|-------------------|
|GET   |/books  |Search for books   |
|POST  |/borrow |Borrow a book      |
|POST  |/return |Return a book      |
|GET   |/overdue|Check overdue books|

Author
	•	Name: ALPHA USMAN JALLOH
	•	Student ID: 905005323
	•	University: Limkokwing University of Creative Technology
	•	Faculty: Information and Communication Technology
	•	Semester: 04
