$(document).ready(function () {

    Page.hideOverlay();
    $(".reader-internet-status").hide()
    $.ajax({
        type: 'GET',
        url: '/dados_equipamento',
        success: function (response) {
            try {
                response = JSON.parse(response)
            } catch (excecao) {
               response = response
            } 
            if (response.status_e == "success") {
                $('.reader-name').html(response.modelo)
                verifyStatus();
            }
            else {
                $('.reader-name').html("O Equipamento não está configurado");

                showToast("success", "Aguarde o painel de configurações", 1000)
                $.ajax({
                    type: 'GET',
                    url: '/configurar/view/',
                    success: function (response) {
                        $(".reader-configurations").html(response)
                        Page.hideOverlay()
                    },
                    error: function (xhr, status, error) {
                        console.error('Erro na solicitação AJAX:', error);
                    }
                })
            }
        },
        error: function (xhr, status, error) {
            console.error('Erro na solicitação AJAX:', error);
        }
    })

    function verifyStatus() {
        $(".reader-internet-status").show()

        $.ajax({
            type: 'GET',
            url: '/status',
            success: function (response) {
                if (response.status == "success") {
                    $(".reader-internet-status").html("<i class='fa-solid fa-wifi'></i> Conectado com a internet").removeClass("disconnected").addClass("connected")
                    showToast(response.status, "Conectado com a internet", duration = 3000)

                }
                else {
                    $(".reader-internet-status").html("<i class='fa-solid fa-wifi'></i> Sem conexão com a internet").removeClass("connected").addClass("disconnected")
                    showToast(response.status, "Sem conexão com a internet", duration = 3000)
                }
            },
            error: function (xhr, status, error) {
                console.error('Erro na solicitação AJAX:', error);
            }
        })
    }
    $(document).on("submit", "#configurar-equipamento", function (e) {
        e.preventDefault();
        $(".info-loader").html(`
        <div class="d-flex justify-content-center">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      `);
        let nome_equipamento = $("#nome_equipamento").val();
        let dados = {
            "nome_equipamento": nome_equipamento
        }
        $.ajax({
            type: 'POST',
            url: '/configurar/equipamento/',
            contentType: 'application/json', // Especifica o tipo de mídia como JSON
            data: JSON.stringify(dados),// Especifica o tipo de mídia como JSON
            success: function (response) {
                if (response.status == "success") {
                    showToast(response.status, response.message, 3000)
                    $(".info-loader").html(`
                <div class="alert alert-success" role="alert">
                    ${response.message}
                </div>
                `)
                }
                else if(response.status == "error") {
                    showToast(response.status, response.message, 3000)
                    $(".info-loader").html(`
                <div class="alert alert-danger" role="alert">
                    ${response.message}: Verifique se o equipamento existe no sistema.
                </div>
                `)
                }

            },
            error: function (xhr, status, error) {
                console.error('Erro na solicitação AJAX:', error);
            }

        });
    })
});