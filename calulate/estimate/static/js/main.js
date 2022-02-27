// fileref.setAttribute ("type", "text/javascript")
console.log('hello word')
//
const url = window.location.href // Получили IP текущей страницы
const searchForm = document.getElementById('search_work') // определили константу - форму по ID
const searchInputWork = document.getElementById('search_field_work')  // поле для поиска
const resultsBoxWork = document.getElementById('results-box-work')   // поле результата поиска
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value // определили константу - csrf токен
console.log(csrf)



const sendSearchData = (work) => { // Обьявляем сонстанту work то что пришло (значение поля input)
    $.ajax({  // в ней ajax вызов
        type: 'POST',
        url: '/estimate/search/work/',
        data: {
            'csrfmiddlewaretoken': csrf, // токен
            'work': work, // Значение из поля input
        },
        success: (result)=> { // В случае успеха 
            console.log(result.data) // Выводим в консоль responce (ответ)
            const data = result.data // Новая константа с данными ответа
            if (Array.isArray(data)) { // Если data это массив
                console.log('we have an array') // Выводим в консоль что это массив
                resultsBoxWork.innerHTML = "" // Присваиваем div пустоту
                var scroll = $(window).scrollTop()
                //console.log(scroll)
                data.forEach(work=> { // добавляем в div результаты
                    resultsBoxWork.innerHTML += `
                        <a href="addwork/${work.pk}/?scroll=${scroll}" class="item">
                            <div class="row mt-2 mb-2">
                                <div class="col-10">
                                    ${work.name}
                                </div>
                            </div>
                        </a>
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

searchInputWork.addEventListener('keyup', e=>{ // Обработчик события, при отпускании (keyup) клавиши...
    console.log(e.target.value) // Выводим зансчение в консоль

    if (resultsBoxWork.classList.contains('not-visible')){ // Если у resultsBoxWork (блок div) есть класс 'not-visible'
        resultsBoxWork.classList.remove('not-visible') // Удаляем его нахрен (становится видимым)
    }

    sendSearchData(e.target.value) // И передаем в функцию sendSearchData значение поля searchInput
})