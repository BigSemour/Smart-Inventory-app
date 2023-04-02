from kivy.uix.popup import Popup

from barcode_reader import scan_barcodes, \
    get_price, create_database, update_database, get_unique_categories, checking

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.button import Button


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
            self.manager.current = "creation"
            pass
        elif MainWindow.action == "Edit List":
            self.manager.current = "selection"
            pass
        elif MainWindow.action == "Stock Prediction":
            pass
        else:
            pass


class CreationWindow(Screen):
    category = StringProperty('')

    def on_release_button(self):
        self.category = self.ids.newlist.text
        self.manager.current = 'product'


class ManualWindow(Screen):
    barcode_data = StringProperty("")
    category = StringProperty("")

    def on_release_button(self):
        name = self.ids.newName.text
        price = self.ids.newPrice.text
        if self.barcode_data is not None:
            update_database(name, self.barcode_data, price, self.category)
            SuccessPopup().open()


class SelectionWindow(Screen):
    pass


class ProductWindow(Screen):
    category = StringProperty('Test')
    barcode_data = StringProperty('')

    def on_release_button(self):
        # barcode_data = "021200523588"
        self.barcode_data = self.ids.newitem.text
        self.ids.newitem.text = ''
        self.data_retrieval(self.barcode_data)

    def launch_camera(self):
        try:
            self.barcode_data = scan_barcodes()
        except ValueError:
            self.barcode_data = ''
            pass
        if self.barcode_data is not None and self.barcode_data != '':
            self.data_retrieval(self.barcode_data)
        else:
            self.ids.newitem.text = ''  # clear text
            ErrorPopup().open()  # pop up error

    def data_retrieval(self, barcode_data):
        # Check the SQL data first
        exists = checking(barcode_data)
        # If it exists, show it popup window that it already exists
        if exists:
            ExistsPopup().open()
        # If it doesn't exist in SQL check the APIs
        else:
            price, name = get_price(barcode_data)
            # Go to the manual entry
            if name is None or price is None:
                # Pass the barcode and category to the third screen
                # self.manager.pass_info(barcode_data, self.category)
                self.manager.current = 'manualform'  # Go to manual Form
            # It is successful and update the database
            else:
                # Display a successful popup window
                update_database(name, barcode_data, price, self.category)
                SuccessPopup().open()


class EditWindow(Screen):
    pass


######################## Popup Section  #####################################
class ErrorPopup(Popup):
    pass


class SuccessPopup(Popup):
    pass


class ExistsPopup(Popup):
    pass


class WindowManager(ScreenManager):
    def pass_info(self, barcode_data, category):
        self.add_widget(ManualWindow(barcode_data=barcode_data, category=category))

    def pass_categ(self, category):
        self.add_widget(ProductWindow(category=category))


# Designate Our .kv design file
kv = Builder.load_file('KivyApp.kv')


class MainApp(App):
    def build(self):
        return kv

    def on_start(self):
        # First access the desired screen
        selection = self.root.get_screen('selection')
        # Then access the target drop-down by id.
        drop_down = selection.ids.drop_content
        # Now iterate over...
        categories = get_unique_categories()
        for name in enumerate(categories):
            btn = Button(
                text=name[1],
                size_hint_y=None,
                height=35,
                background_color='yellow',
                color='black'
            )
            btn.bind(on_release=lambda btn_obj: drop_down.select(btn_obj.text))
            drop_down.add_widget(btn)


if __name__ == '__main__':
    create_database()
    app = MainApp()
    app.run()
