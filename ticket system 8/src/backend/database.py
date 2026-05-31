import mysql.connector
from mysql.connector import Error
from backend.universal_data import CurrentUserdata

class DatabaseError(Exception):
    """Custom Exception class for database errors, to catch them specifically in the frontend."""
    pass

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None

        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="projekt_4_db"
            )

            if self.connection.is_connected():
                print("Successfully connected to the MySQL database!")
                self.cursor = self.connection.cursor()
            else:
                raise DatabaseError("Could not establish a connection to the database.")

        except Error as e:
            raise DatabaseError(f"Error connecting to MySQL: {e}")

    def check_login(self, username, password):
        try:
            query = "SELECT 1 FROM userdata WHERE username = %s AND password = %s"
            self.cursor.execute(query, (username, password))
            return self.cursor.fetchone() is not None
        except Error as e:
            raise DatabaseError(f"Error checking login: {e}")

    def create_user(self, username, password):
        try:
            query = "INSERT INTO userdata (username, password, rank, status) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, (username, password, "user", "private"))
            self.connection.commit()
            print("User erfolgreich erstellt!")
            return True
        except mysql.connector.IntegrityError:
            raise DatabaseError("This username is already taken!")
        except Error as e:
            raise DatabaseError(f"General SQL error while creating the user: {e}")

    def create_messages_table(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS ticket_messages (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    ticket_id INT NOT NULL,
                    sender_id INT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.connection.commit()
        except Error as e:
            raise DatabaseError(f"Error creating the messages table: {e}")

    def send_message(self, ticket_id, sender_id, message):
        try:
            query = "INSERT INTO ticket_messages (ticket_id, sender_id, message) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (ticket_id, sender_id, message))
            self.connection.commit()
            return True
        except Error as e:
            raise DatabaseError(f"Error sending the message: {e}")

    def get_messages(self, ticket_id):
        try:
            query = """
                SELECT userdata.username, ticket_messages.message, DATE_FORMAT(ticket_messages.timestamp, '%d.%m. %H:%i')
                FROM ticket_messages
                JOIN userdata ON ticket_messages.sender_id = userdata.id
                WHERE ticket_messages.ticket_id = %s
                ORDER BY ticket_messages.timestamp ASC
            """
            self.cursor.execute(query, (ticket_id,))
            return self.cursor.fetchall()
        except Error as e:
            raise DatabaseError(f"Error loading messages: {e}")

    def fetch_user_data(self, username, password):
        try:
            print("Fetching user data...")
            query = "SELECT id, rank, username FROM userdata WHERE username = %s AND password = %s"
            self.cursor.execute(query, (username, password,))
            mysql_data = self.cursor.fetchone()
            
            if mysql_data is not None:
                CurrentUserdata.id = mysql_data[0]
                CurrentUserdata.rank = mysql_data[1]
                CurrentUserdata.username = mysql_data[2]
                print(f"current rank of active user: {CurrentUserdata.rank}")
                return True
            else:
                return False
        except Error as e:
            raise DatabaseError(f"Error fetching user data: {e}")

    def get_user_tickets(self, user_id):
        try:
            query = """SELECT ticket_number, date_time, category, short_description, long_description, t.status, handled_by 
                       FROM tickets t
                        JOIN userdata u ON user_id_ref = u.id 
                       WHERE user_id_ref = %s 
                          OR (SELECT rank FROM userdata WHERE id = %s) = 'admin' 
                       ORDER BY (t.factor * (CASE WHEN u.status = 'company' THEN 1.3 ELSE 1 END) + (DATEDIFF(NOW(), date_time) * 0.2)) DESC
                    """
            self.cursor.execute(query, (user_id, user_id))
            return self.cursor.fetchall()
        except Error as e:
            raise DatabaseError(f"Error loading tickets: {e}")

    def create_ticket(self, user_id, factor, category, short_description, long_description, status):
        try:
            query = "INSERT INTO tickets (user_id_ref, factor, category, short_description, long_description, status) VALUES (%s, %s, %s, %s, %s, %s)"
            self.cursor.execute(query, (user_id, factor, category, short_description, long_description, status))
            self.connection.commit()
            return True
        except Error as e:
            raise DatabaseError(f"Error creating the ticket: {e}")

    def delete_ticket(self, ticket_number):
        try:
            print("Delete ticket started")
            query = "DELETE FROM tickets WHERE ticket_number = %s"
            self.cursor.execute(query, (ticket_number,))
            self.connection.commit()
            return True
        except Error as e:
            raise DatabaseError(f"Error deleting the ticket: {e}")

    def ticket_edit_fetch(self, ticket_number):
        try:
            query = "SELECT ticket_number, date_time, category, short_description, long_description, status FROM tickets WHERE ticket_number = %s"
            self.cursor.execute(query, (ticket_number,))
            return self.cursor.fetchone()
        except Error as e:
            raise DatabaseError(f"Error fetching ticket details: {e}")

    def update_status(self, status, ticket_number):
        try:
            # Reset priority (factor) to 0 if the new status is 'closed'
            query = """
                UPDATE tickets 
                SET status = %s, 
                    handled_by = %s, 
                    factor = CASE WHEN %s = 'closed' THEN 0 ELSE factor END 
                WHERE ticket_number = %s
            """
            self.cursor.execute(query, (status, CurrentUserdata.username, status, ticket_number))
            self.connection.commit()
            print("Status Update successful")
            return True
        except Error as e:
            raise DatabaseError(f"Error updating ticket status: {e}")