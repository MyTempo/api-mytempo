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
                atualizaEquipamento();
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
                    loadSysActions();
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
            contentType: 'application/json',
            data: JSON.stringify(dados),
            success: function (response) {
                if (response.status == "success") {
                    showToast(response.status, response.message, 3000)
                    $(".info-loader").html(`
                <div class="alert alert-success" role="alert">
                    ${response.message}
                </div>
                `)
                }
                else if (response.status == "error") {
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

    function loadSysActions() {
        $.ajax({
            type: 'GET',
            url: '/actions/view/',
            success: function (response) {
                $(".reader-configurations").html(response)
            },

            error: function (xhr, status, error) {
                console.error('Erro na solicitação AJAX:', error);
            }
        })
    }

    $(document).on("click", "#brutos-list", function () {
        $.ajax({
            type: 'GET',
            url: '/listar_arquivos/brutos/',
            success: function (response) {
                $(".arquivos-brutos-loader").hide();
                let ulElement = $('.lista-arquivos-brutos');
                ulElement.empty();

                response.forEach(function (o) {

                    let liElement = $('<i class="fa-solid fa-file"></i><li class="list-group-item btn" data-file="' + o.file + '" data-file_size="' + o.file_size + '" data-last_modify="' + o.last_modify + '" data-row_count="' + o.row_count + '" data-total_atletas="' + o.total_atletas + '" data-bs-toggle="modal" data-bs-target="#arquivoModal"></li>');
                    liElement.text(`${o.file}`);
                    ulElement.append(liElement);

                    liElement.text(`${o.file}`);

                    ulElement.append(liElement);
                });
            },

            error: function (xhr, status, error) {
                console.error('Erro na solicitação AJAX:', error);
            }
        })
    })

    $(document).on('show.bs.modal', '#arquivoModal', function (event) {
        var button = $(event.relatedTarget);
        var fileId = button.data('file');
        var fileSize = button.data('file_size');
        var lastModify = button.data('last_modify');
        var totalAtletas = button.data('total_atletas');
        var qtdlinhas = button.data('row_count');



        var modal = $(this);
        modal.find('#fileId').text(fileId);
        modal.find('#fileSize').text(fileSize);
        modal.find('#lastModify').text(lastModify);
        modal.find("#AtletasQtd").text(totalAtletas)
        modal.find("#linhasQtd").text(qtdlinhas)


    });

    $(document).on("click", "#refinados-list", function () {
        $.ajax({
            type: 'GET',
            url: '/listar_arquivos/refinados/',
            success: function (response) {
                $(".arquivos-refinados-loader").hide();
                let ulElement = $('.lista-arquivos-refinados');
                ulElement.empty();

                response.forEach(function (o) {

                    let liElement = $('<i class="fa-solid fa-file"></i><li class="list-group-item btn" data-file="' + o.file + '" data-file_size="' + o.file_size + '" data-last_modify="' + o.last_modify + '" data-row_count="' + o.row_count + '" data-total_atletas="' + o.total_atletas + '" data-bs-toggle="modal" data-bs-target="#arquivoModal"></li>');
                    liElement.text(`${o.file}`);
                    ulElement.append(liElement);

                    liElement.text(`${o.file}`);

                    ulElement.append(liElement);
                });
            },

            error: function (xhr, status, error) {
                console.error('Erro na solicitação AJAX:', error);
            }
        })
    })

    $(document).on('show.bs.modal', '#arquivoModal', function (event) {
        var button = $(event.relatedTarget);
        var fileId = button.data('file');
        var fileSize = button.data('file_size');
        var lastModify = button.data('last_modify');
        var totalAtletas = button.data('total_atletas');
        var qtdlinhas = button.data('row_count');



        var modal = $(this);
        modal.find('#fileId').text(fileId);
        modal.find('#fileSize').text(fileSize);
        modal.find('#lastModify').text(lastModify);
        modal.find("#AtletasQtd").text(totalAtletas)
        modal.find("#linhasQtd").text(qtdlinhas)


    });


    $(document).on("click", "#iniciar-leitura", function () {
        $.ajax({
            type: 'POST',
            url: '/start_reader/',
            data: {},
            success: function (response) {

            },
            error: function (xhr, status, error) {
                console.error('Erro na solicitação AJAX:', error);
            }

        });
    })

    setInterval(function() {
        $.ajax({
            type: 'GET',
            url: '/reader_status',
            success: function (response) {
                if(response.status == "success") {
                    $(".comunicando").html(`<i class="fa-solid fa-arrow-right-arrow-left"></i> Comunicando`)
                    $(".comunicacao-status").removeClass("disconnected")
                    $(".comunicacao-status").addClass("connected")

                    let tags = response.data.data.taginfo;
                    let tableBody = $(".info-table");
                    tableBody.empty();
                   
                    tags.forEach((tag, i)=> {
                        let newRow = $("<tr>");
                    
                        let indexCell = $("<td>").text(i + 1);
                        let tagCell = $("<td>").text(tag.m_code.slice(32, 57).replace(/\s+/g, '')); 
                        let lastTimestamp = $("<td>").text(tag.timestamp); 
                        let countCell = $("<td>").text(tag.m_counts);

                        newRow.append(indexCell);
                        newRow.append(tagCell);
                        newRow.append(countCell);
                        newRow.append(lastTimestamp);
                    
                        tableBody.append(newRow);
                    });

                }
                else {
                    $(".comunicando").html(`<i class="fa-solid fa-arrow-right-arrow-left"></i> Não Comunicando`)
                    $(".comunicacao-status").removeClass("connected")
                    $(".comunicacao-status").addClass("disconnected")

                }
            },
            error: function (xhr, status, error) {
                console.error('Erro na solicitação AJAX:', error);
            }
    
        });
    }, 5000);

    function atualizaEquipamento() {
        $.ajax({
            type: 'POST',
            url: '/atualizar_equipamento',
            data: {},
            success: function (response) {
                showToast(response.status, response.message)
            },
            error: function (xhr, status, error) {
                console.error('Erro na solicitação AJAX:', error);
            }
        })
    }
});

