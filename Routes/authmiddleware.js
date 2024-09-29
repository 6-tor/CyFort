const jwt = require('jsonwebtoken'); // Importa o JWT

// Middleware para autenticação
const authMiddleware = (req, res, next) => {
    const token = req.headers['authorization']; // Obtém o token do cabeçalho

    console.log('Token recebido:', token); // Loga o token recebido

    if (!token) {
        return res.status(403).json({ message: 'Acesso negado.' }); // Sem token, acesso negado
    }

    jwt.verify(token, process.env.JWT_SECRET, (err, decoded) => { // Verifica o token
        if (err) {
            console.log('Erro na verificação do token:', err); // Loga o erro
            return res.status(401).json({ message: 'Token inválido.' }); // Token inválido
        }
        req.user = decoded; // Armazena os dados do usuário na requisição
        next(); // Chama o próximo middleware
    });
};

module.exports = authMiddleware; // Exporta o middleware
