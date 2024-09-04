window.onload = function() {
    document.querySelector('#btnMessage').addEventListener('click', sendMessage)
    document.querySelector('#inputMessage').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage()
        }
    })

    function sendMessage() {
        var message = document.querySelector('#inputMessage')
        
        loadMessageHtml(message.value.trim())

        if (message.value.trim() === '') {
            message.value = ''
        }
    }

    function loadMessageHtml(m) {
        document.querySelector('#boxMessages').innerHTML +=
        `
        <div class="alert alert-primary" role="alert">
            ${m}
            <div>
                <small class="fst-italic fw-bold">${user}</small>
                <small class="float-end">8:33</small>
            </div>
        </div>
        ` 
    }
}

