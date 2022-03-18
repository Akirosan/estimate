// Ajax поиск элементов с добавлением в смету

const url = window.location.href // Получили IP текущей страницы
const searchForm = document.getElementById('search_work') // определили константу - форму по ID
const searchInputWork = document.getElementById('search_field_work')  // поле для поиска
const resultsBoxWork = document.getElementById('results-box-work')   // поле результата поиска
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value // определили константу - csrf токен
const listWork = document.getElementById('list-work') // Список видов работ


const sendSearchData = (work) => { // Обьявляем константу work то что пришло (значение поля input)
    $.ajax({  // в ней ajax вызов
        type: 'POST',
        url: '/estimate/search/work/',
        data: {
            'csrfmiddlewaretoken': csrf, // токен
            'work': work, // Значение из поля input
        },
        success: (result)=> { // В случае успеха 
            const data = result.data // Новая константа с данными ответа
            if (Array.isArray(data)) { // Если data это массив
                resultsBoxWork.innerHTML = "" // Присваиваем div пустоту
                // var scroll = $(window).scrollTop() // Записваем в переменную значение скролла
                data.forEach(work=> { // добавляем в div результаты / forEach выполняет функцию для каждого элемента массива data
                    resultsBoxWork.innerHTML += `
                        <div class="item" onclick="addWorkToCalc(${work.pk})" style="cursor: pointer;">
                            <div class="row mt-2 mb-2">
                                <div class="col-10">
                                    ${work.name}
                                </div>
                            </div>
                        </div>
                    `
                }) //<a href="addwork/${work.pk}/?scroll=${scroll}">
            } else { // Если data не массив, то
                if (searchInputWork.value.length > 0) { // Если длинна вводимого значения  болше 0
                    resultsBoxWork.innerHTML = `<b>${data}</b>` // Вставляем в resultBox
                } else {
                    resultsBoxWork.classList.add('not-visible')
                }
            }
        },
        error: (err)=>{ // при ошибке
            console.log(err)  // Выводим в консоль сообщение
        }
    })
}

searchInputWork.addEventListener('keyup', e=>{ // Обработчик события, при отпускании (keyup) клавиши...
    if (resultsBoxWork.classList.contains('not-visible')){ // Если у resultsBoxWork (блок div) есть класс 'not-visible'
        resultsBoxWork.classList.remove('not-visible') // Удаляем его нахрен (становится видимым)
    }
    sendSearchData(e.target.value) // И передаем в функцию sendSearchData значение поля searchInput
})


function addWorkToCalc(work_pk) {
    $.ajax({
        type: 'POST',
        url: 'calc/addwork/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'work_pk': work_pk,
        },
        success: (result)=> {
            console.log(result.calc_id)
            viewListWork(result.calc_id)
        },
        error: (err)=>{
            console.log(err)
        }
    })
}

// Скрывает выпадающий список при клике на любое место
document.addEventListener('click', e => {
    resultsBoxWork.classList.add('not-visible')
})


function viewListWork(calc_id){ // Выводит текущий список работ
    $.ajax({  // в ней ajax вызов
        type: 'POST',
        url: '/estimate/work/viewlist/',
        data: {
            'csrfmiddlewaretoken': csrf, // токен
            'calc_id': calc_id, // Значение из поля input
        },
        success: (result)=> { // В случае успеха 
            const data = result.data // Новая константа с данными ответа
           
            if (Array.isArray(data)) { // Если data это массив
                listWork.innerHTML = "" // Присваиваем div пустоту
                let counter = 0
                data.forEach(work=> { // добавляем в div результаты / forEach выполняет функцию для каждого элемента массива data
                    counter +=1
                    listWork.innerHTML += `
                        <tr>
                            <th scope="row">${counter}</th>
                            <td><a href="#">${work.name}</a></td>
                            <td>${work.measurement_unit}</td>
                            <td><input id="workPrice_${counter}" class="listWorkElement" size="8" maxlength="10" name="work_price_${work.pk}" type="text" value=${work.price}></td>
                            <td><input id="workQuant_${counter}" class="listWorkElement" size="8" maxlength="10" name="work_quant_${work.pk}" type="text" value=${work.quantity}></td>
                            <td id="workAmount_${counter}"></td>
                            <td></td>
                            <td></td>
                            <td><a href="#">удалить</a></td>
                        </tr>
                    `
                })
            } else { // Если data не массив, то
                if (searchInputWork.value.length > 0) { // Если длинна вводимого значения  болше 0
                    resultsBoxWork.innerHTML = `<b>${data}</b>` // Вставляем в resultBox
                } else {
                    resultsBoxWork.classList.add('not-visible')
                }
            }
        },
        error: (err)=>{ // при ошибке
            console.log(err)  // Выводим в консоль сообщение
        }
    })


}
viewListWork('3')





// Калькуляция сумм всех добавленных элементов

document.addEventListener('keyup', e => { // Слушаем весь документ на предмет изменения цены или колличества
    if (e.target.matches('input[class="matElement"]')) { // Если событие произошло на input ...
        let id = e.target.id.slice(9) // Отделяем id либо от цены либо от количества
        summElements('mat', id)
        summAllElemrnts()
    } 
    if (e.target.matches('input[class="listWorkElement"]')) { // Если событие произошло на input ...
        let id = e.target.id.slice(10) // Отделяем id либо от цены либо от количества
        summElements('work', id)
        summAllElemrnts()
    }
    
  });



function summElements(type_element, id) { // Калькуляция отдельного элемента
    if(!document.querySelector(`[id="${type_element}Price_${id}"]`)) { return false }; // Проверяем наличие
    
    let price = document.querySelector(`[id="${type_element}Price_${id}"]`).value;
    
    if(!document.querySelector(`[id="${type_element}Quant_${id}"]`).value) { console.log('no elements') } ;
    let quaantity = document.querySelector(`[id="${type_element}Quant_${id}"]`).value;
    let summ = +price * +quaantity
    if (summ == undefined) {
        return(False)
    }
    console.log(summ)
    document.getElementById(`${type_element}Amount_${id}`).innerHTML = summ;
    return true
}



function primaryCalculation(){ // Калькуляция всех элементов при первичной загрузке страницы
    for(num=1; num<100; num++) {
        if(!summElements('work', num)) { break }
    }
    for(num=1; num<100; num++) {
        if(!summElements('mat', num)) { break }
    }
}


function summAllElemrnts(){ // Итоговое Суммирование 
    let summ_work = 0
    for(num=1; num<100; ++num) {
        if(!document.getElementById(`workAmount_${num}`)) { break }
        let summand = document.getElementById(`workAmount_${num}`).textContent
        summ_work += +summand
    }
    document.getElementById("work_summ").innerHTML = '<strong>' + summ_work.toFixed(1) + '</strong>';

    let summ_mat = 0
    for(num=1; num<100; ++num) {
        if(!document.getElementById(`matAmount_${num}`)) { break }
        let summand = document.getElementById(`matAmount_${num}`).textContent
        summ_mat += +summand
    }
    document.getElementById("mat_summ").innerHTML = '<strong>' + summ_mat.toFixed(1) + '</strong>';
    
}

primaryCalculation() // Первичное вычисление суммы каждого элемента
summAllElemrnts() // Первичное суммирование всех элементов