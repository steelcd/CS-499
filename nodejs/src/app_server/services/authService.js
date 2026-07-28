const AppUser = require('../../app_api/models/app_user');

async function authenticateUser(email, password) {
    const user = await AppUser.findOne({
        email: email,
        is_active: true
    });

    if (!user || !(await user.validPassword(password))) {
        return null;
    }

    return {
        id: user._id.toString(),
        email: user.email,
        roles: user.roles,
        shelter_claims: user.shelter_claims
    };
}

module.exports = {
    authenticateUser
};
