function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function (data) {
        return data.json();
    })
    .then(function (films) {
        let tbody = document.getElementById('film-list');  // getElementById, а не getElementBy
        tbody.innerHTML = '';
        for(let i = 0; i < films.length; i++) {
            let tr = document.createElement('tr');

            let tdTitle = document.createElement('td');
            let tdTitleRus = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');

            // Исправлены опечатки:
            tdTitle.innerText = films[i].title == films[i].title_ru ? '' : films[i].title;  // .title, а не .titl
            tdTitleRus.innerText = films[i].title_ru;
            tdYear.innerText = films[i].year;  // .year, а не .vear

            let editButton = document.createElement('button'); 
            editButton.innerText = 'редактировать';
            editButton.onclick = function() {
                editFilm(i);  // Добавьте обработчик
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
    if (!confirm('Вы точно хотите удалить фильм "' + title + '"?')) {
        return;
    }
    fetch('/lab7/rest-api/films/' + id, {method: 'DELETE'})
        .then(function() {
            fillFilmList(); // Обновляем список после удаления
        })
        .catch(function(error) {
            console.error('Ошибка при удалении:', error);
        });
}

function editFilm(id) {
    // Пока заглушка - нужно реализовать
    alert('Редактирование фильма ' + id);
}

function addFilm() {
    // Пока заглушка - нужно реализовать
    alert('Добавление нового фильма');
}