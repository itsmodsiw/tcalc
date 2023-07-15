const express = require('express');
const app = express();

app.use(express.static('public'));  // serve static files from the 'public' directory

app.get('/', (req, res) => {
  res.send('Hello, World!');
});

app.listen(process.env.PORT || 3000, () => {
  console.log('App is listening...');
});
