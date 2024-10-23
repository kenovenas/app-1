// Exemplo de código para enviar solicitação POST
function authenticateUser(username) {
    fetch('https://app-1-885k.onrender.com', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message); // Verifique a resposta do servidor
        if (data.access) {
            // Acesso concedido, execute funções da extensão
            console.log("Acesso concedido.");
        } else {
            // Acesso negado
            console.log("Acesso negado.");
        }
    })
    .catch(error => {
        console.error('Erro:', error);
    });
}

// Exemplo de chamada da função
authenticateUser('usuario1'); // Substitua pelo usuário desejado
