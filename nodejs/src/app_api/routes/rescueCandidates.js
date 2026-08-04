const express = require('express');
const router = express.Router();

const Animal = require('../models/animal');
const RescueProfile = require('../models/rescueProfile');

const {
  scoreAnimal,
  buildRequiredQuery
} = require('../services/rescueScoringService');

router.get('/:profileKey', async (req, res) => {
  try {
    const profileKey = req.params.profileKey;

    // Cap at 500 scored records
    const limit = Math.min(
      Number(req.query.limit) || 100,
      500
    );

    // Fetch profile
    const profile = await RescueProfile.findOne({
      profile_key: profileKey,
      active: true
    }).lean();

    if (!profile) {
      return res.status(404).json({
        message: `Rescue profile not found: ${profileKey}`
      });
    }

    const query = buildRequiredQuery(profile);

    const animals = await Animal.find(query)
      .lean();

    // Apply score calculation query result
    const scoredAnimals = animals
      .map((animal) => {
        const scoring = scoreAnimal(animal, profile);

        return {
          _id: animal._id,
          age_upon_outcome: animal.age_upon_outcome,
          animal_id: animal.animal_id,
          animal_type: animal.animal_type,
          breed: animal.breed,
          color: animal.color,
          date_of_birth: animal.date_of_birth,
          datetime: animal.datetime,
          name: animal.name,
          outcome_subtype: animal.outcome_subtype,
          outcome_type: animal.outcome_type,
          sex_upon_outcome: animal.sex_upon_outcome,
          location_lat: animal.location_lat,
          location_long: animal.location_long,
          age_upon_outcome_in_weeks: animal.age_upon_outcome_in_weeks,
          shelter: animal.shelter,
          score: scoring.score
        };
      })
      .filter((animal) => animal.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, limit);
    
    return res
      .status(200)
      .json(scoredAnimals);
  } catch (error) {
    console.error('Error getting rescue candidates:', error);

    return res
      .status(500)
      .json({message: 'Error getting rescue candidates'});
  }
});

module.exports = router;