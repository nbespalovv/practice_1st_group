from typing import Any, Tuple, Union

import networkx as nx
from matplotlib import pyplot as plt

from tg.db import BotDB

Vertex = Any
Edge = Tuple[Vertex, Vertex]
Num = Union[int, float]

DB = BotDB()


class ActorDTO:
    def __init__(self, actor_id, name, coworkers: list, films: list) -> None:
        self.actor_id = actor_id
        self.name = name
        self.coworkers = coworkers
        self.films = films

    def __str__(self) -> str:
        return f'{self.name}'


used_actors = []  # список посещенных актеров для обхода


# Обход полученного графа(списка) актеров в глубину
def DFS(actor: ActorDTO, graph: list[tuple]) -> list[tuple]:
    if actor in used_actors:
        return []
    used_actors.append(actor)
    for coworker in actor.coworkers:
        graph.append((actor, coworker))
        DFS(coworker, graph)
    return graph


# Парсит актеров из бд
def parse_actors(actors_db) -> list[ActorDTO]:
    actors = dict[int, ActorDTO]()
    film_actors = dict[int, list[ActorDTO]]()
    for actor_db in actors_db:
        films = [int(x[0]) for x in actor_db.id_film]
        actor = ActorDTO(actor_db.id_actor, actor_db.name, [], films)
        for film in films:
            if film_actors.get(film) is None:
                film_actors[film] = []
            film_actors[film].append(actor)
        actors[actor.actor_id] = actor

    for actor in actors.values():
        for film in actor.films:
            film_employees = film_actors[film]
            for employee in film_employees:
                if employee.actor_id == actor.actor_id:
                    continue
                actor.coworkers.append(actors[employee.actor_id])

    return list(actors.values())


def get_all_actors() -> list:
    return DB.get_actors()


def get_actor_by_name_and_coworkers(name: str):
    actors = []
    actor = DB.get_actor(name)
    actors.append(actor)
    for film in actor.id_film:
        coworkers = DB.get_actors_by_film(film[0])
        actors.extend(coworkers)

    return actors


if __name__ == '__main__':
    actors_from_db = get_actor_by_name_and_coworkers('Евгений Шварц')  # получаем объекты актеров из бд
    actors = parse_actors(actors_from_db)  # парсим
    data = DFS(actors[0], [])  # обходим список актеров в глубину

    G = nx.Graph(data)  # пихаем всё в граф для отрисовки

    fig = plt.figure(figsize=(100, 100), dpi=100)
    position = nx.spring_layout(G, k=0.5, iterations=30)
    nx.draw(G, pos=position, node_color='yellow', edge_color='black', font_size=30, font_color='black',
            with_labels=True)
    plt.savefig(
        '../../graph.png')  # картиночка
