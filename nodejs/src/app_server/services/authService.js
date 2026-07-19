function authenticateUser(email, password) {
    // TODO: Replace stubbed credentials with MongoDB user lookup and password hashing.
    if(email=='admin@admin.com' && password=='password') {
        return(
            {
                id: 'app-admin',
                email: email,
                role: 'admin'
            }
        );
    }
    
    return null;
}

module.exports = {
    authenticateUser
};