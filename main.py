from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
import cv2
import numpy as np

import os


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def load(self, path, filename):
        self.path = path
        self.filename = filename
        self.dismiss_popup()

    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.text_input.text)

        self.dismiss_popup()

    def erosion(self):
        if not self.filename[0]:
            return
        image = cv2.imread(os.path.join(self.path, self.filename[0]), 0)

        kernel = np.ones((5, 5), np.uint8)

        erosion = cv2.erode(image, kernel, iterations=1)

        self.save_image(erosion, 'erosion_output.jpg')

    def dilatation(self):
        print(self.filename)
        if not self.filename[0]:
            return
        image = cv2.imread(os.path.join(self.path, self.filename[0]), 0)

        kernel = np.ones((5, 5), np.uint8)

        dilation = cv2.dilate(image, kernel, iterations=1)

        self.save_image(dilation, 'dilation_output.jpg')

    def opening(self):
        if not self.filename[0]:
            return

        image = cv2.imread(os.path.join(self.path, self.filename[0]), 0)

        kernel = np.ones((5, 5), np.uint8)

        opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

        self.save_image(opening, 'opening_output.jpg')

    def closing(self):
        if not self.filename[0]:
            return
        image = cv2.imread(os.path.join(self.path, self.filename[0]), 0)

        kernel = np.ones((5, 5), np.uint8)

        closing = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

        self.save_image(closing, 'closing_output.jpg')

    def min_filter(self):
        if not self.filename[0]:
            return
        image = cv2.imread(os.path.join(self.path, self.filename[0]), 0)

        min_filter = cv2.erode(image, None, iterations=1)

        self.save_image(min_filter, 'min_filter_output.jpg')

    def max_filter(self):
        if not self.filename[0]:
            return
        image = cv2.imread(os.path.join(self.path, self.filename[0]), 0)

        max_filter = cv2.dilate(image, None, iterations=1)

        self.save_image(max_filter, 'max_filter_output.jpg')

    def med_filter(self):
        if not self.filename[0]:
            return
        image = cv2.imread(os.path.join(self.path, self.filename[0]), 0)

        new_image = cv2.medianBlur(image, 3)

        self.save_image(new_image, 'med_filter_output.jpg')

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def save_image(self, image, filename):
        save_path = os.path.join(self.path, filename)
        cv2.imwrite(save_path, image)
        cv2.imshow('Saved Image', image)
        cv2.waitKey(0)

class Editor(App):
    pass


Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)

if __name__ == '__main__':
    Editor().run()
