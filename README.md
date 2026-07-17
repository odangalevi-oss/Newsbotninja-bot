# Newsbotninja Bot

A Flask-based news aggregation web application that delivers news from Kenya and around the world with voice brief capabilities and user authentication.

## ✨ Features

- 📰 **News Aggregation** - Multiple categories (Sports, Technology, World, Health, Entertainment, Science)
- 🎙️ **Voice Briefing** - AI text-to-speech news summaries using Google Text-to-Speech
- 👤 **User Authentication** - Secure registration and login with password hashing
- 👨‍💼 **Admin Panel** - User management dashboard with delete functionality
- 📧 **Email Notifications** - Admin receives alerts when new users register
- 🌍 **Multi-category News** - Filter news by region and category
- 🔐 **Role-based Access Control** - First user becomes admin automatically

## 🛠️ Technologies Used

- **Backend Framework**: Flask
- **Database**: SQLAlchemy with SQLite
- **Authentication**: Werkzeug security (password hashing)
- **Email**: Flask-Mail with SMTP
- **News API**: NewsAPI.org
- **Text-to-Speech**: gTTS (Google Text-to-Speech)
- **Frontend**: HTML5, CSS3 with responsive design

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- Internet connection for news API

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/odangalevi-oss/Newsbotninja-bot.git
cd Newsbotninja-bot
```

2. **Create a virtual environment**
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
```

5. **Edit `.env` with your settings:**
```env
# Flask
SECRET_KEY=your-very-secret-key-here

# News API (Get from https://newsapi.org)
NEWS_API_KEY=your_newsapi_key_here

# Email Configuration (Gmail example)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password-here

# Admin notification email
ADMIN_EMAIL=odangalevi@gmail.com
```

6. **Run the application**
```bash
python app.py
```

7. **Access the application**
Open your browser and navigate to `http://localhost:5000`

## 📖 Usage Guide

### User Features

#### Home Page
- Visit `/` to view top Kenya headlines
- Browse different news categories from the navbar

#### News Categories
- **Sports** - Kenya Sports News
- **Tech** - Technology News Worldwide
- **World** - International Headlines
- **Health** - Kenya Health News
- **Entertainment** - Kenya Entertainment News
- **Science** - Science News Worldwide

#### Voice Brief
- Click the "🎙️ Voice Brief" button to get an audio summary of top 3 stories
- Audio is automatically generated and played in your browser

#### User Registration
1. Click "Register" in the navbar
2. Enter username (3+ characters), email, and password (6+ characters)
3. Submit the form
4. **First user automatically becomes admin**
5. Existing users trigger email notification to admin

#### User Login
1. Click "Login" in the navbar
2. Enter your registered email and password
3. Upon successful login, you'll see your username and a logout button

#### Logout
- Click the "Logout" button in the top-right navbar
- Session ends and you're redirected to home page

### Admin Features

#### Accessing Admin Panel
- Only admins can access `/admin`
- Admin users see "Admin Panel" button in navbar
- Click to view the admin dashboard

#### Admin Dashboard
- **View Statistics**: Total registered users count
- **User Management**: View all users with their roles
- **User Deletion**: Remove user accounts (cannot delete your own account)
- **Role Indicators**: See which users are admins vs regular users

#### Email Notifications
- Admins receive email notifications when new users register
- Email includes: username and email of new registrant
- Notifications sent to the configured ADMIN_EMAIL

## 🗄️ Database Schema

### User Model
```
id           : Integer (Primary Key)
username     : String (Required)
email        : String (Unique, Required)
password_hash: String (Hashed with Werkzeug)
is_admin     : Boolean (Default: False)
```

## 🔐 Security Features

- ✅ Passwords hashed with Werkzeug `generate_password_hash()`
- ✅ Session-based authentication
- ✅ Admin-only route protection with `@admin_required` decorator
- ✅ CSRF protection via Flask sessions
- ✅ Email validation
- ✅ Password strength requirements (minimum 6 characters)
- ✅ Environment variables for sensitive configuration

## 🛣️ API Routes

| Route | Method | Description | Auth Required |
|-------|--------|-------------|----------------|
| `/` | GET | Home page - top headlines | No |
| `/category/<cat>` | GET | Category-specific news | No |
| `/register` | GET, POST | User registration | No |
| `/login` | GET, POST | User login | No |
| `/logout` | GET | User logout | Yes |
| `/voice-brief` | GET | Voice briefing (MP3) | No |
| `/admin` | GET | Admin dashboard | Yes (Admin) |
| `/admin/delete_user/<id>` | POST | Delete user account | Yes (Admin) |

## 📧 Email Configuration

### Gmail Setup
1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Use the app password in `MAIL_PASSWORD` in `.env`

### Other Email Providers
Update `MAIL_SERVER` and `MAIL_PORT` for your provider:
- **Outlook**: smtp-mail.outlook.com:587
- **Yahoo**: smtp.mail.yahoo.com:587
- **Custom**: Check your email provider's SMTP settings

## 🚀 Deployment

### For Production
1. Set `debug=False` in `app.py`
2. Use a production WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

3. Use environment-specific configuration
4. Set up HTTPS/SSL certificate
5. Use a production database (PostgreSQL recommended)

## 🐛 Troubleshooting

### "Email already registered" error
- The email is already in the database
- Use a different email or try logging in

### "Invalid email or password" on login
- Check that email and password are correct
- Passwords are case-sensitive
- Ensure caps-lock is off

### Voice Brief not working
- Check your internet connection
- Verify NEWS_API_KEY is valid
- Check if you have articles available

### Email notifications not sending
- Verify MAIL_SERVER and MAIL_PORT settings
- Confirm MAIL_USERNAME and MAIL_PASSWORD are correct
- Check Gmail app-specific password (if using Gmail)
- Verify ADMIN_EMAIL in .env

### Database errors
- Delete `newsbot.db` to reset database
- Ensure `sqlite:///newsbot.db` path is writable

## 📚 Environment Variables Reference

```env
# Flask Configuration
SECRET_KEY              # Flask secret key for sessions
SQLALCHEMY_DATABASE_URI # Database connection string

# News API
NEWS_API_KEY           # API key from newsapi.org

# Email Configuration
MAIL_SERVER            # SMTP server address
MAIL_PORT              # SMTP port (usually 587)
MAIL_USE_TLS           # Use TLS encryption (True/False)
MAIL_USERNAME          # Email address to send from
MAIL_PASSWORD          # Email password or app password

# Admin
ADMIN_EMAIL            # Email to receive notifications
```

## 🔮 Future Enhancements

- [ ] Search functionality
- [ ] Article bookmarking/favorites
- [ ] User preferences and customization
- [ ] Dark mode theme
- [ ] Mobile app
- [ ] Social media sharing
- [ ] Article recommendations based on reading history
- [ ] Multiple language support
- [ ] Push notifications
- [ ] Advanced user analytics

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

**Levi Odanga** - [@odangalevi-oss](https://github.com/odangalevi-oss)

## 📧 Contact

For questions, suggestions, or support:
- Email: [odangalevi@gmail.com](mailto:odangalevi@gmail.com)
- GitHub: [@odangalevi-oss](https://github.com/odangalevi-oss)

## 🙏 Acknowledgments

- [NewsAPI.org](https://newsapi.org) for news data
- [gTTS](https://gtts.readthedocs.io/) for text-to-speech
- [Flask](https://flask.palletsprojects.com/) framework
- Community contributors and users

---

**Happy news reading! 📰🤖**
