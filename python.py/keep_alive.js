const express = require('express');

const app = express();
const PORT = process.env.PORT || 8080;

// Keep-alive endpoint
app.get('/', (req, res) => {
    res.send("I'm alive");
});

// Start the server
app.listen(PORT, () => {
    console.log(`Keep-alive server is running on port ${PORT}`);
});
