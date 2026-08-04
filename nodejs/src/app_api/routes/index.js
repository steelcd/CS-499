var express = require('express');
var router = express.Router();

const animalsController = require('../controllers/animals');

router  
    .route('/animals')
    .get(animalsController.animalsList)
    .post(animalsController.animalsAddAnimal);

router
    .route('/animals/:animalId')
    .get(animalsController.animalsFindById)
    .put(animalsController.animalsUpdateAnimal)
    .delete(animalsController.animalsDeleteById);

module.exports = router;