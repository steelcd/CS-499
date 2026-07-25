const express = require('express');
const session = require('express-session');
const path = require('path');
const { engine } = require('express-handlebars');
const app = express()
const port = 3000
const dashboardRoute = require('./app_server/routes/dashboard');
const { requireLogin, requireAdmin } = require('./app_server/middleware/authMiddleware');
const authController = require('./app_server/controllers/authController');
const rescueCandidatesRouter = require('./app_api/routes/rescueCandidates');

// Define routers
var apiRouter = require('./app_api/routes/index');

// Bring in the database
require('./app_api/models/db');

app.engine('hbs', engine({ extname: '.hbs' }));
app.set('view engine', 'hbs');
app.set('views', path.join(__dirname, 'app_server/views'));

app.use(express.urlencoded({ extended: false }));

// Create login session
app.use(session({
  secret: 'aac-rescue-dev-secret',
  resave: false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,
    secure: true,
    maxAge: 86400000
  },
}));
app.set('trust proxy', 1);
app.use(express.static(path.join(__dirname, 'public')));

app.use('/api', express.json({ limit: '1mb' }), apiRouter);
app.use('/api/rescue-candidates', rescueCandidatesRouter);

// Server vue.js app
app.use('/admin', requireLogin, express.static(path.join(__dirname, 'app-admin/dist')));

app.get('/', (req, res) => {
  if (req.session.user) {
    return res.redirect('/index');
  }

  return res.redirect('/login');
});

app.get('/login', authController.showLogin);
app.post('/login', authController.login);
app.get('/logout', authController.logout);

app.get('/index', requireLogin, (req, res) => {
  res.render('index', { title: 'AAC Rescue' })
})

app.get(/^\/dashboard$/, requireLogin, (req, res) => {
  res.redirect('/dashboard/')
})

app.use('/dashboard', requireLogin, dashboardRoute);

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})
