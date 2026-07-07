# 💰 SmartCart - Household Budget & Wallet Tracker

[![Django Version](https://img.shields.io/badge/django-6.0.6-green.svg)](https://www.djangoproject.com/)
[![Python Version](https://img.shields.io/badge/python-3.14.3-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-purple.svg)](LICENSE)

SmartCart is a robust, production-ready web application built with Django designed to help families and shared households collaboratively manage their finances. It features a custom multi-tenant household system, granular role-based permissions, envelope budgeting mechanics, and real-time ledger tracking.

---

## 📌 Contents
- [About the Project](#-about-the-project)
- [Key Features](#-key-features)
- [Technologies Used](#-technologies-used)
- [Architecture & Design Patterns](#-architecture--design-patterns)
- [Project Structure](#-project-structure)
- [Database Schema (Core Entities)](#-database-schema-core-entities)
- [Installation & Setup](#-installation--setup)
- [Future Roadmap](#-future-roadmap)

---

## 📖 About the Project

Managing shared expenses usually results in messy spreadsheets or misaligned communication. **SmartCart** solves this by introducing a strict **"One Household, One Admin"** financial governance model. 

The application allows users to create standalone Households, invite members, distribute funds into virtual digital "Envelopes" (for targeted budgeting like Groceries, Utilities, Entertainment), and track every transaction with bulletproof data integrity.

---

## ⚡ Key Features

### 🔐 Multi-Tenant Authentication & Accounts (`accounts` app)
- **Django-Powered Registration:** Secure user signup utilizing Django’s strict, built-in password validators (entropy check, similarity checks, min-length 8).
- **Dynamic Session Messages:** A clean UX alert queue ensuring that financial actions (deletions, creations) provide immediate feedback without stale state leakage.

### 🏠 Shared Household Governance
- **Role-Based Access Control (RBAC):** Strict separation between `ADMIN` (the Household owner) and `MEMBER` (the consumers).
- **The Creator-Is-Owner Rule:** Automatically assigns the creator as the Admin.
- **Graceful Offboarding Constraints:** An Admin cannot abandon a household if other members are present, preventing "orphaned data structures." If the Admin is the sole member, leaving the household triggers a cascading purge.
- **Fail-Safe Member Invites:** Comprehensive server-side validation (`try-except` containment on lookup states) preventing crashes when inviting non-existent or duplicate users.

### ✉️ Envelope Budgeting & Transactions *(Core Ledger Layer)*
- Dual-entry logging concept for financial tracking via segregated virtual wallets.

---

## 🛠️ Technologies Used

- **Backend Framework:** Django 6.0.6 (Python 3.14.3)
- **Database:** SQLite (Development) / Architected for seamless PostgreSQL migration
- **Frontend Layer:** Semantic HTML5, CSS3, Django Template Language (DTL)
- **Security Protocols:** Django CSRF Protection, PBKDF2 Password Hashing, `@login_required` middleware access-guards.

---

## 🏗️ Architecture & Design Patterns

The application strictly follows the native Django **MVT (Model-View-Template)** architecture, combined with industry-standard design patterns for clean and maintainable code:

1. **MVT (Model-View-Template) Implementation:**
   - **Model:** Handles the database layer and data validation (e.g., integrity of household relations).
   - **View:** Acts as the controller, handling HTTP POST/GET requests and executing user flow.
   - **Template:** The presentation layer using Django Template Language (DTL) to render dynamic and responsive views.

2. **Fat Models, Skinny Views Pattern:**
   - Business logic is kept inside the models or encapsulated querysets, keeping the `views.py` lightweight, readable, and easy to maintain.

3. **Defensive Programming:**
   - High usage of focused `try-except` blocks on database lookups (such as catching `User.DoesNotExist`) to prevent `500 Internal Server Errors` and ensure a smooth user experience by falling back to safe form states.

---

## 📂 Project Structure

```text
smartcart/
│
├── smartcart/                # Project Configuration Root
│   ├── __init__.py
│   ├── settings.py           # Configuration, Security Keys, Installed Apps
│   ├── urls.py               # Main Routing Ledger
│   └── wsgi.py / asgi.py
│
├── accounts/                 # User Management & Tenancy Domain
│   ├── templates/accounts/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── household_list.html   # Main Dashboard Dashboard
│   │   ├── household_detail.html # Household Workspace
│   │   └── add_member.html       # Defensive form viewport
│   ├── models.py             # Household & Membership definitions
│   ├── views.py              # Strict POST validation controllers
│   ├── urls.py               # Accounts-specific routing API
│   └── tests.py
│
├── manage.py                 # Django administrative entrypoint
└── requirements.txt          # Explicit version-locked dependencies
```

---

## 🗄️ Database Schema (Core Entities)

The architecture maps out human relationships into high-performance relational tables:

### `Household`
- `id` (Int, PK)
- `name` (CharField)
- `created_at` (DateTimeField)

### `HouseholdMembership` (The Gatekeeper Table)
- `id` (PK)
- `user` (ForeignKey -> User, Cascade)
- `household` (ForeignKey -> Household, Cascade)
- `role` (CharField: Choices `ADMIN` or `MEMBER`)

> **Architectural Constraint:** Explicit unique constraint enforced on `(user, household)` combinations to block rogue multi-joining database state corruption.

---

## 🚀 Installation & Setup

Follow these steps to spin up the production environment locally:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/smartcart.git](https://github.com/Kaloyan7878/smartcart.git)
   cd smartcart
   ```
2. **Setup and activate Virtual Environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Execute Database Migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Fire up the local development server:**
   ```bash
   python manage.py runserver
   ```
   Open http://127.0.0.1:8000/ in your browser.
