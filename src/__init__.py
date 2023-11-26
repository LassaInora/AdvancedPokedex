import json
import os
import pathlib

from Tyradex import Pokemon, get_all_pokemons

from utils import Singleton


class Pokedex_Manager(metaclass=Singleton):

    class Manage:
        def __init__(self, __data):
            self.__data = __data
            self.__cursor = 0

        def __str__(self):
            prct = round(float(self) * 100)
            return f"{'█'*prct}{'░'*(100 - prct)} {prct:3}% : {repr(self)}"

        def __repr__(self):
            return '{' + f"{int(self):4}/{str(len(self)):4}" + '}'

        def __bool__(self):
            return False in self.__data.values()

        def __contains__(self, item):
            return self.__data[str(item)]

        def __float__(self):
            return int(self) / len(self)

        def __getitem__(self, item):
            return self.__data[str(item)]

        def __int__(self):
            return list(self.__data.values()).count(True)

        def __iter__(self):
            self.__cursor = 0
            return self

        def __len__(self):
            return len(self.__data)

        def __invert__(self):
            return {id_: not value for id_, value in self.__data.items()}

        def __copy__(self):
            return Pokedex_Manager.Manage(self.__data)

        def __next__(self):
            try:
                cursor = self.__cursor
                self.__cursor += 1
                return self[cursor]
            except IndexError:
                raise StopIteration

        def __setitem__(self, key, value):
            if isinstance(value, bool):
                self.__data[str(key)] = value
            else:
                raise TypeError("Value can only be a boolean")

        def __eq__(self, __o):
            return self.__data == __o.__data if isinstance(__o, Pokedex_Manager.Manage) else False

        @property
        def pokedex_id_true(self):
            return [int(pokedex_id) for pokedex_id, is_true in self.__data.items() if is_true]

        @property
        def pokedex_id_false(self):
            return [int(pokedex_id) for pokedex_id, is_true in self.__data.items() if not is_true]

        def add(self, pokedex_id):
            self.__data[str(pokedex_id)] = True
            Pokedex_Manager().save()

        def remove(self, pokedex_id):
            self.__data[str(pokedex_id)] = False
            Pokedex_Manager().save()

        def init(self, pokedex_id):
            self.__data[str(pokedex_id)] = False
            Pokedex_Manager().save()

        @property
        def data(self):
            return {id_: value for id_, value in self.__data.items()}

    class _Data:
        def __init__(self, pokedex_id, seen, have, shiny):
            self.pokemon = Pokemon(pokedex_id)
            self._pokedex_id = pokedex_id

            self._Seen = seen
            self._Have = have
            self._Shiny = shiny

        def seen_true(self):
            self._Seen[self._pokedex_id] = True

        def seen_false(self):
            self._Seen[self._pokedex_id] = False

        def have_true(self):
            self._Have[self._pokedex_id] = True

        def have_false(self):
            self._Have[self._pokedex_id] = False

        def shiny_true(self):
            self._Shiny[self._pokedex_id] = True

        def shiny_false(self):
            self._Shiny[self._pokedex_id] = False

    def __init__(self):
        self.__data = self._load()
        self.__cursor = 0

        self.Seen = self.Manage(self.__data['seen'])
        self.Have = self.Manage(self.__data['have'])
        self.Shiny = self.Manage(self.__data['shiny'])

    def _load(self):
        path = pathlib.Path(os.getenv('APPDATA') + '/Pokemon Manager/collection/pokedex_data.json')
        try:
            return json.load(open(path, 'r'))
        except FileNotFoundError:
            parent = path.parent
            pile = []
            while not parent.exists():
                pile.insert(0, parent)
                parent = parent.parent
            while len(pile) != 0:
                doss = pile.pop(0)
                os.mkdir(doss)
            sub_data = {str(pok.pokedex_id): False for pok in get_all_pokemons()}
            data = {
                "seen": sub_data,
                "have": sub_data,
                "shiny": sub_data,
            }
            json.dump(data, open(path, 'w'), indent=2)
            return data

    def __bool__(self):
        return bool(self.Seen) and bool(self.Have) and bool(self.Shiny)

    def __float__(self):
        return (float(self.Seen) + float(self.Have) + float(self.Shiny)) / 3

    def __str__(self):
        return f"Seen : {str(self.Seen)}\nHave : {str(self.Have)}\nShiny: {str(self.Shiny)}"

    def __repr__(self):
        return '{' + f"{repr(self.Seen)}, {repr(self.Have)}, {repr(self.Shiny)}" + '}'

    def __getattr__(self, item):
        return self._Data(item, self.Seen, self.Have, self.Shiny)

    def __getitem__(self, item):
        return self._Data(item, self.Seen, self.Have, self.Shiny)

    def __iter__(self):
        self.__cursor = 0
        return self

    def __len__(self):
        return len(self.Seen)

    def __next__(self):
        try:
            cursor = self.__cursor
            self.__cursor += 1
            return self[cursor]
        except IndexError:
            raise StopIteration

    def __eq__(self, __o):
        return (
                self.Seen == __o.Seen and
                self.Have == __o.Have and
                self.Shiny == __o.Shiny
        ) if isinstance(__o, Pokedex_Manager) else False

    @property
    def data(self):
        return {
            'seen': self.Seen.data,
            'have': self.Have.data,
            'shiny': self.Shiny.data,
        }

    def save(self):
        json.dump(self.data, open(os.getenv('APPDATA') + '/Pokemon Manager/collection/pokedex_data.json', 'w'), indent=2)


if __name__ == '__main__':
    print(Pokedex_Manager())
