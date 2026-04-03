const mongoose = require('mongoose');

const IoTSchema = new mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  moisture: { type: Number, required: true },
  ph: { type: Number, required: true },
  nitrogen: { type: Number },
  phosphorus: { type: Number },
  potassium: { type: Number },
  timestamp: {
    type: Date,
    default: Date.now
  }
});

module.exports = mongoose.model('IoTData', IoTSchema);
