# Earnify - Earn Money Through Ads

Earnify is a web platform where users can earn money by interacting with ads, watching videos, completing tasks, and more. It’s built to provide a seamless earning experience while helping advertisers reach their target audience.

---

## Features

- **Ad Interaction**: Users can earn money by viewing and interacting with ads.
- **Task Completion**: Complete small tasks (e.g., surveys, app downloads) to earn rewards.
- **Referral System**: Earn additional income by referring friends to the platform.
- **Withdrawal Options**: Withdraw earnings via PayPal, bank transfer, or other payment methods.
- **User Dashboard**: Track earnings, completed tasks, and referral stats in real-time.
- **Admin Panel**: Manage ads, tasks, and user activities with an easy-to-use admin interface.

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/earnify.git
   cd earnify
2. **Set up a virtual environment:**

bash
Copy
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3 **Install dependencies:**

bash
Copy
pip install -r requirements.txt
4 **Run migrations:**

bash
Copy
python manage.py migrate
5 **Create a superuser (for admin access):**

bash
Copy
python manage.py createsuperuser
6 **Start the development server:**

bash
Copy
python manage.py runserver
7 **Access the app:**
Open your browser and go to http://127.0.0.1:8000/.
