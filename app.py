fetch('https://app-1-885k.onrender.com/authorize', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username: 'nome' }),  // Altere para o nome de usuário atual
})
.then(response => response.json())
.then(data => {
    if (data.status === 'success') {
        console.log('Usuário autorizado:', data.message);
    } else {
        console.log('Erro de autorização:', data.message);
    }
})
.catch((error) => {
    console.error('Erro:', error);
});
