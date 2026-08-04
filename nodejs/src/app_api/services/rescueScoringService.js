function scoreAnimal(animal, profile) {
  let rawScore = 0;
  let maxScore = 0;

  const breakdown = [];

  for (const rule of profile.rules) {
    const animalValue = animal[rule.field];
    const weight = rule.weight || 0;

    maxScore += weight;

    let matched = false;

    if (rule.type === 'equals') {
      matched = animalValue === rule.value;
    }

    if (rule.type === 'in') {
      matched = Array.isArray(rule.values) && rule.values.includes(animalValue);
    }

    if (rule.type === 'range') {
      const numericValue = Number(animalValue);
      matched =
        !Number.isNaN(numericValue) &&
        numericValue >= rule.min &&
        numericValue <= rule.max;
    }

    if (matched) {
      rawScore += weight;
    }

    breakdown.push({
      field: rule.field,
      type: rule.type,
      matched,
      weight,
      points_awarded: matched ? weight : 0,
      animal_value: animalValue
    });
  }

  const score = maxScore > 0
    ? Math.round((rawScore / maxScore) * 100)
    : 0;

  return {
    score
  };
}


// Fetch results for required fields, reduce excess compute to calculate scored on all records
function buildRequiredQuery(profile) {
  const query = {};

  if (!profile.required) {
    return query;
  }

  for (const [field, value] of Object.entries(profile.required)) {
    query[field] = value;
  }

  return query;
}

module.exports = {
  scoreAnimal,
  buildRequiredQuery
};