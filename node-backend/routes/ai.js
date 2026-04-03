const express = require('express');
const router = express.Router();
const { GoogleGenerativeAI } = require('@google/generative-ai');
const auth = require('../middleware/auth');

router.post('/chat', auth, async (req, res) => {
  const { message, language } = req.body;
  
  const apiKey = process.env.GEMINI_API_KEY || "YOUR_DUMMY_GEMINI_KEY_FOR_LOCAL_DEV";
  if (!apiKey) {
    return res.status(500).json({ msg: 'Gemini API Key is not configured' });
  }
  
  try {
    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({ model: "gemini-pro"});
    
    const prompt = `You are an expert, friendly agricultural assistant for an app called Farmer's Friend. 
    You must reply in ${language || 'English'}. The user says: ${message}`;
    
    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();
    
    res.json({ reply: text });
  } catch (err) {
    console.error('Gemini error:', err);
    res.status(500).json({ msg: 'AI Chat integration failed' });
  }
});

module.exports = router;
