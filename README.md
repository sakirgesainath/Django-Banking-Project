# 🏦 Django Banking Management System

A web-based Banking Management System developed using **Python, Django, MySQL, HTML, and CSS**. This application allows users to create bank accounts and perform basic banking operations through a simple web interface.

## 📌 Project Overview

The Django Banking Management System provides essential banking features such as account creation, balance inquiry, deposits, withdrawals, fund transfers, and account closure. It also maintains transaction history and uses password hashing for account security.

## ✨ Features

- **New Account:** Create a bank account with a randomly generated account number.
- **Check Balance:** View the account balance after account verification.
- **Deposit Money:** Add money to an existing account.
- **Withdraw Money:** Withdraw money while checking for sufficient balance.
- **Fund Transfer:** Transfer money between two accounts.
- **Close Account:** Close an account after identity verification and confirmation.
- **Transaction History:** Record deposits, withdrawals, and incoming and outgoing transfers.
- **Password Security:** Store account passwords as hashes instead of plain text.
- **Input Validation:** Validate account details, passwords, and transaction amounts.
- **Responsive Interface:** Navigate banking operations through HTML templates and CSS styling.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web application framework |
| MySQL | Database management |
| HTML5 | Web page structure |
| CSS3 | Styling and layout |
| Django Forms | Form handling and validation |
| Git and GitHub | Version control and project hosting |

## 📂 Project Structure

```text
banking/
│
├── bank/
│   ├── migrations/
│   ├── static/
│   │   └── bank/
│   │       └── style.css
│   ├── templates/
│   │   └── bank/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── new_account.html
│   │       ├── balance.html
│   │       ├── deposit.html
│   │       ├── withdraw.html
│   │       ├── transfer.html
│   │       ├── close_account.html
│   │       ├── result.html
│   │       └── _form.html
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── bankproject/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
```

### 2. Navigate to the Project Folder

```bash
cd banking
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
python -m pip install Django mysqlclient
```

Make sure MySQL Server is installed and running.

### 5. Configure the MySQL Database

Open `bankproject/settings.py` and configure the database settings to match your local MySQL credentials.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bank',
        'USER': 'root',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

Create the database in MySQL:

```sql
CREATE DATABASE bank;
```

Replace `your_mysql_password` with your actual MySQL password.

### 6. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Start the Development Server

```bash
python manage.py runserver
```

### 8. Open the Application

Visit the following URL in your browser:

```text
http://127.0.0.1:8000/
```

## 🧭 Application Modules

| Module | Description |
|---|---|
| Home | Displays the available banking operations |
| New Account | Registers a new customer account |
| Balance | Verifies account details and displays the balance |
| Deposit | Adds money to an account |
| Withdraw | Deducts money after validating the available balance |
| Transfer | Transfers money between customer accounts |
| Close Account | Closes an account after verification |
| Transaction Records | Stores transaction type, amount, date, and resulting balance |

## 🗄️ Database Models

### Account

Stores customer account information, including:

- Account number
- Account holder name
- Hashed password
- Current balance
- Account creation date

### Transaction

Stores financial transaction information, including:

- Related bank account
- Transaction type
- Transaction amount
- Balance after the transaction
- Transaction note
- Transaction date and time

## 🔐 Security Notes

- Account passwords are hashed before being stored.
- Account details are verified before banking operations.
- Withdrawals and transfers check the available balance.
- Database transactions help keep balance updates and transaction records consistent.

**Important:** This project is intended for learning and demonstration. Before using it in production, add stronger authentication and authorization, secure configuration management, appropriate logging, and additional security testing.

## 🚀 Future Enhancements

- Customer login and logout
- Admin dashboard
- Customer profile management
- Downloadable bank statements
- Search and filter transaction history
- Email or SMS transaction notifications
- Improved security and automated tests

## 👨‍💻 Author

**Your Name**

GitHub: [Your GitHub Profile](https://github.com/)

LinkedIn: [Your LinkedIn Profile](https://www.linkedin.com/)

## 📄 License

This project is available for educational and learning purposes. Add a license file if you intend to distribute it under a specific open-source license.
