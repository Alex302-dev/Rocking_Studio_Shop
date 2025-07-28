# 🛍️ Rocking Studio Shop

A scalable virtual asset storefront built with **Django** and **Tailwind CSS**. This e-commerce platform supports product listings, user authentication, secure payments, and a fully functional admin dashboard.

---

## 🚀 Features

- 🔐 **User Authentication** – Register, login, and manage secure user sessions
- 🎨 **Tailwind UI** – Fast and responsive styling with utility-first CSS
- 🛒 **Product Management** – Easily list and update virtual products
- 💳 **Payments** – (Planned or integrated) secure checkout for digital assets
- 🛠️ **Admin Dashboard** – Manage products, users, and orders via Django Admin

---

## 🧰 Tech Stack

| Layer          | Technology        |
|----------------|-------------------|
| Backend        | Django             |
| Frontend       | Tailwind CSS       |
| Auth & Admin   | Django Auth & Admin Panel |
| Database       | (default: SQLite, customizable) |
| Payments       | (Add Stripe, PayPal, etc.) |

---

## 🛠️ Installation

> Clone the repo and run it locally:

```bash
git clone https://github.com/Alex302-dev/Rocking_Studio_Shop.git
cd Rocking_Studio_Shop
python -m venv env
source env/bin/activate  # or `env\Scripts\activate` on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
