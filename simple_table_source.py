import toga
from toga.constants import COLUMN, ROW
from toga.sources import Source
from toga.style import Pack


class StaffMember:
    # A class to wrap individual staff
    # Attribute names must match table headings
    # (after lower case conversion and swapping spaces for underscores)
    def __init__(self, last_name, first_name, shifts_per_roster):
        self.last_name = last_name
        self.first_name = first_name
        self.shifts_per_roster = int(shifts_per_roster)


class StaffMemberSource(Source):
    def __init__(self):
        super().__init__()
        self._staff = []

    def __len__(self):
        return len(self._staff)

    def __getitem__(self, index):
        return self._staff[index]

    def index(self, entry):
        return self._staff.index(entry)

    def add(self, entry):
        staff_member = StaffMember(*entry)
        self._staff.append(staff_member)
        self._staff.sort(key=lambda s: s.last_name)
        self._notify(
            "insert", index=self._staff.index(staff_member), item=staff_member
        )

    def remove(self, item):
        index = self.index(item)
        self._notify("pre_remove", index=index, item=item)
        del self._staff[index]
        self._notify("remove", index=index, item=item)

    def clear(self):
        self._staff = []
        self._notify("clear")


class AddStaffMemberWindow(toga.Window):
    def __init__(self, table):
        super().__init__()
        self.title = "Add Staff Member"
        self.table = table
        btn_add = toga.Button(
            "Add", on_press=self.add_handler, style=Pack(flex=1, width=200)
        )

        last_name_label = toga.Label("Last Name", style=Pack(padding=10))
        self.last_name_input = toga.TextInput(
            placeholder="enter last name here"
        )

        first_name_label = toga.Label("First Name", style=Pack(padding=10))
        self.first_name_input = toga.TextInput(
            placeholder="enter first name here"
        )

        shifts_per_roster_label = toga.Label(
            "Shifts Per Roster", style=Pack(padding=10)
        )
        self.shifts_per_roster_input = toga.NumberInput()

        add_staff_box = toga.Box(
            children=[
                btn_add,
                last_name_label,
                self.last_name_input,
                first_name_label,
                self.first_name_input,
                shifts_per_roster_label,
                self.shifts_per_roster_input,
            ],
            style=Pack(flex=1, direction="column"),
        )
        self.content = add_staff_box

    def add_handler(self, widget, **kwargs):
        self.table.data.add(
            [
                self.last_name_input.value,
                self.first_name_input.value,
                self.shifts_per_roster_input.value,
            ]
        )
        self.close()


class SimpleTableSourceApp(toga.App):
    def delete_staff_handler(self, widget, **kwargs):
        if self.staff_table.selection:
            self.staff_table.data.remove(self.staff_table.selection)
            self.staff_table.focus()
        else:
            self.main_window.error_dialog("Error", "No item selected.")

    # Button callback functions
    def add_staff_handler(self, widget, **kwargs):
        add_staff_window = AddStaffMemberWindow(self.staff_table)
        self.windows.add(add_staff_window)
        add_staff_window.show()

    def startup(self):
        self.main_window = toga.MainWindow(title=self.name)

        self.staff_table = toga.Table(
            headings=["Last Name", "First Name", "Shifts Per Roster"],
            data=StaffMemberSource(),
            style=Pack(flex=1),
            missing_value="",
        )

        self.staff_table.data.add(["Bloggs", "Fred", 10])
        self.staff_table.data.add(["Smith", "John", 20])
        self.staff_table.data.add(["Brown", "Billy", 30])
        self.staff_table.data.add(["Wallow", "Frog", 40])

        tablebox = toga.Box(children=[self.staff_table], style=Pack(flex=1))

        btn_add_staff = toga.Button(
            "Add Staff",
            on_press=self.add_staff_handler,
            style=Pack(flex=1, width=200),
        )

        btn_del_staff = toga.Button(
            "Delete Staff",
            on_press=self.delete_staff_handler,
            style=Pack(flex=1, width=200),
        )

        # Most outer box
        outer_box = toga.Box(
            children=[btn_add_staff, btn_del_staff, tablebox],
            style=Pack(
                flex=1,
                direction=COLUMN,
                padding=10,
            ),
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return SimpleTableSourceApp("Simple Table Source", "myapp")


if __name__ == "__main__":
    app = main()
    app.main_loop()
