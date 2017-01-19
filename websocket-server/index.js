var WebSocketServer = require('ws').Server;

var PORT = 8479;

var wss = new WebSocketServer({port: PORT});

var messages = [];



wss.on('connection', function (ws) {
  messages.forEach(function(message){
    ws.send(message);
  });
  ws.on('message', function (message) {
    messages.push(message);
    console.log('Message Received: %s', message);
    
    //console.log(messages.indexOf('{"text": "Event View Atualizado..."}'));
    //console.log(messages.length);

    for(var i=0; i<messages.length; i++){
      console.log("=====> "+i, messages[i]);
      if (messages[i]=='{"text": "Event View Atualizado..."}'){
        console.log("achou");
        delete messages[i];
      }
    }

    //SETANDO O ARRAY PARA ARMAZENAR 10 MSG DEPOIS IR APAGANDO O REGISTRO INICIAL
    if (messages.length > 10){
      console.log('Limpando o primeiro registro do array para manter sempre 10');
      messages.shift();
      
    }

    wss.clients.forEach(function (conn) {
      conn.send(message);
    });
  });
});
