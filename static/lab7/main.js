function fillFilmList() {       // Функция для заполнения таблицы со списком фильмов
    fetch('/lab7/rest-api/films/')      // Отправляем GET-запрос на сервер для получения списка фильмов
    .then(function (data) {
        return data.json();     // Преобразуем ответ в JSON
    })
    .then(function (films) {
        let tbody = document.getElementById('film-list');   // Находим тело таблицы
        tbody.innerHTML = '';    // Очищаем текущее содержимое
        for(let i = 0; i < films.length; i++) {         // Перебираем все полученные фильмы
            let tr = document.createElement('tr');      // Создаем строку таблицы

            // Создаем ячейки для каждого поля фильма
            let tdTitle = document.createElement('td');     // Оригинальное название
            let tdTitleRus = document.createElement('td');  // Русское название
            let tdYear = document.createElement('td');      // Год выпуска
            let tdActions = document.createElement('td');   // Описание

            // Заполняем ячейки данными из объекта фильма
            tdTitle.innerText = films[i].title;      // Оригинальное название
            tdTitleRus.innerText = films[i].title_ru; // Русское название
            tdYear.innerText = films[i].year || '';   // Год (или пустая строка)

            let editButton = document.createElement('button');      // Создаем кнопку "редактировать"
            editButton.innerText = 'редактировать';
            editButton.onclick = function() {
                editFilm(films[i].id);      // Используем ID из БД, а не индекс массива
            };

            let delButton = document.createElement('button');   // Создаем кнопку "удалить"
            delButton.innerText = 'удалить';
            delButton.onclick = function() {
                deleteFilm(films[i].id, films[i].title_ru);  // Передаем ID и название для подтверждения
            };
            
            // Добавляем кнопки в ячейку действий
            tdActions.append(editButton);       
            tdActions.append(delButton);

            // Добавляем ячейки в строку таблицы
            tr.append(tdTitleRus);  // Русское название
            tr.append(tdTitle);     // Оригинальное название
            tr.append(tdYear);      // Год
            tr.append(tdActions);   // Описание

            tbody.append(tr);       // Добавляем строку в таблицу
        }
    })
    .catch(function(error) {
        console.error('Ошибка при загрузке фильмов:', error);
    });
}

function deleteFilm(id, title) {        // Функция для удаления фильма
    if(! confirm(`Вы точно хотите удалить фильм "${title}"?`)) {        // Показываем диалог подтверждения удаления
        return;     // Если пользователь отменил, выходим из функции
    }

    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})     // Отправляем DELETE-запрос на сервер
        .then(function (response) {
            if (response.status === 204) {
                fillFilmList();  // Обновляем список после удаления
            } else if (response.status === 404) {
                alert('Фильм не найден');
            } else {
                console.error('Ошибка при удалении:', response.status);
                alert('Ошибка при удалении фильма');
            }
        })
        .catch(function(error) {
            console.error('Ошибка при удалении:', error);
            alert('Ошибка сети при удалении фильма');
        });
}

function showModal() {      // Функция для показа модального окна
    document.querySelector('div.modal').style.display ='block';
}

function hideModal() {      // Функция для скрытия модального окна
    document.querySelector('div.modal').style.display ='none';
}

function cancel() {     // Функция для отмены действия и закрытия модального окна
    hideModal();
}


function addFilm() {    // Функция для подготовки формы к добавлению нового фильма
    document.getElementById('id').value = '';           // Очищаем скрытое поле ID
    document.getElementById('title').value = '';        // Очищаем поле оригинального названия
    document.getElementById('title-ru').value = '';     // Очищаем поле русского названия
    document.getElementById('year').value = '';         // Очищаем поле года
    document.getElementById('description').value = '';  // Очищаем поле описания
    showModal();        // Показываем модальное окно
}

function sendFilm() {       // Функция для отправки данных фильма на сервер. Отправляет POST-запрос для создания или PUT-запрос для обновления фильма
    const id = document.getElementById('id').value;     // Получаем значения из формы
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: document.getElementById('year').value,
        description: document.getElementById('description').value
    };
    
    document.getElementById('description-error').innerText = '';    // Очищаем предыдущие ошибки
    
    if (!film.title_ru.trim()) {        // Проверка обязательных полей
        alert('Введите русское название фильма');
        return;
    }
    if (!film.year) {
        alert('Введите год выпуска фильма');
        return;
    }
    
    if (!film.title.trim() && film.title_ru.trim()) {       // Логика: если оригинальное название пустое, используем русское
        film.title = film.title_ru;
        document.getElementById('title').value = film.title;    // Также обновляем значение в поле ввода, чтобы пользователь видел
    }

    const url = id === '' ? '/lab7/rest-api/films/' : `/lab7/rest-api/films/${id}`;     // Определяем URL и метод HTTP в зависимости от того, редактируем или добавляем
    const method = id === '' ? 'POST' : 'PUT';

    fetch(url, {        // Отправляем запрос на сервер
        method: method,
        headers: {"Content-Type": "application/json"},      // Указываем тип содержимого
        body: JSON.stringify(film)      // Преобразуем объект в JSON-строку
    })
    .then(function(response) {      // Обрабатываем ответ сервера. Если успешно, обновляем список фильмов и скрываем модальное окно
        if (response.ok) {
            fillFilmList();
            hideModal();
            return {};
        } 
        return response.json();
    })
    .then(function(errors){         // Обрабатываем ошибки валидации с сервера
        if (errors) {
            let errorMessages = [];
            if (errors.title) errorMessages.push(errors.title);
            if (errors.title_ru) errorMessages.push(errors.title_ru);
            if (errors.year) errorMessages.push(errors.year);
            if (errors.description) errorMessages.push(errors.description);
            
            if (errorMessages.length > 0) {     // Если есть ошибки, показываем их в алерте
                alert('Ошибки:\n' + errorMessages.join('\n'));
            }
        }
    });
}

function editFilm(id) {     // Функция для загрузки данных фильма для редактирования
    fetch(`/lab7/rest-api/films/${id}`)     // Отправляем GET-запрос для получения данных фильма
    .then(function (data) {
        return data.json();
    })
    .then(function (film) {     // Заполняем форму данными фильма
        document.getElementById('id').value = id;       // Заполняем скрытое поле ID
        
        document.getElementById('title').value = film.title || film.title_ru;       // Если оригинальное название отсутствует, используем русское
        document.getElementById('title-ru').value = film.title_ru;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;

        document.getElementById('description-error').innerText = '';    // Очищаем ошибку при редактировании

        showModal();
    })
    .catch(function(error) {
        console.error('Ошибка при загрузке фильма:', error);
        alert('Ошибка при загрузке фильма');
    });
}

document.addEventListener('DOMContentLoaded', function() {      // Загружаем список фильмов при загрузке страницы
    fillFilmList();
});