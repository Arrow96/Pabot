const hablar = document.getElementById('buttonInput');
let recognition;
let micro = false;
    function getBotResponse(){
        var rawText = $("#textInput").val();
        var userHtml = '<p class = "userText"><span>' + '(Humano)  ' + rawText + '</span></p>';
        $("#textInput").val("");
        document.getElementById('userInput').scrollIntoView({block:'start',behaviour:'smooth'});
        $.get("/get-spanish", {msg:rawText }).done(function(data) {
            var botHtml = '<p class ="botText"><span>' + data + '  (Bot)' + '</span></p>';
            $("#chatbox").append(userHtml);
            $("#chatbox").append(botHtml);
            document.getElementById('userInput').scrollIntoView({block : 'start',behaviour:'smooth'});

            const mensaje = new SpeechSynthesisUtterance(data);
            mensaje.voiceURI = 'Juan';
            mensaje.lang = 'es-MX';
            mensaje.rate = 0.9;
            speechSynthesis.speak(mensaje);
        });
    }
    function iniciar(event){
        for (i = event.resultIndex; i < event.results.length; i++){
            $("#textInput").val(event.results[i][0].transcript);
        }
    }

    if (!('webkitSpeechRecognition' in window)) {
        alert("Lo siento, no tienes permitido utilizar esta API");
    } else{
        recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interim = true;
        recognition.lang = "es-CL";
        recognition.addEventListener("result", iniciar);
    }
    hablar.addEventListener('click', () => {
        if(micro == false){
            recognition.start();
            hablar.style.background = 'yellow';
            micro = true;
        }
        else{
            recognition.abort();
            hablar.style.background = '#144EFA';
            micro = false
        }
    });
    $("#textInput").keypress(function(e) {
        if(e.which == 13) {
            recognition.abort();
            getBotResponse();
        }
    });
