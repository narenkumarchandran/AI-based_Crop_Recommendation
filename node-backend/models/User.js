const mongoose = require('mongoose');

const UserSchema = new mongoose.Schema({
  username: {
    type: String,
    required: true,
    unique: true
  },
  password: {
    type: String,
    required: true
  },
  tier: {
    type: String,
    enum: ['free_tier', 'premium_iot_tier'],
    default: 'free_tier'
  },
  farmLocation: {
    lat: { type: Number },
    lon: { type: Number },
    city: { type: String },
    state: { type: String }
  },
  preferredLanguage: {
    type: String,
    enum: ['en', 'hi', 'ta'],
    default: 'en'
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

module.exports = mongoose.model('User', UserSchema);
