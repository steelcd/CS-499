const mongoose = require('mongoose');

const RescueProfileSchema = new mongoose.Schema(
  {
    profile_key: {
      type: String,
      required: true,
      unique: true
    },
    profile_name: String,
    active: {
      type: Boolean,
      default: true
    },
    display_order: Number,
    description: String,
    recommendation_threshold: Number,

    required: {
      type: mongoose.Schema.Types.Mixed,
      default: {}
    },

    rules: [
      {
        field: String,
        type: String,
        values: [mongoose.Schema.Types.Mixed],
        value: mongoose.Schema.Types.Mixed,
        min: Number,
        max: Number,
        weight: Number
      }
    ]
  },
  {
    collection: 'rescue_profiles'
  }
);

module.exports = mongoose.model('RescueProfile', RescueProfileSchema);