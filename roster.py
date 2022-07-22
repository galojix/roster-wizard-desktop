"""Roster Wizard GUI."""
import toga
from toga.constants import COLUMN
from toga.style import Pack


class RosterApp(toga.App):
    def _create_options(self):
        label_box0 = toga.Label("This is Box 0 ", style=Pack(padding=10))
        label_box1 = toga.Label("This is Box 1 ", style=Pack(padding=10))
        label_box2 = toga.Label("This is Box 2 ", style=Pack(padding=10))
        label_box3 = toga.Label("This is Box 3 ", style=Pack(padding=10))
        label_box4 = toga.Label("This is Box 4 ", style=Pack(padding=10))
        label_box5 = toga.Label("This is Box 5 ", style=Pack(padding=10))
        label_box6 = toga.Label("This is Box 6 ", style=Pack(padding=10))
        label_box7 = toga.Label("This is Box 7 ", style=Pack(padding=10))

        box0 = toga.Box(children=[label_box0])
        box1 = toga.Box(children=[label_box1])
        box2 = toga.Box(children=[label_box2])
        box3 = toga.Box(children=[label_box3])
        box4 = toga.Box(children=[label_box4])
        box5 = toga.Box(children=[label_box5])
        box6 = toga.Box(children=[label_box6])
        box7 = toga.Box(children=[label_box7])

        self.optioncontainer.add("Staff", box0)
        self.optioncontainer.add("Day Groups", box1)
        self.optioncontainer.add("Shifts", box2)
        self.optioncontainer.add("Skill Mix", box3)
        self.optioncontainer.add("Shift Sequences", box4)
        self.optioncontainer.add("Leave", box5)
        self.optioncontainer.add("Staff Requests", box6)
        self.optioncontainer.add("Roster", box7)

    def set_next_tab(self, widget):
        if (
            self.optioncontainer.current_tab.index
            < len(self.optioncontainer.content) - 1
        ):
            self.optioncontainer.current_tab += 1

    def set_previous_tab(self, widget):
        if self.optioncontainer.current_tab.index > 0:
            self.optioncontainer.current_tab -= 1

    def on_select_tab(self, widget, option):
        pass

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        self.optioncontainer = toga.OptionContainer(
            on_select=self.on_select_tab, style=Pack(padding_bottom=20)
        )
        self._create_options()

        # Outermost box
        outer_box = toga.Box(
            children=[
                self.optioncontainer,
            ],
            style=Pack(
                flex=1,
                direction=COLUMN,
                padding=10,
            ),
        )

        self.commands.add(
            toga.Command(
                self.set_next_tab,
                "Next tab",
                shortcut=toga.Key.MOD_1 + toga.Key.RIGHT,
                group=toga.Group.COMMANDS,
                order=1,
            ),
            toga.Command(
                self.set_previous_tab,
                "Previous tab",
                shortcut=toga.Key.MOD_1 + toga.Key.LEFT,
                group=toga.Group.COMMANDS,
                order=1,
            ),
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return RosterApp(
        formal_name="Roster Wizard",
        app_id="org.beeware.widgets.optioncontainer",
        icon="wizard_hat",
        version="0.1",
    )


if __name__ == "__main__":
    app = main()
    app.main_loop()
