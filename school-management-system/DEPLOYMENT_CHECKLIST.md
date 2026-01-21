# 📋 Deployment Checklist

## Pre-Deployment (Do This Now)

### 🔐 Security
- [ ] Generate new SECRET_KEY
  ```python
  from django.core.management.utils import get_random_secret_key
  print(get_random_secret_key())
  ```
- [ ] Change admin password from `admin123`
- [ ] Create strong DATABASE_URL with unique credentials
- [ ] Review CORS_ALLOWED_ORIGINS - set to your domain only
- [ ] Review ALLOWED_HOSTS - set to your domain
- [ ] Enable HTTPS/SSL certificate

### 🗄️ Database
- [ ] Database service selected (PostgreSQL)
- [ ] Database backup strategy planned
- [ ] Database migration script tested
- [ ] Admin user password changed

### 📦 Environment Variables
- [ ] DEBUG = False
- [ ] SECRET_KEY = (secure random key)
- [ ] ALLOWED_HOSTS = your-domain.com
- [ ] CORS_ALLOWED_ORIGINS = https://your-domain.com
- [ ] DATABASE_URL = postgresql://...

### 🧪 Testing
- [ ] Login functionality tested ✓ (Already confirmed)
- [ ] API endpoints tested
- [ ] Frontend loads correctly
- [ ] All features working
- [ ] No console errors

---

## Deployment Day (Choose One Path)

### 🚂 Path A: Railway.app (Recommended - 5 min)

```
Step 1: Go to railway.app
Step 2: Click "New Project" → "Deploy from GitHub"
Step 3: Select your repository
Step 4: Add PostgreSQL plugin
Step 5: Set environment variables (from above)
Step 6: Deploy!
Duration: 5 minutes
Cost: Free tier available
```

**✅ Checklist:**
- [ ] Railway account created
- [ ] GitHub connected
- [ ] Environment variables set
- [ ] PostgreSQL added
- [ ] Deploy button clicked
- [ ] App running at railway.app domain
- [ ] Can access /login
- [ ] Can login with admin credentials

---

### 🔴 Path B: Heroku (Traditional - 10 min)

```bash
# Step 1: Install & Login
heroku login

# Step 2: Create app
heroku create your-school-app

# Step 3: Add database
heroku addons:create heroku-postgresql:standard-0

# Step 4: Set config
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=<your-key>
heroku config:set ALLOWED_HOSTS=your-school-app.herokuapp.com
heroku config:set CORS_ALLOWED_ORIGINS=https://your-school-app.herokuapp.com

# Step 5: Deploy
git push heroku main

# Step 6: Migrate & Create Admin
heroku run python backend/manage.py migrate
heroku run python backend/create_admin.py
```

**✅ Checklist:**
- [ ] Heroku account created
- [ ] Heroku CLI installed
- [ ] App created
- [ ] PostgreSQL added
- [ ] Config vars set
- [ ] Code pushed
- [ ] Migrations ran
- [ ] Admin user created
- [ ] App accessible at herokuapp.com

---

### 🐳 Path C: Docker on VPS (20 min)

```bash
# On your VPS (DigitalOcean/Linode/AWS/Azure):

# Step 1: Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Step 2: Clone repo
git clone https://github.com/anurag9931043461/mtcs.git
cd school-management-system

# Step 3: Configure .env
cp backend/.env.production backend/.env
# Edit .env with your values

# Step 4: Start services
docker-compose up -d

# Step 5: Verify
docker-compose ps
```

**✅ Checklist:**
- [ ] VPS created
- [ ] SSH access confirmed
- [ ] Docker installed
- [ ] Repository cloned
- [ ] .env configured
- [ ] docker-compose up -d ran
- [ ] Containers running
- [ ] App accessible at http://vps-ip:3000

---

## Post-Deployment (Do This After)

### ✅ Verification
- [ ] Frontend loads at your domain
- [ ] Login page visible
- [ ] Can login with admin/admin123
- [ ] Dashboard loads
- [ ] API docs accessible at /api/docs/
- [ ] Admin panel at /admin/ accessible

### 🔒 Security Hardening
- [ ] Change admin password to new strong password
- [ ] Update admin email address
- [ ] Enable API rate limiting
- [ ] Enable HTTPS redirect
- [ ] Add security headers
- [ ] Configure firewall rules
- [ ] Enable database backups
- [ ] Set up error tracking (Sentry)
- [ ] Enable logging/monitoring

### 📊 Configuration
- [ ] Set up school information
- [ ] Create academic years
- [ ] Add classes
- [ ] Add subjects
- [ ] Create user roles if needed
- [ ] Configure fee structures
- [ ] Set transport routes

### 👥 User Setup
- [ ] Create additional admin users
- [ ] Create teacher accounts
- [ ] Create parent accounts
- [ ] Create student accounts
- [ ] Verify role-based access working

### 📱 Testing Features
- [ ] [ ] Test student enrollment
- [ ] [ ] Test attendance marking
- [ ] [ ] Test fee payment entry
- [ ] [ ] Test exam scheduling
- [ ] [ ] Test mark entry
- [ ] [ ] Test result publishing
- [ ] [ ] Test notification system

### 🚀 Performance
- [ ] Check page load times
- [ ] Check API response times
- [ ] Monitor server CPU/Memory
- [ ] Check database performance
- [ ] Verify email delivery (if configured)

### 📈 Monitoring Setup
- [ ] Enable server monitoring
- [ ] Set up log aggregation
- [ ] Configure alerts
- [ ] Set up uptime monitoring
- [ ] Monitor API usage
- [ ] Track user growth

---

## Ongoing Maintenance

### 🔄 Regular Tasks
- [ ] Daily: Check error logs
- [ ] Weekly: Verify database backups
- [ ] Weekly: Review user activity
- [ ] Monthly: Update dependencies
- [ ] Monthly: Review security logs
- [ ] Quarterly: Update system software

### 📚 Documentation
- [ ] Document admin credentials (secure location)
- [ ] Document deployment steps
- [ ] Document database backup procedures
- [ ] Create runbooks for common issues
- [ ] Document custom configurations

### 🤝 User Support
- [ ] Create help documentation
- [ ] Set up support email
- [ ] Create FAQ page
- [ ] Document all features
- [ ] Train admin users

---

## Critical URLs

Once deployed, save these:

```
Frontend:    https://your-domain.com
Backend API: https://your-domain.com/api
Admin Panel: https://your-domain.com/admin
API Docs:    https://your-domain.com/api/docs/
Login:       https://your-domain.com/login
```

---

## Emergency Contacts & Resources

### If Something Goes Wrong:

1. **Can't login?**
   - Check admin user exists: `python backend/manage.py shell`
   - Reset password: `python backend/manage.py changepassword admin`

2. **Database connection error?**
   - Verify DATABASE_URL format
   - Check database is running
   - Verify credentials

3. **Static files missing?**
   - Run: `python backend/manage.py collectstatic`

4. **CORS errors?**
   - Update CORS_ALLOWED_ORIGINS
   - Restart backend

5. **Need help?**
   - Check docs: GitHub repository
   - Review error logs
   - Open GitHub issue

---

## Success Criteria ✅

Your deployment is successful when:

✅ Frontend loads without errors
✅ Can login with admin account
✅ Dashboard displays correctly
✅ Can access admin panel
✅ API endpoints responding
✅ Database connected
✅ Static files loading
✅ No console errors
✅ No server errors
✅ Can perform basic operations

---

## Deployment Status

- [ ] Pre-deployment checklist complete
- [ ] Deployment executed
- [ ] Post-deployment verification complete
- [ ] All systems operational
- [ ] Users notified
- [ ] Monitoring active

---

**Deployed on:** _________________ (Date)

**Deployed by:** _________________ (Name)

**Platform:** _________________ (Railway/Heroku/VPS/etc)

**Domain:** _________________ 

**Backup location:** _________________

---

**Congratulations! Your School Management System is now live! 🎉**
