# A GUI for ordering food.
# This was inspired by a listing from "Beginning Pyqt - A Hands-on Approach to GUI Programming" by Joshua Willman
# I modified the listing by writing functions and methods which make it easier to add new tabs and menu items to the GUI
# I also changed the colour-scheme and added some of my own menu items to the GUI

# TODO - make a general "add to order" button that can be used for all tabs

# import necessary modules
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QTabWidget,
                             QLabel, QRadioButton, QButtonGroup, QGroupBox, QPushButton,
                             QVBoxLayout, QHBoxLayout, QGridLayout)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

# Set up style sheet for the entire GUI
style_sheet = """
    QWidget{
        background-color: #016593;
    }
    QWidget#Tabs{
        background-color: #FCEBCD;
        border-radius: 4px
    }
    QWidget#ImageBorder{
        background-color: #FCF9F3;
        border-width: 2px;
        border-style: solid;
        border-radius: 4px;
        border-color: #FABB4C
    }
    QWidget#Side{
        background-color: #EFD096;
        border-radius: 4px
    }
    QLabel{
        background-color: #EFD096;
        border-width: 2px;
        border-style: solid;
        border-radius: 4px;
        border-color: #EFD096
    }
    QLabel#Header{
        background-color: #EFD096;
        border-width: 2px;
        border-style: solid;
        border-radius: 4px;
        border-color: #EFD096;
        padding-left: 10px;
        color: #e61838
    }
    QLabel#ImageInfo{
        background-color: #FCF9F3;
        border-radius: 4px
    }
    QGroupBox{
        background-color: #FCEBCD;
        color: #e61838
    }
    QRadioButton{
        background-color: #FCF9F3
    }
    QPushButton{
        background-color: #016593;
        border-radius: 4px;
        padding: 6px;
        color: #FFFFFF
    }
    QPushButton:pressed{
        background-color: #C86354;
        border-radius: 4px;
        padding: 6px;
        color: #DFD8D7
    }
"""


class FoodOrderGUI(QWidget):

    def __init__(self):
        super().__init__()
        self.initialize_ui()

    def initialize_ui(self):
        """
        Initialize the window and display its contents to the screen.
        """
        self.setMinimumSize(600, 700)
        self.setWindowTitle('6.1 – Food Order GUI')

        self.create_hierarchy()
        self.setup_tabs_and_layout()

        self.show()

    def create_hierarchy(self):
        """Create hierarchy structure using dictionaries (including all necessary
            QGroupBoxes and QButtonGroups"""
        self.crust_groupbox = QGroupBox()
        self.toppings_groupbox = QGroupBox()
        self.wings_groupbox = QGroupBox()
        self.sides_groupbox = QGroupBox()
        self.drinks_groupbox = QGroupBox()

        self.crust_buttongroup = QButtonGroup()
        self.toppings_buttongroup = QButtonGroup()
        self.wings_buttongroup = QButtonGroup()
        self.sides_buttongroup = QButtonGroup()
        self.drinks_buttongroup = QButtonGroup()

        self.choose_crust = {
            "header": "CHOOSE YOUR CRUST",
            "flavours": ["Hand-Tossed", "Flat", "Stuffed"],
            "groupbox": self.crust_groupbox,
            "buttongroup": self.crust_buttongroup,
            "exclusive": True
        }

        self.choose_toppings = {
            "header": "CHOOSE YOUR TOPPINGS",
            "flavours": ["Pepperoni", "Sausage", "Bacon", "Canadian Bacon",
                         "Beef", "Pineapple", "Mushroom", "Onion",
                         "Olive", "Green Pepper", "Tomato", "Spinach", "Cheese"],
            "groupbox": self.toppings_groupbox,
            "buttongroup": self.toppings_buttongroup,
            "exclusive": False
        }

        self.choose_wings = {
            "header": "CHOOSE YOUR FLAVOUR",
            "flavours": ["Buffalo", "Sweet-Sour", "Teriyaki", "Barbecue"],
            "groupbox": self.wings_groupbox,
            "buttongroup": self.wings_buttongroup,
            "exclusive": True
        }

        self.choose_sides = {
            "header": "CHOOSE YOUR SIDE",
            "flavours": ["Fries", "Hash Browns", "Salad", "Choc Chip Cookie"],
            "groupbox": self.sides_groupbox,
            "buttongroup": self.sides_buttongroup,
            "exclusive": True
        }

        self.choose_drinks = {
            "header": "CHOOSE A DRINK",
            "flavours": ["Orange Juice", "Lemonade", "Protein Shake", "Chocolate Milk"],
            "groupbox": self.drinks_groupbox,
            "buttongroup": self.drinks_buttongroup,
            "exclusive": True
        }

        self.pizza_tab_info = {
            "header": "BUILD YOUR OWN PIZZA",
            "image_path": "pizza.png",
            "description": "Build a custom pizza for you. Start with your favorite crust and add any toppings,"
                           " plus the perfect amount of cheese and sauce.",
            "options": [self.choose_crust, self.choose_toppings],
            "order_button": QPushButton("Add to order"),
            "add_to_order_func": self.display_pizza_in_order
        }
        self.wings_tab_info = {
            "header": "TRY OUR DELICIOUS WINGS",
            "image_path": "wings.png",
            "description": "6 pieces of rich-tasting, white meat chicken that will have you coming back for more.",
            "options": [self.choose_wings],
            "order_button": QPushButton("Add to order"),
            "add_to_order_func": self.display_wings_in_order
        }
        self.sides_tab_info = {
            "header": "TOP IT OFF WITH SOME IRRESISTIBLE SIDES",
            "image_path": "sides.png",
            "description": "No meal is complete without a lil something extra on the side.",
            "options": [self.choose_sides, self.choose_drinks],
            "order_button": QPushButton("Add to order"),
            "add_to_order_func": self.display_sides_in_order
        }

    def setup_tabs_and_layout(self):
        """
        Creates structure for the tabs and layout for the main window. Set up tab bar and different tab widgets.
        Also, create the side widget to display items selected.
        """
        # Create tab bar, different tabs and set object names
        self.tab_bar = QTabWidget(self)

        self.pizza_tab = QWidget()
        self.wings_tab = QWidget()
        self.sides_tab = QWidget()

        # use setObjectName("Tabs") so that the stylesheet can distinguish QWidgets which are meant to act as tabs from
        # other QWidgets
        self.pizza_tab.setObjectName("Tabs")
        self.wings_tab.setObjectName("Tabs")
        self.sides_tab.setObjectName("Tabs")

        self.tab_bar.addTab(self.pizza_tab, "Pizza")
        self.tab_bar.addTab(self.wings_tab, "Wings")
        self.tab_bar.addTab(self.sides_tab, "Sides and Drink")

        # Create the child widgets and place them in a layout for each tab
        pizza_tab_layout = self.make_tab(self.pizza_tab_info)
        wings_tab_layout = self.make_tab(self.wings_tab_info)
        sides_tab_layout = self.make_tab(self.sides_tab_info)

        # assign the layouts to the tabs
        self.pizza_tab.setLayout(pizza_tab_layout)
        self.wings_tab.setLayout(wings_tab_layout)
        self.sides_tab.setLayout(sides_tab_layout)

        # Set up side widget which is not part of the tab widget
        self.side_widget = QWidget()
        self.side_widget.setObjectName("Tabs")
        order_label = QLabel("YOUR ORDER")
        order_label.setObjectName("Header")

        items_box = QWidget()
        items_box.setObjectName("Side")
        pizza_label = QLabel("Pizza Type: ")
        self.display_pizza_label = QLabel("")
        toppings_label = QLabel("Toppings: ")
        self.display_toppings_label = QLabel("")
        extra_label = QLabel("Extra: ")
        self.display_wings_label = QLabel("")

        # Set grid layout for objects in side widget
        items_grid = QGridLayout()
        items_grid.addWidget(pizza_label, 0, 0, Qt.AlignRight)  # x = 0, y = 0, alignment = right
        items_grid.addWidget(self.display_pizza_label, 0, 1)  # x = 0, y = 1, no alignment
        items_grid.addWidget(toppings_label, 1, 0, Qt.AlignRight)
        items_grid.addWidget(self.display_toppings_label, 1, 1)
        items_grid.addWidget(extra_label, 2, 0, Qt.AlignRight)
        items_grid.addWidget(self.display_wings_label, 2, 1)
        items_box.setLayout(items_grid)

        # Set main layout for side widget (contains
        side_v_box = QVBoxLayout()
        side_v_box.addWidget(order_label)
        side_v_box.addWidget(items_box)
        side_v_box.addStretch()
        self.side_widget.setLayout(side_v_box)

        # Add widgets to main window and set layout
        main_h_box = QHBoxLayout()
        main_h_box.addWidget(self.tab_bar)
        main_h_box.addWidget(self.side_widget)

        self.setLayout(main_h_box)

    def make_tab(self, tab_info):
        # get variables from tab dictionary. tab_info is something like self.pizza_tab_info or self.wings_tab_info
        header_text = tab_info["header"]
        image_path = tab_info["image_path"]
        description = tab_info["description"]
        options = tab_info["options"]
        order_button = tab_info["order_button"]
        add_to_order_func = tab_info["add_to_order_func"]

        # Set up widgets and layouts to display information to the user about the page
        tab_header_label = QLabel(header_text)
        tab_header_label.setObjectName("Header")
        description_box = QWidget()
        description_box.setObjectName("ImageBorder")
        image = self.load_image(image_path)
        desc = QLabel()
        desc.setObjectName("ImageInfo")
        desc.setText(description)
        desc.setWordWrap(True)

        h_box = QHBoxLayout()
        h_box.addWidget(image)
        h_box.addWidget(desc)
        description_box.setLayout(h_box)

        # create layout for tab
        tab_v_box = QVBoxLayout()
        tab_v_box.addWidget(tab_header_label)
        tab_v_box.addWidget(description_box)
        for option in options:
            groupbox = option["groupbox"]
            groupbox.setTitle(option["header"])

            # create radio buttons for each flavour and add each to both a QVBoxLayout (and the buttongroup)
            groupbox_v_layout = QVBoxLayout()
            for flavour in option["flavours"]:
                flavor_rb = QRadioButton(flavour)
                groupbox_v_layout.addWidget(flavor_rb)
                option["buttongroup"].addButton(flavor_rb)  # (and the buttongroup)

            if option["exclusive"] is False:
                option["buttongroup"].setExclusive(False)  # allows more than one option to be selected

            # set the QVBoxLayout as the layout for the groupbox
            groupbox.setLayout(groupbox_v_layout)

            # Add the groupbox to the tab layout
            tab_v_box.addWidget(groupbox)

        # Create button to add information to side widget when clicked
        order_button.clicked.connect(add_to_order_func)
        tab_v_box.addWidget(order_button, alignment=Qt.AlignRight)
        tab_v_box.addStretch()

        # return the layout of the tab
        return tab_v_box

    def load_image(self, img_path):
        """
        Load and scale images.
        """
        try:
            with open(img_path):
                image = QLabel(self)
                image.setObjectName("ImageInfo")
                pixmap = QPixmap(img_path)
                image.setPixmap(pixmap.scaled(image.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
                return image
        except FileNotFoundError:
            print("Image not found.")

    def collect_toppings_in_list(self):
        """
        Create list of all checked toppings radio buttons.
        """
        # what the fuck?
        toppings_buttongroup = self.choose_toppings["buttongroup"]
        toppings_list = [button.text() for i, button in enumerate(toppings_buttongroup.buttons()) if button.isChecked()]
        return toppings_list

    def display_pizza_in_order(self):
        """
        Collect the text from the radio buttons that are checked
        on pizza page. Display text in side widget.
        """
        try:
            crust_buttongroup = self.choose_crust["buttongroup"]
            crust_text = crust_buttongroup.checkedButton().text()
            self.display_pizza_label.setText(crust_text)

            toppings = self.collect_toppings_in_list()
            toppings_str = '\n'.join(toppings)
            self.display_toppings_label.setText(toppings_str)

            self.repaint()
        except AttributeError:
            print("No value selected.")
            pass

    def display_wings_in_order(self):
        """
        Collect the text from the radio buttons that are checked
        on wings page. Display text in side widget.
        """
        try:
            wings_buttongroup = self.choose_wings["buttongroup"]
            text = wings_buttongroup.checkedButton().text() + " Wings"
            old_text = self.display_wings_label.text()
            new_text = old_text + "\n" + text
            self.display_wings_label.setText(new_text)
            self.repaint()
        except AttributeError:
            print("No value selected.")
            pass

    def display_sides_in_order(self):
        """
        Collect the text from the radio buttons that are checked
        on sides page. Display text in side widget
        """
        try:
            sides_buttongroup = self.choose_sides["buttongroup"]
            text = sides_buttongroup.checkedButton().text()
            old_text = self.display_wings_label.text()   # note display_wings_label is the 'extras' label
            new_text = old_text + "\n" + text
            self.display_wings_label.setText(new_text)
            self.repaint()
        except AttributeError:
            print("No value selected.")
            pass

        try:
            drinks_buttongroup = self.choose_drinks["buttongroup"]
            text = drinks_buttongroup.checkedButton().text()
            old_text = self.display_wings_label.text()   # note display_wings_label is the 'extras' label
            new_text = old_text + "\n" + text
            self.display_wings_label.setText(new_text)
            self.repaint()
        except AttributeError:
            print("No value selected.")
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = FoodOrderGUI()
    sys.exit(app.exec_())
