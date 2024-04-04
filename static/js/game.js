console.log('Стрипт странички игры успешно загружен');

// Для поиска:
// Вкладки


// Меню для уточнения количества
const chooseList = document.querySelector('.choose-list');

// Отображаемые в интерфейсе параметры, одновляются при запросе на сервер
let statusGame = {
    year: 800,
    turn: 1,
    end_turn: false,
    endTurnKnow: true, // Оповещен ли игрок о новом ходе

    // Логи
    acts: [],           // Запись планируемых действий с описанием
    // actsText: [],       // Запись планируемых действий в виде текста понятного для игрока
    logsText: [],       // Запись итогов хода в виде текста понятного для игрока
    logsTextAllTurns: [],       // Запись итогов хода в виде текста понятного для игрока
    allLogs: [],        // Все логи итогов хода всех стран
    allLogsParty: [],        // Все логи итогов хода всех стран за всю партию

    // Игрок
    dynastyName: "Страна не загрузилась",
    gold: 0,            // Золото игрока
    title: 0,           // Титул игрока, пока числом, будет строкой, типо "Ярл"
    bodyPoints: 0,      // Очки действия для игрока


    // Игроки
    dynastyList: [],
    curNumPlayers: 0,
    maxPlayers: 12,
    // Победа и победители
    winPoints: 0,
    wpForWin: 0,
    winners: [],

    user_name: "",
    game_id: "",        // ИД партии. Будем передавать вместе с ходом.
    date_create: "",

    autoUpdate: true,  // Таймер автообновления странички
};

// Старое
// Поселение
let statusSettlement = {
    buildingsList: [],  // Список построек
    population: 0,  // Размер населения
    populationGold: 0,  // Золото населения
    wealthStatus: "",  // Благосостояние населения
    settlementName: "Поселение",
    food: 0,        // Производство еды
    balanceFood: 0, // Баланс еды
    buildPoints: 0,  // Очки строительства
}
// Новое
let statusSettlements = []

// Постройки для отображения при строительстве
// Тут список обьектов.
// 0 - Название
// 1 - Стоимость
// 2 - Название иконки
// 3 - Описание
let statusBuildings = []

// Обработка вкладок
// О партии
document.getElementById('party-button').addEventListener('click', () => {
    hiddenAllWindows();
    document.getElementById("party-window").setAttribute('style','visibility:visible;');
    document.getElementById("party-button").setAttribute('style','color:red; cursor: pointer;');
});
// Поселение
document.getElementById('settlement-button').addEventListener('click', () => {
    hiddenAllWindows();
    document.getElementById("settlement-window").setAttribute('style','visibility:visible');
    document.getElementById("settlement-button").setAttribute('style','color:red; cursor: pointer;');
});
// Торговля
document.getElementById('trade-button').addEventListener('click', () => {
    hiddenAllWindows();
    document.getElementById("trade-window").setAttribute('style','visibility:visible');
    document.getElementById("trade-button").setAttribute('style','color:red; cursor: pointer;');
});
// Карта
document.getElementById('map-button').addEventListener('click', () => {
    hiddenAllWindows();
    document.getElementById("map-window").setAttribute('style','visibility:visible');
    document.getElementById("map-button").setAttribute('style','color:red; cursor: pointer;');
});
// Династия
document.getElementById('dynasty-button').addEventListener('click', () => {
    hiddenAllWindows();
    document.getElementById("dynasty-window").setAttribute('style','visibility:visible');
    document.getElementById("dynasty-button").setAttribute('style','color:red; cursor: pointer;');
});
// Армия
document.getElementById('army-button').addEventListener('click', () => {
    hiddenAllWindows();
    document.getElementById("army-window").setAttribute('style','visibility:visible');
    document.getElementById("army-button").setAttribute('style','color:red; cursor: pointer;');
});
// Игроки
document.getElementById('players-button').addEventListener('click', () => {
    hiddenAllWindows();
    document.getElementById("players-window").setAttribute('style','visibility:visible');
    document.getElementById("players-button").setAttribute('style','color:red; cursor: pointer;');
});


// Первичная загрузка шапки таблицы с провинциями
// function tableStart() {
//     document.getElementById(`tab-province`).innerHTML = `
//     <table class="table" id="table-province">        
//         <thead>    
//             <tr class="table">
//                 <th class="th" id='th-loc' style="width: 200px">Локация</th>
//                 <th class="th" id='th-pop' style="width: 70px">Нас.</th>
//                 <th class="th" id='th-wealth style="width: 70px"'>Благ.</th>
//                 <th class="th" id='th-food' style="width: 70px">Еда произв.</th>
//                 <th class="th" id='th-food-balace' style="width: 70px">Еда баланс</th>
//                 <th class="th" id='th-dom' style="width: 70px">Строй</th>

//                 <th class="th" id='th-buildings' style="width: 300px">Постройки</th>
//             </tr>
//         </thead>
//     </table>`;
// }
// // Отображаем таблички под разные статусы
// tableStart();

// Модальное окно
// Получить модальное окно
const modal = document.getElementById("my-modal");

// Получить кнопку, которая открывает модальное окно
const btnShowAllLogsParty = document.getElementById("show_all_logs_party");
const btnShowAllLogsPartyPlayers = document.getElementById("show_all_logs_party_players");

// Получить элемент <span>, который закрывает модальное окно
const span = document.getElementsByClassName("close")[0];


// Основная функция обновления параметров на страничке
// Неплохо бы делать вывод только тех товаров, что есть в наличии через создание верстки перебором массива с ресурсами forEach
// !!!!!!!!!!! Внимание, разделение вывода по старым окошкам
function updateVar() {
    // Первое меню
    // document.getElementById('province-name').innerText = statusGame.settlementName; 
    // Золото
    document.getElementById('player-gold').innerHTML = `Казна: ` + statusGame.gold;  // 'Золото: ' + 
    // document.getElementById('player-gold').innerHTML = `<img class="icon" src="/static/image/icon/money.png"> ` + statusGame.gold;  // 'Золото: ' + 
    // Очки действий. Покрасим в красный цвет в случае ухода в минус
    const showBodyPoints = document.getElementById('body-points');
    // showBodyPoints.forEach((item, id) => {
    //     item.innerText = `Очки действий: ${statusGame.bodyPoints - statusGame.acts.length}`;
    //     if (statusGame.bodyPoints - statusGame.acts.length < 0) {
    //         console.log("Нехватает очков действий");
    //         item.classList.add("set-red-font");
    //     } else {
    //         item.classList.remove("set-red-font");   
    //     }
    // })
    showBodyPoints.innerText = `Очки действий: ${statusGame.bodyPoints - statusGame.acts.length}`;
    if (statusGame.bodyPoints - statusGame.acts.length < 0) {
        console.log("Нехватает очков действий");
        showBodyPoints.classList.add("set-red-font");
    } else {
        showBodyPoints.classList.remove("set-red-font");   
    }
    document.getElementById('rank').innerText = 'Титул: ' + statusGame.title;  // Титул(ранг) игрока    
    document.getElementById('win-points').innerText = 'Победные очки: ' + statusGame.winPoints;

    document.getElementById('cur-num-players').innerText = `Игроков: ${statusGame.curNumPlayers}`;
    document.getElementById('max-players').innerText = `Макс.игроков: ${statusGame.maxPlayers}`;
    document.getElementById('victory-conditions').innerText = `Условия победы: Набрать ${statusGame.wpForWin} очков`;
    document.getElementById('winners').innerText = 'Победители: ' + statusGame.winners;

    document.getElementById('year-turn').innerText = 'Дата: ' + statusGame.year + " Ход: " + statusGame.turn;
    if (statusGame.end_turn) {
        document.getElementById('end-turn-bool').innerText = "Ход ГОТОВ"
    } else {
        document.getElementById('end-turn-bool').innerText = "Ход НЕ готов"
    }

    // Поселение
    const settName = document.querySelectorAll(".settlement-name")
    settName.forEach((i, id) => {
        i.innerText = statusSettlement.settlementName;
    })
    document.getElementById("build-points").innerText = `Очки строительства: ${statusSettlement.buildPoints}`
    // document.getElementById("population").innerText = statusSettlement.population;  // wealthStatus
    // document.getElementById("wealth-status").innerText = statusSettlement.wealthStatus + " (" + statusSettlement.populationGold + ")";
    // document.getElementById("food").innerText = statusSettlement.food;
    // document.getElementById("balance-food").innerText = statusSettlement.balanceFood;

    // Вкладка торговли
    // Тут отображена доступность покупки и продажы товаров.
    // !!!!!!!!! 

    // Меню разработки
    document.getElementById('player').innerText = 'Игрок: ' + statusGame.user_name;
    document.getElementById('game-id').innerText = 'Игра: ' + statusGame.game_id;
    document.getElementById('game-date').innerText = 'Дата создания: ' + statusGame.date_create;

    if (statusGame.endTurnKnow == false) {
        confimRecTurnModal();
    };


};

updateVar();


// "Отдельный" запрос на сервер, получающий дату, номер хода и другие общие параметры
// Будет актуально для "наблюдающего", например для Админа
function requestStatus() {
    const request = new XMLHttpRequest();
    request.open('GET', '/req_status_game');
    request.addEventListener('load', () => {
        if (request.status === 200) {
            if (request.response == "") {
                console.log("К нам пришла пустая строка");
                
            } else {
                const response = JSON.parse(request.response);
                // После обсчета хода игрок один раз получает сообщение, что пришел новый ход
                // Баг!!! При сообщении о новом ходе все параметры висят по нулям
                // По скольку это временный вариант, чинить не буду
                // if (statusGame.year < response.year) {
                //     // Обновим параметры на странице
                //     actualVar(response);
                //     alert(`Новый ход обработан. Текущий год: ${response.year}`);
                // } else {
                //     // Обновим параметры на странице
                //     actualVar(response);
                // }
                actualVar(response);
                // Тут же проверим победителя                
                if (response.winners.length > 0) {
                    console.log(`Есть победитель, династия ${response.winners}`)
                    let infoHtml = `<p style="font-size: 20px;">Есть победитель(и), династия(и) ${response.winners}</p>` 
                    infoModal(infoHtml)
                };

            };
        } else {
            console.log("Ответ от сервера не получег");
        }
    });
    request.send();
}

// Запрос на сервер уже конкретно параметров "страны" игрока
function requestStatusPlayer() {
    const request = new XMLHttpRequest();
    request.open('GET', '/req_status_game_player');
    request.addEventListener('load', () => {
        if (request.status === 200) {
            if (request.response == "") {
                console.log("К нам пришла пустая строка");
                alert("Произошла ошибка на сервере!")
                
            } else {
                const response = JSON.parse(request.response);
                console.log("statusGame response")
                console.log(response)
                actualVarPlayer(response);
                console.log("Ответ от сервера. Статус хода: " + response.end_turn)
            };
        } else {
            console.log("Ответ от сервера не получен");
        }
    });
    request.send();
}

requestStatus();
requestStatusPlayer();

// Делаем новый таймер, он работает от включенной переменной autoUpdate
function autoUpdate() {
    // const tm = document.getElementById("timer");
    if (statusGame.autoUpdate) {
    //     console.log("Таймер работает")
    //     let timer = setInterval(tm.innerHTML = `<p>10</p>`, 1000)
    //     for (i = 10; i >= 0; i--) {
    //     }
    //     clearInterval(timerId2)
    //     // Отключим таймер для разработки
        // console.log("Внимание, таймер отключен")
        requestStatus();
        requestStatusPlayer();
        
    }
};
function showTimer() {

}
//     // Отключим таймер для разработки
// let timerId = setInterval(() => autoUpdate(), 5000);

// // autoUpdate();
// function autoUpdateTimer() {
//     // while (statusGame.end_turn) {
//     //     setTimeout(autoUpdate, 3000)
//     //     console.log("Таймер работает")
//     //     // requestStatus();
//     //     // requestStatusPlayer();
//     // }
//     // if (statusGame.end_turn) {
//     //     requestStatus();
//     //     requestStatusPlayer();
//     // }
//     let timerId = setInterval(() => autoUpdate(), 5000);
// };
// autoUpdateTimer();

// Обновим общие параметры
function actualVar(res) {
    statusGame.winners = res.winners;

    // Год и ход
    statusGame.year = res.year;
    statusGame.turn = res.turn;

    // Инфа об условиях победы
    statusGame.wpForWin = res.need_win_points_for_win

    // Логи
    statusGame.allLogs = res.all_logs;
    statusGame.allLogsParty = res.all_logs_party;

    // Имя игрока и инфа о партии
    statusGame.user_name = res.user_name;
    statusGame.game_id = res.game_id;
    statusGame.date_create = res.date_create;
    statusGame.curNumPlayers = res.dynasty_list.length  // Текущим количеством игроков выведем длинну списка стран
    statusGame.maxPlayers = res.max_players

    updateVar();
    logAllResultStart();
    // При загрузке запустим запрос статистики игроков для отображения в отдельном окошке
    req_status_all_player_head();
};



const settlementNameHtml = document.querySelector(".stats-settlement");
const goodsNameHtml = document.querySelector(".stats-resources");
const buildingsNameHtml = document.querySelector(".stats-buildings");
const availableGoodsBuyNameHtml = document.querySelector(".stats-trade-buy");
const availableGoodsSellNameHtml = document.querySelector(".stats-trade-sell");

// Обновим параметры управляемой "страной"
function actualVarPlayer(res) {
    console.log("statusGame old")
    console.log(statusGame)
    statusGame.winPoints = res[0].win_points
    statusGame.dynastyName = res[0].name_rus
    statusGame.gold = res[0].gold

    statusGame.title = res[0].title
    statusGame.bodyPoints = res[0].body_points
    statusGame.end_turn = res[0].end_turn

    // Игроки    

    //  Запись не выполненных действий, массив обновляется на беке при выполнении и остаток возвращается на фронт
    statusGame.acts = res[0].acts    
    statusGame.endTurnKnow = res[0].end_turn_know;

    // Логи игрока
    // statusGame.logsText = [...res[0].result_logs_text, ...res[1].result_events_text]
    // statusGame.logsTextAllTurns = [...res[0].result_logs_text_all_turns, ...res[1].result_events_text_all_turns]
    
    // statusGame.logsText = [...res[0].result_logs_text, ...res[1]["result_events_text"]]
    statusGame.logsText = [...res[0].result_logs_text, "Внимание, логи приходят не все."]
    statusGame.logsTextAllTurns = [...res[0].result_logs_text_all_turns, "Внимание, логи приходят не все."]
    
    console.log(statusGame.logsText)

    // Логи поселения. Или события, то, что напрямую не зависит от игрока.
    // statusGame.logsText = res[1].result_events_text
    // statusGame.logsTextAllTurns += res[1].result_events_text_all_turns
    // console.log(typeof(statusGame.logsText))
    // console.log(typeof(statusGame.logsTextAllTurns))


    console.log("statusGame new")
    console.log(statusGame)

    // Поселение
    // !!!!!!!!!!! Отключаем, делаем под несколько поселений
    // statusSettlement.buildingsList = res[1].buildings_list;
    // statusSettlement.settlementName = res[1].name_rus;
    // statusSettlement.population = res[1].population;
    // statusSettlement.populationGold = res[1].gold;
    // statusSettlement.wealthStatus = res[1].wealth_status;
    // statusSettlement.food = res[1].food;
    // statusSettlement.balanceFood = res[1].balance_food;
    // statusSettlement.buildPoints = res[1].build_points;

    // Доступность торговли
    statusSettlement.availableGoodsBuy = res[1].available_goods_buy;

    // !!!!!!!!!!! Отключаем, делаем под несколько поселений
    // statusBuildings[0] = res[1].available_buildings;
    // statusBuildings[1] = res[1].buildings_cost;
    // statusBuildings[2] = res[1].buildings_icon_name;
    // statusBuildings[3] = res[1].buildings_description;
    // console.log("Инфа о строительстве")     
    // console.log(statusBuildings)   
    // console.log(statusBuildings[0])   
    // console.log(statusBuildings[1])
    // console.log(statusBuildings[2])
    // console.log(statusBuildings[3])

    // Новый вывод инфы сразу о всех наших локациях
    // С бека мы получаем массив, нужен цикл для переноса инфы
    console.log("!!!!!!!!! ДО")
    console.log(statusSettlements);
    statusSettlements = []
    console.log("!!!!!!!!! ПОСЛЕ")
    console.log(statusSettlements);
    console.log("Вывод поселений.")
    for (i=0; i<res[1].length; i++) {
        console.log(res[1][i]);
        statusSettlements.push(res[1][i])
    }
    console.log(statusSettlements);

    // <th class="th" id='th-loc' style="min-width: 200px">Локация</th>
    // <th class="th" id='th-pop' style="min-width: 70px">Нас.</th>
    // <th class="th" id='th-wealth style="min-width: 70px"'>Благ.</th>
    // <th class="th" id='th-food' style="min-width: 70px">Еда произв.</th>
    // <th class="th" id='th-food-balace' style="min-width: 70px">Еда баланс</th>
    // <th class="th" id='th-dom' style="min-width: 70px">Строй</th>

    // <th class="th" id='th-buildings' style="min-width: 300px">Постройки</th>

    tab = document.getElementById('table-province');
    res[1].forEach((item, num) => {
        // Преобразуем некоторые значения при необходимости
        let buildings = []
        
        console.log("Выводим иконки построек.");
        console.log(item["buildings_list"].length);
        console.log(item["buildings_list"]);
        // for(i=0; i<item["buildings_list"].length; i++) {
        //     console.log("Выводим иконки построек.");
        // }
        for (let key in item["buildings_list"]) {
            if (item["buildings_list"][key]>0) {
                buildings.push(`<img style="width: 30px" src="../static/image/buildings/${item["buildings_icon_name"][key]}" alt="Картинки нет, сорян" >`)
                console.log(`key ${key}`);
            }
        }
        tab.insertAdjacentHTML("beforeend", 
            `<tr class="table">
                <td id='th-loc'>${item["name_rus"]}</th>
                <td id='th-pop'>${item["population"]}</th>
                <td id='th-wealth_status'>${item["wealth_status"]}</th>
                <td id='th-food'>${item["food"]}</th>
                <td id='th-food-balace'>${item["balance_food"]}</th>
                <td id='th-dom'>${item["build_points"]}</th>

                <td id='th-buildings'>${buildings}</th>
            </tr>`
        )
    });

    // <td id='th-buildings'>${item["buildings"]}</th>
    // <img src="../static/image/buildings/${statusBuildings[2][build]}" alt="Картинки нет, сорян" width = 50px> 
            
    

    // Старый вариант для одного поселения
    // Вывод построек в поселении
    buildingsNameHtml.innerHTML = `<div style="margin-top: 2px; text-align: center;">Постройки</div>`;
    for (let key in statusSettlement.buildingsList) {
        if (statusSettlement.buildingsList[key] > 0) {
            buildingsNameHtml.innerHTML +=   
            `<div>
                ${key}: ${statusSettlement.buildingsList[key]}
            </div>`;
        }
    }
    // Вывод доступных для покупки товаров
    availableGoodsBuyNameHtml.innerHTML = `<div style="margin-top: 2px; text-align: center;">Доступно к покупке</div>`;
    for (let key in statusSettlement.availableGoodsBuy) {
        availableGoodsBuyNameHtml.innerHTML +=   
            `<div>
                ${key}: ${statusSettlement.availableGoodsBuy[key]}
            </div>`;
    }
    // if (res[1].buildings_list.length > 0) {
    //     console.log("Постройки есть.");
        
    //     res[1].buildings_list.forEach((item, id) => {
    //     // res[1].buildings_name_list.forEach((item, id) => {
    //         console.log("forEach 3 Тут выводим список ресурсов");
    //         if (res[1].buildings_list[item] > 0) {
    //             buildingsNameHtml.innerHTML +=   
    //             `<div>
    //                 ${item}: ${res[1].buildings_list[item]}
    //             </div>`;
    //         };        
    //     });
    // } else {
    //     buildingsNameHtml.innerHTML += `<div>Ничего нет</div>`;
    // }

    // console.log(`Список построек1:? ${res[1].buildings_list[2]}`);
    // console.log(`Список построек2:? ${statusSettlement.buildingsList["Гавань1"]}`);

    // !!!!!!!!!!!!!! Старое
    // Вывод на экран количества ресурсов и построек
    // goodsNameHtml.innerHTML = `<div style="margin-top: 2px; text-align: center;">Ресурсы</div>`;
    // statusGame.goodsListForSell = []
    //     res.goods_name_list.forEach((item, id) => {        
    //         console.log("forEach 2 Тут выводим список ресурсов");
    //         if (res.goods_list[item] > 0) {
    //             // Добавим товар в массив который выводится при выборе товара для продажи
    //             statusGame.goodsListForSell.push(item);
    //             goodsNameHtml.innerHTML +=   
    //             `<div>
    //                 ${item}: ${res.goods_list[item]}
    //             </div>`;
    //         };        
    //     });
    
    // console.log(statusGame.goodsListForSell);


    updateVar();
    logStart();
    logResultStart();
    logAllResultStart();
}

// Отмена приказов
document.getElementById('cancel-all-acts').addEventListener('click', () => {
    cancelAct("all");
});

document.getElementById('cancel-act').addEventListener('click', () => {
    cancelAct("last");
});

function cancelAct(what) {
    const req = new XMLHttpRequest();
    req.open("GET", `/cancel_act?gameId=${statusGame.game_id}&what=${what}`);
    req.addEventListener('load', () => {
        console.log("Xmmm");
        requestStatusPlayer();
        // То что ниже в комментах оставим, интересно....
        // Если ответ есть, запустить функцию отображения
        // if (response) {
            // writeComment(response, id);
        // };
    });
    req.addEventListener('error', () => {
        console.log('error')
    });
    req.send();
};

// Отправка хода с модалкой
document.getElementById('end-turn-btn').addEventListener('click', () => {
    if (statusGame.acts.length < statusGame.bodyPoints) {
        // confimModalEndTurd("У вас еще остались очки действий. Точно отправить ход?")
        modal.style.display = "block";
        let content = document.getElementById("show-content");
        content.innerHTML = `<div style="font-size: 25px">У вас еще остались очки действий. Точно отправить ход?</div>`
        content.innerHTML += `<button onclick = "postTurn(statusGame.game_id); closeModal();" style="font-size: 25px; width: 100px">Да</button>`
        content.innerHTML += `<button onclick = closeModal() style="font-size: 25px; width: 100px">Нет</button>`
    } else {
        postTurn(statusGame.game_id);
    }
    // postTurn(statusGame.game_id); // Передадим ИД партии аргументом, он сразу уйдет на Бек для определения к какой партии присвоить ход
})


function postTurn() {
    const request = new XMLHttpRequest();
    request.open('POST', `/post_turn?gameID=${statusGame.game_id}`);
    request.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    
    // console.log(JSON.stringify(country.acts))
    // request.send(JSON.stringify("turn"));
    console.log(JSON.stringify(statusGame.acts))
    request.send(JSON.stringify(statusGame.acts));

    request.addEventListener('load', () => {
        console.log("Автообновление");

        // Обновим общие параметры и параметры игрока
        requestStatus();
        requestStatusPlayer();

        // Временно отключу автообновление, неудобно для тестов
        // autoUpdateTimer();

        // Автообновление параметров игры после обсчета хода
        // getVar()
    });

    // requestStatus();
    // requestStatusPlayer();

    // autoUpdateTimer();
};

// Отправка одного действия
// По факту не одного, а сразу всех. И бек не пушит в массив, а перезаписывает заново
// Функция Необходима для отображения актуального списка действий, 
// который не будет пропадать и сбиваться при обновлении странички 
// Ход при этом не считается отправленным
function postAct(gameId) {
    const request = new XMLHttpRequest();
    request.open('POST', `/post_act?gameID=${gameId}`);
    request.setRequestHeader('Content-type', 'application/json; charset=utf-8');

    // Помимо самих ид действий, нужно еще отправить текстовое описание действий.
    // Текстовая теперь запись идет в массиве действия под нулевым индексом
    // post = {
    //     acts: statusGame.acts,
    //     // actsText: statusGame.actsText,
    // }
    
    console.log(JSON.stringify(statusGame.acts))
    request.send(JSON.stringify(statusGame.acts));

    request.addEventListener('load', () => {
        console.log("Автообновление");
        requestStatus();
        requestStatusPlayer();
    });
};

function confirmRecTurn() {  // Подтвердить получение хода, чтобы не вылазило оповещение

    closeModal(); // Закроем модальное окошко

    const request = new XMLHttpRequest();
    request.open('GET', `/confirm_rec_turn?gameID=${statusGame.game_id}`);
    request.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    
    console.log(JSON.stringify(statusGame.acts));
    // Это можно удалить???
    request.send(JSON.stringify(statusGame.acts));

    request.addEventListener('load', () => {
        console.log("Автообновление");
        requestStatus();
        requestStatusPlayer();
        closeModal(); // Закроем модальное окошко
    });

}

// Функции отображения логов. До хода и итогов хода

function logStart() {       //Функция запуска будущего лога
    let listLogs = document.getElementById('logs');
    listLogs.innerText = 'Ваши действия';  // Очистим
    if (statusGame.bodyPoints - statusGame.acts.length < 0) {
        listLogs.innerText += '\n Внимание, вы запланировали больше чем у вас доступно "очков действий", все не выполненные перенесутся на следующий ход.'
    }
    statusGame.acts.forEach((item, num) => {  
        // let a = document.getElementById('logs');
        listLogs.insertAdjacentHTML('beforeend', `<div>${num + 1}: ${item[0]}</div>`);
    });
}

function logResultStart() {       //Функция запуска лога итога хода
    document.getElementById('logs-result').innerText = 'Лог прошлого хода';  // Очистим + подсказка
    console.log(`Тут выведем все логи: ${statusGame.logsText}`)
    statusGame.logsText.forEach((item, num) => {  
        let a = document.getElementById('logs-result');
        a.insertAdjacentHTML('beforeend', `<div>${num + 1}: ${item}</div>`);
    }); 
}

function logAllResultStart() {       //Функция запуска лога итога хода всех игроков
    document.getElementById('all-logs-result').innerText = 'Общий лог прошлого хода';  // Очистим + подсказка
    statusGame.allLogs.forEach((item, num) => {  
        let a = document.getElementById('all-logs-result');
        a.insertAdjacentHTML('beforeend', `<div>${num + 1}: ${item}</div>`);
    }); 
}


// Запись действий игрока

// Строительство 
// Модалка для строительства
document.getElementById('menu-new-building').addEventListener('click', () => {
    hiddenAllMenu();  // Скроем все меню
    // chooseList.innerHTML = `<span>Пока что здесь пусто</span>`;  // Добавим подсказку
    // Старый функционал
    // chooseList.innerHTML = `<span>Выберите постройку:</span>`;  // Добавим подсказку
    // statusGame.colonyListForBuild.forEach((item, id) => {
    //     // if (id > 0) {
    //         chooseList.innerHTML += `<button class="menu-buttons-choose custom-btn btn-15">${item} Стоимость: ${statusGame.colonyPrice[item]}</button>`;
    //         console.log(item);
    //     // };        
    // });

    modal.style.display = "block";
    let content = document.getElementById("show-content");  // <div>Сделать пожертвование.</div>
    content.innerHTML = `
        <div style="font-size: 20px">
            <div>Строительство</div>
    `;
    // statusBuildings[0].forEach((item, id) => {
    //     content.innerHTML += `${item} ${id}`
    // });
    // for (i = 0; i <= statusBuildings[0].length; i++) {
    console.table(`Доступные постройки ${statusBuildings}`)
    console.log(`Доступные постройки0 ${statusBuildings[0]}`)
    console.log(`Доступные постройки1 ${statusBuildings[1]}`)
    statusBuildings[0].forEach((build, num) => {
        console.log(`Доступная постройка ${build}`)
        let cost = statusBuildings[1][build];
        let description = statusBuildings[3][build];
        content.innerHTML += `
        <div class="wrapper" style="border: solid; margin-top: 5px;">
            <div>
                <img src="../static/image/buildings/${statusBuildings[2][build]}" alt="Картинки нет, сорян" width = 50px> 
            </div>
            <button onclick = build111('${build}')>Построить</button>
            <div> 
                <div>${build}.</div> 
                <div>Стоимость: ${cost}.</div> 
                <div>${description}</div> 
            </div>
        </div>
        `
        // Описание: 
    })
    // for (let build in statusBuildings[0]) {
        

        // <div style="font-size: 20px">${build}</div>
        // <div style="font-size: 15px">Стоимость: ${cost}</div>  onclick = build111(${build})
    
    content.innerHTML += `
            <div style="font-size: 20px">
                <button onclick = closeModal() style="font-size: 25px; margin-top: 20px">Отмена</button>
            </div>
        </div>
    `;
    
    console.log("Модалка открыта");
    // Нарисуем кнопку отмены(выхода)
    // chooseList.innerHTML += `<button class="menu-choose-exit custom-btn btn-15" id="menu-choose-exit">Отмена</button>`;
    // document.getElementById('menu-choose-exit').addEventListener('click', () => { chooseList.innerHTML = ''; exitToMainMenuButtons(); });

    // Старый функционал
    // Определяем позицию кнопки и "создаем" соответсвующий приказ
    // document.querySelectorAll(".menu-buttons-choose").forEach((btn, i) => {
    //     btn.addEventListener('click', () => {
    //         statusGame.acts.push([
    //             `Строим: ${statusGame.colonyListForBuild[i-1]}`, 101, statusGame.colonyListForBuild[i-1]
    //         ]);         
    //         // 101 это главный ид действия. i индекс постройки в списке построек в беке. Ну и текст описание действия
    //         postAct(statusGame.game_id);
    //         logStart();
    //         console.log(statusGame.acts);
    //         exitToMainMenuButtons();    // Скрываем меню
    //         chooseList.innerHTML = '';  // Чистим(скрываем) список
    //     });
    // });

});

// Вызываем эту фукнцию из создаваемой кнопки в html
function build111(buildings_name){
    console.log(`Строим: ${buildings_name}.`);
    statusGame.acts.push([
        `Строим: ${buildings_name}`, 101, buildings_name
    ]);    
    postAct(statusGame.game_id);
    logStart();
    closeModal();
};

document.getElementById('make-donation').addEventListener('click', () => {

});

// Торговля
document.getElementById('menu-trade').addEventListener('click', () => {
    hiddenAllMenu();
    console.log("Запуск торговли")
    document.getElementById("main-menu-buttons").setAttribute('style','display:none');
    document.getElementById("menu-buttons-trade").setAttribute('style','visibility:visible');
    tradeChooseCity();  // Вызов функции выбора города для торговли из Антички

    // Нарисуем кнопку отмены(выхода)
    chooseList.innerHTML += `<button class="menu-choose-exit custom-btn btn-15" id="menu-show-trade-exit">Выход</button>`;
    document.getElementById('menu-show-trade-exit').addEventListener('click', () => { 
        chooseList.innerHTML = ''; 
        exitToMainMenuButtons(); 
    });
});

// !!!!!!!!!!!!! Старое
// Выбрать город для торговли
function tradeChooseCity() { 
    console.log("Городов для выбора нет");
    chooseList.innerHTML += 
        `<span>
            Пока что здесь пусто.
        </span>`;
    // statusGame.cities.forEach((item, id) => {
    //     chooseList.innerHTML += 
    //     `<button class="menu-buttons-show-trade custom-btn btn-15">
    //         ${item}
    //     </button>`;
    // });
    

    // Определяем позицию кнопки и "создаем" соответсвующий приказ
    document.querySelectorAll(".menu-buttons-show-trade").forEach((btn, i) => {
        btn.addEventListener('click', () => {
            console.log(`Вы выбрали город номер: ${btn}, ${i}`);
            console.log(`Вы выбрали город: ${statusGame.cities[i]}`);
            // !!!!! Старое  tradeChooseAction(statusGame.cities[i]); // Запустим дальнейшую функицю, передав ид (!не)города(ИД по списку предложенных к выбору)
        });
    });
};

// После выбора города определим дальнейшие дествия
function tradeChooseAction(city) {
    chooseList.innerHTML = `Продаем товар в ${city}:`;
    console.log(`Продаем товар в город ${city}`);
    // Выведем список только тех товаров, которые есть в наличии
    statusGame.goodsListForSell.forEach((item, id) => {
        chooseList.innerHTML += 
        `<button class="menu-buttons-show-trade trade-goods custom-btn btn-15">
            Продать ${item}. Цена: ${statusGame.allGoodsPrices[city][item]}
        </button>`;
    });     
    chooseList.innerHTML += 
    `<button class="custom-btn btn-15 menu-buttons-show-trade" id="sell-all-goods">
        Продать весь товар
    </button>`;
    // Нарисуем кнопку отмены(выхода)
    chooseList.innerHTML += `<button class="custom-btn btn-15 menu-choose-exit" id="menu-show-trade-exit">Выход</button>`;
    // Определяем позицию кнопки и "создаем" соответсвующий приказ
    document.querySelectorAll(".trade-goods").forEach((btn, i) => {
        btn.addEventListener('click', () => {
            console.log(btn);
            console.log(statusGame.goodsListForSell[i]);
            tradeChooseNumGoodsTrade(statusGame.goodsListForSell[i], city);
        });
    });
    // Определяем еще одну кнопку
    document.getElementById("sell-all-goods").addEventListener('click', () => {
        console.log("А попробем-ка продать весь товар");
        statusGame.acts.push([`Продаем весь товар в ${city}`, 202, city]); 
        postAct(statusGame.game_id);
        logStart();
        chooseList.innerHTML = ''; 
        exitToMainMenuButtons(); 
    });    
    // Событие выхода на соответствующую кнопку
    document.getElementById('menu-show-trade-exit').addEventListener('click', () => { 
        chooseList.innerHTML = ''; 
        exitToMainMenuButtons(); 
    });
}

// После выбора города и выбора товара уточняем количество
function tradeChooseNumGoodsTrade(goods, city) {
    chooseList.innerHTML = "Продаем товар:";
    chooseList.innerHTML += 
    `<button class="custom-btn btn-15 menu-buttons-show-trade" id="sell-all-goods">
        Продать все
    </button>`;

    chooseList.innerHTML += 
    `<fieldset> 
        <legend>Выберете количество</legend>
        <p>
            <input id="goods-value" type="range" min="0" max="${statusGame.goods_list[goods]}" 
            onchange="document.getElementById('rangeValue').innerHTML = this.value;" 
            list="rangeList"> 
            <span id="rangeValue">0</span>
        </p>
        <button class="custom-btn btn-15 menu-buttons-show-trade" id="sell-num-goods">
            Продать
        </button>
    </fieldset>`;
    // Нарисуем кнопку отмены(выхода)
    chooseList.innerHTML += `<button class="custom-btn btn-15 menu-choose-exit" id="menu-show-trade-exit">Выход</button>`; 
    // Продать весь выбранный товар. Аргумент -1 для бекенда
    document.getElementById('sell-all-goods').addEventListener('click', () => { 
        console.log("А попробем-ка продать веь выбранный товар");
        statusGame.acts.push([`Продаем весь товар ${goods} в ${city}`, 201, city, goods, -1]); 
        postAct(statusGame.game_id);
        logStart();
        chooseList.innerHTML = ''; 
        exitToMainMenuButtons(); 
    });
    // Продать выбранное число товара
    document.getElementById('sell-num-goods').addEventListener('click', () => { 
        num = document.getElementById('goods-value').value;
        statusGame.acts.push([`Продаем ${num} товар ${goods} в ${city}`, 201, city, goods, num]); 
        console.log(`Продадим ${num} товар ${goods} в ${city}`);
        postAct(statusGame.game_id);
        logStart();
        chooseList.innerHTML = ''; 
        exitToMainMenuButtons(); 
    });
    // Определяем позицию кнопки и "создаем" соответсвующий приказ

    document.getElementById('menu-show-trade-exit').addEventListener('click', () => { 
        chooseList.innerHTML = ''; 
        exitToMainMenuButtons(); 
    });
}

// Решения 
document.getElementById('menu-decision').addEventListener('click', () => {
    hiddenAllMenu();
    console.log("Запуск решений")
    document.getElementById("main-menu-buttons").setAttribute('style','display:none');
    document.getElementById("menu-buttons-decision").setAttribute('style','visibility:visible');

});

// document.getElementById('buy-title').addEventListener('click', () => {

//     modal.style.display = "block";
//     let content = document.getElementById("show-content");
//     content.innerHTML = `
//         <div style="font-size: 20px">
//             <div>Купить титул</div>
//             <div>Стоимость: 1000 за 1 ранг + 100 за каждый купленный ранг игроками.</div>
//             <button onclick = buyTitle() style="font-size: 25px; margin-top: 10px">Купить</button>
//             <button onclick = closeModal() style="font-size: 25px">Отмена</button>
//         </div>
//     `;
    
//     console.log("Модалка открыта");

// });

function buyTitle() {
    console.log("Раздать деньги");
    statusGame.acts.push([`Раздаем деньги`, 301]); 
    postAct(statusGame.game_id);
    logStart();
    chooseList.innerHTML = ''; 
    closeModal();
    exitToMainMenuButtons(); 
}

document.getElementById('make-donation').addEventListener('click', () => {

    modal.style.display = "block";
    let content = document.getElementById("show-content");  // <div>Сделать пожертвование.</div>
    content.innerHTML = `
        <div style="font-size: 20px">
            <div>Раздать часть казны жителям поселения.</div>
            <button onclick = makeDonation(10) style="font-size: 25px; margin-top: 10px">10</button>
            <button onclick = makeDonation(20) style="font-size: 25px; margin-top: 10px">20</button>
            <button onclick = makeDonation(30) style="font-size: 25px; margin-top: 10px">30</button>
            <button onclick = makeDonation(40) style="font-size: 25px; margin-top: 10px">40</button>
            <button onclick = makeDonation(50) style="font-size: 25px; margin-top: 10px">50</button>

            <button onclick = closeModal() style="font-size: 25px">Отмена</button>
        </div>
    `;
    
    console.log("Модалка открыта");
});

function makeDonation(sum) {
    console.log("Раздать деньги");
    statusGame.acts.push([`Раздаем деньги: ${sum} с.`, 301, sum]); 
    postAct(statusGame.game_id);
    logStart();
    chooseList.innerHTML = ''; 
    closeModal();
    exitToMainMenuButtons();     
}


//
// Просмотр "Дипломатии"
document.getElementById('menu-diplomaty').addEventListener('click', () => {
    hiddenAllMenu();
    document.getElementById("main-menu-buttons").setAttribute('style','display:none');
    document.getElementById("menu-buttons-diplomaty").setAttribute('style','visibility:visible');
    req_status_all_player();
});

// Отображение всех игроков с основными параметрами(золото, имя, готовность хода)
function req_status_all_player() {
    console.log(statusGame.game_id)
    console.log("Запрос статистики игроков")
    const request = new XMLHttpRequest();
    request.open("GET", `/req_status_all_player?gameId=${statusGame.game_id}`);
    request.addEventListener('load', () => {
        console.log("Xmmm")
        if (request.status === 200) {
            if (request.response == "") {
                console.log("К нам пришла пустая строка");
                
            } else {
                const response = JSON.parse(request.response);
                console.log(response)
                displayStatisticsOfAllPlayers(response);
                // displayStatisticsOfAllPlayersOnBoard(response);
            };
        } else {
            console.log("Ответ от сервера не получен");
        }
    });
    request.addEventListener('error', () => {
        console.log('error')
    });
    request.send();
};

// Убрал, ибо похоже это с прошлой версии отображение всех в шапке, пока не используется, но надо бы перенести в левую часть экрана
// И такая же функция для отображения в шапке
function req_status_all_player_head() {
    console.log(statusGame.game_id)
    console.log("Запрос статистики игроков")
    const request = new XMLHttpRequest();
    request.open("GET", `/req_status_all_player?gameId=${statusGame.game_id}`);
    request.addEventListener('load', () => {
        console.log("Xmmm")
        if (request.status === 200) {
            if (request.response == "") {
                console.log("К нам пришла пустая строка");
                
            } else {
                const response = JSON.parse(request.response);
                console.log(response)
                displayStatisticsOfAllPlayersOnBoard(response);
            };
        } else {
            console.log("Ответ от сервера не получен");
        }
    });
    request.addEventListener('error', () => {
        console.log('error')
    });
    request.send();
};

function displayStatisticsOfAllPlayers(playersList) {
    playersList.forEach((item, id) => {
        status_end_turn = ""
        if (playersList[id]["end_turn"] == true) {
            status_end_turn = "Готов"
        } else {
            status_end_turn = "НЕ готов"
        }  
        chooseList.innerHTML += 
        `<button class="menu-buttons-show-diplomaty custom-btn btn-15">
        ${playersList[id]["name_rus"]}.
        Золото: ${playersList[id]["gold"]}.
        Очки: ${playersList[id]["win_points"]}
        </button>`; 
    });
    // Нарисуем кнопку отмены(выхода)    
    chooseList.innerHTML += `<button class="menu-choose-exit custom-btn btn-15" id="menu-show-diplomaty-exit">Выход</button>`;
        document.getElementById('menu-show-diplomaty-exit').addEventListener('click', () => { 
            chooseList.innerHTML = ''; 
            exitToMainMenuButtons(); 
        });
}
function displayStatisticsOfAllPlayersOnBoard(playersList) {
    const playersStatusList = document.querySelector(".players-stat");
    // Ниже старая надпись для окошка с игроками
    playersStatusList.innerHTML = `<div style="margin-top: 2px; text-align: center;"></div>`
    console.log("Запуск функции отображения статистики игроков в шапке")
    playersList.forEach((item, id) => {
        if (playersList[id]["end_turn"] == true) {
            // status_end_turn = "Готов"
            playersStatusList.innerHTML += 
            `<div>
            ${playersList[id]["name_rus"]}: <span style="background-color: green;"> Готов </span>
            </div>`; 

        } else {
            // status_end_turn = "НЕ готов"
            playersStatusList.innerHTML += 
            `<div>
            ${playersList[id]["name_rus"]}: <span style="background-color: red;"> НЕ готов </span>
            </div>`; 

        }  
        // playersStatusList.innerHTML += 
        // `<div>
        // ${playersList[id]["name_rus"]}: <span style="background-color: red;"> ${status_end_turn} </span>
        // </div>`; 
    });
}

// Модальное окно
// Получение самого элемента вверху скрипта
// // Получить модальное окно
// const modal = document.getElementById("my-modal");

// // Получить кнопку, которая открывает модальное окно
// const btnShowAllLogsParty = document.getElementById("show_all_logs_party");

// // Получить элемент <span>, который закрывает модальное окно
// const span = document.getElementsByClassName("close")[0];

// Открыть модальное окно по нажатию
btnShowAllLogsParty.onclick = function() {
    modal.style.display = "block";
    let content = document.getElementById("show-content");
    content.innerHTML = ""
    console.log("Модалка открыта")
    statusGame.allLogsParty.forEach((item, id) => {
        console.log(item)
        content.innerHTML += `<div>${item}</div>`
    });
    content.innerHTML += `<button onclick = closeModal() style="font-size: 20px">Выйти</button>`
};

btnShowAllLogsPartyPlayers.onclick = function() {
    modal.style.display = "block";
    let content = document.getElementById("show-content");
    content.innerHTML = ""
    console.log("Модалка открыта")
    statusGame.logsTextAllTurns.forEach((item, id) => {
        console.log(item)
        content.innerHTML += `<div>${item}</div>`
    });
    content.innerHTML += `<button onclick = closeModal() style="font-size: 20px">Выйти</button>`
};

// Когда пользователь нажимает на <span> (x), закройте модальное окно
span.onclick = function() {
  modal.style.display = "none";
  exitToMainMenuButtons(); // На всякий случай выйдем в главное меню кнопок
}

// Общая функция закрытия модального окна
function closeModal() {
    modal.style.display = "none";   
    exitToMainMenuButtons(); // На всякий случай выйдем в главное меню кнопок
}

// Информационное модальное окошко
function infoModal(text) {
    modal.style.display = "block";
    let content = document.getElementById("show-content");
    content.innerHTML = text 
    content.innerHTML += `<button onclick = closeModal() style="font-size: 25px">Хорошо</button>`

}

// Модальное окошко подтверждения
// Не получается пока сдать универсальное
function confimModal(text, fn) {
    fn = postTurn
    modal.style.display = "block";
    let content = document.getElementById("show-content");
    content.innerHTML = `<div style="font-size: 25px">${text}</div>`
    content.innerHTML += `<button onclick = ${fn} style="font-size: 25px; width: 100px">Да</button>`
    content.innerHTML += `<button onclick = closeModal() style="font-size: 25px; width: 100px">Нет</button>`

}

function confimRecTurnModal() {
    modal.style.display = "block";
    let content = document.getElementById("show-content");
    content.innerHTML = `<div style="font-size: 25px">Новый ${statusGame.turn} ход</div>`;
    content.innerHTML += `<button onclick = confirmRecTurn() style="font-size: 25px; width: 150px">Отлично</button>`;
    // Сразу подвердим получени хода, чтобы окошко не выскакивало два раза
    statusGame.endTurnKnow = true;
}