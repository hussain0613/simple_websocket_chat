var opening_form = document.getElementById("opening_form");
var messages = document.getElementById("messages");
var chat_form = document.getElementById("chat_form");
var msg_ta = document.getElementById("msg_ta");
var retry_button = document.getElementById("retry");
retry_button.addEventListener("click", retry);
var ws = null;

msg_ta.placeholder = "type your message here\npress 'enter' to send\npress 'shift+enter' to add a new line";
msg_ta.addEventListener("keydown", function(e) {
    if (e.keyCode == 13 && !e.shiftKey) {
        e.preventDefault();
        send_chat_message(ws);
    }
});

opening_form.addEventListener("submit", function(event) {
    event.preventDefault();
    var display_name = opening_form.display_name.value;
    var password = opening_form.password.value;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/login", true);
    xhr.onreadystatechange = function(ev){
        if(this.readyState==4){
            if(this.status==200){
                var response = JSON.parse(this.responseText);
                // create messages
                opening_form.style.display = "none";
                retry_button.style.display = "none";
                chat_form.style.display = "flex";
                create_message("server", response.message, "green");
                
                // create socket
                ws  = create_websocket();

            }else if(this.status == 401){
                var response = JSON.parse(this.responseText);
                alert("Unauthenticated! " + response.message);
            }else if(this.status == 403){
                var response = JSON.parse(this.responseText);
                alert("Fobidden: " + response.message);
            }else{
                alert("Error: " + this.status);
            }
        }
    }
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({
        "display_name": display_name,
        "password": password
    }));
});

chat_form.addEventListener("submit", function(event) {
    event.preventDefault();
    send_chat_message(ws);
});