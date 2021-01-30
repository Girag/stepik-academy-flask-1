from flask import Flask, render_template, abort
import data

app = Flask(__name__)


@app.errorhandler(404)
def render_not_found(_):
    return "Ничего не нашлось! Вот неудача, отправляйтесь на главную!", 404


@app.route("/")
def render_main():
    # return "Здесь будет главная"
    return render_template("index.html")


@app.route("/departures/")
@app.route("/departures/<departure>/")
def render_departures(departure=None):
    if not departure:
        return "Здесь будут направления"
    return render_template("departure.html", departure=departure)


@app.route("/tours/")
@app.route("/tours/<int:id>/")
def render_tours(id=None):
    if not id:
        return "Здесь будут туры"
    return render_template("tour.html", id=id)


@app.route("/data/")
def render_data():
    result = f"<h1>Все туры:</h1>\n\n"
    for i in range(1, len(data.tours) + 1):
        result += f"""<p>{data.tours[i]['country']}: <a href="/data/tours/{i}/">{data.tours[i]['title']} 
            {data.tours[i]['price']} {data.tours[i]['stars']}* </a></p>\n"""
    return result


@app.route("/data/departures/<departure>/")
def render_data_departures(departure):
    if departure in data.departures:
        result = f"<h1>Туры по направлению {data.departures[departure][0].lower()}" \
                 f"{data.departures[departure][1:]}:</h1>\n\n"

        for tour in data.tours:
            if data.tours[tour]['departure'] == departure:
                result += f"""<p>{data.tours[tour]['country']}: <a href = "/data/tours/{tour}/"> 
                    {data.tours[tour]['title']} {data.tours[tour]['price']} {data.tours[tour]['stars']}* </a></p>\n"""
        return result
    else:
        abort(404)


@app.route("/data/tours/<int:id>/")
def render_data_tours(id):
    if id in data.tours:
        result = f"""
        <h1>{data.tours[id]['country']}: {data.tours[id]['title']} {data.tours[id]['price']}:</h1>
        <p>{data.tours[id]['nights']} ночей</p>
        <p>Стоимость: {data.tours[id]['price']} ₽</p>
        <p>{data.tours[id]['description']}</p>
        """
        return result
    else:
        abort(404)


app.run(debug=True)
