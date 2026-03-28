# Smart Expense Tracker (Django)
**Author:** Shree Hari S L | **Project:** CN_EXPENSE_TRACKER

---

## ⚡ Quick Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Apply database migrations
```bash
python manage.py migrate
```

### 3. (Optional) Create an admin superuser
```bash
python manage.py createsuperuser
```

### 4. Run the development server
```bash
python manage.py runserver
```

### 5. Open in browser
```
http://127.0.0.1:8000/
```

---

## 📁 Project Structure
```
expense_tracker/
├── manage.py
├── requirements.txt
├── db.sqlite3              ← auto-created after migrate
├── tracker_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── expenses/
    ├── models.py           ← Expense model
    ├── views.py            ← All views (auth, CRUD, export)
    ├── forms.py            ← ExpenseForm
    ├── urls.py             ← URL routing
    ├── utils.py            ← Auto category prediction
    └── templates/
        ├── base.html
        ├── login.html
        ├── signup.html
        ├── dashboard.html
        └── expense_form.html
```

---

## ✨ Features
- User Registration & Login (Django Auth)
- Add / Edit / Delete expenses
- Auto category prediction from description keywords
- Filter by Today / Week / Month / All
- Pie chart (category-wise) + Bar chart (daily spending)
- Export to CSV and PDF
- Responsive Bootstrap 5 UI

## 🛠 Tech Stack
- **Backend:** Python, Django
- **Database:** SQLite
- **Frontend:** HTML, CSS, Bootstrap 5, Chart.js
- **PDF Export:** ReportLab

## 🔗 GitHub
[Shree04ISRO/CN_EXPENSE_TRACKER](https://github.com/Shree04ISRO/CN_EXPENSE_TRACKER)
