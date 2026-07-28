const { default: mongoose } = require('mongoose');
const Animal = require('../models/animal');

function getShelterFilter(req) {
    const user = req.session.user;
    const roles = user?.roles || [];

    if (roles.includes('admin')) {
        return {};
    }

    return {
        shelter: {
            $in: user?.shelter_claims || []
        }
    };
}

function canManageShelter(req, shelter) {
    const user = req.session.user;
    const roles = user?.roles || [];

    return roles.includes('admin') || (user?.shelter_claims || []).includes(shelter);
}

// GET: /animals - lists all animals
const animalsList = async(req, res) => {
    try {
        const q = await Animal
            .find(getShelterFilter(req))
            .exec();

        return res
            .status(200)
            .json(q);
    } catch (err) {
        return res
            .status(500)
            .json(
                {
                    message: 'Error retrieving animals',
                    error: err.message
                }
            );
    }
};

// POST /animals - add a new animal
const animalsAddAnimal = async(req, res) => {
    const now = new Date();

    if (!canManageShelter(req, req.body.shelter)) {
        return res
            .status(403)
            .json(
                {
                    message: 'Not authorized for this shelter'
                }
            );
    }

    const newAnimal = new Animal({
        age_upon_outcome: req.body.age_upon_outcome,
        animal_id: req.body.animal_id,
        animal_type: req.body.animal_type,
        breed: req.body.breed,
        color: req.body.color,
        date_of_birth: req.body.date_of_birth,
        datetime: now,
        name: req.body.name,
        outcome_subtype: req.body.outcome_subtype,
        outcome_type: req.body.outcome_type,
        sex_upon_outcome: req.body.sex_upon_outcome,
        location_lat: req.body.location_lat,
        location_long: req.body.location_long,
        age_upon_outcome_in_weeks: req.body.age_upon_outcome_in_weeks,
        shelter: req.body.shelter
    });

    try {
        const q = await newAnimal
            .save();

        if(!q)
        {
            return res
                .status(400)
                .json(
                    {
                        message: "Animal not saved"
                    }
                );
        } else {
            return res
                .status(200)
                .json(q);
        }
    } catch(err) {
        return res.status(500).json(
            {
            message: 'Error saving animal',
            error: err.message
            }
        );
    }
};


// PUT: /animals/:animalId - update a single animal
const animalsUpdateAnimal = async(req, res) => {
    if (!canManageShelter(req, req.body.shelter)) {
        return res
            .status(403)
            .json(
                {
                    message: 'Not authorized for this shelter'
                }
            );
    }

    try{
        const q = await Animal
            .findOneAndUpdate(
                {
                    'animal_id': req.params.animalId,
                    ...getShelterFilter(req)
                },
                {
                    age_upon_outcome: req.body.age_upon_outcome,
                    animal_type: req.body.animal_type,
                    breed: req.body.breed,
                    color: req.body.color,
                    date_of_birth: req.body.date_of_birth,
                    name: req.body.name,
                    outcome_subtype: req.body.outcome_subtype,
                    outcome_type: req.body.outcome_type,
                    sex_upon_outcome: req.body.sex_upon_outcome,
                    location_lat: req.body.location_lat,
                    location_long: req.body.location_long,
                    age_upon_outcome_in_weeks: req.body.age_upon_outcome_in_weeks,
                    shelter: req.body.shelter
                },
                { new: true, runValidators: true }
            )
            .exec();

        if(!q)
        {
            return res
            .status(404)
            .json(
                {
                    message: 'Animal not found'
                }
            );
        } else {
            return res
                .status(201)
                .json(q);
        }
    } catch (err) {
        return res.status(500).json(
            {
                message: 'Error updating animal',
                error: err.message
            }
        );
    }
};


// GET: /animals/:animalId - returns a single animal
const animalsFindById = async(req, res) => {
    try {
        const q = await Animal
            .findOne({
                'animal_id' : req.params.animalId,
                ...getShelterFilter(req)
            })
            .exec();

        if(!q)
        { // Database returned no data
            return res
                .status(404)
                .json(
                    {
                        message: 'No record found'
                    }
                );
        } else { // Return matching animal
            return res
                .status(200)
                .json(q)
        }
    } catch(err) {
        return res
            .status(500)
            .json({
                message: 'Error getting animal record',
                error: err.message
            });
    }
};

// DELETE: /animals/:animalId - deletes a single animal
const animalsDeleteById = async(req, res) => {
    try {
        const q = await Animal
            .findOneAndDelete({
                'animal_id': req.params.animalId,
                ...getShelterFilter(req)
            })
            .exec();

        if(!q) {
            return res
                .status(404)
                .json(
                    {
                        message: 'Animal not found'
                    }
                )
        }

        return res
            .status(200)
            .json(
                {
                    message: 'Animal deleted'
                }
            )
    } catch(err) {
        return res
            .status(500)
            .json(
                {
                    message: 'Error deleting animal',
                    error: err.message
                }
            )
    }
}

module.exports = {
    animalsList,
    animalsUpdateAnimal,
    animalsAddAnimal,
    animalsFindById,
    animalsDeleteById
};
