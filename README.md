


```markdown
# 🧠 Identity Reconciliation API – FastAPI + PostgreSQL

This project is a backend service built using **FastAPI** and **PostgreSQL** to resolve identities from fragmented contact information. It is designed for Moonrider’s integration with Zamazon.com, where users like "Doc" may use different emails and phone numbers across purchases.

The goal: **link different contact entries to a unified identity**, using smart matching and merging logic.

---

## 🗂️ Features

- ✅ Accepts JSON input with `email` and/or `phoneNumber`
- ✅ Creates primary contact if no match found
- ✅ Links overlapping entries as secondary contacts
- ✅ Maintains `primaryContactId`, `emails`, `phoneNumbers`, and `secondaryContactIds`
- ✅ Smart merging when overlaps occur
- ✅ Unit-tested and Docker-ready

---

## 📁 Project Structure

```
identity-reconciliation/
├── app/
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── test_app.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Technologies Used

- Python 3.11
- FastAPI
- PostgreSQL (Dockerized)
- SQLAlchemy
- Uvicorn
- Pytest

---

## 🚀 How to Run Locally

### 1️⃣ Clone the Repo

```bash
git clone https://github.com/manu-vasamsetti/identity-reconciliation.git
cd identity-reconciliation
```

### 2️⃣ Create & Activate Virtual Environment

```bash
python -m venv venv
.\venv\Scripts\activate   # For Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

> If `requirements.txt` is missing, generate it using:
> ```bash
> pip freeze > requirements.txt
> ```

### 4️⃣ Start PostgreSQL via Docker

```bash
docker run --name contact-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=pass -e POSTGRES_DB=contacts_db -p 5432:5432 -d postgres
```

> If container already exists:
> ```bash
> docker start contact-db
> ```

### 5️⃣ Set Up `.env` File

Create a `.env` file in the root folder:

```
DATABASE_URL=postgresql://postgres:pass@localhost:5432/contacts_db
```

---

### 6️⃣ Run the Application

```bash
uvicorn app.main:app --reload
```

> Open your browser at: [http://localhost:8000/docs](http://localhost:8000/docs) to test the `/identify` API.

---

## 🧪 Run Tests

```bash
pytest test_app.py
```

You should see:
```
2 passed in X.XXs
```

---

## 📤 API Endpoint

### POST `/identify`

**Request:**
```json
{
  "email": "doc@zamazon.com",
  "phoneNumber": "9998887776"
}
```

**Response:**
```json
{
  "contact": {
    "primaryContactId": 1,
    "emails": ["doc@zamazon.com"],
    "phoneNumbers": ["9998887776"],
    "secondaryContactIds": []
  }
}
```

---

## 📄 License

This project is for educational and demonstration purposes only.

---

## 🙏 Acknowledgements

Thanks to Moonrider and Zamazon.com for this futuristic mission to unify identities across time and space.

---

```

Let me know if you want a short version for the GitHub description or if you'd like to generate a `requirements.txt` now.
