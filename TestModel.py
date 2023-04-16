import os
from datetime import date
import json
import sqlite3 as sql

class AccountModel():
    '''TODO: Change working directory once this program is converted to a .exe'''

    def __init__(self):
        self.root_path = os.getcwd()
        self.config_file_name = 'athlete_db_config_file.txt'
        self.config_file_name_path = os.path.join(self.root_path, self.config_file_name)
        self.download_file_path = None
        self.db_conn = None

        # Check if config file exists
        config_exists = False
        for file in os.listdir(self.root_path):
            if file == self.config_file_name:
                config_exists = True
        if config_exists == False:
            with open(self.config_file_name_path, 'w') as config_file:
                print('Successfully created config file.')

        # Check if config file is empty or corrupted
        config_empty = True
        config_corrupted = False
        with open(self.config_file_name_path, 'r') as config_file:
            pass

    def validate_login(self, username):
        login_response = {'success': False, 'message': None}
        with open(self.config_file_name_path, 'r') as config_file:
            for row in config_file:
                account_info = json.loads(row)
                if username == account_info['username']:
                    database = account_info['database']
                    self.db_conn = sql.connect(database)
                    login_response['success'] = True
                    return login_response

        login_response['message'] = 'There was an unexpected error. Check the configuration file to see if the ' \
                                    'username exists.'
        return login_response

    def get_usernames(self):
        '''Access the entries in the configuration file.'''
        account_list = []
        with open(self.config_file_name_path, 'r') as config_file:
            for row in config_file:
                account_list.append(json.loads(row))

        usernames = [account['username'] for account in account_list]

        return usernames

    def get_user_count(self):
        return 1

    def create_account(self, username):
        '''Trigger the instantiation of a new database and create an account entry in the configuration file.'''
        db_file_name = username + '.db'
        if self.validate_file_name(db_file_name):
            full_database_path = os.path.join(self.root_path, db_file_name)

            # Instantiate Database
            self.instantiate_database_schema(db_file_name)
            self.instantiate_static_tables(db_file_name)
            self.instantiate_dynamic_tables(db_file_name)

            # Create config file entry
            with open(self.config_file_name_path, 'a') as config_file:
                entry_dict = {"username": username, "database": db_file_name,
                              "directory": self.root_path}
                config_file.write(json.dumps(entry_dict) + '\n')
                print('written kitten', entry_dict)
        else:
            # TODO: Return an error
            pass

    def validate_file_name(self, file_name):
        return True

    def instantiate_database_schema(self, db_name):
        '''Do full database table instantiation'''
        temp_conn = sql.connect(db_name)
        cursor = temp_conn.cursor()

        # Do full database table instantiation
        cursor.execute('''
        CREATE TABLE workout_class (
        workout_class_id INTEGER PRIMARY KEY,
        workout_class_name TEXT NOT NULL UNIQUE
        )''')

        cursor.execute('''
        CREATE TABLE workout_type (
        workout_type_id INTEGER PRIMARY KEY,
        workout_type_name TEXT NOT NULL,
        workout_class_id INTEGER NOT NULL,
        UNIQUE (workout_type_name, workout_class_id)
        FOREIGN KEY(workout_class_id) REFERENCES workout_class(workout_class_id)
        )''')

        cursor.execute('''
        CREATE TABLE measure (
        measure_id INTEGER PRIMARY KEY,
        measure_name TEXT NOT NULL UNIQUE
        )''')
        
        cursor.execute('''
        CREATE TABLE workout (
        workout_id INTEGER PRIMARY KEY,
        workout_name TEXT NOT NULL,
        workout_type_id INTEGER NOT NULL,
        UNIQUE (workout_name, workout_type_id)
        FOREIGN KEY(workout_type_id) REFERENCES workout_type(workout_type_id)
        )''')
        
        cursor.execute('''
        CREATE TABLE exercise (
        exercise_id INTEGER PRIMARY KEY,
        exercise_name TEXT NOT NULL UNIQUE,
        workout_type_id INTEGER NOT NULL,
        measure_id INTEGER NOT NULL,
        FOREIGN KEY(workout_type_id) REFERENCES workout_type(workout_type_id),
        FOREIGN KEY(measure_id) REFERENCES measure(measure_id)
        )''')
        
        cursor.execute('''
        CREATE TABLE day (
        day_id INTEGER PRIMARY KEY,
        date TEXT NOT NULL UNIQUE,
        calories INTEGER,
        protein INTEGER,
        weight REAL,
        sleep REAL
        )''')
        
        cursor.execute('''
        CREATE TABLE exercise_goal (
        exercise_goal_id INTEGER PRIMARY KEY,
        exercise_id INTEGER NOT NULL,
        goal_value REAL NOT NULL,
        target_end_date TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT,
        status TEXT,
        FOREIGN KEY(exercise_id) REFERENCES exercise(exercise_id)
        )''')
        
        cursor.execute('''
        CREATE TABLE weight_goal (
        weight_goal_id INTEGER PRIMARY KEY,
        goal_value REAL NOT NULL,
        target_end_date TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT,
        status TEXT
        )''')
        
        cursor.execute('''
        CREATE TABLE workout_class_goal (
        workout_class_goal_id INTEGER PRIMARY KEY,
        workout_class_id INTEGER NOT NULL,
        goal_value INTEGER NOT NULL,
        target_end_date TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT,
        status TEXT,
        FOREIGN KEY(workout_class_id) REFERENCES workout_class(workout_class_id)
        )''')
        
        cursor.execute('''
        CREATE TABLE workout_session (
        workout_session_id INTEGER PRIMARY KEY,
        workout_id INTEGER NOT NULL,
        time_elapsed INTEGER,
        workout_quality_num INTEGER,
        workout_quality_text TEXT,
        date TEXT NOT NULL,
        FOREIGN KEY(workout_id) REFERENCES workout(workout_id)
        )''')
        
        cursor.execute('''
        CREATE TABLE exercise_session (
        exercise_session_id INTEGER PRIMARY KEY,
        exercise_id INTEGER NOT NULL,
        value INTEGER NOT NULL,
        repetitions INTEGER,
        date TEXT NOT NULL,
        FOREIGN KEY(exercise_id) REFERENCES exercise(exercise_id)
        )''')

        temp_conn.commit()
        temp_conn.close()

    def instantiate_static_tables(self, db_name):
        temp_conn = sql.connect(db_name)
        cursor = temp_conn.cursor()

        workout_class_data = [(1, 'Weight Lifting'),
                              (2, 'Running'),
                              (3, 'Bicycling'),
                              (4, 'Swimming'),
                              (5, 'Sport'),
                              ]
        cursor.executemany('INSERT INTO workout_class (workout_class_id, workout_class_name) VALUES (?, ?)',
                           workout_class_data)

        workout_type_data = [('Chest', 1),
                             ('Legs', 1),
                             ('Back', 1),
                             ('Arms', 1),
                             ('Shoulders', 1),
                             ('Abs', 1),
                             ('Push', 1),
                             ('Pull', 1),
                             ('Distance', 2),
                             ('Sprints', 2),
                             ('Agility', 2),
                             ('Road', 3),
                             ('Stationary', 3),
                             ('Distance', 4),
                             ('Basketball', 5),
                             ('Volleyball', 5),
                             ('Rugby', 5),
                             ('Tennis', 5),
                             ('Martial Arts', 5),
                             ('Soccer', 5),
                             ('Golf', 5),
                             ]
        cursor.executemany('INSERT INTO workout_type (workout_type_name, workout_class_id) VALUES (?, ?)',
                           workout_type_data)

        measure_data = [('pounds',),
                        ('seconds',),
                        ('minutes',),
                        ('miles',),
                        ('meters',),
                        ('reps',),
                        ]
        cursor.executemany('INSERT INTO measure (measure_name) VALUES (?)', measure_data)

        temp_conn.commit()
        temp_conn.close()

    def instantiate_dynamic_tables(self, db_name):
        temp_conn = sql.connect(db_name)
        cursor = temp_conn.cursor()

        exercise_data = [('Dumbbell Bench Press', 1, 1),
                        ('Barbell Bench Press', 1, 1),
                        ('Push-ups', 1, 6),
                        ('Barbell Squat', 2, 1),
                        ('Goblet Squat', 2, 1),
                        ('Bulgarian Split Squat', 2, 1),
                        ('Hip Thrust', 2, 1),
                        ('Deadlift', 3, 1),
                        ('Bent Over Row', 3, 1),
                        ('Cable Row', 3, 1),
                        ('Lat Pull-down', 3, 1),
                        ('Pull-up', 3, 6),
                        ('Dumbbell Curl', 4, 1),
                        ('Barbell Curl', 4, 1),
                        ('Preacher Curl', 4, 1),
                        ('Skull Crushers', 4, 1),
                        ('Overhead Tricep Extention', 4, 1),
                        ('Standing Dumbbell Shoulder Press', 5, 1),
                        ('Seated Dumbbell Shoulder Press', 5, 1),
                        ('Standing Barbell Shoulder Press', 5, 1),
                        ('Seated Barbell Shoulder Press', 5, 1),
                        ('Hanging Leg Raise', 6, 6),
                         ]
        cursor.executemany('INSERT INTO exercise (exercise_name, workout_type_id, measure_id) VALUES (?, ?, ?)',
                           exercise_data)

        workout_data = [('Chest', 1),
                             ('Legs', 1),
                             ('Back', 1),
                             ('Arms', 1),
                             ('Shoulders', 1),
                             ('Abs', 1),
                             ('Push', 1),
                             ('Pull', 1),
                             ('Distance', 2),
                             ('Sprints', 2),
                             ('Agility', 2),
                             ('Road', 3),
                             ('Stationary', 3),
                             ('Distance', 4),
                             ('Basketball', 5),
                             ('Volleyball', 5),
                             ('Rugby', 5),
                             ('Tennis', 5),
                             ('Martial Arts', 5),
                             ('Soccer', 5),
                             ('Golf', 5),
                             ]
        cursor.executemany('INSERT INTO workout (workout_name, workout_type_id) VALUES (?, ?)',
                           workout_data)

        temp_conn.commit()
        temp_conn.close()


class StartModel():
    def __init__(self, db_conn):
        ...
        self.db_conn = db_conn
        self.tracked_exercises = ['Dumbbell Bench Press (8-reps)',
                                  'Bulgarian Split',
                                  '1 Rep Deadlift',]

    def get_top_exercises(self):
        cursor = self.db_conn.cursor()

        cursor.execute('''SELECT e.exercise_name, COUNT(*) AS count
                        FROM exercise_session es
                        JOIN exercise e ON e.exercise_id = es.exercise_id
                        GROUP BY e.exercise_id
                        HAVING COUNT(*) >= 5
                        ORDER BY count DESC
                        LIMIT 15''')

        data = [i[0] for i in cursor.fetchall()]

        if data == []:
            cursor.execute('''SELECT e.exercise_name, COUNT(*) AS count
                            FROM exercise_session es
                            JOIN exercise e ON e.exercise_id = es.exercise_id
                            GROUP BY e.exercise_id
                            ORDER BY count DESC
                            LIMIT 15''')

            data = [i[0] for i in cursor.fetchall()]

        return data

    def get_repetitions_by_exercise(self, exercise_name):
        cursor = self.db_conn.cursor()

        cursor.execute('''SELECT DISTINCT repetitions
                          FROM exercise_session es
                          JOIN exercise e ON es.exercise_id = e.exercise_id
                          WHERE e.exercise_name = ?''', (exercise_name,))

        data = [i[0] for i in cursor.fetchall()]
        return data

    def get_exercise_sessions_by_exercise(self, entry_dict):
        cursor = self.db_conn.cursor()

        cursor.execute('''SELECT es.date, es.value
        FROM exercise_session es
        JOIN exercise e ON es.exercise_id = e.exercise_id
        WHERE e.exercise_name = ?
        AND es.repetitions = ?
        ORDER BY es.date''',
                       (entry_dict['exercise_name'], entry_dict['repetitions']))
        
        data = {'dates': [], 'values': []}


        for i in cursor.fetchall():
            data['dates'].append(i[0])
            data['values'].append(i[1])

        cursor.close()
        return data


class WorkoutSessionModel():

    def __init__(self, db_conn):
        self.db_conn = db_conn
        self.workout_quality_list = ['1: I initiated the workout',
                                     '2: I completed part of the workout, but half-assed it',
                                     '3: I half assed the entired workout',
                                     '4: I completed 50% of the workout at an average intensity',
                                     '5: I completed 75% of the workout at an average intensity',
                                     '6: I completed the workout at an average intensity',
                                     '7: I completed the workout at an above average intensity',
                                     '8: I had a high intensity or completed extra sets during the workout',
                                     '9: I had a high intensity and completed extra sets during the workout',
                                     '10: I had the workout of my life']

    def create(self, entry_dict):
        cursor = self.db_conn.cursor()

        # Convert workout quality to integer type
        workout_quality_num = ''
        for i in entry_dict['workout_quality']:
            try:
                int(i)
                workout_quality_num = workout_quality_num + i
            except:
                break
        workout_quality_num = int(workout_quality_num)

        # Get workout_id
        cursor.execute('''SELECT workout_id
                     FROM workout
                     WHERE workout_name = ?''',
                       (entry_dict['workout_name'],))
        workout_id = cursor.fetchone()[0]

        entry_tuple = (workout_id,
                       entry_dict['time_elapsed'],
                       workout_quality_num,
                       entry_dict['workout_quality'],
                       entry_dict['date'])
        cursor.execute('''INSERT INTO workout_session (workout_id,
         time_elapsed,
          workout_quality_num,
           workout_quality_text,
            date) 
            VALUES (?, ?, ?, ?, ?)''', entry_tuple)

        self.db_conn.commit()
        cursor.close()

        # response = {'success': True, 'message': None}
        # return response

    def get(self):
        pass

    def delete(self, entry_id):
        cursor = self.db_conn.cursor()

        cursor.execute('''DELETE FROM workout_session WHERE workout_session_id = ?''', (entry_id,))

        self.db_conn.commit()
        cursor.close()

    def update(self, entry_dict):
        cursor = self.db_conn.cursor()

        # Convert workout quality to integer type
        workout_quality_num = ''
        for i in entry_dict['workout_quality']:
            try:
                int(i)
                workout_quality_num = workout_quality_num + i
            except:
                break
        workout_quality_num = int(workout_quality_num)

        # Get exercise_id from the database
        cursor.execute('''SELECT w.workout_id
                        FROM workout w
                        WHERE w.workout_name = ?''',
                       (entry_dict['workout_name'],))
        workout_id = cursor.fetchone()[0]

        entry_tuple = (workout_id,
                       entry_dict['time_elapsed'],
                       workout_quality_num,
                       entry_dict['workout_quality'],
                       entry_dict['date'],
                       entry_dict['workout_session_id'])

        cursor.execute('''UPDATE workout_session
                            SET workout_id = ?,
                            time_elapsed = ?,
                            workout_quality_num = ?,
                            workout_quality_text = ?,
                            date = ?
                            WHERE workout_session_id = ?''',
                       (entry_tuple))

        self.db_conn.commit()
        cursor.close()

    def get_all(self):
        table_name = 'workout_session'
        cursor = self.db_conn.cursor()

        # cursor.execute(f"PRAGMA table_info({table_name})")
        # columns = [col[1] for col in cursor.fetchall()]
        columns = ['workout_session_id', 'date', 'workout_name', 'time_elapsed', 'workout_quality']

        cursor.execute(f'''SELECT ws.workout_session_id, ws.date, w.workout_name, ws.time_elapsed,
                            ws.workout_quality_text
                            FROM workout_session ws
                            JOIN workout w ON w.workout_id = ws.workout_id''')
        entry_data = [i for i in cursor.fetchall()]

        data = {'columns': columns, 'entry_data': entry_data}

        cursor.close()

        return data

    def get_workout_names(self) -> list:
        cursor = self.db_conn.cursor()

        cursor.execute('''SELECT workout_name FROM workout''')
        workout_names = [i[0] for i in cursor.fetchall()]

        cursor.close()
        return workout_names

    def get_today(self):
        return date.today()


class ExerciseSessionModel():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def create(self, entry_dict):
        cursor = self.db_conn.cursor()

        # Get exercise_id from the database
        cursor.execute('''SELECT e.exercise_id
                        FROM exercise e
                        JOIN workout_type wt ON e.workout_type_id = wt.workout_type_id
                        JOIN workout_class wc ON wt.workout_class_id = wc.workout_class_id
                        JOIN measure m ON e.measure_id = m.measure_id
                        WHERE wc.workout_class_name = ?
                        AND wt.workout_type_name = ?
                        AND e.exercise_name = ?
                        AND m.measure_name = ?''',
                       (entry_dict['workout_class_name'], entry_dict['workout_type_name'],
                        entry_dict['exercise_name'], entry_dict['measure_name']))
        exercise_id = cursor.fetchone()[0]

        entry_tuple = (exercise_id,
                       entry_dict['value'],
                       entry_dict['repetitions'],
                       entry_dict['date'])

        cursor.execute('''INSERT INTO exercise_session (exercise_id, value, repetitions, date)
                    VALUES (?, ?, ?, ?)''', entry_tuple)

        self.db_conn.commit()
        cursor.close()

        # response = {'success': True, 'message': None}
        # return response

    def get(self):
        pass

    def delete(self, entry_id):
        cursor = self.db_conn.cursor()

        cursor.execute('''DELETE FROM exercise_session WHERE exercise_session_id = ?''', (entry_id,))

        self.db_conn.commit()
        cursor.close()

    def update(self, entry_dict):
        cursor = self.db_conn.cursor()

        # Get exercise_id from the database
        cursor.execute('''SELECT e.exercise_id
                        FROM exercise e
                        JOIN workout_type wt ON e.workout_type_id = wt.workout_type_id
                        JOIN workout_class wc ON wt.workout_class_id = wc.workout_class_id
                        JOIN measure m ON e.measure_id = m.measure_id
                        WHERE wc.workout_class_name = ?
                        AND wt.workout_type_name = ?
                        AND e.exercise_name = ?
                        AND m.measure_name = ?''',
                       (entry_dict['workout_class_name'], entry_dict['workout_type_name'], entry_dict['exercise_name'],
                        entry_dict['measure_name']))
        exercise_id = cursor.fetchone()[0]

        entry_tuple = (exercise_id,
                       entry_dict['value'],
                       entry_dict['repetitions'],
                       entry_dict['date'],
                       entry_dict['exercise_session_id'])

        cursor.execute('''UPDATE exercise_session
                            SET exercise_id = ?,
                            value = ?,
                            repetitions = ?,
                            date = ?
                            WHERE exercise_session_id = ?''',
                       (entry_tuple))

        self.db_conn.commit()
        cursor.close()

    def get_all(self):
        table_name = 'exercise_session'
        cursor = self.db_conn.cursor()

        # cursor.execute(f"PRAGMA table_info({table_name})")
        # columns = [col[1] for col in cursor.fetchall()]
        columns = ['exercise_session_id', 'date', 'exercise_name', 'value', 'measure_name', 'repetitions',
                   'workout_type_name', 'workout_class_name']

        cursor.execute(f'''SELECT es.exercise_session_id, es.date, e.exercise_name, es.value, m.measure_name, 
                            es.repetitions, wt.workout_type_name, wc.workout_class_name
                            FROM exercise_session es
                            JOIN exercise e ON e.exercise_id = es.exercise_id
                            JOIN workout_type wt ON wt.workout_type_id = e.workout_type_id
                            JOIN workout_class wc ON wc.workout_class_id = wt.workout_class_id
                            JOIN measure m ON m.measure_id = e.measure_id;''')
        entry_data = [i for i in cursor.fetchall()]

        data = {'columns': columns, 'entry_data': entry_data}

        cursor.close()

        return data

    def get_workout_classes(self) -> list:
        cursor = self.db_conn.cursor()

        cursor.execute('''SELECT workout_class_name FROM workout_class''')
        workout_classes = [i[0] for i in cursor.fetchall()]

        cursor.close()
        return workout_classes

    def get_workout_types_by_class(self, workout_class_name):
        cursor = self.db_conn.cursor()

        cursor.execute('''SELECT workout_type_name
                        FROM workout_type
                        WHERE workout_class_id = (SELECT workout_class_id 
                                                  FROM workout_class 
                                                  WHERE workout_class_name = ?)''',
                       (workout_class_name,))

        workout_types = [i[0] for i in cursor.fetchall()]

        cursor.close()
        return workout_types

    def get_exercises_by_workout_type(self, workout_type_name):
        cursor = self.db_conn.cursor()

        cursor.execute('''SELECT exercise_name
                        FROM exercise
                        WHERE workout_type_id = (SELECT workout_type_id 
                                                  FROM workout_type 
                                                  WHERE workout_type_name = ?)''',
                       (workout_type_name,))

        exercises = [i[0] for i in cursor.fetchall()]

        cursor.close()
        return exercises

    def get_exercise_measure(self, exercise_name):
        cursor = self.db_conn.cursor()

        cursor.execute('''SELECT m.measure_name
                        FROM measure m
                        JOIN exercise e ON m.measure_id = e.measure_id
                        WHERE e.exercise_name = ?''',
                       (exercise_name,))

        measure = cursor.fetchall()[0][0]

        cursor.close()
        return measure

    def get_today(self):
        return date.today()

    def get_measures(self):
        cursor = self.db_conn.cursor()

        cursor.execute('''SELECT measure_name FROM measure''')
        measures = [i[0] for i in cursor.fetchall()]

        cursor.close()
        return measures


class DateModel():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def create(self, entry_dict):
        cursor = self.db_conn.cursor()

        entry_tuple = (entry_dict['date'],
                       entry_dict['calories'],
                       entry_dict['protein'],
                       entry_dict['weight'],
                       entry_dict['sleep'])

        cursor.execute('''INSERT INTO day (date, calories, protein, weight, sleep)
                    VALUES (?, ?, ?, ?, ?)''', entry_tuple)

        self.db_conn.commit()
        cursor.close()

        # response = {'success': True, 'message': None}
        # return response

    def get(self):
        pass

    def delete(self, entry_id):
        cursor = self.db_conn.cursor()

        cursor.execute('''DELETE FROM day WHERE day_id = ?''', (entry_id,))

        self.db_conn.commit()
        cursor.close()

    def update(self, entry_dict):
        cursor = self.db_conn.cursor()

        entry_tuple = (entry_dict['date'],
                       entry_dict['calories'],
                       entry_dict['protein'],
                       entry_dict['weight'],
                       entry_dict['sleep'],
                       entry_dict['day_id'],
                       )

        cursor.execute('''UPDATE day
                            SET date = ?,
                            calories = ?,
                            protein = ?,
                            weight = ?,
                            sleep = ?
                            WHERE day_id = ?''',
                       (entry_tuple))

        self.db_conn.commit()
        cursor.close()

    def get_all(self):
        table_name = 'day'
        cursor = self.db_conn.cursor()

        # cursor.execute(f"PRAGMA table_info({table_name})")
        # columns = [col[1] for col in cursor.fetchall()]
        columns = ['day_id', 'date', 'calories', 'protein', 'weight', 'sleep']
        cursor.execute(f'''SELECT day_id, date, calories, protein, weight, sleep
                           FROM day''')
        entry_data = [i for i in cursor.fetchall()]
        data = {'columns': columns, 'entry_data': entry_data}

        cursor.close()
        return data

    def get_today(self):
        return date.today()


class WorkoutModel():

    def __init__(self, db_conn):
        self.db_conn = db_conn

    def create(self, entry_dict):
        cursor = self.db_conn.cursor()

        workout_name, workout_class_name, workout_type_name = (entry_dict['workout_name'],
                                                               entry_dict['workout_class_name'],
                                                               entry_dict['workout_type_name'])

        # Get workout_type_id by workout_type_name and workout_class_id
        cursor.execute('''SELECT workout_type_id
                     FROM workout_type
                     WHERE workout_type_name = ? 
                     AND workout_class_id = (SELECT workout_class_id 
                                             FROM workout_class 
                                             WHERE workout_class_name = ?)''',
                     (workout_type_name, workout_class_name))

        workout_type_id = cursor.fetchone()[0]


        entry_tuple = (workout_name, workout_type_id)
        cursor.execute('''INSERT INTO workout (workout_name, workout_type_id)
                    VALUES (?, ?)''', entry_tuple)

        self.db_conn.commit()
        cursor.close()

        # response = {'success': True, 'message': None}
        # return response

    def get_workout_classes(self) -> tuple:
        cursor = self.db_conn.cursor()

        cursor.execute('''SELECT workout_class_name FROM workout_class''')
        workout_classes = [i[0] for i in cursor.fetchall()]

        cursor.close()
        return workout_classes

    def get_workout_types_by_class(self, workout_class_name):
        cursor = self.db_conn.cursor()

        cursor.execute('''SELECT workout_type_name
                        FROM workout_type
                        WHERE workout_class_id = (SELECT workout_class_id 
                                                  FROM workout_class 
                                                  WHERE workout_class_name = ?)''',
                       (workout_class_name,))

        workout_types = [i[0] for i in cursor.fetchall()]

        cursor.close()
        return workout_types


class ExerciseModel():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def create(self, entry_dict):
        cursor = self.db_conn.cursor()

        exercise_name, workout_class_name, workout_type_name, measure_name = (entry_dict['exercise_name'],
                                                                             entry_dict['workout_class_name'],
                                                                             entry_dict['workout_type_name'],
                                                                             entry_dict['measure_name'])

        # Get workout_type_id and measure_id from the database
        cursor.execute('''SELECT workout_type_id
                     FROM workout_type
                     WHERE workout_type_name = ? 
                     AND workout_class_id = (SELECT workout_class_id 
                                             FROM workout_class 
                                             WHERE workout_class_name = ?)''',
                     (workout_type_name, workout_class_name))
        workout_type_id = cursor.fetchone()[0]
        cursor.execute('''SELECT measure_id FROM measure WHERE measure_name = ?''',
                     (measure_name,))
        measure_id = cursor.fetchone()[0]


        entry_tuple = (exercise_name, workout_type_id, measure_id)
        cursor.execute('''INSERT INTO exercise (exercise_name, workout_type_id, measure_id)
                    VALUES (?, ?, ?)''', entry_tuple)

        self.db_conn.commit()
        cursor.close()

        # response = {'success': True, 'message': None}
        # return response

    def get_workout_classes(self) -> list:
        cursor = self.db_conn.cursor()

        cursor.execute('''SELECT workout_class_name FROM workout_class''')
        workout_classes = [i[0] for i in cursor.fetchall()]

        cursor.close()
        return workout_classes

    def get_workout_types_by_class(self, workout_class_name):
        cursor = self.db_conn.cursor()

        cursor.execute('''SELECT workout_type_name
                        FROM workout_type
                        WHERE workout_class_id = (SELECT workout_class_id 
                                                  FROM workout_class 
                                                  WHERE workout_class_name = ?)''',
                       (workout_class_name,))

        workout_types = [i[0] for i in cursor.fetchall()]

        cursor.close()
        return workout_types

    def get_measures(self):
        cursor = self.db_conn.cursor()

        cursor.execute('''SELECT measure_name FROM measure''')
        measures = [i[0] for i in cursor.fetchall()]

        cursor.close()
        return measures


class GoalModel():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def create(self, entry_dict):
        cursor = self.db_conn.cursor()

        date, calories, protein, weight, sleep, = (entry_dict['date'],
                                                     entry_dict['calories'],
                                                     entry_dict['protein'],
                                                     entry_dict['weight'],
                                                     entry_dict['sleep'])

        entry_tuple = (date, calories, protein, weight, sleep)
        cursor.execute('''INSERT INTO day (date, calories, protein, weight, sleep)
                    VALUES (?, ?, ?, ?, ?)''', entry_tuple)

        self.db_conn.commit()
        cursor.close()

        # response = {'success': True, 'message': None}
        # return response

    def get_goal_types(self):
        return ['Exercise', 'Workouts', 'Weight']


class ExerciseGoalModel():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def create(self, entry_dict):

        cursor = self.db_conn.cursor()

        exercise_name, measure, goal_value, target_end_date, start_date = (entry_dict['exercise_name'],
                                                                      entry_dict['measure'],
                                                                         entry_dict['value'],
                                                                         entry_dict['target_date'],
                                                                         entry_dict['start_date'])
        #Get exercise_id from exercise_name and measure
        cursor.execute('''SELECT e.exercise_id FROM exercise e 
                            JOIN measure m ON e.measure_id = m.measure_id
                            WHERE e.exercise_name = ? AND m.measure_name = ?''',
                       (exercise_name, measure))
        exercise_id = cursor.fetchone()[0]

        entry_tuple = (exercise_id, goal_value, target_end_date, start_date)
        cursor.execute('''INSERT INTO exercise_goal (exercise_id, goal_value, target_end_date, start_date)
                    VALUES (?, ?, ?, ?)''', entry_tuple)

        self.db_conn.commit()
        cursor.close()

        # response = {'success': True, 'message': None}
        # return response

    def get_exercises(self):
        cursor = self.db_conn.cursor()

        cursor.execute('''SELECT exercise_name FROM exercise''')
        exercises = [i[0] for i in cursor.fetchall()]

        cursor.close()
        return exercises

    def get_measures_by_exercise(self, exercise_name):
        cursor = self.db_conn.cursor()


        cursor.execute('''SELECT m.measure_name
                            FROM measure m
                            INNER JOIN exercise e ON m.measure_id = e.measure_id
                            WHERE e.exercise_name = ?''',
                       (exercise_name,))
        measures = [i[0] for i in cursor.fetchall()]

        cursor.close()
        return measures

    def get_today(self):
        return date.today()


class WorkoutClassGoalModel():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def create(self, entry_dict):

        cursor = self.db_conn.cursor()

        workout_class_name, goal_value, target_end_date, start_date = (entry_dict['workout_class_name'],
                                                                         entry_dict['value'],
                                                                         entry_dict['target_date'],
                                                                         entry_dict['start_date'])
        cursor.execute('''SELECT workout_class_id
                        FROM workout_class
                        WHERE workout_class_name = ?''',
                       (workout_class_name,))
        workout_class_id = cursor.fetchone()[0]

        entry_tuple = (workout_class_id, goal_value, target_end_date, start_date)
        cursor.execute('''INSERT INTO workout_class_goal (workout_class_id, goal_value, target_end_date, start_date)
                    VALUES (?, ?, ?, ?)''', entry_tuple)

        self.db_conn.commit()
        cursor.close()

        # response = {'success': True, 'message': None}
        # return response

    def get_workout_classes(self):
        cursor = self.db_conn.cursor()

        cursor.execute('''SELECT workout_class_name FROM workout_class''')
        workout_classes = [i[0] for i in cursor.fetchall()]

        cursor.close()
        return workout_classes

    def get_today(self):
        return date.today()


class WeightGoalModel():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def create(self, entry_dict):

        cursor = self.db_conn.cursor()

        goal_value, target_end_date, start_date = (entry_dict['value'],
                                                     entry_dict['target_date'],
                                                     entry_dict['start_date'])

        entry_tuple = (goal_value, target_end_date, start_date)
        cursor.execute('''INSERT INTO weight_goal (goal_value, target_end_date, start_date)
                    VALUES (?, ?, ?)''', entry_tuple)

        self.db_conn.commit()
        cursor.close()

        # response = {'success': True, 'message': None}
        # return response

    def get_today(self):
        return date.today()


class EmptyModel():
    def __init__(self, db_conn):
        ...
        self.db_conn = db_conn
        self.tracked_exercises = ['1 Rep Bench Press',
                                  '1 Rep Squat',
                                  '1 Rep Deadlift',]


class TableDataModel():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def get_table_names(self):
        cursor = self.db_conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        table_names = [i[0] for i in cursor.fetchall()]

        cursor.close()
        return table_names

    def get_table_data(self, table_name):
        cursor = self.db_conn.cursor()

        cursor.execute(f"SELECT * FROM {table_name}")
        table_data = [i for i in cursor.fetchall()]
        print(table_data)

        cursor.close()
        return []
