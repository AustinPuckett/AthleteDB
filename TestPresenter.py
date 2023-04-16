import csv
import os
# import tkinter as tk
# from tkinter import ttk, font
import Visualization as viz
from TestView import *


class LoginPresenter():
    def __init__(self, master, model, view):
        self.master = master
        self.model = model
        self.view = view

    def login(self, event):
        username = self.view.username_entry.get()
        # password = self.view.bar.get()
        login_response = self.model.validate_login(username)
        if login_response['success'] == True:
            self.master.change_view(StartView)
        else:
            # trigger the view.error method and show the login response
            print(login_response['message'])

    def show_create_account_view(self, event):
        self.master.change_view(CreateAccountView)

    def run(self):
        if self.model.get_user_count() == 0:
            self.master.change_view(CreateView)
        else:
            self.view.init_ui(self)
            self.view.username_entry.config(values=self.model.get_usernames())
            self.view.grid()


    def exit_view(self):
        self.view.grid_forget()


class CreateAccountPresenter():
    def __init__(self, master, model, view):
        self.master = master
        self.model = model
        self.view = view

    def create_account(self, event):
        username = self.view.username_entry.get()
        self.model.create_account(username)
        self.master.change_view(LoginView)

    def show_login_view(self, event):
        self.master.change_view(LoginView)

    def run(self):
        self.view.init_ui(self)
        self.view.grid()

    def exit_view(self):
        self.view.grid_forget()


class StartPresenter():
    def __init__(self, master, model, view):
        self.master = master
        self.model = model
        self.view = view

    def show_log_workout_view(self, event):
        self.master.change_view(WorkoutSessionView)

    def show_log_exercise_view(self, event):
        self.master.change_view(ExerciseSessionView)

    def show_date_view(self, event):
        self.master.change_view(DateView)
        
    def get_repetitions(self, event):
        exercise_name = self.view.exercise_selection.get()
        repetitions = self.model.get_repetitions_by_exercise(exercise_name)
        
        self.view.rep_selection.config(values=repetitions)
        self.view.rep_selection.set('')

    def render_graph(self, event):
        exercise_name = self.view.exercise_selection.get()
        repetitions = self.view.rep_selection.get()
        entry_dict = {'exercise_name': exercise_name, 'repetitions': repetitions}

        if (event != None) and (self.view.canvas != None):
            self.view.canvas.get_tk_widget().destroy()

        data = self.model.get_exercise_sessions_by_exercise(entry_dict)
        dates = data['dates']
        values = data['values']

        title = exercise_name + ' ' + str(repetitions) + ' reps'
        self.view.canvas = viz.line_plot(self.view.frame2, dates, values, title=title)
        self.view.canvas.get_tk_widget().grid(row=4, column=0, padx=1, pady=3, rowspan=1, columnspan=1)

    def run(self):
        self.view.init_ui(self)

        exercises = self.model.get_top_exercises()
        if exercises == []: #TODO: refactor model response as dictionary with a key:value pair to indicate empty result
            pass
        else:
            self.view.exercise_selection.config(values=exercises)
            self.view.exercise_selection.set(exercises[0])
            self.view.rep_selection.config(values=self.model.get_repetitions_by_exercise(exercises[0]))
            self.view.rep_selection.set(self.model.get_repetitions_by_exercise(exercises[0])[0])
            self.render_graph(None)
        self.view.grid()

    def exit_view(self):
        self.view.grid_forget()


class WorkoutSessionPresenter():
    def __init__(self, master, model, view):
        self.master = master
        self.model = model
        self.view = view

    def submit_entry(self, event):
        workout_session_id = self.view.id_entry.cget('text')
        workout_name = self.view.workout_name_entry.get()
        time_elapsed = self.view.time_elapsed_entry.get()
        workout_quality = self.view.workout_quality_entry.get()
        date = self.view.date_entry.get()

        entry_dict = {'workout_session_id': workout_session_id,
                      'workout_name': workout_name,
                      'time_elapsed': time_elapsed,
                      'workout_quality': workout_quality,
                      'date': date,
                      }
        # If id is populated, edit the existing entry. Warning! Dependent on id_entry = '' convention
        if entry_dict['workout_session_id'] == '':
            self.model.create(entry_dict)
        else:
            self.model.update(entry_dict)

        self.clear_view_entries(None)
        self.load_tree_entries()

    def get_entry(self, event=None):
        tree_entry_id = self.view.tree.focus()

        tree_entry_vals = self.view.tree.item(tree_entry_id)['values']
        tree_entry_dict = dict(zip(self.tree_columns, tree_entry_vals))

        self.clear_view_entries(None)

        self.view.id_entry.config(text=tree_entry_dict['workout_session_id'])
        self.view.workout_name_entry.set(tree_entry_dict['workout_name'])
        self.view.date_entry.insert(0, tree_entry_dict['date'])
        self.view.time_elapsed_entry.insert(0, tree_entry_dict['time_elapsed'])
        self.view.workout_quality_entry.insert(0, tree_entry_dict['workout_quality'])

    def delete_entry(self, event=None):
        tree_entry_id = self.view.tree.focus()

        tree_entry_vals = self.view.tree.item(tree_entry_id)['values']
        tree_entry_dict = dict(zip(self.tree_columns, tree_entry_vals))

        entry_id = tree_entry_dict['workout_session_id']

        self.model.delete(entry_id)

        self.load_tree_entries()

    def show_tree_menu(self, event):
        # Retrieve selected item from treeview
        item = self.view.tree.focus()

        # If item is selected, display context menu
        if item:
            self.view.tree_menu.post(event.x_root, event.y_root)

    def show_start_view(self, event):
        self.master.change_view(StartView)

    def clear_view_entries(self, event):
        self.view.id_entry.configure(text='')
        self.view.workout_name_entry.delete(0, 'end')
        self.view.time_elapsed_entry.delete(0, 'end')
        self.view.workout_quality_entry.delete(0, 'end')
        self.view.date_entry.delete(0, 'end')

    def instantiate_tree(self):
        data = self.model.get_all()
        self.tree_columns = data['columns']
        self.view.tree.config(columns=self.tree_columns, selectmode='browse')

        for col in self.tree_columns:
            self.view.tree.column(col, minwidth=0, width=110, stretch=False)
            self.view.tree.heading(col, text=col.title())

    def load_tree_entries(self):
        data = self.model.get_all()
        for item in self.view.tree.get_children():
            self.view.tree.delete(item)

        for row in data['entry_data']:
            self.view.tree.insert('', 0, values=row)
        # self.view.grid(row=0, column=0, padx=1, pady=2)

    def run(self):
        self.view.init_ui(self)

        self.instantiate_tree()
        self.load_tree_entries()

        self.view.workout_name_entry.set("Select a Workout")
        self.view.workout_name_entry.config(values=self.model.get_workout_names())
        self.view.date_entry.insert(0, self.model.get_today())
        self.view.workout_quality_entry.set("How was the quality?")
        self.view.workout_quality_entry.config(values=self.model.workout_quality_list)

        self.view.grid()

    def exit_view(self):
        self.view.grid_forget()


class ExerciseSessionPresenter():
    def __init__(self, master, model, view):
        self.master = master
        self.model = model
        self.view = view

    def submit_entry(self, event):
        exercise_session_id = self.view.id_entry.cget('text')
        exercise_name = self.view.exercise_entry.get()
        workout_type_name = self.view.workout_type_entry.get()
        workout_class_name = self.view.workout_class_entry.get()
        measure_name = self.view.measure_entry.cget('text')
        date = self.view.date_entry.get()
        value = self.view.value_entry.get()
        repetitions = self.view.reps_entry.get()

        entry_dict = {'exercise_session_id': exercise_session_id,
                      'exercise_name': exercise_name,
                      'workout_class_name': workout_class_name,
                      'workout_type_name': workout_type_name,
                      'measure_name': measure_name,
                      'value': value,
                      'date': date,
                      'repetitions': repetitions,
                      }

        # If id is populated, edit the existing entry. Warning! Dependent on id_entry = '' convention
        if entry_dict['exercise_session_id'] == '':
            self.model.create(entry_dict)
        else:
            self.model.update(entry_dict)

        self.clear_view_entries(None)
        self.load_tree_entries()

    def get_entry(self, event=None):
        tree_entry_id = self.view.tree.focus()

        tree_entry_vals = self.view.tree.item(tree_entry_id)['values']
        tree_entry_dict = dict(zip(self.tree_columns, tree_entry_vals))

        self.clear_view_entries(None)

        self.view.id_entry.config(text=tree_entry_dict['exercise_session_id'])
        self.view.exercise_entry.set(tree_entry_dict['exercise_name'])
        self.view.workout_type_entry.set(tree_entry_dict['workout_type_name'])
        self.view.workout_class_entry.set(tree_entry_dict['workout_class_name'])
        self.view.measure_entry.config(text=tree_entry_dict['measure_name'])
        self.view.date_entry.insert(0, tree_entry_dict['date'])
        self.view.value_entry.insert(0, tree_entry_dict['value'])
        self.view.reps_entry.insert(0, tree_entry_dict['repetitions'])

    def delete_entry(self, event=None):
        tree_entry_id = self.view.tree.focus()

        tree_entry_vals = self.view.tree.item(tree_entry_id)['values']
        tree_entry_dict = dict(zip(self.tree_columns, tree_entry_vals))

        entry_id = tree_entry_dict['exercise_session_id']

        self.model.delete(entry_id)

        self.load_tree_entries()

    def get_workout_type_list(self, event):
        # Call the model to get the workout type list where workout_class = workout_class
        self.view.workout_type_entry.delete(0, 'end')
        self.view.exercise_entry.delete(0, 'end')
        workout_class = self.view.workout_class_entry.get()
        workout_types = self.model.get_workout_types_by_class(workout_class)
        self.view.workout_type_entry.config(values=workout_types)

    def get_exercise_list(self, event):
        # Call the model to get the exercise list where workout_type_id = workout_type_id
        self.view.exercise_entry.delete(0, 'end')
        workout_type = self.view.workout_type_entry.get()
        exercises = self.model.get_exercises_by_workout_type(workout_type)
        self.view.exercise_entry.config(values=exercises)

    def get_measure_list(self, event):
        # Call the model to get the measure list where exercise_id = exercise_id
        self.view.measure_entry.config(text='')
        exercise = self.view.exercise_entry.get()
        measure = self.model.get_exercise_measure(exercise)
        self.view.measure_entry.config(text=measure)

    def show_tree_menu(self, event):
        # Retrieve selected item from treeview
        item = self.view.tree.focus()

        # If item is selected, display context menu
        if item:
            self.view.tree_menu.post(event.x_root, event.y_root)

    def show_start_view(self, event):
        self.master.change_view(StartView)

    def clear_view_entries(self, event):
        self.view.id_entry.configure(text='')
        self.view.date_entry.delete(0, 'end')
        self.view.exercise_entry.delete(0, 'end')
        self.view.workout_type_entry.delete(0, 'end')
        self.view.workout_class_entry.delete(0, 'end')
        self.view.measure_entry.config(text='')
        self.view.value_entry.delete(0, 'end')
        self.view.reps_entry.delete(0, 'end')

    def instantiate_tree(self):
        data = self.model.get_all()
        self.tree_columns = data['columns']
        self.view.tree.config(columns=self.tree_columns, selectmode='browse')

        for col in self.tree_columns:
            self.view.tree.column(col, minwidth=0, width=110, stretch=False)
            self.view.tree.heading(col, text=col.title())

    def load_tree_entries(self):
        data = self.model.get_all()
        for item in self.view.tree.get_children():
            self.view.tree.delete(item)

        for row in data['entry_data']:
            self.view.tree.insert('', 0, values=row)
        # self.view.grid(row=0, column=0, padx=1, pady=2)

    def run(self):
        self.view.init_ui(self)

        self.instantiate_tree()
        self.load_tree_entries()

        self.view.date_entry.insert(0, self.model.get_today())
        self.view.workout_class_entry.config(values=self.model.get_workout_classes())

        self.view.grid()

    def exit_view(self):
        self.view.grid_forget()


class DatePresenter():
    def __init__(self, master, model, view):
        self.master = master
        self.model = model
        self.view = view

    def submit_entry(self, event):
        day_id = self.view.id_entry.cget('text')
        date = self.view.date_entry.get()
        calories = self.view.calories_entry.get()
        protein = self.view.protein_entry.get()
        weight = self.view.weight_entry.get()
        sleep = self.view.sleep_entry.get()

        entry_dict = {'day_id': day_id,
                      'date': date,
                      'calories': calories,
                      'protein': protein,
                      'weight': weight,
                      'sleep': sleep,
                      }

        # If id is populated, edit the existing entry. Warning! Dependent on id_entry = '' convention
        if entry_dict['day_id'] == '':
            self.model.create(entry_dict)
        else:
            self.model.update(entry_dict)

        self.clear_view_entries(None)
        self.load_tree_entries()

        # self.view.calories_entry.delete(0, 'end')
        # self.view.protein_entry.delete(0, 'end')
        # self.view.weight_entry.delete(0, 'end')
        # self.view.sleep_entry.delete(0, 'end')

    def get_entry(self, event=None):
        tree_entry_id = self.view.tree.focus()

        tree_entry_vals = self.view.tree.item(tree_entry_id)['values']
        tree_entry_dict = dict(zip(self.tree_columns, tree_entry_vals))

        self.clear_view_entries(None)

        self.view.id_entry.config(text=tree_entry_dict['day_id'])
        self.view.date_entry.insert(0, tree_entry_dict['date'])
        self.view.calories_entry.insert(0, tree_entry_dict['calories'])
        self.view.protein_entry.insert(0, tree_entry_dict['protein'])
        self.view.weight_entry.insert(0, tree_entry_dict['weight'])
        self.view.sleep_entry.insert(0, tree_entry_dict['sleep'])

    def delete_entry(self, event=None):
        tree_entry_id = self.view.tree.focus()

        tree_entry_vals = self.view.tree.item(tree_entry_id)['values']
        tree_entry_dict = dict(zip(self.tree_columns, tree_entry_vals))

        entry_id = tree_entry_dict['day_id']

        self.model.delete(entry_id)

        self.load_tree_entries()

    def show_tree_menu(self, event):
        # Retrieve selected item from treeview
        item = self.view.tree.focus()

        # If item is selected, display context menu
        if item:
            self.view.tree_menu.post(event.x_root, event.y_root)

    def show_start_view(self, event):
        self.master.change_view(StartView)

    def clear_view_entries(self, event):
        self.view.id_entry.configure(text='')
        self.view.date_entry.delete(0, 'end')
        self.view.calories_entry.delete(0, 'end')
        self.view.protein_entry.delete(0, 'end')
        self.view.weight_entry.delete(0, 'end')
        self.view.sleep_entry.delete(0, 'end')

    def instantiate_tree(self):
        data = self.model.get_all()
        self.tree_columns = data['columns']
        self.view.tree.config(columns=self.tree_columns, selectmode='browse')

        for col in self.tree_columns:
            self.view.tree.column(col, minwidth=0, width=110, stretch=False)
            self.view.tree.heading(col, text=col.title())

    def load_tree_entries(self):
        data = self.model.get_all()
        for item in self.view.tree.get_children():
            self.view.tree.delete(item)

        for row in data['entry_data']:
            self.view.tree.insert('', 0, values=row)
        # self.view.grid(row=0, column=0, padx=1, pady=2)

    def run(self):
        self.view.init_ui(self)

        self.instantiate_tree()
        self.load_tree_entries()

        self.view.date_entry.insert(0, self.model.get_today())

        self.view.grid()

    def exit_view(self):
        self.view.grid_forget()


class WorkoutPresenter():
    def __init__(self, master, model, view):
        self.master = master
        self.model = model
        self.view = view

    def get_workout_type_list(self, event):
        # Call the model to get the workout type list where workout_class = workout_class
        self.view.workout_type_entry.delete(0, 'end')
        workout_class = self.view.workout_class_entry.get()
        workout_types = self.model.get_workout_types_by_class(workout_class)
        self.view.workout_type_entry.config(values=workout_types)

    def submit_form(self, event):
        workout_name = self.view.workout_name_entry.get()
        workout_type_name = self.view.workout_type_entry.get()
        workout_class_name = self.view.workout_class_entry.get()

        workout_entry = {'workout_name': workout_name,
                         'workout_class_name': workout_class_name,
                         'workout_type_name': workout_type_name,
                         }
        self.model.create(workout_entry)

        self.view.workout_name_entry.delete(0, 'end')
        self.view.workout_type_entry.delete(0, 'end')
        self.view.workout_class_entry.delete(0, 'end')

    def show_start_view(self, event):
        self.master.change_view(StartView)

    def run(self):
        self.view.init_ui(self)
        self.view.workout_class_entry.config(values=self.model.get_workout_classes())
        self.view.grid()

    def exit_view(self):
        self.view.grid_forget()


class ExercisePresenter():
    def __init__(self, master, model, view):
        self.master = master
        self.model = model
        self.view = view

    def get_workout_type_list(self, event):
        # Call the model to get the workout type list where workout_class = workout_class
        self.view.workout_type_entry.delete(0, 'end')
        workout_class = self.view.workout_class_entry.get()
        workout_types = self.model.get_workout_types_by_class(workout_class)
        self.view.workout_type_entry.config(values=workout_types)

    def submit_form(self, event):
        exercise_name = self.view.exercise_name_entry.get()
        workout_type_name = self.view.workout_type_entry.get()
        workout_class_name = self.view.workout_class_entry.get()
        measure_name = self.view.measure_entry.get()

        workout_entry = {'exercise_name': exercise_name,
                         'workout_class_name': workout_class_name,
                         'workout_type_name': workout_type_name,
                         'measure_name': measure_name
                         }
        self.model.create(workout_entry)

        self.view.exercise_name_entry.delete(0, 'end')
        self.view.workout_type_entry.delete(0, 'end')
        self.view.workout_class_entry.delete(0, 'end')
        self.view.measure_entry.delete(0, 'end')

    def show_start_view(self, event):
        self.master.change_view(StartView)

    def run(self):
        self.view.init_ui(self)
        self.view.workout_class_entry.config(values=self.model.get_workout_classes())
        self.view.measure_entry.config(values=self.model.get_measures())
        self.view.grid()

    def exit_view(self):
        self.view.grid_forget()


class GoalPresenter():
    def __init__(self, master, model, view):
        self.master = master
        self.model = model
        self.view = view

        self.goal_type_map = {'Exercise': ExerciseGoalView,
                              'Workouts': WorkoutClassGoalView,
                              'Weight': WeightGoalView}

    def show_goal_type_view(self, event):
        goal_type = self.view.goal_type_entry.get()
        self.master.change_view(self.goal_type_map[goal_type])


    def show_start_view(self, event):
        self.master.change_view(StartView)

    def run(self):
        self.view.init_ui(self)
        self.view.goal_type_entry.set("Select a Goal Type")
        self.view.goal_type_entry.config(values=self.model.get_goal_types())
        self.view.grid()

    def exit_view(self):
        self.view.grid_forget()


class ExerciseGoalPresenter():
    def __init__(self, master, model, view):
        self.master = master
        self.model = model
        self.view = view

    def get_measures(self, event):
        exercise_name = self.view.exercise_name_entry.get()
        self.view.measure_entry.config(values=self.model.get_measures_by_exercise(exercise_name))

    def submit_form(self, event):
        exercise_name = self.view.exercise_name_entry.get()
        value = self.view.value_entry.get()
        measure = self.view.measure_entry.get()
        start_date = self.view.start_date_entry .get()
        target_date = self.view.target_date_entry.get()

        goal_entry = {'exercise_name': exercise_name,
                     'measure': measure,
                     'value': value,
                     'start_date': start_date,
                     'target_date': target_date,
                     }
        self.model.create(goal_entry)

        self.view.exercise_name_entry.delete(0, 'end')
        self.view.value_entry.delete(0, 'end')
        self.view.measure_entry.delete(0, 'end')
        self.view.start_date_entry.delete(0, 'end')
        self.view.target_date_entry.delete(0, 'end')

    def show_start_view(self, event):
        self.master.change_view(StartView)

    def run(self):
        self.view.init_ui(self)
        self.view.exercise_name_entry.config(values=self.model.get_exercises())
        self.view.start_date_entry.insert(0, self.model.get_today())
        self.view.grid()

    def exit_view(self):
        self.view.grid_forget()


class WorkoutClassGoalPresenter():
    def __init__(self, master, model, view):
        self.master = master
        self.model = model
        self.view = view

    def submit_form(self, event):
        workout_class_name = self.view.workout_class_entry.get()
        value = self.view.value_entry.get()
        start_date = self.view.start_date_entry .get()
        target_date = self.view.target_date_entry.get()

        goal_entry = {'workout_class_name': workout_class_name,
                     'value': value,
                     'start_date': start_date,
                     'target_date': target_date,
                     }
        self.model.create(goal_entry)

        self.view.workout_class_entry.delete(0, 'end')
        self.view.value_entry.delete(0, 'end')
        self.view.start_date_entry.delete(0, 'end')
        self.view.target_date_entry.delete(0, 'end')

    def show_start_view(self, event):
        self.master.change_view(StartView)

    def run(self):
        self.view.init_ui(self)
        self.view.workout_class_entry.config(values=self.model.get_workout_classes())
        self.view.start_date_entry.insert(0, self.model.get_today())
        self.view.grid()

    def exit_view(self):
        self.view.grid_forget()


class WeightGoalPresenter():
    def __init__(self, master, model, view):
        self.master = master
        self.model = model
        self.view = view

    def submit_form(self, event):
        value = self.view.value_entry.get()
        start_date = self.view.start_date_entry.get()
        target_date = self.view.target_date_entry.get()

        goal_entry = {'value': value,
                     'start_date': start_date,
                     'target_date': target_date,
                     }
        self.model.create(goal_entry)

        self.view.value_entry.delete(0, 'end')
        self.view.start_date_entry.delete(0, 'end')
        self.view.target_date_entry.delete(0, 'end')

    def show_start_view(self, event):
        self.master.change_view(StartView)

    def run(self):
        self.view.init_ui(self)
        self.view.start_date_entry.insert(0, self.model.get_today())
        self.view.grid()

    def exit_view(self):
        self.view.grid_forget()


class TextPagePresenter():
    def __init__(self, master, model, view):
        self.master = master
        self.model = model
        self.view = view

    def show_start_view(self, event):
        self.master.change_view(StartView)

    def run(self):
        self.view.init_ui(self)
        self.view.grid()

    def exit_view(self):
        self.view.grid_forget()


class TableDataPresenter():
    def __init__(self, master, model, view):
        self.master = master
        self.model = model
        self.view = view


    def show_table(self, event):
        table_name = self.view.table_entry.get()
        # table_data = self.model.get_table_data(table_name)
        table_data = {'columns': ['Col1', 'Col2'], 'entry_data': [[0, 'Oh Yeah'], [1, 'Oh No'], [2, 'Heck Maybe']]}
        for i in range(3, 100):
            table_data['entry_data'].append([i, f'Entry {i}'])
        self.view.show_table(table_data)
        self.view.tree.grid()


    def show_start_view(self, event):
        self.master.change_view(StartView)

    def run(self):
        self.view.init_ui(self)
        self.view.table_entry.set("Select a Table")
        self.view.table_entry.config(values=self.model.get_table_names())
        self.view.grid()

    def exit_view(self):
        self.view.grid_forget()