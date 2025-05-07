//Função para configuração socket do grafico

const socket = new WebSocket('ws://'+window.location.host+'/ws/chat/'+destinatrio_id+'/');
const destinatrio_id = operador.id
socket.onmessage = function(e)
{
   const data = Json.parse(e.data);
   const mensagens = document.getElementById("mensagens");
   const novaMensagem = document.createElement("div");
   novaMensagem.textContent = "Mensagem de ID"+data.remetente_id+":"+data.conteudo;
   mensagens.appendChild(novaMensagem);
}

function enviarMensagem()
{
    const input = document.getElementById("mensagem");
    socket.send(JSON.stringify({"cconteudo": input.value=""}))
};

