const mongoose = require('mongoose');
const { type } = require('node:os');
// Define the animal schema
const animalSchema = new mongoose.Schema({
    age_upon_outcome: { type: String, required: true },
    animal_id: { type: String, required: true, index: true, unique: true },
    animal_type: { type: String, required: true, index: true },
    breed: { type: String, required: true, index: true },
    color: { type: String, required: true },
    date_of_birth: { type: Date, required: true, index: true },
    datetime: { type: Date, required: true },
    name: { type: String, required: false },
    outcome_subtype: { type: String, required: false, index: true },
    outcome_type: { type: String, required: true, index: true },
    sex_upon_outcome: { type: String, required: true, index: true },
    location_lat: { type: Number, required: true },
    location_long: { type: Number, required: true },
    age_upon_outcome_in_weeks: { type: Number, required: true },
    shelter: { type: String, required: true }
});
const Animal = mongoose.model('animals', animalSchema);
module.exports = Animal;