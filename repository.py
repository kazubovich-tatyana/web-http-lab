from psycopg import sql, Connection, errors
import models

# для notes

def add_note_in_db(conn:Connection, note_data:dict)->dict|None:
    with conn.cursor() as cur:
        try:
            cur.execute(models.POST_NOTE, (note_data['title'], note_data['content'], note_data['status'], note_data['user_id']))
            new_note = cur.fetchone()
            return new_note
        except errors.ForeignKeyViolation:
            raise ValueError(f'User with this id = {note_data["user_id"]} does not exist')
        except errors.DatabaseError as e:
            raise ValueError(f'Error database validation data: {e}')


def get_notes_in_db(conn: Connection, limit:int, offset:int)->dict:
    with conn.cursor() as cur:
        cur.execute(models.TOTAL_NOTES)
        total_notes = cur.fetchone()['total']
        cur.execute(models.SELECT_ALL_NOTES,(limit, offset))
        notes = cur.fetchall()
        return {'total': total_notes,
                'limit': limit,
                'offset': offset,
                'notes': notes}


def get_note_in_db(conn:Connection, note_id:int):
    with conn.cursor() as cur:
        cur.execute(models.GET_NOTE, (note_id, ))
        note = cur.fetchone()
        if note is None:
            raise LookupError(f'Note {note_id} not found')
        return note


def check_note_in_db(conn:Connection, note_id:int):
    with conn.cursor() as cur:
        cur.execute(models.EXISTS_NOTE, (note_id,))
        note = cur.fetchone()
        return note is not None


def update_note_in_db(conn:Connection, note_id:int, update_fields:dict)->dict:
    sql_request_param = []
    sql_request_values = []
    for field_name, field_value in update_fields.items():
        sql_request_param.append(sql.SQL("{}=%s").format(sql.Identifier(field_name)))
        sql_request_values.append(field_value)
    sql_request_values.append(note_id)
    sql_request_body = sql.SQL('''
                           UPDATE notes 
                           SET {fields} 
                           WHERE id = %s 
                           RETURNING id, title, content, status, time_created, user_id
                           ''').format(fields=sql.SQL(',').join(sql_request_param))

    with conn.cursor() as cur:
        try:
            cur.execute(sql_request_body, sql_request_values)
        except errors.ForeignKeyViolation as e:
            raise ValueError(f'User with this id does not exist')
        except errors.DatabaseError as e:
            raise ValueError(f'Error database validation data: {e}')

        if cur.rowcount == 0:
            raise LookupError(f'Note id = {note_id} not found')
        note = cur.fetchone()
        return note


def delete_note_in_db(conn:Connection, note_id:int)->None:
    with conn.cursor() as cur:
        cur.execute(models.DELETE_NOTE, (note_id,))
        note_id = cur.fetchone()
        if note_id is None:
            raise LookupError(f'Note {note_id} does not exist')


# для users

def add_user_in_db(conn:Connection, user_data:dict)->dict:
    with conn.cursor() as cur:
        cur.execute(models.POST_USER,(user_data['name'], ))
        user = cur.fetchone()
        if user is None:
            raise LookupError(f'User {user_data["name"]} didn\'t created')
        return user

def get_user_in_db(conn:Connection, user_id:int)->dict:
    with conn.cursor() as cur:
        cur.execute(models.GET_USER, (user_id,))
        user = cur.fetchone()
        if user is None:
            raise LookupError(f'User {user_id} not found')
        return user


def check_user_in_db(conn, user_id):
    with conn.cursor() as cur:
        cur.execute(models.EXISTS_USER, (user_id,))
        user = cur.fetchone()
        return user is None


def get_user_notes_in_db(conn:Connection, user_id:int, limit:int, offset:int)->dict:
    with conn.cursor() as cur:
        try:
            cur.execute(models.TOTAL_USER_NOTES,(user_id, ))
            total_notes = cur.fetchone()['total']
            cur.execute(models.SELECT_USER_NOTES, (user_id, limit, offset))
            notes = cur.fetchall()
            return {'total': total_notes,
                    'limit': limit,
                    'offset': offset,
                    'notes': notes}
        except errors.ForeignKeyViolation as e:
            raise ValueError(f'User with this id does not exist')


def delete_user_in_db(conn:Connection, user_id:int)->None:
    with conn.cursor() as cur:
        user_id = cur.execute(models.DELETE_USER, (user_id,))
        if user_id is None:
            raise LookupError(f'User {user_id} does not exist')