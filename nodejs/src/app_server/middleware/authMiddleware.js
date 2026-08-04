function requireLogin(req, res, next) {
    if (!req.session.user) {
        return res.redirect('/login');
    }

    next();
}

function requireShelterAdmin(req, res, next) {
    if (
        !req.session.user || !req.session.user.roles || !(req.session.user.roles.includes('admin') || req.session.user.roles.includes('shelter_admin'))){
        return res.status(403).send('Forbidden');
    }

    next();
}

module.exports = {
    requireLogin,
    requireShelterAdmin
};
