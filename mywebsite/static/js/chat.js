$(function() {
    console.log(user, room_id)
    var url = 'ws://' + window.location.host + '/ws/room/' + room_id + '/'
    console.log(url)
    var chatSocket = new WebSocket(url)
    console.log(chatSocket)

    chatSocket.onopen = function(e) {
        console.log('Websocket open')
    }
    chatSocket.onclose = function(e) {
        console.log('Websocket close')
    }
    chatSocket.onmessage = function(data) {
        const datamsj = JSON.parse(data.data)
        var msj = datamsj.message
        var username = datamsj.username
        var datatime = datamsj.datatime
        document.querySelector('#boxMessages').innerHTML +=
        `
        <div class="alert alert-info" role="alert">
            ${msj}
            <div>
                <small class="fst-italic fw-bold">${username}</small>
                <small class="float-end">${datatime}</small>
            </div>
        </div>
        ` 
    }


    document.querySelector('#btnMessage').addEventListener('click', sendMessage)
    document.querySelector('#inputMessage').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage()
        }
    })

    function sendMessage() {
        var message = document.querySelector('#inputMessage')
        
        if (message.value.trim() !== '') {
            loadMessageHtml(message.value.trim())
            chatSocket.send(JSON.stringify({
                'message': message.value.trim(),
                'username': user,
                'room_id': room_id
            }))
            console.log(message.value.trim())
            message.value = ''
        } else {
            console.log('Envio un mensaje vacio')
        }
    }

    function loadMessageHtml(m) {
        const dateObject = new Date()
        const hour = dateObject.getHours()
        const minutes = dateObject.getMinutes()
        const formattedTime = `${hour}:${minutes}`
        document.querySelector('#boxMessages').innerHTML +=
        `
        <div class="alert alert-warning" role="alert">
            ${m}
            <div>
                <small class="fst-italic fw-bold">${user}</small>
                <small class="float-end">${formattedTime}</small>
            </div>
        </div>
        ` 
        }
})





