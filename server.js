const express = require('express'); // Importa o Express
const jwt = require('jsonwebtoken'); // Importa o JWT para autenticação
const privateRoutes = require('./routes/privateRoutes'); // Importa as rotas privadas
const app = express(); // Inicializa a aplicação Express
const port = 3000; // Define a porta do servidor

app.use(express.json()); // Permite o uso de JSON no corpo das requisições

app.use('/api', privateRoutes); // Define as rotas privadas sob o prefixo '/api'

// Rota para login
app.post('/login', (req, res) => {
    const { username, password } = req.body; // Extrai username e password do corpo da requisição

    // Aqui deve ser feita a validação real do usuário e senha (consultando um banco de dados, por exemplo)
    const token = jwt.sign({ username }, process.env.JWT_SECRET, { expiresIn: '1h' }); // Cria um token JWT
    res.json({ token }); // Retorna o token como resposta
});

// Inicia o servidor
app.listen(port, () => {
    console.log(`Servidor rodando em http://localhost:${port}`); // Mensagem de confirmação no console
});

require('dotenv').config(); // Carrega variáveis do arquivo .env