const express = require('express');
const router = express.Router();
const auth = require('../middleware/auth');
const IoTData = require('../models/IoTData');

// @route   POST api/iot/sensor-data
// @desc    Receive IoT telemetry
router.post('/sensor-data', auth, async (req, res) => {
  try {
    const { moisture, ph, nitrogen, phosphorus, potassium } = req.body;
    const newData = new IoTData({
      user: req.user.id,
      moisture,
      ph,
      nitrogen,
      phosphorus,
      potassium
    });
    
    const data = await newData.save();
    res.json(data);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

// @route   GET api/iot/sensor-data
// @desc    Get user's latest IoT telemetry
router.get('/sensor-data', auth, async (req, res) => {
  try {
    const data = await IoTData.find({ user: req.user.id }).sort({ timestamp: -1 }).limit(10);
    res.json(data);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

module.exports = router;
