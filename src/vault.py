import os
import sqlite3
from datetime import datetime
from typing import Optional


class Application:
    def __init__(self, id: int, name: str, created_at: datetime) -> None:
        self.id: int = id
        self.name: str = name
        self.created_at: datetime = created_at

    def __str__(self) -> str:
        return f"Application(id={self.id}, name={self.name}, created_at={self.created_at})"

class Field:
    def __init__(self, id: int, application_id: int, name: str, value: str, created_at: datetime) -> None:
        self.id: int = id,
        self.application_id: int = application_id, # foreign key to Application.id
        self.name: str = name
        self.value: str = value,
        self.created_at: datetime = created_at,


class Vault():
    def __init__(self) -> None:        
        self.path = os.path.join(os.path.dirname(__file__), "data", "vault.db")
        self.connection: sqlite3.Connection = None
        self._pm: str = None
        self.hint: str = None
        self.key: str = None

    @property
    def empty(self):
        return self._pm is None
    
    @property
    def pm_hash(self):
        """
        password master
        """
        return self._pm

    def init(self):
        self.create_db()

        if not self.empty:
            self.hint = self.connection.execute("SELECT hint from PasswordManager").fetchone()

    def create_db(self) -> None:

        if not os.path.exists(self.path):
            open(self.path, "w").close()    
            self.connection = sqlite3.connect(self.path)
            
            self.connection.execute("CREATE TABLE PasswordManager ( id INTEGER PRIMARY KEY, pm_hash TEXT NOT NULL, hint TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
            self.connection.execute("CREATE TABLE Applications ( id INTEGER PRIMARY KEY, name TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
            self.connection.execute("CREATE TABLE Fields ( id INTEGER PRIMARY KEY, application_id INTEGER NOT NULL, name TEXT NOT NULL, value TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (application_id) REFERENCES Applications(id));")
            self.connection.execute("CREATE TABLE Credentials ( id INTEGER PRIMARY KEY, application_id INTEGER NOT NULL, field_id INTEGER, value TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (application_id) REFERENCES Applications(id), FOREIGN KEY (field_id) REFERENCES Fields(id));")
        else:
            self.connection = sqlite3.connect(self.path)

        self._pm = self.connection.execute("SELECT pm_hash FROM PasswordManager").fetchone()


    def fetch_applications(self, name: Optional[str] = None) -> list[Application]:
        query = ""
        query += "SELECT * FROM Applications"

        if name:
            query += f" WHERE name = {name}"


        res = self.connection.execute(query).fetchall()
        applications = [
            Application(a[0], a[1], datetime.fromisoformat(a[2])) for a in res
        ]
        print([a.__str__() for a in applications])
        return applications
    
    def fetch_fields(self, name: Optional[str] = None, value: Optional[str] = None) -> list[Field]:
        query = ""
        query += "SELECT * FROM Fields"

        if name:
            query += f" WHERE name = {name}"

        if value:
            if name:
                query += " AND"
            query += f" WHERE value = {value}"


        res = self.connection.execute(query).fetchall()
        fields = [
            Field(a[0], a[1], a[2], datetime.fromisoformat(a[3])) for a in res
        ]
        print([a.__str__() for a in fields])
        return fields


vault = Vault()
vault.init()

vault.fetch_fields()



