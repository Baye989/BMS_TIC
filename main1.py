import cv2
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

class BMS_IMG(App):
    def build(self):
        # Interface utilisateur
        layout = BoxLayout(orientation='vertical', spacing=10)

        # File Chooser pour sélectionner l'image
        file_chooser = FileChooserIconView()
        file_chooser.bind(selection=self.on_file_selection)
        layout.add_widget(file_chooser)

        # Bouton pour télécharger une image depuis le smartphone
        upload_button = Button(text='Télécharger une image', background_color=(0, 1, 0, 1))
        upload_button.bind(on_release=self.upload_image)
        layout.add_widget(upload_button)

        # TextInput pour la matrice de convolution
        self.matrix_input = TextInput(hint_text='Entrez la matrice de convolution (séparée par des virgules)')
        layout.add_widget(self.matrix_input)

        # Bouton pour appliquer la convolution
        process_button = Button(text='Appliquer la convolution', background_color=(0, 1, 0, 1))
        process_button.bind(on_release=self.process_image)
        layout.add_widget(process_button)

        # Widget d'image pour afficher le résultat
        self.image_widget = Image(allow_stretch=True)
        layout.add_widget(self.image_widget)

        # Bouton Sortir
        exit_button = Button(text='Sortir', size_hint=(1, None), height=40, background_color=(1, 0, 0, 1))
        exit_button.bind(on_release=self.exit_app)
        layout.add_widget(exit_button)

        return layout

    def on_file_selection(self, instance, selection):
        # Chargement de l'image sélectionnée
        if selection:
            self.image_path = selection[0]
            self.image_widget.source = self.image_path

    def upload_image(self, instance):
        # Ouvrir une fenêtre de sélection de fichier
        file_chooser = FileChooserIconView()
        file_chooser.bind(selection=self.on_file_selection)
        popup = Popup(title='Sélectionner une image', content=file_chooser, size_hint=(0.9, 0.9))
        popup.open()

    def process_image(self, instance):
        # Vérification de l'image sélectionnée
        if not hasattr(self, 'image_path'):
            self.show_popup('Erreur', 'Veuillez sélectionner une image.')
            return

        # Vérification de la matrice de convolution
        matrix_text = self.matrix_input.text
        try:
            rows = matrix_text.split(';')
            rows = [row.strip() for row in rows]
            matrix = []
            for row in rows:
                values = row.split(' ')
                values = [int(value) for value in values]
                matrix.append(values)
            matrix = np.array(matrix)
        except (ValueError, IndexError):
            self.show_popup('Erreur', 'Matrice de convolution invalide.')
            return

        # Chargement de l'image
        image = cv2.imread(self.image_path)

        # Application de la convolution
        result = cv2.filter2D(image, -1, matrix)

        # Affichage du résultat
        cv2.imwrite('result.jpg', result)
        self.image_widget.source = 'result.jpg'

    def show_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size_hint=(None, None), size=(400, 200))
        popup.open()

    def exit_app(self, instance):
        App.get_running_app().stop()
        Window.close()

if __name__ == '__main__':
    BMS_IMG().run()
