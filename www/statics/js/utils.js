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
        if(data.active_users){
            show_active_users(data.active_users);
        }
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


function show_active_users(active_users) {
    var active_users_p = document.createElement("p");
    active_users_p.classList.add("active_users_p");
    active_users_p.align = "center";
    active_users_p.innerHTML = `<span class = "active_users_title">Active Users: </span>`;
    for(var i = 0; i < active_users.length; i++) {
        var user = active_users[i];
        var user_span = document.createElement("span");
        user_span.classList.add("active_user_span");
        user_span.innerHTML = user;
        active_users_p.appendChild(user_span);
    }
    document.getElementById("messages").appendChild(active_users_p);
}
