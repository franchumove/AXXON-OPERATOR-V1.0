const express = require('express');
const { google } = require('googleapis');
require('dotenv').config();

const app = express();
const port = 3000;

const oauth2Client = new google.auth.OAuth2(
  process.env.GOOGLE_CLIENT_ID,
  process.env.GOOGLE_CLIENT_SECRET,
  process.env.REDIRECT_URI
);

// Paso 1: Redirigir al login de Google
app.get('/', (req, res) => {
  const url = oauth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: ['https://www.googleapis.com/auth/drive.file'],
  });
  res.send(`<a href="${url}">Iniciar sesión con Google</a>`);
});

// Paso 2: Recibir el código y mostrar token
app.get('/oauth2callback', async (req, res) => {
  const code = req.query.code;
  try {
    const { tokens } = await oauth2Client.getToken(code);
    oauth2Client.setCredentials(tokens);
    res.send(`<pre>${JSON.stringify(tokens, null, 2)}</pre>`);
  } catch (err) {
    res.send('Error al obtener token: ' + err.message);
  }
});

app.listen(port, () => {
  console.log(`Servidor listo en http://localhost:${port}`);
});