import networkx as nx
import matplotlib.pyplot as plt
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import json


def draw_social_graph(actor_name):

    engine = create_engine(f"mysql+pymysql://root:password@localhost:3306/kinorium")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    session = session()

    # Создаем пустой граф
    G = nx.Graph()

    # Получаем id актера по его имени
    query = text("SELECT id_actor FROM actor WHERE name = :actor_name")
    result = session.execute(query, params={"actor_name": actor_name})
    actor_id = result.fetchone()[0]

    # Получаем список фильмов, в которых снимался актер
    query = text("SELECT id_film FROM actor WHERE id_actor = :actor_id")
    result = session.execute(query, params={"actor_id": actor_id})
    films_temp = [row[0] for row in result.fetchall()]
    films = []
    json_str = films_temp[0]  # Get the string from the list
    temp_list = json.loads(json_str)  # Parse the JSON string
    for item in temp_list:  # Only take the first 3 items
        number = item[0]
        number = number.replace("[", "")
        number = number.replace("]", "")
        films.append([int(number)])


    # Добавляем актера в граф
    G.add_node(actor_name)

    # Добавляем всех актеров, снимавшихся с данным актером в фильмах, в граф
    for film in films:
        query = text("SELECT name FROM actor WHERE id_film = :film_id")
        result = session.execute(query, params={"film_id": film})
        actors = [row[0] for row in result.fetchall()]
        G.add_edges_from([(actor_name, actor) for actor in actors])

    # Отрисовываем граф
    nx.draw(G, with_labels=True)
    plt.show()
    #plt.savefig('C:/Users/1/Desktop/hfg.png')

