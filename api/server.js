// api/server.js
import express from 'express';
const app = express();
app.use(express.json());

app.post('/evaluate', (req, res) => {
  const { prompt } = req.body || {};

  let answer = 'Mock answer';

  // Rule-based responses for Postman tests
  if (prompt) {
    if (prompt.toLowerCase().includes('capital of france')) {
      answer = 'Paris';
    } else if (prompt.toLowerCase().includes('hello')) {
      answer = 'Hello -> answer';
    } else {
      answer = `${prompt} -> answer`;
    }
  } else {
    answer = 'Mock: no prompt';
  }

  res.json({ response: answer });
});

app.listen(8000, () => console.log('Mock LLM running on port 8000'));

