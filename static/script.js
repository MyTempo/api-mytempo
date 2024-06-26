class Page {

    static hideOverlay() {
        $("#overlay").fadeOut('slow', function() {});    
    }
    static showOverlay() {
        $("#overlay").fadeIn(1000).delay(3000)
    }
}

function startCountdown(duration, elementId) {
    var count = duration;
    var countdownElement = document.getElementById(elementId); 
  
    var interval = setInterval(function() {
      if (count <= 0) {
        clearInterval(interval);
      } else {
        countdownElement.textContent = count; 
        count--;
      }
    }, 1000);
  }
  
  // Exemplo de uso:
  startCountdown(10, 'contador'); // Contador de 10 segundos no elemento com ID 'contador'
  
  
function showToast(type="success", message="", duration=3000) {
    let bodyPage = document.body;

    let toastContainer = document.createElement("div");
    toastContainer.className = "toast-container position-fixed top-0 end-0 p-6";

    let toastHTML = '';
    if (type === "error") {
        toastHTML = `
            <div class="toast bg-danger" role="alert" aria-live="assertive" aria-atomic="true" style="color:white;" data-delay="${duration}">
                <div class="toast-body">
                    <div class="d-flex gap-4">
                        <span><i class="fa-solid fa-circle-xmark fa-lg icon-error"></i></span>
                        <div class="d-flex flex-column flex-grow-1 gap-2">
                            <div class="d-flex align-items-center">
                                <span class="fw-semibold">Ocorreu um erro!</span>
                                <button type="button" class="btn-close btn-close-sm ms-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                            </div>
                            <span>${message}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    } else if (type === "success") {
        toastHTML = `
            <div class="toast bg-success" role="alert" aria-live="assertive" aria-atomic="true" style="color:white;" data-delay="${duration}">
                <div class="toast-body">
                    <div class="d-flex gap-4">
                        <span><i class="fa-solid fa-circle-check fa-lg icon-success"></i></span>
                        <div class="d-flex flex-column flex-grow-1 gap-2">
                            <div class="d-flex align-items-center">
                                <span class="fw-semibold">Sucesso!</span>
                                <button type="button" class="btn-close btn-close-sm ms-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                            </div>
                            <span>${message}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    } else {
        // Tipo desconhecido
        console.error("Tipo de toast desconhecido:", type);
        return;
    }

    toastContainer.innerHTML = toastHTML;


    bodyPage.appendChild(toastContainer);

    let toastLiveExample = toastContainer.querySelector(".toast");
    let toast = new bootstrap.Toast(toastLiveExample);
    toast.show();
}

function criarCaixaDialogo(textoPergunta, textoCancelar, textoDeletar, funcaoDeletar) {
    var overlay = document.createElement('div');
    overlay.classList.add('overlay');
    overlay.id = 'overlay';

    var confirmationBox = document.createElement('div');
    confirmationBox.classList.add('confirmation-box');
    confirmationBox.id = 'confirmationBox';

    var paragrafo = document.createElement('p');
    paragrafo.textContent = textoPergunta;
    confirmationBox.appendChild(paragrafo);

    var botaoCancelar = document.createElement('button');
    botaoCancelar.classList.add('cancel-button');
    botaoCancelar.textContent = textoCancelar;
    botaoCancelar.onclick = function () {
        fecharOverlay();
    };
    confirmationBox.appendChild(botaoCancelar);

    var botaoDeletar = document.createElement('button');
    botaoDeletar.classList.add('delete-button');
    botaoDeletar.textContent = textoDeletar;
    botaoDeletar.onclick = function () {
        if (typeof funcaoDeletar === 'function') {
            funcaoDeletar();
            fecharOverlay(); 
        }
    };
    confirmationBox.appendChild(botaoDeletar);

  
    overlay.appendChild(confirmationBox);


    document.body.appendChild(overlay);

    abrirOverlay();
}

function abrirOverlay() {
    var overlay = document.getElementById('overlay');
    var confirmationBox = document.getElementById('confirmationBox');

    overlay.style.display = 'flex';
    setTimeout(function () {
        overlay.classList.add('active');
        confirmationBox.classList.add('active');
    }, 10);
}

function fecharOverlay() {
    var overlay = document.getElementById('overlay');
    var confirmationBox = document.getElementById('confirmationBox');

    overlay.classList.remove('active');
    confirmationBox.classList.remove('active');

    setTimeout(function () {
        overlay.style.display = 'none';
        
        document.body.removeChild(overlay);
    }, 300);
}

function confirmarDelecao() {
    
    alert("Item deletado com sucesso!");
    
}
function extractSessionNumber(filename) {
    let regex = /-Sess-(\d{3})/;
    
    let match = regex.exec(filename);
    
    if (match) {
        return match[1];  
    } else {
        return "";  
    }
}