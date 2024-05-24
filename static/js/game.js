console.log('Стрипт странички игры успешно загружен');

// Для поиска:
// Вкладки


// Меню для уточнения количества
const chooseList = document.querySelector('.choose-list');

// Отображаемые в интерфейсе параметры, одновляются при запросе на сервер
// Старое, можно попробовать переходить на новый словарь, который просто копирует весь ответ сервера.
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
    playerId: 0,
    gold: 0,            // Золото игрока
    title: 0,           // Титул игрока, пока числом, будет строкой, типо "Ярл"
    bodyPoints: 0,      // Очки действия для игрока

    // Управление поселениями
    ourSettlements: [],

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

// Отображаемые в интерфейсе параметры, одновляются при запросе на сервер
// Новое
// Общая инфа о партии
let statusGameDictInfo = {

}
// Инфа об игроке
let statusGameDictPlayer = {

}
// Инфа о юнитах игрока
let statusGameDictPlayerUnits = {

}
// Инфа об армиях игрока
let statusGameDictPlayerArmy = {

}
// Инфа о поселениях
let statusGameDictSettlements = {

}

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
// Список всех поселений со всей информацией в разных форматах
let statusSettlements = []
let statusSettlementsNames = {}
let statusSettlementsNamesRus = {}
let statusSettlementsId = {}

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
    // Откроем меню провинций
    document.getElementById("table-province").setAttribute('style', 'visibility: visible');
});
// Поселение
document.getElementById('settlement-button').addEventListener('click', () => {
    hiddenAllWindows();
    document.getElementById("settlement-window").setAttribute('style','visibility:visible');
    document.getElementById("settlement-button").setAttribute('style','color:red; cursor: pointer;');
    // Откроем меню провинций
    document.getElementById("table-province").setAttribute('style', 'visibility: visible');
});
// Торговля
document.getElementById('trade-button').addEventListener('click', () => {
    hiddenAllWindows();
    document.getElementById("trade-window").setAttribute('style','visibility:visible');
    document.getElementById("trade-button").setAttribute('style','color:red; cursor: pointer;');
    // Откроем меню провинций
    document.getElementById("table-province").setAttribute('style', 'visibility: visible');
});
// Карта
document.getElementById('map-button').addEventListener('click', () => {
    hiddenAllWindows();
    document.getElementById("map-window").setAttribute('style','visibility:visible');
    document.getElementById("map-button").setAttribute('style','color:red; cursor: pointer;');
    // Откроем меню провинций
    document.getElementById("table-province").setAttribute('style', 'visibility: visible');
});
// Династия
document.getElementById('dynasty-button').addEventListener('click', () => {
    hiddenAllWindows();
    document.getElementById("dynasty-window").setAttribute('style','visibility:visible');
    document.getElementById("dynasty-button").setAttribute('style','color:red; cursor: pointer;');
    // Откроем меню провинций
    document.getElementById("table-province").setAttribute('style', 'visibility: visible');
});
// Армия
document.getElementById('army-button').addEventListener('click', () => {
    hiddenAllWindows();
    document.getElementById("army-window").setAttribute('style','visibility:visible');
    document.getElementById("army-button").setAttribute('style','color:red; cursor: pointer;');
    // Дополнительно скроем меню провинций
    document.getElementById("table-province").setAttribute('style', 'display: none');
});
// Игроки
document.getElementById('players-button').addEventListener('click', () => {
    hiddenAllWindows();
    document.getElementById("players-window").setAttribute('style','visibility:visible');
    document.getElementById("players-button").setAttribute('style','color:red; cursor: pointer;');
    // Откроем меню провинций
    document.getElementById("table-province").setAttribute('style', 'visibility: visible');
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
    // Новое, копирование всего сразу в один словарь
    statusGameDictInfo = res
    console.log('!!!!!!!! statusGameDictInfo');
    console.log(statusGameDictInfo)

    // Старое
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
    statusGame.playerId = res.player_id;
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
const armyNameHtml = document.querySelector(".stats-army");
const unitsNameHtml = document.querySelector(".stats-units");

// Обновим параметры управляемой "страной"
function actualVarPlayer(res) {
    // Новое, копирование всего сразу в один словарь
    statusGameDictPlayer = res[0]
    statusGameDictPlayerUnits = res[2]
    statusGameDictPlayerArmy = res[3]

    console.log('!!!!!!!! statusGameDictPlayer');
    console.log(statusGameDictPlayer)

    statusGameDictSettlements = res[1]
    console.log('!!!!!!!! statusGameDictSettlements');
    console.log(statusGameDictSettlements)

    console.log('!!!!!!!! statusGameDictPlayerUnits');
    console.log(statusGameDictPlayerUnits)

    console.log('!!!!!!!! statusGameDictPlayerArmy');
    console.log(statusGameDictPlayerArmy)

    console.log("statusGame old")
    console.log(statusGame)
    statusGame.winPoints = res[0].win_points
    statusGame.dynastyName = res[0].name_rus
    statusGame.playerId = res[0].player_id
    statusGame.gold = res[0].gold

    statusGame.ourSettlements = res[0].our_settlements

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


    // console.log("statusGame new")
    // console.log(statusGame)

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
    statusSettlements = []
    console.log("Вывод поселений.")
    for (i=0; i<res[1].length; i++) {
        statusSettlements.push(res[1][i])
        statusSettlementsNames[res[1][i]["name_eng"]] = res[1][i]
        statusSettlementsNamesRus[res[1][i]["name_rus"]] = res[1][i]
        statusSettlementsId[res[1][i]["row_id"]] = res[1][i]
    }
    // console.log("Новые способы сохранения инфы.")
    console.log("statusSettlements");
    console.log(statusSettlements);
    console.log("statusSettlementsNames");
    console.log(statusSettlementsNames);
    console.log("statusSettlementsNamesRus");
    console.log(statusSettlementsNamesRus);
    console.log("statusSettlementsId");
    console.log(statusSettlementsId);

    let tab = document.getElementById('table-province');
    tab.innerHTML = `            
        <thead>    
            <tr class="table">
                <th class="th" id='th-loc' style="min-width: 100px">Локация</th>
                <th class="th" id='th-relation' style="min-width: 60px">Отнош.</th>
                <th class="th" id='th-pop' style="min-width: 40px">Нас.</th>
                <th class="th" id='th-wealth_status style="min-width: 80px"'>Благ.</th>
                <th class="th" id='th-food' style="min-width: 40px">Еда произв.</th>
                <th class="th" id='th-food-balace' style="min-width: 40px">Еда баланс</th>
                <th class="th" id='th-dom' style="min-width: 50px">Строй</th>

                <th class="th" id='th-buildings' style="min-width: 400px; ">Постройки</th>
                <th class="th" id='th-action' style="min-width: 70px; ">Действие</th>
            </tr>
        </thead>`
    
    
    res[1].forEach((item, num) => {
        // Преобразуем некоторые значения при необходимости
        let buildings = []

        for (let key in item["buildings_list"]) {
            if (item["buildings_list"][key]>0) {
                // console.log("Выводим иконки построек.");
                // console.log(`key ${key}`);
                for (i = 1; i <= item["buildings_list"][key]; i++) {
                    buildings.push(`<img style="width: 30px" src="../static/image/buildings/${item["buildings_icon_name"][key]}" alt="Картинки нет, сорян" >`)
                }// console.log(`key ${key}`);
            }
        }
        // Выясним отношение поселения
        let relation = ''
        // console.log("Выясняем отношения.")
        // console.log(statusGame.playerId)
        if (statusGame.playerId == item["ruler"]) {
            relation = 'Дом'
        } else if (item["row_id"] in statusGame.ourSettlements) {
            relation = 'Наш'
        } else {
            relation = 'Нейтрал.'
        }
        tab.insertAdjacentHTML("beforeend", 
            `<tr class="table table-location">
                <td id='th-loc'>${item["name_rus"]}</th>
                <td id='th-relation'>${relation}</th>
                <td id='th-pop'>${item["population"]}</th>
                <td id='th-wealth_status'>${item["wealth_status"]}</th>
                <td id='th-food'>${item["food"]}</th>
                <td id='th-food-balace'>${item["balance_food"]}</th>
                <td id='th-dom'>${item["build_points"]}</th>

                <td id='th-buildings'>${buildings}</th>

                <td id='th-action'>
                    <div class="dropdown">
                        <button id="btn-act-${item["row_id"]}" class="dropbtn">Выбрать</button>
                        <div id="dropdownProv${item["row_id"]}" class="dropdown-content">
                            <a id="btn-act-war${item["row_id"]}">Атаковать</a>
                            <a id="btn-act-build${item["row_id"]}">Строительство</a>
                        </div>
                    </div> 
                </th>

            </tr>`
        );

        // <td id='th-action'><button id="btn-act-${item["row_id"]}">Выбрать</button></th>
        // <button id="btn-act-${item["row_id"]}">Выбрать</button>
        document.getElementById(`btn-act-${item["row_id"]}`).addEventListener(('click'), () => {
            console.log(`Нажата кнопка выбора действия в провинции с ид: ${item["row_id"]}`);
            dropdownProvince(item["row_id"])
        });
        document.getElementById(`btn-act-war${item["row_id"]}`).addEventListener(('click'), () => {
            console.log(`Нажата кнопка нападения на провинцию с ид: ${item["row_id"]}`);
        });
        document.getElementById(`btn-act-build${item["row_id"]}`).addEventListener(('click'), () => {
            console.log(`Нажата кнопка строительства в провинции с ид: ${item["row_id"]}`);
            menuNewBuilding(item);
        });        
    });

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
    showUnits(document.getElementById('table-units'));  // Сделать таблицу с юнитами
    logStart();
    logResultStart();
    logAllResultStart();
}

// Открыващее меню для действий с поселениями/провинциями.
/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function dropdownProvince(id_prov) {
    document.getElementById(`dropdownProv${id_prov}`).classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {

    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
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
        console.log("Фукнции requestStatus и requestStatusPlayer отключены.");
        // requestStatus();
        // requestStatusPlayer();
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

// Меню армии
// document.getElementById('create-army').addEventListener('click', () => {
//     createArmy();
// });

// Функция сбора и отображения юнитов
function showUnits(unitsTab) {
    // let unitsTab = document.getElementById('table-units');
    unitsTab.innerHTML = ''
    unitsTab.insertAdjacentHTML('beforeend', `            
        <thead>    
            <tr class="table-units">
                <th class="th"><span"> Расположение</span> </th>

                <th class="th"><span class="rotate-sm-90"> Кол-во.</span></th>
                <th class="th"><span class="rotate-sm-90"> HP</span></th>
                <th class="th"><span class="rotate-sm-90"> Выносл.</span></th>

                <th class="th"><span class="rotate-sm-90"> Сила</span></th>
                <th class="th"><span class="rotate-sm-90"> Ловкость</span></th>

                <th class="th"><span class="rotate-sm-90"> Броня</span></th>
                <th class="th"><span class="rotate-sm-90"> Щит</span></th>

                <th class="th"><span class="rotate-sm-90"> Бл. бой</span></th>
                <th class="th"><span class="rotate-sm-90"> Оружие</span></th>
                <th class="th"><span class="rotate-sm-90"> Дал. бой</span></th>
                <th class="th"><span class="rotate-sm-90"> Лук</span></th>
                <th class="th"><span class="rotate-sm-90"> Опыт</span></th>
                <th class="th">Имя</th>
                <th class="th"></th>
            </tr>
        </thead>`)
    console.log("Собираем юниты");
    console.log(statusGameDictPlayerUnits)
    for (i=0;i<statusGameDictPlayerUnits.length;i++) {
        // console.log(statusGameDictPlayerArmy[i])
        unitsTab.insertAdjacentHTML("beforeend", 
            `<tr class="table units">
                <td>${statusGameDictPlayerUnits[i][0]["location_name"]}</th>
                <td>${statusGameDictPlayerUnits[i][1].length}</th>
                <td>${statusGameDictPlayerUnits[i][0]["hp_cur"]}/${statusGameDictPlayerUnits[i][0]["hp_max"]}</th>
                <td>${statusGameDictPlayerUnits[i][0]["endurance_cur"]}/${statusGameDictPlayerUnits[i][0]["endurance_max"]}</th>
                <td>${statusGameDictPlayerUnits[i][0]["strength"]}</th>
                <td>${statusGameDictPlayerUnits[i][0]["agility"]}</th>
                <td>${statusGameDictPlayerUnits[i][0]["armor"]}</th>
                <td>${statusGameDictPlayerUnits[i][0]["shield"]}</th>
                <td>${statusGameDictPlayerUnits[i][0]["melee_skill"]}</th>
                <td>${statusGameDictPlayerUnits[i][0]["melee_weapon"]}</th>
                <td>${statusGameDictPlayerUnits[i][0]["ranged_skill"]}</th>
                <td>${statusGameDictPlayerUnits[i][0]["ranged_weapon"]}</th>
                <td>${statusGameDictPlayerUnits[i][0]["experience"]}</th>
                <td>${statusGameDictPlayerUnits[i][0]["name"]}</th>
                
                <td><label for="cheсked-unit-${statusGameDictPlayerUnits[i][0]["row_id"]}">Выбрать
                    <input class="cheсked-unit" id="cheсked-unit-${statusGameDictPlayerUnits[i][0]["row_id"]}" type="checkbox">
                </label></th>
                                
            </tr>`
        );

    }

    // Кнопка подтвердить для изменений с юнитаи
    document.getElementById('apply-changes-units').addEventListener('click', () => {
        const chooseAction = document.getElementById('unit-select-action');
        console.log("Выбираем действие с юнитами.");
        console.log(chooseAction.value);
        const checkBoxs = document.querySelectorAll('.cheсked-unit');
        let ckeckedUnits = []  // Список для сохранание ид выбранных юнитов.
        for (c=0;c<checkBoxs.length;c++) { 
            if (checkBoxs[c].checked) {
                ckeckedUnits.push(checkBoxs[c].id.slice(13))
            }
        }
        console.log(`Выбранные юниты: ${ckeckedUnits}`)
        let arg = [ckeckedUnits]  // Первый аргумент список юнитов. Остальное добавлять по необходимости.
        if (ckeckedUnits.length > 0) {
            if (chooseAction.value == "dismiss") {
                console.log("dismissUnits");
                console.log(arg);
                dismissUnits(arg)
            } else if (chooseAction.value == "train") {
                console.log("trainUnits");
                console.log(arg);
                trainUnits(arg)
            } else if (chooseAction.value == "create-army") {
                console.log("createArmy");
                console.log(arg);
                // Если не выбрана армия к которой присоединяются юниты, передаем 0, будет создана новая
                arg.push(0)
                createArmy(arg)
            }
        } else {
            alert("Юниты не выбраны.")
        }
        // console.log(checkBoxs);
        // console.log(checkBoxs[0]);
        // console.log(checkBoxs[0].id.slice(13));

    });

}


function dismissUnits(arg) {
    console.log("Распустить юниты.");
    statusGame.acts.push([`Распустить юниты...`, 401, arg]); 
    postAct(statusGame.game_id);
    logStart();
    // Для модалки.
    // chooseList.innerHTML = ''; 
    // closeModal();
    // exitToMainMenuButtons();     
}

function trainUnits(arg) {
    console.log("Тренировать юниты.");
    statusGame.acts.push([`Тренировать юниты...`, 402, arg]); 
    postAct(statusGame.game_id);
    logStart();
}


// function createArmy() {
//     modal.style.display = "block";
//     let content = document.getElementById("show-content");  // <div>Сделать пожертвование.</div>
//     content.innerHTML = `
//         <div style="font-size: 20px">
//             <div>Формирование армии</div>
//                 <table class="table" id="table-units-modal">  
                    
//     `;
//     let content2 = document.getElementById("table-units-modal");
//     showUnits(content2);
//     // Выясним отношение поселения для определения чьи юниты =)
//     console.log("Выясняем отношения.")
// };

// function createArmy(arg) {

//     modal.style.display = "block";
//     let content = document.getElementById("show-content"); 
//     // Начало конента модального окна
//     content.innerHTML = `
//         <div style="font-size: 20px">
//             <div>Формирование армии</div>
                    
//     `;
//     // Пункт присвоения названии армии
//     content.insertAdjacentHTML('beforeend', `
//         <div>
//             <span>Введите название армии:</span>
//             <input id="new-army-name" value="default"></input>
//         </div>
//     `);
//     // Начало выбора местораположения армии
//     content.insertAdjacentHTML('beforeend', `
//         <div>
//             <span>Выберете месторасположение армии:</span>
//             <select id="new-army-location">
//     `)
//     // Цикл добавления поселения для выбора стартовой локации
//     for (i=0; i<statusGameDictPlayer["our_settlements"].length; i++) {
//         content.insertAdjacentHTML('beforeend', `
//             <option value="train" name="1">
//                 Поселение с ид: ${statusGameDictPlayer["our_settlements"][i]}
//             </option>
//         `);

//     }
//     // // Конец выбора местораположения армии
//     // content.insertAdjacentHTML('beforeend', `

//     //         </select>
//     //     </div>`)
//     // // Конец контента модального окна
//     // content.insertAdjacentHTML('beforeend', `
//     //     </div>
//     // `)
//     console.log("Сформировать армию.");
//     statusGame.acts.push([`Сформировать армию..`, 403, arg]); 
//     // postAct(statusGame.game_id);
//     logStart();
// }


function createArmy(arg) {

    modal.style.display = "block";
    let content = document.getElementById("show-content");  // 
    // Начало конента модального окна
    let contentHTML = ""
    contentHTML = `
        <div style="font-size: 20px">
            <div>Формирование армии</div>
                    
    `;
    // Пункт присвоения названии армии
    contentHTML += `
        <div>
            <span>Введите название армии:</span>
            <input id="new-army-name" value="default"></input>
        </div>
    `;
    // Начало выбора местораположения армии
    contentHTML += `
        <div>
            <span>Выберете месторасположение армии:</span>
            <select id="new-army-location">
    `;
    // Цикл добавления поселения для выбора стартовой локации
    for (i=0; i<statusGameDictPlayer["our_settlements"].length; i++) {
        contentHTML += `
            <option value="train" name="1">
                Поселение с ид: ${statusGameDictPlayer["our_settlements"][i]}
            </option>
        `;

    }
    // Конец выбора местораположения армии
    contentHTML += `

            </select>
        </div>`
    // Конец контента модального окна
    contentHTML += `
        </div>
    `
    content.innerHTML = contentHTML
    console.log("Сформировать армию.");
    statusGame.acts.push([`Сформировать армию..`, 403, arg]); 
    // postAct(statusGame.game_id);
    logStart();

};


// Строительство 
// Модалка для строительства
document.getElementById('menu-new-building').addEventListener('click', () => {
    menuNewBuilding();
});


// Новая фукнция для строительства при управлении несолькими локациями.
function menuNewBuilding(settlement) {
    hiddenAllMenu();  // Скроем все меню
    // chooseList.innerHTML = `<span>Пока что здесь пусто</span>`;  // Добавим подсказку
    modal.style.display = "block";
    let content = document.getElementById("show-content");  // <div>Сделать пожертвование.</div>
    content.innerHTML = `
        <div style="font-size: 20px">
            <div>Строительство</div>
    `;

    console.table(`Поселение ${settlement["name_rus"]}`)
    console.log(`Доступные постройки0 ${settlement["available_buildings"]}`)
    // console.log(`Доступные постройки1 ${statusBuildings[1]}`)
    settlement["available_buildings"].forEach((build, num) => {
        // console.log(`Доступная постройка ${build}`);
        let cost = settlement["buildings_cost"][build];
        // console.log(`Ее стоимость: ${cost}`);
        let description = settlement["buildings_description"][build];
        // console.log(`Описание: ${description}`);
        // console.log(`Ид поселения: ${settlement["row_id"]}`);
        let id = String(settlement["row_id"])
        content.insertAdjacentHTML('beforeend', `
            <div class="wrapper" style="border: solid; margin-top: 5px;">
                <div>
                    <img src="../static/image/buildings/${settlement["buildings_icon_name"][build]}" alt="Картинки нет, сорян" width = 50px> 
                </div>
                <button id='build1-${num}'>Построить</button>
                <div> 
                    <div>${build}.</div> 
                    <div>Стоимость: ${cost}.</div> 
                    <div>${description}</div> 
                </div>
            </div>`
        )
        document.getElementById(`build1-${num}`).addEventListener(('click'), () => {
            console.log("Вешаем событие постройки.")
            build111(build, id);
        });
    })
    content.insertAdjacentHTML('beforeend', `
                <div style="font-size: 20px">
                    <button onclick = closeModal() style="font-size: 25px; margin-top: 20px">Отмена</button>
                </div>
            </div>`
    )
    console.log("Модалка открыта");
}


// Вызываем эту фукнцию из создаваемой кнопки в html
function build111(build, settl_id){
    console.log(`Строим: ${build}.`);
    statusGame.acts.push([`Строим: ${build}`, 101, build, settl_id]) 
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
    console.log(`Запрос статистики игроков. id партии ${statusGame.game_id}`)
    const request = new XMLHttpRequest();
    request.open("GET", `/req_status_all_player?gameId=${statusGame.game_id}`);
    request.addEventListener('load', () => {
        // console.log("Xmmm")
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
    // console.log("Запуск функции отображения готовности игроков.");
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