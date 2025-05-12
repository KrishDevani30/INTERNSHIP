## Sample GUI 
#### Using PyQt5

---

I uxe QApplication, QMainWindow , QWidget , QVBoxLayout , QHBoxLayout , QLabel , QComboBox , QLineEdit , QPushButton , QFrame , QSizePolicy from PyQt5.QtWidgets.

- Make sure you have **Python and PyQt5 Installed**
- For run this GUI **python .\sample_gui.py**

---

- **SampleGUI(QMainWindow):** Main application window class.
- **QVBoxLayout, QHBoxLayout:** Used for arranging widgets vertically and horizontally.
- **QComboBox:** Dropdown widgets for dynamic selections.
- **QLineEdit:** Input field for entering a name.
- **QFrame:** Containers for header, footer, navbar, and name input section.

---

### Function overview
```
def update_subcategory(self):
        self.subcategory_combo.clear()
        category = self.category_combo.currentText()
        if category == "Electronics":
            self.subcategory_combo.addItems(["Laptops", "Phones", "Tablets", "Accessories"])
        elif category == "Clothing":
            self.subcategory_combo.addItems(["Men", "Women", "Kids", "Accessories"])
        elif category == "Food":
            self.subcategory_combo.addItems(["Fruits", "Vegetables", "Dairy", "Bakery"])
        elif category == "Books":
            self.subcategory_combo.addItems(["Fiction", "Non-Fiction", "Educational", "Magazines"])
```

This block of code has Dropdown menu combo of Category and Subcategory. If we chagne Category then there is change in Subcategory accordingly.

<br>

```
def update_city(self):
        self.city_combo.clear()
        location = self.location_combo.currentText()
        if location == "North":
            self.city_combo.addItems(["Punjab", "Rajasthan", "Kashmir"])
        elif location == "South":
            self.city_combo.addItems(["Karnataka", "Telangana", "Kerala"])
        elif location == "East":
            self.city_combo.addItems(["Bihar", "Chhattisgarh", "Odisha"])
        elif location == "West":
            self.city_combo.addItems(["Gujarat", "Goa", "Maharashtra"])
```

This block of code has Dropdown menu combo of Location and City. If we chagne Location then there is change in City accordingly.

<br>

```
def update_team(self):
        self.team_combo.clear()
        department = self.department_combo.currentText()
        if department == "IT":
            self.team_combo.addItems(["Development", "QA", "DevOps", "Support"])
        elif department == "HR":
            self.team_combo.addItems(["Recruitment", "Training", "Employee Relations"])
        elif department == "Finance":
            self.team_combo.addItems(["Accounting", "Tax", "Audit", "Investment"])
        elif department == "Marketing":
            self.team_combo.addItems(["Digital", "Content", "Brand", "Social Media"])
```

This block of code has Dropdown menu combo of Department and Team. If we chagne Department then there is change in Team accordingly.

<br>

---

### Basic code Explaination 

```
category_label = QLabel("Category:")
category_label.setStyleSheet("color: white; font-size: 14px;")
self.category_combo = QComboBox()
self.category_combo.setStyleSheet(dropdown_style)
self.category_combo.addItems(["Electronics", "Clothing", "Food", "Books"])
self.category_combo.currentIndexChanged.connect(self.update_subcategory)
```
In this Lines we make one drop-down menu for Categoty and give styles and then call a function if we change in any Category.There is 4 same drop-down menus for Subcategoty , Location , City , Department and Team. 

---
### Output


![Sample GUI Screenshot](https://github.com/user-attachments/assets/4717ffbc-16a9-4b50-90a1-68bd149b62be)

