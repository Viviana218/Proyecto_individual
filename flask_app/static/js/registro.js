var formulario = document.getElementById('registro_js');
formulario.onsubmit = function(e){
    e.preventDefault();
    var formData = new FormData(formulario)
    fetch("/add_usuario", {method: 'POST', body: formData})
    .then(response => response.json())
    .then(data => {
        if (data.message == 'Correcto'){
            window.location.href = '/dashboard';
        }
        var alertMessage = document.getElementById('alertMessage');
        alertMessage.innerText = data.message;
        alertMessage.classList.add('alert');
        alertMessage.classList.add('alert-danger');
    })
}

function aceptaPolitica() {
    var aceptaPolitica = document.querySelector('.politica')
    aceptaPolitica.remove();
    let registro = document.getElementById('registro');
    registro.disabled = false;
}


