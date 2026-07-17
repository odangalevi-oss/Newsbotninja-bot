# Render Configuration Guide

## Deploying Newsbotninja-Bot to Render

### Prerequisites
- GitHub account with this repository
- Render account (free tier available)
- NewsAPI key (from https://newsapi.org)
- Gmail account with app-specific password (for email notifications)

### Step-by-Step Deployment

#### 1. Push Code to GitHub
Make sure all code is pushed to your GitHub repository:
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

#### 2. Create a New Web Service on Render

1. Go to [https://dashboard.render.com](https://dashboard.render.com)
2. Click **"New+"** button and select **"Web Service"**
3. Connect your GitHub repository (authorize if needed)
4. Select **Newsbotninja-bot** repository
5. Fill in the configuration:
   - **Name**: `newsbotninja-bot` (or your preferred name)
   - **Environment**: Python 3
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free (or Starter for better performance)

#### 3. Set Environment Variables

In the Render dashboard, go to **Environment** tab and add:

```
SECRET_KEY=your-very-secret-key-here-generate-random-string

NEWS_API_KEY=your-newsapi-key-from-newsapi.org

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password-from-gmail

ADMIN_EMAIL=odangalevi@gmail.com

FLASK_ENV=production
```

**Important Notes:**
- **SECRET_KEY**: Generate a random string (at least 32 characters)
- **NEWS_API_KEY**: Get from https://newsapi.org (free plan available)
- **MAIL_PASSWORD**: Use Gmail app-specific password, NOT your regular password
  - Enable 2FA on Gmail
  - Generate app password: https://myaccount.google.com/apppasswords
- **FLASK_ENV**: Set to `production`

#### 4. Configure Database

Render automatically provides persistent storage at `/var/data/`. The app uses SQLite which will be stored there.

If you want to use PostgreSQL (recommended for production):

1. Create a PostgreSQL database on Render
2. Get the connection string
3. Set `DATABASE_URL` environment variable to the PostgreSQL connection string
4. Update `requirements.txt` to include `psycopg2-binary`

#### 5. Deploy

1. Click **"Create Web Service"**
2. Render will automatically build and deploy your app
3. Wait for deployment to complete (usually 2-3 minutes)
4. Your app will be available at: `https://newsbotninja-bot.onrender.com`

#### 6. Monitor Deployment

- Check deployment logs in the Render dashboard
- Look for any build or runtime errors
- Test your application at the provided URL

### First Time Setup on Render

When your app first starts on Render:

1. The SQLite database will be created automatically
2. Navigate to `/register` to create your first account
3. The first account will automatically be an admin
4. You're ready to use your app!

### Troubleshooting

**Build fails with "No such file"**
- Make sure all required files are pushed to GitHub
- Check that `Procfile` exists in the root directory

**App crashes after deployment**
- Check Logs in Render dashboard
- Ensure all environment variables are set correctly
- Verify NEWS_API_KEY is valid

**Email not sending**
- Verify Gmail app password is correct (not regular password)
- Check that 2FA is enabled on Gmail
- Ensure MAIL_USERNAME and ADMIN_EMAIL are correct

**Database errors on first run**
- This is normal - the database is being created
- Refresh the page after a few seconds

**Free tier goes to sleep**
- Free tier services go idle after 15 minutes of inactivity
- They restart automatically when accessed
- Upgrade to Starter tier for always-on service

### Upgrade from Free to Paid

For production use:
1. Go to instance settings
2. Upgrade to **Starter** or **Standard** tier
3. Billing will be prorated

### Custom Domain (Optional)

1. In Render dashboard, go to **Settings**
2. Add custom domain in **Domains** section
3. Configure DNS records at your domain provider
4. Set up free SSL certificate automatically

### Performance Tips

- Upgrade to at least **Starter** tier for production
- Use PostgreSQL instead of SQLite for multiple users
- Enable caching for news articles
- Monitor resource usage in Render dashboard

---

**Your app will be live at**: `https://your-app-name.onrender.com`

Enjoy your deployed news bot! 🚀📰
