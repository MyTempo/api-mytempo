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
                $(".id_equip").html(response.equipamento)
                $(".id_prova").html(response.idprova)
                $(".id_checkpoint").html(response.idcheck)
                $(".prova_assoc").html(response.tituloprova)
                $(".fabricante").html(response.fabricante)
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

                    let sessionNumber = extractSessionNumber(o.file);

                    let liElement = $('<li class="list-group-item btn" data-file="' + o.file + '" data-session="' + sessionNumber + '" data-file_size="' + o.file_size + '" data-last_modify="' + o.last_modify + '" data-row_count="' + o.row_count + '" data-total_atletas="' + o.total_atletas + '" data-bs-toggle="modal" data-type="bruto" data-bs-target="#arquivoModal"></li>');

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
        var sessionFile = button.data("session");

        var modal = $(this);
        modal.find('#fileId').text(fileId);
        modal.find('#fileSize').text(fileSize);
        modal.find('#lastModify').text(lastModify);
        modal.find("#AtletasQtd").text(totalAtletas)
        modal.find("#linhasQtd").text(qtdlinhas)
        modal.find("#deletar-arquivo-btn").data("file-session", sessionFile);



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
                    let sessionNumber = extractSessionNumber(o.file);

                    let liElement = $('<li class="list-group-item btn" data-file="' + o.file + '" data-session="' + sessionNumber + '" data-file_size="' + o.file_size + '" data-last_modify="' + o.last_modify + '" data-row_count="' + o.row_count + '" data-total_atletas="' + o.total_atletas + '" data-bs-toggle="modal" data-type="refinado"  data-bs-target="#arquivoModal"></li>');

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
        var sessionFile = button.data("session");
        var arqType = button.data("type")


        var modal = $(this);
        modal.find('#fileId').text(fileId);
        modal.find('#fileSize').text(fileSize);
        modal.find('#lastModify').text(lastModify);
        modal.find("#AtletasQtd").text(totalAtletas)
        modal.find("#linhasQtd").text(qtdlinhas)
        modal.find("#deletar-arquivo-btn").attr("data-file-session", sessionFile);

        $(document).on('click', "#deletar-arquivo-btn", function () {
            console.log(sessionFile)
            $.ajax({
                type: 'GET',
                url: `/deletar/arquivo/${arqType}/${sessionFile}`,
                contentType: 'application/json',
                success: function (response) {
                    showToast(response.status, response.message, 3000);
                },
                error: function (xhr, status, error) {
                    console.error('Erro na solicitação AJAX:', error);
                }
            });
        })


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

    setInterval(function () {
        $.ajax({
            type: 'GET',
            url: '/reader_status',
            success: function (response) {
                if (response.status == "success") {
                    $(".comunicando").html(`<i class="fa-solid fa-arrow-right-arrow-left"></i> A leitura está em andamento`)
                    $(".comunicacao-status").removeClass("disconnected")
                    $(".comunicacao-status").addClass("connected")

                    let tags = response.data.data.taginfo;
                    let tableBody = $(".info-table");
                    tableBody.empty();

                    tags.forEach((tag, i) => {
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

    $(document).on("click", "#parar-leitura", function () {
        $.ajax({
            type: 'POST',
            url: '/stop_reader/',
            data: {},
            success: function (response) {
                console.log(response)

            },
            error: function (xhr, status, error) {
                console.error('Erro na solicitação AJAX:', error);
            }
        })
    })

    $(document).on("click", "#pegar-primeiros-tempos", function () {
        $.ajax({
            type: 'POST',
            url: '/pegar/primeiros-tempos',
            data: {},
            success: function (response) {
                console.log(response)

            },
            error: function (xhr, status, error) {
                console.error('Erro na solicitação AJAX:', error);
            }
        })
    })

    // $(document).on("click", "#iniciar-comunicacao", function () {
    //     $.ajax({
    //         type: 'POST',
    //         url: '/iniciar/comunicacao/',
    //         data: {},
    //         success: function (response) {
    //             console.log(response)

    //         },
    //         error: function (xhr, status, error) {
    //             console.error('Erro na solicitação AJAX:', error);
    //         }
    //     })
    // })

    var intervalId;

    function startCommunication() {
        if (!intervalId) {
            $("#iniciar-comunicacao").prop("disabled", true);
            intervalId = setInterval(function () {
                $.ajax({
                    type: 'POST',
                    url: '/iniciar/comunicacao/',
                    contentType: 'application/json',
                    data: {},
                    success: function (response) {
                        showToast(response.status, response.message, 3000);
                    },
                    error: function (xhr, status, error) {
                        console.error('Erro na solicitação AJAX:', error);
                    }
                });
            }, 5000);
        }
    }

    function pauseCommunication() {
        clearInterval(intervalId);
        intervalId = null;
        $("#iniciar-comunicacao").prop("disabled", false);
        $.ajax({
            type: 'POST',
            url: '/insert/tempos',
            contentType: 'application/json',
            data: JSON.stringify({ "acao": "desligar" }),
            success: function (response) {
                showToast(response.status, response.message, 3000);
            },
            error: function (xhr, status, error) {
                console.error('Erro na solicitação AJAX:', error);
            }
        });
    }

    $(document).on("click", "#iniciar-comunicacao", function () {
        startCommunication();
    });

    $(document).on("click", "#pausar-comunicacao", function () {
        pauseCommunication();
    });
    $(document).on("click", "#limpar-atletas", function () {
        $.ajax({
            type: 'POST',
            url: '/limpar/atletas_local',
            contentType: 'application/json',
            data: {},
            success: function (response) {
                showToast(response.status, response.message, 3000);
            },
            error: function (xhr, status, error) {
                console.error('Erro na solicitação AJAX:', error);
            }
        });
    });
    $(document).on("click", ".mostrar-atletas", function () {
        $(".mostrar-atletas-card").removeClass("d-none");
        $(".mostrar-atletas").addClass("esconder");
        $(".mostrar-atletas").text("Esconder Atletas")
        updateTable();
    });

    function updateTable() {
        $.ajax({
            type: 'GET',
            url: '/atletas_chegaram',
            contentType: 'application/json',
            data: {},
            success: function (response) {
                $(".atletas-chegaram").addClass("d-none");
                let tableBody = $(".info-table-atletas");
                tableBody.empty();
                if (response.data.length > 0) {
                    response.data.forEach((element, i) => {
                        let newRow = $("<tr>");
                        let indexCell = $("<td>").text(i + 1);
                        let atleta = $("<td>").text(element[4]);
                        let tempos = $("<td>").text(element[5]);
                        let idcheck = $("<td>").text(element[2]);
                        let equipamento = $("<td>").text(element[3]);
                        newRow.append(indexCell);
                        newRow.append(atleta);
                        newRow.append(tempos);
                        newRow.append(idcheck);
                        newRow.append(equipamento);
                        tableBody.append(newRow);
                    });
                } else {
                    tableBody.html("Sem resultados");
                }
            },
            error: function (xhr, status, error) {
                console.error('Erro na solicitação AJAX:', error);
            }
        });
    }

    setInterval(updateTable, 5000);




    $(document).on("click", "#desligar-envio", function () {
        $.ajax({
            type: 'POST',
            url: '/insert/tempos',
            contentType: 'application/json',
            data: JSON.stringify({ "acao": "desligar" }),
            success: function (response) {
                showToast(response.status, response.message, 3000);
            },
            error: function (xhr, status, error) {
                console.error('Erro na solicitação AJAX:', error);
            }
        });
    });

    $(document).on("click", "#ativa-envio", function () {
        $.ajax({
            type: 'POST',
            url: '/insert/tempos',
            contentType: 'application/json',
            data: JSON.stringify({ "acao": "ligar" }),
            success: function (response) {
                showToast(response.status, response.message, 3000);
            },
            error: function (xhr, status, error) {
                console.error('Erro na solicitação AJAX:', error);
            }
        });
    });

    $(document).on('click', ".apagar-todos-brutos", function() {
        $.ajax({
            type: 'GET',
            url: `/deletar/tudo/bruto`,
            contentType: 'application/json',
            success: function (response) {
                showToast(response.status, response.message, 3000);
            },
            error: function (xhr, status, error) {
                console.error('Erro na solicitação AJAX:', error);
            }
        });
    });

    $(document).on('click', ".apagar-todos-refinados", function() {
        $.ajax({
            type: 'GET',
            url: `/deletar/tudo/refinado`,
            contentType: 'application/json',
            success: function (response) {
                showToast(response.status, response.message, 3000);
            },
            error: function (xhr, status, error) {
                console.error('Erro na solicitação AJAX:', error);
            }
        });
    });

    $(document).on("click", ".esconder", function(e) {
        $(".mostrar-atletas").removeClass("esconder")
        $(".mostrar-atletas-card").addClass("d-none");
        $(".mostrar-atletas").text("Mostrar atletas enviados")
    });
});

