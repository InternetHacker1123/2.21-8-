import click
import json
import os.path
import sqlite3


def add_train(rasp, punkt, number, time):
    """
    Добавить данные о поезде.
    """
    rasp.append(
        {
            "punkt": punkt,
            "number": number,
            "time": time
        }
    )
    return rasp


def display_train(rasp):
    """
    Отобразить список поездов.
    """
    if rasp:
        line = '+-{}-+-{}-+-{}-+'.format(
            '-' * 30,
            '-' * 20,
            '-' * 8
        )
        click.echo(line)
        click.echo(
            '| {:^30} | {:^20} | {:^8} |'.format(
                "Пункт назначения",
                "Номер поезда",
                "Время отправления"
            )
        )
        click.echo(line)
        for train in rasp:
            click.echo(
                '| {:<30} | {:<20} | {:>8} |'.format(
                    train.get('punkt', ''),
                    train.get('number', ''),
                    train.get('time', '')
                )
            )
            click.echo(line)
    else:
        click.echo("Расписание пусто.")


def select_trains(rasp, number):
    result = []
    for train in rasp:
        if number in train.values():
            result.append(train)
    return result


def save_trains(file_name, rasp):
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(rasp, fout, ensure_ascii=False, indent=4)


def load_trains(file_name):
    if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
        with open(file_name, "r", encoding="utf-8") as fin:
            return json.load(fin)
    else:
        return []


def create_tables():
    conn = sqlite3.connect('trains.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS Trains
                 (id INTEGER PRIMARY KEY,
                 punkt TEXT NOT NULL,
                 number TEXT NOT NULL,
                 time TEXT NOT NULL)''')

    conn.commit()
    conn.close()


def add_train_to_db(punkt, number, time):
    conn = sqlite3.connect('trains.db')
    c = conn.cursor()
    c.execute("INSERT INTO Trains (punkt, number, time) VALUES (?, ?, ?)",
              (punkt, number, time))
    conn.commit()
    conn.close()


def display_trains_from_db():
    conn = sqlite3.connect('trains.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Trains")
    rows = c.fetchall()
    conn.close()

    for row in rows:
        print(row)


@click.command()
@click.argument("filename", required=True)
@click.option("--punkt", help="Название пункта назначения")
@click.option("--number", help="Номер поезда")
@click.option("--time", help="Время отправления")
@click.option("--number_train", help="Искомый номер поезда")
def main(filename, punkt, number, time, number_train):
    rasp = load_trains(filename)

    if punkt and number and time:
        add_train_to_db(punkt, number, time)
        rasp = add_train(rasp, punkt, number, time)
        save_trains(filename, rasp)
    elif number_train:
        selected = select_trains(rasp, number_train)
        display_train(selected)
    else:
        display_trains_from_db()


if __name__ == "__main__":
    create_tables()
    main()
