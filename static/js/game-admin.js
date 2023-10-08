console.log('Стрипт админской странички игры успешно загружен');

let statusGame = {
    dynastyName: "Админ",
    year: -300,
    turn: 1,
 
    allLogs: [],        // Все логи итогов хода всех стран
 
};

function updateVar() {
    document.getElementById('year-turn').innerText = 'Дата: ' + statusGame.year + " Ход: " + statusGame.turn;

}

updateVar();

document.getElementById('act-logs').addEventListener('click', () => {
    requestStatus();
});

function requestStatus() {
    const request = new XMLHttpRequest();
    request.open('GET', '/req_status_game');
    request.addEventListener('load', () => {
        if (request.status === 200) {
            if (request.response == "") {
                console.log("К нам пришла пустая строка");
                
            } else {
                const response = JSON.parse(request.response);
                console.log(response);
                actualVar(response);
                console.log(response)
                console.log("Ответ от сервера")
            };
        } else {
            console.log("Ответ от сервера не получен");
        }
    });
    request.send();

}

// Обновим общие параметры
function actualVar(res) {
    statusGame.year = res.year;
    statusGame.turn = res.turn;
    statusGame.allLogs = res.all_logs;


    updateVar();
    logAllResultStart();
};

function logAllResultStart() {       //Функция запуска лога итога хода всех игроков
    document.getElementById('all-logs-result').innerText = 'Общий лог прошлого хода';  // Очистим + подсказка
    statusGame.allLogs.forEach((item, num) => {  
        let a = document.getElementById('all-logs-result');
        a.insertAdjacentHTML('beforeend', `<div>${num + 1}: ${item}</div>`);
    }); 
}