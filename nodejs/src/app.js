const express = require('express');
const session = require('express-session');
const path = require('path');
const { engine } = require('express-handlebars');
const app = express()
const port = 3000
const dashboardRoute = require('./app_server/routes/dashboard');
const { requireLogin, requireShelterAdmin } = require('./app_server/middleware/authMiddleware');
const authController = require('./app_server/controllers/authController');
const rescueCandidatesRouter = require('./app_api/routes/rescueCandidates');
const animalsController = require('./app_api/controllers/animals');

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
// Set local variable admin page access
app.use((req, res, next) => {
  const roles = req.session.user?.roles || [];
  res.locals.canAccessAdmin = roles.includes('admin') || roles.includes('shelter_admin');
  next();
});
app.set('trust proxy', 1);
app.use(express.static(path.join(__dirname, 'public')));

app.get('/api/animals', animalsController.animalsList);
app.use('/api/rescue-candidates', rescueCandidatesRouter);
app.use('/api/admin', express.json({ limit: '1mb' }), requireLogin, requireShelterAdmin, apiRouter);

// Server vue.js app
app.get(/^\/admin$/, requireLogin, requireShelterAdmin, (req, res) => {
  res.redirect('/admin/');
});
app.get(/^\/admin\/$/, requireLogin, requireShelterAdmin, (req, res) => {
  res.sendFile(path.join(__dirname, 'app-admin/dist/index.html'));
});
app.use('/admin', requireLogin, requireShelterAdmin, express.static(path.join(__dirname, 'app-admin/dist')));
app.get(/^\/admin\/.*$/, requireLogin, requireShelterAdmin, (req, res) => {
  res.sendFile(path.join(__dirname, 'app-admin/dist/index.html'));
});

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
