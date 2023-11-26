import os
import sys
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk
from Tyradex import get_all_pokemons

from src import Pokedex_Manager
from utils import get_path


class PokemonApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Pokémon Manager")

        # Fixer la taille de la fenêtre
        self.master.geometry("957x683")
        self.master.resizable(False, False)
        # self.master.iconbitmap(get_path() + 'libs/imgs/logo.ico')

        self.__lasted = None

        # Empêcher le redimensionnement de la fenêtre

        # Appeler get_all_pokemons une seule fois et stocker les résultats dans une variable
        self.all_pokemons = get_all_pokemons()
        self.pokedex_manager = Pokedex_Manager()

        # Liste déroulante pour sélectionner la méthode
        self.selection_type = ttk.Combobox(master, values=["Seen", "Have", "Shiny"], state="readonly")
        self.selection_type.grid(row=1, column=5)
        self.selection_type.set("Seen")  # Définir une valeur par défaut
        self.selection_type.bind("<<ComboboxSelected>>", self.show_selected_pokemon)

        # Liste déroulante pour sélectionner un Pokémon
        self.pokemon_list = ttk.Combobox(master, values=self.all_pokemons, state="readonly")
        self.pokemon_list.grid(row=1, column=1)
        self.pokemon_list.set(self.all_pokemons[1])  # Définir une valeur par défaut
        self.pokemon_list.bind("<<ComboboxSelected>>", self.show_selected_pokemon)

        # Nom du Pokémon
        self.pokemon_name_label = tk.Label(master, text="")
        self.pokemon_name_label.grid(row=1, column=3)

        # État actuel du sprite (normal ou shiny)
        self.current_sprite_is_shiny = False

        # Sprite du Pokémon
        self.pokemon_sprite = tk.Canvas(master, bd=0, highlightthickness=0)
        self.pokemon_sprite.grid(row=2, column=3)
        self.pokemon_sprite.bind("<Button-1>", self.toggle_sprite_state)

        # Image "checker"
        self.checker_image = tk.Canvas(master, bd=0, highlightthickness=0)
        self.checker_image.grid(row=3, column=3)

        # Chemins vers les images
        self.prev_image_path = get_path() + "libs/imgs/Precedent.png"
        self.next_image_path = get_path() + "libs/imgs/Suivant.png"
        self.attrape_image_path = get_path() + "libs/imgs/Attrape.png"
        self.perd_image_path = get_path() + "libs/imgs/Perd.png"

        # Image cliquable "Précédent"
        self.prev_image = Image.open(self.prev_image_path)
        self.prev_image = self.prev_image.resize((30, 300), Image.LANCZOS)
        self.prev_image_tk = ImageTk.PhotoImage(self.prev_image)
        self.prev_button = tk.Canvas(master, width=30, height=300, bd=0, highlightthickness=0)
        self.prev_button.grid(row=2, column=1)
        self.prev_button.create_image(0, 0, anchor=tk.NW, image=self.prev_image_tk)
        self.prev_button.bind("<Button-1>", self.show_previous_pokemon)

        # Image cliquable "Suivant"
        self.next_image = Image.open(self.next_image_path)
        self.next_image = self.next_image.resize((30, 300), Image.LANCZOS)
        self.next_image_tk = ImageTk.PhotoImage(self.next_image)
        self.next_button = tk.Canvas(master, width=30, height=300, bd=0, highlightthickness=0)
        self.next_button.grid(row=2, column=5)
        self.next_button.create_image(0, 0, anchor=tk.NW, image=self.next_image_tk)
        self.next_button.bind("<Button-1>", self.show_next_pokemon)

        # Associer les touches du clavier aux fonctions correspondantes
        self.master.bind("<Left>", lambda event: self.show_previous_pokemon())
        self.master.bind("<Right>", lambda event: self.show_next_pokemon())

        # Associer la touche Entrée au bouton "J'ai"
        self.master.bind("<Return>", lambda event: self.mark_as_have())

        # Associer la touche "Backspace" au bouton "J'ai plus"
        self.master.bind("<BackSpace>", lambda event: self.mark_as_have_not())

        # Bouton "J'ai"
        attrape_image = Image.open(self.attrape_image_path)
        # attrape_image = attrape_image.resize((50, 50), Image.LANCZOS)
        self.attrape_image_tk = ImageTk.PhotoImage(attrape_image)

        self.attrape_button = tk.Button(master, image=self.attrape_image_tk, command=self.mark_as_have)
        self.attrape_button.grid(row=3, column=2)

        # Bouton "J'ai plus"
        perd_image = Image.open(self.perd_image_path)
        # perd_image = perd_image.resize((50, 50), Image.LANCZOS)
        self.perd_image_tk = ImageTk.PhotoImage(perd_image)

        self.perd_button = tk.Button(master, image=self.perd_image_tk, command=self.mark_as_have_not)
        self.perd_button.grid(row=3, column=4)

        # Initialiser la première vue
        self.current_pokemon_index = 1
        self.show_current_pokemon()

    def get_all_pokemon_ids(self):
        return [str(pokemon.pokedex_id) for pokemon in self.all_pokemons]

    def show_selected_pokemon(self, event):
        # Fonction appelée lorsqu'un Pokémon est sélectionné dans la liste déroulante
        self.show_current_pokemon()

    def toggle_sprite_state(self, event):
        # Fonction appelée lorsqu'on clique sur le sprite du Pokémon pour basculer entre normal et shiny
        self.current_sprite_is_shiny = not self.current_sprite_is_shiny
        if self.current_sprite_is_shiny:
            self.__lasted = self.selection_type.get()
            self.selection_type.set("Shiny")
        else:
            self.selection_type.set(self.__lasted)
        self.show_current_pokemon()

    def show_current_pokemon(self):
        selected_pokemon_name = self.pokemon_list.get()
        selected_pokemon = next((pokemon for pokemon in self.all_pokemons if str(pokemon) == selected_pokemon_name), None)

        if selected_pokemon:
            # Afficher les détails du Pokémon actuel
            formatted_name = f"#{selected_pokemon.pokedex_id:04} {selected_pokemon}"
            self.pokemon_name_label.config(text=formatted_name, font=("Helvetica", 24, "bold"))
            # Ajoutez la logique pour afficher le sprite du Pokémon

            # Charger le chemin du sprite en fonction de l'état actuel
            sprite_folder = "shiny" if self.current_sprite_is_shiny else "regular"
            sprite_path = get_path() + f".cache/sprites/{sprite_folder}/"
            if self.current_sprite_is_shiny and f"{selected_pokemon.pokedex_id:04}.jpg" not in os.listdir(sprite_path):
                sprite_path = get_path() + f".cache/sprites/regular/"
            sprite_path += f"{selected_pokemon.pokedex_id:04}.jpg"

            # Charger l'image et afficher sur le Canvas
            sprite_image = Image.open(sprite_path)
            sprite_image_tk = ImageTk.PhotoImage(sprite_image)

            # Charger le chemin de l'image en fonction de l'état actuel
            image_path = (get_path() + f"libs/imgs/checks/"
                           f"{int(selected_pokemon.pokedex_id in self.pokedex_manager.Seen)}"
                           f"{int(selected_pokemon.pokedex_id in self.pokedex_manager.Have)}"
                           f"{int(selected_pokemon.pokedex_id in self.pokedex_manager.Shiny)}.png")

            # Charger l'image et afficher sur le Canvas
            checker_image = Image.open(image_path)
            checker_image_tk = ImageTk.PhotoImage(checker_image)

            # Mettre à jour l'image sur le Canvas
            self.checker_image.config(width=checker_image.width, height=checker_image.height)
            self.checker_image.create_image(0, 0, anchor=tk.NW, image=checker_image_tk)
            self.checker_image.image = checker_image_tk  # Conserver une référence pour éviter la suppression par le garbage collector


            # Mettre à jour l'image sur le Canvas
            self.pokemon_sprite.config(width=sprite_image.width, height=sprite_image.height)
            self.pokemon_sprite.create_image(0, 0, anchor=tk.NW, image=sprite_image_tk)
            self.pokemon_sprite.image = sprite_image_tk  # Conserver une référence pour éviter la suppression par le garbage collector

    def show_previous_pokemon(self, event=None):
        self.current_pokemon_index = (self.current_pokemon_index - 1) % len(self.all_pokemons)
        self.pokemon_list.set(self.all_pokemons[self.current_pokemon_index])
        self.show_current_pokemon()

    def show_next_pokemon(self, event=None):
        self.current_pokemon_index = (self.current_pokemon_index + 1) % len(self.all_pokemons)
        self.pokemon_list.set(self.all_pokemons[self.current_pokemon_index])
        self.show_current_pokemon()

    def mark_as_have(self):
        selected_type = self.selection_type.get()

        selected_pokemon_name = self.pokemon_list.get()
        selected_pokemon = next((pokemon for pokemon in self.all_pokemons if str(pokemon) == selected_pokemon_name), None)

        if selected_type is not None and selected_pokemon is not None:
            match selected_type:
                case "Seen":
                    self.pokedex_manager.Seen.add(selected_pokemon.pokedex_id)
                case "Have":
                    self.pokedex_manager.Have.add(selected_pokemon.pokedex_id)
                case "Shiny":
                    self.pokedex_manager.Shiny.add(selected_pokemon.pokedex_id)
        self.show_current_pokemon()

    def mark_as_have_not(self):
        selected_type = self.selection_type.get()

        selected_pokemon_name = self.pokemon_list.get()
        selected_pokemon = next((pokemon for pokemon in self.all_pokemons if str(pokemon) == selected_pokemon_name), None)

        if selected_type is not None and selected_pokemon is not None:
            match selected_type:
                case "Seen":
                    self.pokedex_manager.Seen.remove(selected_pokemon.pokedex_id)
                case "Have":
                    self.pokedex_manager.Have.remove(selected_pokemon.pokedex_id)
                case "Shiny":
                    self.pokedex_manager.Shiny.remove(selected_pokemon.pokedex_id)
        self.show_current_pokemon()

    def set_window_icon(self):
        icon_path = os.path.join(sys._MEIPASS, 'libs/imgs/logo.ico')
        if os.path.exists(icon_path):
            img = Image.open(icon_path)
            img = img.resize((32, 32), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            self.master.tk.call('wm', 'iconphoto', self.master._w, img)


if __name__ == "__main__":
    root = tk.Tk()
    app = PokemonApp(root)
    app.set_window_icon()
    root.mainloop()
