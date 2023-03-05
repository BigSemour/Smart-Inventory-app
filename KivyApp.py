from barcode_reader import scan_barcodes

try:
    from kivy.app import App
except ImportError:
    import pip._internal as pip

    pip.main(['install', 'kivy'])
    from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder


class MainWindow(Screen):
    checks = []
    action = ' '

    def checkbox_click(self, instance, value, topping):
        if value:
            MainWindow.checks.append(topping)
            tops = ''
            for x in MainWindow.checks:
                tops = f'{tops} {x}'
            MainWindow.action = x

        else:
            MainWindow.checks.remove(topping)
            tops = ''
            for x in MainWindow.checks:
                tops = f'{tops} {x}'

    def on_press_button(self):

        if MainWindow.action == 'Create List':
            self.manager.current = "second"
            pass
        elif MainWindow.action == "Edit List":
            pass
        elif MainWindow.action == "Stock Prediction":
            pass
        else:
            pass


class SecondWindow(Screen):

    def on_release_button(self):
        temp = scan_barcodes()
        # if temp is None:
        self.manager.current = 'third' # form

        #database(temp)
        pass


class ThirdWindow(Screen):

    def on_release_button1(self):
        #database(temp)
        pass


class WindowManager(ScreenManager):
    pass


# Designate Our .kv design file
kv = Builder.load_file('KivyApp.kv')


class MainApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    app = MainApp()
    app.run()
