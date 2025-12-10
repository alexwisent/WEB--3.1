function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function (data) {
        return data.json();
    })
    .then(function (films) {
        let tbody = document.getElementById('film-list');  
        tbody.innerHTML = '';
        for(let i = 0; i < films.length; i++) {
            let tr = document.createElement('tr');

            let tdTitle = document.createElement('td');
            let tdTitleRus = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');

            tdTitle.innerText = films[i].title == films[i].title_ru ? '' : films[i].title; 
            tdTitleRus.innerText = films[i].title_ru;
            tdYear.innerText = films[i].year;   

            let editButton = document.createElement('button'); 
            editButton.innerText = 'редактировать';
            editButton.onclick = function() {
                editFilm(i);
            };

            let delButton = document.createElement('button'); 
            delButton.innerText = 'удалить';
            delButton.onclick = function() {
                deleteFilm(i, films[i].title_ru);
            };

            tdActions.append(editButton);
            tdActions.append(delButton);

            tr.append(tdTitle);
            tr.append(tdTitleRus);
            tr.append(tdYear);
            tr.append(tdActions);

            tbody.append(tr);
        }
    })
    .catch(function(error) {
        console.error('Ошибка при загрузке фильмов:', error);
    });
}

function deleteFilm(id, title) {
    if(! confirm(`Вы точно хотите удалить фильм "${title}"?`)) {
        return;
    }

    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
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

function showModal() {
    document.querySelector('div.modal').style.display ='block';
}

function hideModal() {
    document.querySelector('div.modal').style.display ='none';
}

function cancel() {
    hideModal();
}


function addFilm() { 
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = ''; 
    document.getElementById('description').value = '';
    showModal();
}

function sendFilm() {
    const id = document.getElementById('id').value;
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
    
    const url = `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';

    fetch(url, {
        method: method,
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(film)
    })
    .then(function(response) {
        if (response.ok) {
            fillFilmList();
            hideModal();
            return {};
        } 
        return response.json();
    })
    .then(function(errors){ 
        if(errors.description) 
            document.getElementById('description-error').innerText = errors.description;
    });
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function (data) {
        return data.json();
    })
    .then(function (film) {
        document.getElementById('id').value = id;
        document.getElementById('title').value = film.title;
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