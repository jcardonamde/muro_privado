from types import ClassMethodDescriptorType
from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
import math

class Message:
    def __init__(self, data):
        self.id = data ['id']
        self.content = data['content']
        self.sender_id = data['sender_id']
        self.receiver_id = data['receiver_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        #No tenemos en las columnas pero que vamos a poder obtener gracias al query
        self.sender_name = data['sender_name']
        self.receiver_name = data['receiver_name']
        
        
    def time_span(self):
        now = datetime.now()
        delta = now - self.created_at
        print(delta.days)
        print(delta.total_seconds())
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"
    
    @classmethod
    def save(cls, formulario):
        #formulario = {content: "mensaje", sender_id: ID del que manda, receiver_id: ID del que va recibir}
        query = "INSERT INTO messages (content, sender_id, receiver_id) VALUES (%(content)s, %(sender_id)s, %(receiver_id)s);"
        result = connectToMySQL('esquema_mundo_privado').query_db(query, formulario)
        return result
        
    @classmethod
    def get_user_messages(cls, formulario):
        query = "SELECT messages.*, senders.first_name as sender_name, receivers.first_name as receiver_name FROM messages LEFT JOIN users as senders ON senders.id = sender_id LEFT JOIN users as receivers ON receivers.id = receiver_id WHERE receiver_id = %(id)s;"
        results = connectToMySQL('esquema_mundo_privado').query_db(query, formulario)
        messages = []
        for message in results:
            messages.append(cls(message))
        return messages
    
    @classmethod
    def destroy(cls, formulario):
        query = "DELETE FROM messages WHERE messages.id = %(id)s;"
        result = connectToMySQL('esquema_mundo_privado').query_db(query, formulario)
        return result
    
    @staticmethod
    def validate_delete(data):
        query = " SELECT * FROM messages where id = %(id)s and receiver_id = %(receiver_id)s;"
        result = connectToMySQL('esquema_mundo_privado').query_db(query, data)
        if len(result) > 0:
            return True
        return False