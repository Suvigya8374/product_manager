from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty
from kivy.core.window import Window
from kivy.config import Config
import mysql.connector
from mysql.connector import Error
from kivy.clock import Clock

# Optional: Set window size (desktop testing)
Window.size = (400, 700)

# Load .kv files manually
Builder.load_file("home.kv")
Builder.load_file("edit.kv")
Builder.load_file("add.kv")

class HomeScreen(Screen):
    company_names = ListProperty()
    product_names = ListProperty()
    
    db_config = {
        'host': '103.239.139.219',
        'database': 'vtechtest',
        'user': 'vtech',
        'password': 'Vtech@12@',
        'port': 3306
    }
        
    def on_enter(self):
        # Connect to database and load data, reset Spinners
        self.conn = None
        self.cursor = None
        try:
            self.conn = mysql.connector.connect(**self.db_config)
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT DISTINCT coname FROM liclogNOTIS WHERE coname IS NOT NULL")
            self.company_names = [row[0] for row in self.cursor.fetchall()]
            self.cursor.execute("SELECT DISTINCT product FROM liclogNOTIS WHERE product IS NOT NULL")
            self.product_names = [row[0] for row in self.cursor.fetchall()]
            print(f"Loaded company_names: {self.company_names}")
            print(f"Loaded product_names: {self.product_names}")
            if hasattr(self, 'ids') and 'company_spinner' in self.ids and 'product_spinner' in self.ids:
                self.ids.company_spinner.text = "Select Company"
                self.ids.product_spinner.text = "Select Product"
        except Error as e:
            print(f"Error loading data: {e}")
        finally:
            if self.conn and self.conn.is_connected():
                self.conn.close()

class EditScreen(Screen):
    def on_enter(self):
        # Clear text boxes only if not coming from "Find"
        print(f"Entering EditScreen, checking ids: {hasattr(self, 'ids')}")
        if hasattr(self, 'ids'):
            required_ids = ['message_input', 'expiry_date_input', 'trade_date_input', 'system_date_input', 'api_input']
            print(f"Available ids: {self.ids.keys()}")
            if all(id in self.ids for id in required_ids):
                if not hasattr(self, 'from_find') or not self.from_find:
                    print("Clearing text boxes on initial entry or submit")
                    self.ids.message_input.text = ""
                    self.ids.expiry_date_input.text = ""
                    self.ids.trade_date_input.text = ""
                    self.ids.system_date_input.text = ""
                    self.ids.api_input.text = ""

    def find_entry(self):
        # Fetch and populate data based on selected company and product
        company = self.manager.get_screen('home').ids.company_spinner.text
        product = self.manager.get_screen('home').ids.product_spinner.text
        print(f"find_entry called with company: {company}, product: {product}")
        print(f"Has ids: {hasattr(self, 'ids')}, All ids check: {all(id in self.ids for id in ['message_input', 'expiry_date_input', 'trade_date_input', 'system_date_input', 'api_input'])}")
        if company != "Select Company" and product != "Select Product":
            print("First if condition met")
            if hasattr(self, 'ids') and all(id in self.ids for id in ['message_input', 'expiry_date_input', 'trade_date_input', 'system_date_input', 'api_input']):
                print("Second if condition met, proceeding with query")
                conn = None
                try:
                    conn = mysql.connector.connect(
                        host="103.239.139.219",
                        database="vtechtest",
                        user="vtech",
                        password="Vtech@12@",
                        port=3306
                    )
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT msg, expirydate, trddate, sysdate, API 
                        FROM liclogNOTIS 
                        WHERE coname = %s AND product = %s
                    """, (company, product))
                    result = cursor.fetchone()
                    print(f"Query result: {result}")
                    if result:
                        self.from_find = True
                        Clock.schedule_once(lambda dt: self._update_text_boxes(result), 0)
                    else:
                        print("No matching entry found in database.")
                except Error as e:
                    print(f"Error executing query: {e}")
                finally:
                    if conn and conn.is_connected():
                        conn.close()
            else:
                print("Widgets not fully initialized or IDs missing")

    def _update_text_boxes(self, result):
        # Update text boxes after screen is loaded
        if hasattr(self, 'ids') and all(id in self.ids for id in ['message_input', 'expiry_date_input', 'trade_date_input', 'system_date_input', 'api_input']):
            print("Updating text boxes with result")
            self.ids.message_input.text = result[0] if result[0] else ""
            self.ids.expiry_date_input.text = result[1] if result[1] else ""
            self.ids.trade_date_input.text = result[2] if result[2] else ""
            self.ids.system_date_input.text = result[3] if result[3] else ""
            self.ids.api_input.text = result[4] if result[4] else ""
        else:
            print("Failed to update text boxes: IDs not available")

    def submit_entry(self):
        # Update database with edited values and ensure only the specific entry is edited
        company = self.manager.get_screen('home').ids.company_spinner.text
        product = self.manager.get_screen('home').ids.product_spinner.text
        print(f"submit_entry called with company: {company}, product: {product}")
        if hasattr(self, 'ids') and all(id in self.ids for id in ['message_input', 'expiry_date_input', 'trade_date_input', 'system_date_input', 'api_input']):
            message = self.ids.message_input.text
            expiry_date = self.ids.expiry_date_input.text
            trade_date = self.ids.trade_date_input.text
            system_date = self.ids.system_date_input.text
            api = self.ids.api_input.text
            conn = None
            try:
                conn = mysql.connector.connect(
                    host="103.239.139.219",
                    database="vtechtest",
                    user="vtech",
                    password="Vtech@12@",
                    port=3306
                )
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM liclogNOTIS WHERE coname = %s AND product = %s", (company, product))
                if cursor.fetchone()[0] == 1:
                    cursor.execute("""
                        UPDATE liclogNOTIS 
                        SET msg = %s, expirydate = %s, trddate = %s, sysdate = %s, API = %s 
                        WHERE coname = %s AND product = %s
                    """, (message, expiry_date, trade_date, system_date, api, company, product))
                    conn.commit()
                    print(f"Updated entry for {company}, {product}")
                    if hasattr(self, 'from_find'):
                        del self.from_find
                    self.manager.current = 'home'
                else:
                    print(f"No unique entry found for {company}, {product} to update.")
            except Error as e:
                print(f"Error submitting entry: {e}")
            finally:
                if conn and conn.is_connected():
                    conn.close()

class AddScreen(Screen):
    def save_entry(self):
        # Insert new entry into database
        if hasattr(self, 'ids') and all(id in self.ids for id in ['hdd_input', 'login_input', 'product_input', 'msg_input', 'coname_input', 'user_input', 'pwd_input', 'expirydate_input', 'trddate_input', 'api_input', 'sysdate_input']):
            hdd = self.ids.hdd_input.text
            login = self.ids.login_input.text
            product = self.ids.product_input.text
            msg = self.ids.msg_input.text
            coname = self.ids.coname_input.text
            user = self.ids.user_input.text
            pwd = self.ids.pwd_input.text
            expirydate = self.ids.expirydate_input.text
            trddate = self.ids.trddate_input.text
            api = self.ids.api_input.text
            sysdate = self.ids.sysdate_input.text
            conn = None
            try:
                conn = mysql.connector.connect(
                    host="103.239.139.219",
                    database="vtechtest",
                    user="vtech",
                    password="Vtech@12@",
                    port=3306
                )
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO liclogNOTIS (hdd, login, product, msg, coname, user, pwd, expirydate, trddate, API, sysdate)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (hdd, login, product, msg, coname, user, pwd, expirydate, trddate, api, sysdate))
                conn.commit()
                print(f"Added new entry for {coname}, {product}")
                self.manager.current = 'home'
            except Error as e:
                print(f"Error adding entry: {e}")
            finally:
                if conn and conn.is_connected():
                    conn.close()

class ProductManagerApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(EditScreen(name="edit"))
        sm.add_widget(AddScreen(name="add"))
        return sm

if __name__ == '__main__':
    ProductManagerApp().run()