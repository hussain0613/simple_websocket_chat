function create_message(user, message, color="black") {
    var message_p = document.createElement("p");
    if(user == "server") {
        message_p.align = "center";
        message_p.style.color = color;
        message_p.innerHTML = message;
    }else{
        message_p.innerHTML = `<b>${user}: </b><br>${message}`;
    }
    message_p.style.whiteSpace = "pre-wrap";
    document.getElementById("messages").appendChild(message_p);
}

function create_websocket() {
    var ws = new WebSocket(location.origin.replace(location.protocol, "ws:")+"/ws");
    ws.onclose = function(ev){
        create_message("server", "Connection closed", "red");
        document.getElementById("chat_form").style.display = "none";
        document.getElementById("opening_form").style.display = "block";
        document.getElementById("retry").style.display = "block";
    }
    ws.onmessage = function(ev){
        var data = JSON.parse(ev.data);
        create_message(data.user, data.message);
    }

    return ws;
}

function send_chat_message(socket) {
    var message = chat_form.message.value;
    chat_form.message.value = "";
    socket.send(JSON.stringify({
        "message": message
    }));
}

function retry(){
    ws = create_websocket();
    document.getElementById("retry").style.display = "none";
    document.getElementById("opening_form").style.display = "none";
    document.getElementById("chat_form").style.display = "flex";
    return ws;
}