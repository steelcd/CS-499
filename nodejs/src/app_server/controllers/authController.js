const authService = require('../services/authService');

const showLogin = (req, res) => {
    if (req.session.user) {
        return res.redirect('/index');
    }
    
    res.render('login', { title: 'AAC Rescue Login' });
};

const login = (req, res) => {
    const { email, password } = req.body;

    const user = authService.authenticateUser(email, password);

    if (!user) {
        return res.status(401).render('login', {
        title: 'AAC Rescue Login',
        error: 'Invalid email or password',
        email,
        });
    }

    req.session.user = user;
    return res.redirect('/index');
};

const logout = (req, res) => {
  req.session.destroy(() => {
    res.redirect('/login');
  });
};

module.exports = {
  showLogin,
  login,
  logout,
};