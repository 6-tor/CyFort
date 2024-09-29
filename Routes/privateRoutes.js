const authMiddleware = require('./authMiddleware'); // Importa o middleware de autenticação
const express = require('express'); // Importa o Express
const router = express.Router(); // Cria um roteador

// Rota privada protegida
router.get('/private', authMiddleware, (req, res) => {
    res.json({ message: 'Esta é uma rota privada!' }); // Retorna mensagem de sucesso
});

// Rota de login
router.post('/login', (req, res) => {
    const { username, password } = req.body; // Extrai username e password do corpo da requisição

    // Validação de usuário (exemplo hardcoded)
    if (username === 'user' && password === 'pass') {
        const token = jwt.sign({ username }, process.env.JWT_SECRET); // Cria um token JWT
        return res.json({ token }); // Retorna o token
    }
    return res.status(401).json({ message: 'Usuário ou senha inválidos' }); // Mensagem de erro
});

// Exporta as rotas
module.exports = router;