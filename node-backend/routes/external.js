const express = require('express');
const router = express.Router();
const axios = require('axios');
const xml2js = require('xml2js');
const auth = require('../middleware/auth');

router.get('/weather', auth, async (req, res) => {
  const { city, state } = req.query;
  const apiKey = process.env.WEATHER_API_KEY || '4e5616eb1d4743d4b4b203604252309';
  
  try {
    const response = await axios.get(`https://api.weatherapi.com/v1/current.json`, {
      params: { key: apiKey, q: `${city},${state},India`, aqi: 'no' }
    });
    res.json(response.data);
  } catch (err) {
    console.error('Weather fetching error', err.message);
    res.status(500).json({ msg: 'Weather fetch failed' });
  }
});

router.get('/market-prices', auth, async (req, res) => {
  const { state, district, commodity } = req.query;
  const apiKey = process.env.AGMARKNET_API_KEY || '579b464db66ec23bdd000001f1ce979336e3422966acd01a029a17be';
  
  try {
    const response = await axios.get(`https://api.data.gov.in/resource/35985678-0d79-46b4-9ed6-6f13308a1d24`, {
      params: {
        'api-key': apiKey,
        format: 'xml',
        offset: 0,
        limit: 10,
        'filters[State]': state ? state.toLowerCase() : undefined,
        'filters[District]': district ? district.toLowerCase() : undefined,
        'filters[Commodity]': commodity ? commodity.toLowerCase() : undefined
      }
    });
    
    // Parse XML
    const parser = new xml2js.Parser({ explicitArray: false });
    parser.parseString(response.data, (err, result) => {
      if (err) {
        return res.status(500).json({ msg: 'Failed to parse XML from Agmarknet' });
      }
      res.json(result);
    });
  } catch (err) {
    console.error('Agmarknet Fetching error', err.message);
    res.status(500).json({ msg: 'Agmarknet fetch failed' });
  }
});

module.exports = router;
