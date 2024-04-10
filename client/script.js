document.addEventListener('DOMContentLoaded', function () {
    function createBoard() {
        const gameArea = document.getElementById('gameArea');
        const table = document.createElement('table');
        table.setAttribute('id', 'board');

        let counter = 1;
        for (let i = 0; i < 15; i++) {
            const tr = document.createElement('tr');
            for (let j = 0; j < 15; j++) {
                const td = document.createElement('td');
                let counterId = counter++;
                td.setAttribute('id', counterId);
                td.onclick = function() { cellClick(counterId); };
                td.textContent = '';
                tr.appendChild(td);
            }
            table.appendChild(tr);
        }

        gameArea.appendChild(table);
    }

    createBoard();

    var ws = new WebSocket("ws://localhost:8000/ws");
    let player = null
    let currentPlayer = null
    let gameOver = false
    let currentPlyerDisplay = document.getElementById('current-player')
    let infoDisplay = document.getElementById('info')
    let infoPlayer = document.getElementById('player')
    swaper = {
        "X": "O",
        "O": "X"
    }

    function toggleplayer() {
        currentPlayer = swaper[currentPlayer]
        console.log("Toggler ", player, currentPlayer);
        if (player == currentPlayer) {
            infoDisplay.innerHTML = "Your turn!"
            currentPlyerDisplay.innerHTML = player
        } else {
            infoDisplay.innerHTML = "Your opponent's turn!"
            currentPlyerDisplay.innerHTML = swaper[player]
        }
    }

    function checkCell(cell) {
        if (cell.innerHTML == '' & player == currentPlayer) {
            return true
        }
        return false
    }
    function updateCell(id, sign) {
        console.log(id);
        console.log(sign);
        cell = document.getElementById(id)
        cell.innerHTML = sign
    }
    function updateInfo(message) {
        infoDisplay.innerHTML = message
    }
    function cellClick(id) {
        console.log('Cell clicked:', id);
        if (gameOver) {
            return
        }
        cell = document.getElementById(id)
        if (checkCell(cell)) {
            ws.send(JSON.stringify({player: player, cell: id }))
        } else {
            infoDisplay.innerHTML = "Choose another cell! Or wait for your turn!"
        }
    }

    ws.onmessage = function(e) {
        response = JSON.parse(e.data)
        console.log("On message",response);
        if (response.init) {
            infoDisplay.innerHTML = "You play by: "+ response.player + ". " + response.message
            infoPlayer.innerHTML = response.player
            if (response.message != "Waiting for another player") {
                player = response.player
            }
            currentPlayer = "X"
            currentPlyerDisplay.innerHTML = "X"
        } else {
            if (response.message == 'move') {
                updateCell(response.cell, response.player)
                toggleplayer()
            } else if (response.message == 'draw') {
                updateInfo("It's a draw")
                updateCell(response.cell, response.player)
                highlightAll()
                ws.close(1000)
            } else if (response.message == 'won') {
                updateInfo("Player " + response.player + " won!")
                updateCell(response.cell, response.player)
                hightLightRow()
                ws.close(1000)
            } else if (response.player == player & response.message == 'choose another one') {
                updateInfo("Cell is not available")
            } else {
                console.log(response);
            }
        }
    }

    ws.onclose = function(e) {
        if (e.code == 4000) {
            infoDisplay.innerHTML = "No more places!!"
        } else if (e.code != 1000){
            infoDisplay.innerHTML = "Error"
        }
        gameOver = true
    }
});
