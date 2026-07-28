const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

const SALT_ROUNDS = 12;

const AppUserSchema = new mongoose.Schema(
    {
        "email": {
            type: String,
            required: true,
            unique: true
        },
        "password_hash": {
            type: String,
            required: true
        },
        "is_active": {
            type: Boolean,
            required: true
        },
        "roles": {
            type: [String],
            required: true
        },
        "shelter_claims": {
            type: [String]
        }
    },
    {
        collection: 'app_users'
    }
);

// Method to set the password on this record.
AppUserSchema.methods.setPassword = async function(password) {
    this.password_hash = await bcrypt.hash(password, SALT_ROUNDS);
};

// Method to compare entered password against stored hash
AppUserSchema.methods.validPassword = async function(password) {
    return bcrypt.compare(password, this.password_hash);
};

const AppUser = mongoose.model('app_users', AppUserSchema);
module.exports = AppUser;
