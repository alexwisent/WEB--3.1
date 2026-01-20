from flask import Blueprint, render_template, request

sessia = Blueprint('sessia', __name__, template_folder='templates')

@sessia.route("/sessia", methods=["GET", "POST"])
def sessia_index():
    result = None
    error = None

    if request.method == "POST":
        # Получаем числа из формы
        numbers = [request.form.get(f"num{i}") for i in range(1, 6)]

        # Проверка на пустые поля
        if any(n.strip() == "" for n in numbers):
            error = "Все поля должны быть заполнены!"
        else:
            try:
                # Преобразуем строки в числа
                numbers = [float(n) for n in numbers]
                # Сортируем по убыванию и берём два максимальных
                numbers_sorted = sorted(numbers, reverse=True)
                result = numbers_sorted[:2]
            except ValueError:
                error = "Все поля должны содержать только числа!"

    return render_template("sessia.html", result=result, error=error)