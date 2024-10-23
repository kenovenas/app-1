fetch('https://<SEU_ENDPOINT_DO_RENDER>/authorize', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username: 'user' }), // Substitua pelo nome do usuário
})
.then(response => response.json())
.then(data => {
    if (data.status === 'success') {
        console.log('Usuário autorizado');
        // Lógica para continuar a execução da extensão
    } else {
        console.log('Usuário não autorizado');
    }
})
.catch((error) => {
    console.error('Erro:', error);
});
