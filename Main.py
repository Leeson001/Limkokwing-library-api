import asyncio
from datetime import date, timedelta
from typing import Optional

# ---------- Simulated Database ----------
books_db: dict[str, dict] = {
    "B101": {"title": "Learning Python", "author": "Mark Lutz", "available": True},
    "B202": {"title": "Clean Code", "author": "Robert Martin", "available": True},
}

loans_db: dict[str, dict] = {}   # key: f"{user_id}_{book_id}"
fines_per_day: float = 0.50


# ---------- Endpoint Simulations ----------

async def get_books(query: str) -> dict:
    """GET /books — search by keyword"""
    await asyncio.sleep(0.1)   # simulate I/O
    results = [
        {**info, "book_id": bid}
        for bid, info in books_db.items()
        if query.lower() in info["title"].lower()
        or query.lower() in info["author"].lower()
    ]
    return {"status": "success", "count": len(results), "results": results}


async def borrow_book(user_id: str, book_id: str) -> dict:
    """POST /borrow — borrow a book"""
    await asyncio.sleep(0.2)   # simulate DB write delay
    if book_id not in books_db:
        return {"status": "error", "message": "Book not found"}
    if not books_db[book_id]["available"]:
        return {"status": "error", "message": "Book is currently unavailable"}

    books_db[book_id]["available"] = False
    due = date.today() + timedelta(days=14)
    loan_key = f"{user_id}_{book_id}"
    loans_db[loan_key] = {
        "user_id": user_id,
        "book_id": book_id,
        "borrow_date": str(date.today()),
        "due_date": str(due),
    }
    return {
        "status": "borrowed",
        "book_id": book_id,
        "due_date": str(due),
        "message": "Book borrowed successfully",
    }


async def return_book(user_id: str, book_id: str) -> dict:
    """POST /return — return a book and compute fine"""
    await asyncio.sleep(0.2)
    loan_key = f"{user_id}_{book_id}"
    if loan_key not in loans_db:
        return {"status": "error", "message": "No active loan found"}

    loan = loans_db.pop(loan_key)
    books_db[book_id]["available"] = True
    due = date.fromisoformat(loan["due_date"])
    overdue_days = max(0, (date.today() - due).days)
    fine = round(overdue_days * fines_per_day, 2)

    return {
        "status": "returned",
        "overdue_days": overdue_days,
        "fine_usd": fine,
        "message": "Returned on time" if fine == 0 else f"Fine of ${fine} applied",
    }


async def check_overdue(user_id: Optional[str] = None) -> dict:
    """GET /overdue — list overdue loans"""
    await asyncio.sleep(0.1)
    today = date.today()
    overdue = []
    for loan in loans_db.values():
        if user_id and loan["user_id"] != user_id:
            continue
        due = date.fromisoformat(loan["due_date"])
        days = (today - due).days
        if days > 0:
            overdue.append({**loan, "days_overdue": days, "fine": round(days * fines_per_day, 2)})
    return {"status": "success", "overdue_count": len(overdue), "overdue_books": overdue}


# ---------- Multi-User Concurrent Simulation ----------

async def main() -> None:
    print("=== Limkokwing Library API Simulation ===\n")

    # 1. Search
    print(">> GET /books?query=python")
    result = await get_books("python")
    print(result, "\n")

    # 2. Two users borrow concurrently
    print(">> Two users borrowing concurrently...")
    borrow_results = await asyncio.gather(
        borrow_book("U01", "B101"),
        borrow_book("U02", "B202"),
    )
    for r in borrow_results:
        print(r)
    print()

    # 3. Attempt duplicate borrow (conflict test)
    print(">> U03 tries to borrow already-borrowed B101:")
    print(await borrow_book("U03", "B101"), "\n")

    # 4. Return a book
    print(">> U01 returns B101:")
    print(await return_book("U01", "B101"), "\n")

    # 5. Overdue check
    print(">> GET /overdue:")
    print(await check_overdue(), "\n")


if __name__ == "__main__":
    asyncio.run(main())