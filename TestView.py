import tkinter as tk
from tkinter import ttk, font


class BaseView(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

    def init_ui(self, presenter):
        ...

    def error_pop_up(self, error_title=None, error_message=None):
        error_window = tk.Toplevel()
        error_window.title = error_title
        error_message_label = tk.Label(error_window, text=error_message)
        error_message_label.pack()


class LoginView(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

    def init_ui(self, presenter):
        # Widget settings
        title_font = font.Font(family='Segoe UI', size=15, weight='bold')
        label_font = font.Font(family='Segoe UI', size=12, weight='bold')
        entry_font = font.Font(family='Segoe UI', size=11, weight='normal')
        button_font = font.Font(family='Segoe UI', size=11, weight='normal')

        # Instantiate widgets
        self.title_text = ttk.Label(self, text='Login', font=title_font)
        # self.login_label = ttk.Label(self, text='Login', font=label_font)
        self.username_entry = ttk.Combobox(self, font=entry_font, width=15)
        self.username_entry_text = ttk.Label(self, text='Username:', font=label_font)
        self.login_button = ttk.Button(self, text='Login')
        self.create_account_button = ttk.Button(self, text='Create Account')

        # Place widgets
        self.title_text.grid(row=0, column=0, pady=15, columnspan=2, sticky='N')
        # self.login_label.grid(row=0, column=1)
        self.username_entry.grid(row=1, column=1, sticky='W', padx=2, pady=1)
        self.username_entry_text.grid(row=1, column=0, sticky='E', padx=2, pady=1)

        self.create_account_button.grid(row=2, column=0, sticky='E', padx=2, pady=5)
        self.login_button.grid(row=2, column=1, sticky='W', padx=2, pady=5)

        # Presenter Bindings
        self.login_button.bind('<Button-1>', presenter.login)
        self.create_account_button.bind('<Button-1>', presenter.show_create_account_view)


class CreateAccountView(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

    def init_ui(self, presenter):
        # Widget settings
        title_font= font.Font(family='Segoe UI', size=15, weight='bold')
        label_font = font.Font(family='Segoe UI', size=12, weight='bold')
        entry_font = font.Font(family='Segoe UI', size=11, weight='normal')
        button_font = font.Font(family='Segoe UI', size=11, weight='normal')

        # Instantiate widgets
        self.title_text = ttk.Label(self, text='  Set Workout Goal', font=title_font)
        # self.login_label = ttk.Label(self, text='Create New Login', font=label_font)
        self.username_entry = ttk.Entry(self, font=entry_font, width=20)
        self.username_entry_text = ttk.Label(self, text='Username:', font=label_font)
        
        self.login_button = ttk.Button(self, text='Back to Login')
        self.create_account_button = ttk.Button(self, text='Create Account')

        # Place widgets
        self.title_text.grid(row=0, column=0, pady=15, columnspan=2, sticky='N')
        # self.login_label.grid(row=1, column=1)
        self.username_entry.grid(row=1, column=1, sticky='W', padx=2, pady=1)
        self.username_entry_text.grid(row=1, column=0, sticky='E', padx=2, pady=1)

        self.login_button.grid(row=2, column=0, sticky='E', padx=2, pady=5)
        self.create_account_button.grid(row=2, column=1, sticky='W', padx=2, pady=5)

        # Presenter Bindings
        self.login_button.bind('<Button-1>', presenter.show_login_view)
        self.create_account_button.bind('<Button-1>', presenter.create_account)


class StartView(tk.Frame):
    """The start/Home page of the application window.

    Attributes
    ----------
    dashboard_selection: str
        the dashboard to display
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

    def init_ui(self, presenter):

        color1 = '#f7dcb5'
        color2 = '#f7e4b5'

        # Frame 1
        self.frame1 = tk.Frame(self, bd=2, relief='ridge', height = 200, width = 200, bg=color1)

        # Widget settings
        title_font= font.Font(family='Segoe UI', size=15, weight='bold')
        label_font = font.Font(family='Segoe UI', size=12, weight='bold')
        entry_font = font.Font(family='Segoe UI', size=11, weight='normal')
        button_font = font.Font(family='Segoe UI', size=11, weight='normal')
        action_label_font = font.Font(family='Helvetica', size=18, weight='bold')
        my_font = font.Font(family='Helvetica', size=15)

        button_height = 2
        button_width = 20

        label_height = 2
        # label_width = 20

        # frame1 widgets
        actions_label = tk.Label(self.frame1, text='Log Data', height=label_height, width=button_width, anchor='center',
                                 bg=color1) #, height=button_height
        button_log_workout = tk.Button(self.frame1, text='Log Workout', height=button_height, width=button_width,
                                       bg='SystemButtonFace')
        button_log_exercise = tk.Button(self.frame1, text='Log Exercise', height=button_height, width=button_width,
                                        bg='SystemButtonFace')
        button_log_diet = tk.Button(self.frame1, text='Log Diet', height=button_height, width=button_width,
                                    bg='SystemButtonFace')
        
        actions_label.grid(row=0, column=0, padx=1, pady=2)
        button_log_workout.grid(row=1, column=0, padx=1, pady=2)
        button_log_exercise.grid(row=2, column=0, padx=1, pady=2)
        button_log_diet.grid(row=3, column=0, padx=1, pady=2)

        # action_label_font.configure(underline=True)
        actions_label['font'] = action_label_font
        button_log_exercise['font'] = my_font
        button_log_workout['font'] = my_font
        button_log_diet['font'] = my_font

        

        # frame2
        self.frame2 = tk.Frame(self, bd=2, relief='ridge', height=400, width=400, bg=color2)
        
        dashboard_header = tk.Label(self.frame2, text='Dashboard', height=label_height, width=60, anchor='center',
                                    bg=color2)
        self.exercise_selection = ttk.Combobox(self.frame2, height=button_height, width=20)
        self.rep_selection = ttk.Combobox(self.frame2, height=button_height, width=20)
        self.visualization = tk.Label(self.frame2)

        exercise_selection_text = tk.Label(self.frame2, font=label_font)
        rep_selection_text = tk.Label(self.frame2, text='reps', font=label_font)
        
        dashboard_header.grid(row=0, column=0, columnspan=1)
        # exercise_selection_text.grid(row=1, column=0, columnspan=1)
        self.exercise_selection.grid(row=1, column=0, columnspan=1)
        self.rep_selection.grid(row=2, column=0, columnspan=1)
        rep_selection_text.grid(row=3, column=0, columnspan=1)

        dashboard_header['font'] = action_label_font
        
        # Frame placement
        self.frame1.grid(row=0, column=0, rowspan=2, sticky="NSEW")
        self.frame2.grid(row=0, column=1, rowspan=2, sticky="NSEW")

        # Presenter Bindings
        button_log_workout.bind('<Button-1>', presenter.show_log_workout_view)
        button_log_exercise.bind('<Button-1>', presenter.show_log_exercise_view)
        button_log_diet.bind('<Button-1>', presenter.show_date_view)
        self.exercise_selection.bind('<<ComboboxSelected>>',presenter.get_repetitions)
        self.rep_selection.bind('<<ComboboxSelected>>', presenter.render_graph)


class WorkoutView(tk.Frame):
    """The window where a user may enter a new workout into the database.

    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

    def init_ui(self, presenter):

        # Widget settings
        title_font= font.Font(family='Segoe UI', size=15, weight='bold')
        label_font = font.Font(family='Segoe UI', size=12, weight='bold')
        entry_font = font.Font(family='Segoe UI', size=11, weight='normal')
        button_font = font.Font(family='Segoe UI', size=11, weight='normal')

        # Instantiate Widgets
        self.title_text = ttk.Label(self, text='Create New Workout', font=title_font)
        self.workout_name_entry = ttk.Entry(self, font=entry_font, width=20)
        self.workout_class_entry = ttk.Combobox(self, font=entry_font, width=20)
        self.workout_type_entry = ttk.Combobox(self, font=entry_font, width=20)

        workout_name_entry_text = ttk.Label(self, text='Workout Name:', font=label_font)
        workout_class_entry_text = ttk.Label(self, text='Workout Class:', font=label_font)
        workout_type_entry_text = ttk.Label(self, text='Workout Type:', font=label_font)

        self.button_submit = ttk.Button(self, text='Submit')
        self.button_home = ttk.Button(self, text='Home')

        # Place widgets
        self.workout_name_entry.grid(row=1, column=1, sticky='W', padx=2, pady=1)
        self.workout_class_entry.grid(row=2, column=1, sticky='W', padx=2, pady=1)
        self.workout_type_entry.grid(row=3, column=1, sticky='W', padx=2, pady=1)

        self.title_text.grid(row=0, column=0, pady=15, columnspan=2, sticky='N')
        workout_name_entry_text.grid(row=1, column=0, sticky='E', padx=2, pady=1)
        workout_class_entry_text.grid(row=2, column=0, sticky='E', padx=2, pady=1)
        workout_type_entry_text.grid(row=3, column=0, sticky='E', padx=2, pady=1)

        self.button_home.grid(row=4, column=0, sticky='E', padx=2, pady=5)
        self.button_submit.grid(row=4, column=1, sticky='W', padx=2, pady=5)

        # Presenter Bindings
        self.workout_class_entry.bind('<<ComboboxSelected>>', presenter.get_workout_type_list)
        self.button_submit.bind('<Button-1>', presenter.submit_form)
        self.button_home.bind('<Button-1>', presenter.show_start_view)


class ExerciseView(tk.Frame):
    """The window where a user may enter a new exercise into the database.

    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

    def init_ui(self, presenter):

        # Widget settings
        title_font= font.Font(family='Segoe UI', size=15, weight='bold')
        label_font = font.Font(family='Segoe UI', size=12, weight='bold')
        entry_font = font.Font(family='Segoe UI', size=11, weight='normal')
        button_font = font.Font(family='Segoe UI', size=11, weight='normal')

        # Create Entry Widgets
        self.title_text = ttk.Label(self, text='Create New Exercise', font=title_font)
        self.exercise_name_entry = ttk.Entry(self, font=entry_font, width=20)
        self.workout_class_entry = ttk.Combobox(self, font=entry_font, width=20)
        self.workout_type_entry = ttk.Combobox(self, font=entry_font, width=20)
        self.measure_entry = ttk.Combobox(self, font=entry_font, width=20)

        exercise_name_entry_text = ttk.Label(self, text='Exercise Name:', font=label_font)
        workout_class_entry_text = ttk.Label(self, text='Workout Class:', font=label_font)
        workout_type_entry_text = ttk.Label(self, text='Workout Type:', font=label_font)
        measure_entry_text = ttk.Label(self, text='Measure Type:', font=label_font)

        button_submit = ttk.Button(self, text='Submit')
        button_exit = ttk.Button(self, text='Home')

        # Place widgets
        self.exercise_name_entry.grid(row=1, column=1, sticky='W', padx=2, pady=1)
        self.workout_class_entry.grid(row=2, column=1, sticky='W', padx=2, pady=1)
        self.workout_type_entry.grid(row=3, column=1, sticky='W', padx=2, pady=1)
        self.measure_entry.grid(row=4, column=1, sticky='W', padx=2, pady=1)

        self.title_text.grid(row=0, column=0, pady=15, columnspan=2, sticky='N')
        exercise_name_entry_text.grid(row=1, column=0, sticky='E', padx=2, pady=1)
        workout_class_entry_text.grid(row=2, column=0, sticky='E', padx=2, pady=1)
        workout_type_entry_text.grid(row=3, column=0, sticky='E', padx=2, pady=1)
        measure_entry_text.grid(row=4, column=0, sticky='E', padx=2, pady=1)

        button_exit.grid(row=5, column=0, sticky='E', padx=2, pady=5)
        button_submit.grid(row=5, column=1, sticky='W', padx=2, pady=5)

        # Presenter Bindings
        self.workout_class_entry.bind('<<ComboboxSelected>>', presenter.get_workout_type_list)
        button_submit.bind('<Button-1>', presenter.submit_form)
        button_exit.bind('<Button-1>', presenter.show_start_view)


class WorkoutSessionView(tk.Frame):
    """The window where a user may enter a workout into the database.

    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

    def init_ui(self, presenter):

        # Widget settings
        title_font= font.Font(family='Segoe UI', size=18, weight='bold')
        header_font = font.Font(family='Segoe UI', size=15, weight='bold')
        label_font = font.Font(family='Segoe UI', size=12, weight='bold')
        entry_font = font.Font(family='Segoe UI', size=11, weight='normal')
        button_font = font.Font(family='Segoe UI', size=11, weight='normal')

        # Frame1
        self.frame1 = tk.Frame(self)
        self.title_text = ttk.Label(self.frame1, text='Workout Sessions', font=title_font, anchor='center')
        self.tree = ttk.Treeview(self.frame1, show="headings")
        self.title_text.grid(row=0, column=0, sticky="NSEW")
        self.tree.grid(row=1, column=0, sticky="NSEW")

        self.tree_menu = tk.Menu(self.frame1, tearoff=0)
        self.tree_menu.add_command(label="Edit", command=lambda: presenter.get_entry())
        self.tree_menu.add_command(label="Delete", command=lambda: presenter.delete_entry())

        # Frame1 Presenter Bindings
        self.tree.bind('<Button-3>', presenter.show_tree_menu)

        # Frame2
        self.frame2 = tk.Frame(self)
        
        # Create Widgets
        self.frame2_header_text = ttk.Label(self.frame2, text='Log Exercise Session', font=header_font)
        self.id_entry = ttk.Label(self.frame2, text='', font=entry_font)
        self.date_entry = ttk.Entry(self.frame2, font=entry_font, width=20)
        self.workout_name_entry = ttk.Combobox(self.frame2, font=entry_font, width=20)
        self.time_elapsed_entry = ttk.Entry(self.frame2, font=entry_font, width=20)
        self.workout_quality_entry = ttk.Combobox(self.frame2, height=10, font=entry_font, width=60)

        id_entry_text = ttk.Label(self.frame2, text='id:', font=label_font)
        date_entry_text = ttk.Label(self.frame2, text='Date:', font=label_font)
        workout_name_entry_text = ttk.Label(self.frame2, text='Workout:', font=label_font)
        time_elapsed_entry_text = ttk.Label(self.frame2, text='Time Spent (minutes):', font=label_font)
        workout_quality_entry_text = ttk.Label(self.frame2, text='Workout Quality:', font=label_font)

        # Place entry and text widgets
        self.frame2_header_text.grid(row=0, column=2, pady=15, columnspan=2, sticky='W')
        
        id_entry_text.grid(row=1, column=0, sticky='E', padx=2, pady=1)
        date_entry_text.grid(row=2, column=0, sticky='E', padx=2, pady=1)
        
        self.id_entry.grid(row=1, column=1, sticky='W', padx=2, pady=1)
        self.date_entry.grid(row=2, column=1, sticky='W', padx=2, pady=1)

        workout_name_entry_text.grid(row=1, column=2, sticky='E', padx=2, pady=1)
        time_elapsed_entry_text.grid(row=2, column=2, sticky='E', padx=2, pady=1)
        workout_quality_entry_text.grid(row=3, column=2, sticky='E', padx=2, pady=1)
        
        self.workout_name_entry.grid(row=1, column=3, sticky='W', padx=2, pady=1)
        self.time_elapsed_entry.grid(row=2, column=3, sticky='W', padx=2, pady=1)
        self.workout_quality_entry.grid(row=3, column=3, sticky='W', padx=2, pady=1)

        # Frame3
        self.frame3 = tk.Frame(self)
        self.button_submit = ttk.Button(self.frame3, text='Submit')
        self.button_exit = ttk.Button(self.frame3, text='Home')
        self.button_clear = ttk.Button(self.frame3, text='Clear')

        self.button_exit.grid(row=0, column=0, sticky='S', padx=2, pady=5)
        self.button_clear.grid(row=0, column=1, sticky='S', padx=2, pady=5)
        self.button_submit.grid(row=0, column=2, sticky='S', padx=2, pady=5)

        self.button_submit.bind('<Button-1>', presenter.submit_entry)
        self.button_exit.bind('<Button-1>', presenter.show_start_view)
        self.button_clear.bind('<Button-1>', presenter.clear_view_entries)

        # Frame placements
        self.frame1.grid(row=0, column=0, padx=10, pady=2)
        self.frame2.grid(row=1, column=0, padx=1, pady=5, sticky="NSEW")
        self.frame3.grid(row=2, column=0, padx=1, pady=5, sticky="NSEW")


class ExerciseSessionView(tk.Frame):
    """The window where a user may enter a new exercise into the database.

    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

    def init_ui(self, presenter):
        # Widget settings
        title_font= font.Font(family='Segoe UI', size=18, weight='bold')
        header_font = font.Font(family='Segoe UI', size=15, weight='bold')
        label_font = font.Font(family='Segoe UI', size=12, weight='bold')
        entry_font = font.Font(family='Segoe UI', size=11, weight='normal')
        button_font = font.Font(family='Segoe UI', size=11, weight='normal')
        
        #Frame 1
        self.frame1 = tk.Frame(self)
        self.title_text = ttk.Label(self.frame1, text='Exercise Sessions', font=title_font, anchor='center')
        self.tree = ttk.Treeview(self.frame1, show="headings")
        self.title_text.grid(row=0, column=0, sticky="NSEW")
        self.tree.grid(row=1, column=0, sticky="NSEW")

        self.tree_menu = tk.Menu(self.frame1, tearoff=0)
        self.tree_menu.add_command(label="Edit", command=lambda: presenter.get_entry())
        self.tree_menu.add_command(label="Delete", command=lambda: presenter.delete_entry())

        # Frame1 Presenter Bindings
        self.tree.bind('<Button-3>', presenter.show_tree_menu)

        #Frame 2
        self.frame2 = tk.Frame(self)

        # Create Widgets
        self.frame2_header_text = ttk.Label(self.frame2, text='Log Exercise Session', font=header_font)
        self.id_entry = ttk.Label(self.frame2, font=entry_font, width=20)
        self.date_entry = ttk.Entry(self.frame2, font=entry_font, width=20)
        self.workout_class_entry = ttk.Combobox(self.frame2, font=entry_font, width=18)
        self.workout_type_entry = ttk.Combobox(self.frame2, font=entry_font, width=18)
        self.exercise_entry = ttk.Combobox(self.frame2, font=entry_font, width=20)
        self.value_entry = ttk.Entry(self.frame2, font=entry_font, width=20)
        self.measure_entry = ttk.Label(self.frame2, font=entry_font, width=10)
        self.reps_entry = ttk.Entry(self.frame2, font=entry_font, width=20)

        id_entry_text = ttk.Label(self.frame2, text='id:', font=label_font)
        date_entry_text = ttk.Label(self.frame2, text='Date:', font=label_font)
        workout_class_entry_text = ttk.Label(self.frame2, text='Workout Class:', font=label_font)
        workout_type_entry_text = ttk.Label(self.frame2, text='Workout Type:', font=label_font)
        exercise_entry_text = ttk.Label(self.frame2, text='Exercise:', font=label_font)
        value_entry_text = ttk.Label(self.frame2, text='Value:', font=label_font)
        reps_entry_text = ttk.Label(self.frame2, text='Repetitions:', font=label_font)
        # measure_entry_text = ttk.Label(self.frame2, text='Measure:', font=label_font)

        # Place entry and text widgets
        self.frame2_header_text.grid(row=0, column=2, pady=15, columnspan=2, sticky='E')

        id_entry_text.grid(row=1, column=0, sticky='E', padx=2, pady=1)
        date_entry_text.grid(row=2, column=0, sticky='E', padx=2, pady=1)

        self.id_entry.grid(row=1, column=1, sticky='W', padx=2, pady=1)
        self.date_entry.grid(row=2, column=1, sticky='W', padx=2, pady=1)

        workout_class_entry_text.grid(row=1, column=2, sticky='E', padx=2, pady=1)
        workout_type_entry_text.grid(row=2, column=2, sticky='E', padx=2, pady=1)
        exercise_entry_text.grid(row=1, column=4, sticky='E', padx=2, pady=1)
        value_entry_text.grid(row=2, column=4, sticky='E', padx=2, pady=1)
        reps_entry_text.grid(row=3, column=4, sticky='E', padx=2, pady=1)

        self.workout_class_entry.grid(row=1, column=3, sticky='W', padx=2, pady=1)
        self.workout_type_entry.grid(row=2, column=3, sticky='W', padx=2, pady=1)
        self.exercise_entry.grid(row=1, column=5, sticky='W', padx=2, pady=1)
        self.value_entry.grid(row=2, column=5, sticky='W', padx=2, pady=1)
        self.reps_entry.grid(row=3, column=5, sticky='W', padx=2, pady=1)

        self.measure_entry.grid(row=2, column=6, sticky='E', padx=2, pady=1)

        # Frame2 Presenter Bindings
        self.workout_class_entry.bind('<<ComboboxSelected>>', presenter.get_workout_type_list)
        self.workout_type_entry.bind('<<ComboboxSelected>>', presenter.get_exercise_list)
        self.exercise_entry.bind('<<ComboboxSelected>>', presenter.get_measure_list)

        # Frame3
        self.frame3 = tk.Frame(self)
        self.button_submit = ttk.Button(self.frame3, text='Submit')
        self.button_exit = ttk.Button(self.frame3, text='Home')
        self.button_clear = ttk.Button(self.frame3, text='Clear')

        self.button_exit.grid(row=0, column=0, sticky='S', padx=2, pady=5)
        self.button_clear.grid(row=0, column=1, sticky='S', padx=2, pady=5)
        self.button_submit.grid(row=0, column=2, sticky='S', padx=2, pady=5)

        self.button_submit.bind('<Button-1>', presenter.submit_entry)
        self.button_exit.bind('<Button-1>', presenter.show_start_view)
        self.button_clear.bind('<Button-1>', presenter.clear_view_entries)

        # Frame placements
        self.frame1.grid(row=0, column=0, padx=10, pady=2)
        self.frame2.grid(row=1, column=0, padx=1, pady=5, sticky="NSEW")
        self.frame3.grid(row=2, column=0, padx=1, pady=5, sticky="NSEW")


class DateView(tk.Frame):
    """The window where a user may enter a new exercise into the database.

    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

    def init_ui(self, presenter):

        # Widget settings
        title_font= font.Font(family='Segoe UI', size=18, weight='bold')
        header_font = font.Font(family='Segoe UI', size=15, weight='bold')
        label_font = font.Font(family='Segoe UI', size=12, weight='bold')
        entry_font = font.Font(family='Segoe UI', size=11, weight='normal')
        button_font = font.Font(family='Segoe UI', size=11, weight='normal')

        # Frame1
        self.frame1 = tk.Frame(self)
        self.title_text = ttk.Label(self.frame1, text='Daily Log', font=title_font, anchor='center')
        self.tree = ttk.Treeview(self.frame1, show="headings")
        self.title_text.grid(row=0, column=0, sticky="NSEW")
        self.tree.grid(row=1, column=0, sticky="NSEW")

        self.tree_menu = tk.Menu(self.frame1, tearoff=0)
        self.tree_menu.add_command(label="Edit", command=lambda: presenter.get_entry())
        self.tree_menu.add_command(label="Delete", command=lambda: presenter.delete_entry())

        # Frame1 Presenter Bindings
        self.tree.bind('<Button-3>', presenter.show_tree_menu)
        
        # Frame 2
        self.frame2 = tk.Frame(self)

        # Create Widgets
        self.frame2_header_text = ttk.Label(self.frame2, text='Log Data', font=header_font)
        self.id_entry = ttk.Label(self.frame2, text='', font=entry_font) 
        self.date_entry = ttk.Entry(self.frame2, font=entry_font, width=20)
        self.calories_entry = ttk.Entry(self.frame2, font=entry_font, width=20)
        self.protein_entry = ttk.Entry(self.frame2, font=entry_font, width=20)
        self.weight_entry = ttk.Entry(self.frame2, font=entry_font, width=20)
        self.sleep_entry = ttk.Entry(self.frame2, font=entry_font, width=20)
        
        id_entry_text = ttk.Label(self.frame2, text='id:', font=label_font)
        date_entry_text = ttk.Label(self.frame2, text='Date:', font=label_font)
        calories_entry_text = ttk.Label(self.frame2, text='Calories:', font=label_font)
        protein_entry_text = ttk.Label(self.frame2, text='Protein (g):', font=label_font)
        weight_entry_text = ttk.Label(self.frame2, text='Weight (lbs):', font=label_font)
        sleep_entry_text = ttk.Label(self.frame2, text='Sleep (hrs):', font=label_font)

        # Place entry and text widgets
        self.frame2_header_text.grid(row=0, column=2, pady=15, columnspan=2, sticky='W')
        
        id_entry_text.grid(row=1, column=0, sticky='E', padx=2, pady=1)
        date_entry_text.grid(row=2, column=0, sticky='E', padx=2, pady=1)
        
        self.id_entry.grid(row=1, column=1, sticky='W', padx=2, pady=1)
        self.date_entry.grid(row=2, column=1, sticky='W', padx=2, pady=1)
        
        calories_entry_text.grid(row=1, column=2, sticky='E', padx=2, pady=1)
        protein_entry_text.grid(row=2, column=2, sticky='E', padx=2, pady=1)
        weight_entry_text.grid(row=3, column=2, sticky='E', padx=2, pady=1)
        sleep_entry_text.grid(row=4, column=2, sticky='E', padx=2, pady=1)
        
        self.calories_entry.grid(row=1, column=3, sticky='W', padx=2, pady=1)
        self.protein_entry.grid(row=2, column=3, sticky='W', padx=2, pady=1)
        self.weight_entry.grid(row=3, column=3, sticky='W', padx=2, pady=1)
        self.sleep_entry.grid(row=4, column=3, sticky='W', padx=2, pady=1)

        # Frame3
        self.frame3 = tk.Frame(self)
        self.button_submit = ttk.Button(self.frame3, text='Submit')
        self.button_exit = ttk.Button(self.frame3, text='Home')
        self.button_clear = ttk.Button(self.frame3, text='Clear')

        self.button_exit.grid(row=0, column=0, sticky='S', padx=2, pady=5)
        self.button_clear.grid(row=0, column=1, sticky='S', padx=2, pady=5)
        self.button_submit.grid(row=0, column=2, sticky='S', padx=2, pady=5)

        self.button_submit.bind('<Button-1>', presenter.submit_entry)
        self.button_exit.bind('<Button-1>', presenter.show_start_view)
        self.button_clear.bind('<Button-1>', presenter.clear_view_entries)

        # Frame placements
        self.frame1.grid(row=0, column=0, padx=10, pady=2)
        self.frame2.grid(row=1, column=0, padx=1, pady=5, sticky="NSEW")
        self.frame3.grid(row=2, column=0, padx=1, pady=5, sticky="NSEW")


class GoalView(tk.Frame):
    """The window where a user may enter a new exercise into the database.

    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

    def init_ui(self, presenter):

        # Widget settings
        title_font= font.Font(family='Segoe UI', size=15, weight='bold')
        label_font = font.Font(family='Segoe UI', size=12, weight='bold')
        entry_font = font.Font(family='Segoe UI', size=11, weight='normal')
        button_font = font.Font(family='Segoe UI', size=11, weight='normal')

        # Create Widgets
        self.title_text = ttk.Label(self, text='  Select Goal Type', font=title_font)
        self.goal_type_entry = ttk.Combobox(self, font=entry_font, width=20)
        self.goal_type_entry_text = ttk.Label(self, text='Goal Type:', font=label_font)

        self.button_exit = ttk.Button(self, text='Home')

        # Place entry and text widgets
        self.title_text.grid(row=0, column=0, pady=15, columnspan=2, sticky='N')
        self.goal_type_entry.grid(row=1, column=1, sticky='W', padx=2, pady=1)
        self.goal_type_entry_text.grid(row=1, column=0, sticky='E', padx=2, pady=1)

        self.button_exit.grid(row=2, column=0, padx=2, pady=5, columnspan=2)

        # Presenter Bindings
        self.goal_type_entry.bind('<<ComboboxSelected>>', presenter.show_goal_type_view)
        self.button_exit.bind('<Button-1>', presenter.show_start_view)


class ExerciseGoalView(tk.Frame):
    """The window where a user may enter a new exercise into the database.

    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

    def init_ui(self, presenter):

        # Widget settings
        title_font= font.Font(family='Segoe UI', size=15, weight='bold')
        label_font = font.Font(family='Segoe UI', size=12, weight='bold')
        entry_font = font.Font(family='Segoe UI', size=11, weight='normal')
        button_font = font.Font(family='Segoe UI', size=11, weight='normal')

        # Create Widgets
        self.title_text = ttk.Label(self, text='  Set Exercise Goal', font=title_font)
        self.exercise_name_entry = ttk.Combobox(self, font=entry_font, width=20)
        self.exercise_name_entry_text = ttk.Label(self, text='Exercise Name:', font=label_font)
        self.value_entry = ttk.Entry(self, font=entry_font, width=20)
        self.value_entry_text = ttk.Label(self, text='Value:', font=label_font)
        self.measure_entry = ttk.Combobox(self, font=entry_font, width=20)
        self.measure_entry_text = ttk.Label(self, text='Measure:', font=label_font)
        self.start_date_entry = ttk.Entry(self, text='', font=entry_font, width=20)
        self.start_date_entry_text = ttk.Label(self, text='Start Date:', font=label_font)
        self.target_date_entry = ttk.Entry(self, text='', font=entry_font, width=20)
        self.target_date_entry_text = ttk.Label(self, text='Target Completion Date:', font=label_font)

        self.button_exit = ttk.Button(self, text='Home')
        self.button_submit = ttk.Button(self, text='Submit')

        self.title_text.grid(row=0, column=0, pady=15, columnspan=2, sticky='N')
        self.exercise_name_entry.grid(row=1, column=1, sticky='W', padx=2, pady=1)
        self.exercise_name_entry_text.grid(row=1, column=0, sticky='E', padx=2, pady=1)
        self.value_entry.grid(row=2, column=1, sticky='W', padx=2, pady=1)
        self.value_entry_text.grid(row=2, column=0, sticky='E', padx=2, pady=1)
        self.measure_entry.grid(row=3, column=1, sticky='W', padx=2, pady=1)
        self.measure_entry_text.grid(row=3, column=0, sticky='E', padx=2, pady=1)
        self.start_date_entry.grid(row=4, column=1, sticky='W', padx=2, pady=1)
        self.start_date_entry_text.grid(row=4, column=0, sticky='E', padx=2, pady=1)
        self.target_date_entry.grid(row=5, column=1, sticky='W', padx=2, pady=1)
        self.target_date_entry_text.grid(row=5, column=0, sticky='E', padx=2, pady=1)

        self.button_exit.grid(row=6, column=0, sticky='E', padx=2, pady=5)
        self.button_submit.grid(row=6, column=1, sticky='W', padx=2, pady=5)

        # Presenter Bindings
        self.exercise_name_entry.bind('<<ComboboxSelected>>', presenter.get_measures)
        self.button_exit.bind('<Button-1>', presenter.show_start_view)
        self.button_submit.bind('<Button-1>', presenter.submit_form)


class WorkoutClassGoalView(tk.Frame):
    """The window where a user may enter a new exercise into the database.

    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

    def init_ui(self, presenter):

        # Widget settings
        title_font= font.Font(family='Segoe UI', size=15, weight='bold')
        label_font = font.Font(family='Segoe UI', size=12, weight='bold')
        entry_font = font.Font(family='Segoe UI', size=11, weight='normal')
        button_font = font.Font(family='Segoe UI', size=11, weight='normal')

        # Create Widgets
        self.title_text = ttk.Label(self, text='  Set Workout Goal', font=title_font)
        self.workout_class_entry = ttk.Combobox(self, font=entry_font, width=20)
        self.workout_class_entry_text = ttk.Label(self, text='Workout Class:', font=label_font)
        self.value_entry = ttk.Entry(self, font=entry_font, width=20)
        self.value_entry_text = ttk.Label(self, text='Workouts/week:', font=label_font)
        self.start_date_entry = ttk.Entry(self, font=entry_font, width=20)
        self.start_date_entry_text = ttk.Label(self, text='Start Date:', font=label_font)
        self.target_date_entry = ttk.Entry(self, font=entry_font, width=20)
        self.target_date_entry_text = ttk.Label(self, text='Target Completion Date:', font=label_font)

        self.button_exit = ttk.Button(self, text='Home')
        self.button_submit = ttk.Button(self, text='Submit')

        self.title_text.grid(row=0, column=0, columnspan=2, pady=15)
        self.workout_class_entry.grid(row=1, column=1, sticky='W', padx=2, pady=1)
        self.workout_class_entry_text.grid(row=1, column=0, sticky='E', padx=2, pady=1)
        self.value_entry.grid(row=2, column=1, sticky='W', padx=2, pady=1)
        self.value_entry_text.grid(row=2, column=0, sticky='E', padx=2, pady=1)
        self.start_date_entry.grid(row=3, column=1, sticky='W', padx=2, pady=1)
        self.start_date_entry_text.grid(row=3, column=0, sticky='E', padx=2, pady=1)
        self.target_date_entry.grid(row=4, column=1, sticky='W', padx=2, pady=1)
        self.target_date_entry_text.grid(row=4, column=0, sticky='E', padx=2, pady=1)

        self.button_exit.grid(row=5, column=0, sticky='E', padx=2, pady=5)
        self.button_submit.grid(row=5, column=1, sticky='W', padx=2, pady=5)


        # Presenter Bindings
        self.button_exit.bind('<Button-1>', presenter.show_start_view)
        self.button_submit.bind('<Button-1>', presenter.submit_form)


class WeightGoalView(tk.Frame):
    """The window where a user may enter a new exercise into the database.

    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

    def init_ui(self, presenter):

        # Widget settings
        title_font= font.Font(family='Segoe UI', size=15, weight='bold')
        label_font = font.Font(family='Segoe UI', size=12, weight='bold')
        entry_font = font.Font(family='Segoe UI', size=11, weight='normal')
        button_font = font.Font(family='Segoe UI', size=11, weight='normal')

        # Create Widgets
        self.title_text = ttk.Label(self, text='  Set Weight Goal', font=title_font)

        self.value_entry = ttk.Entry(self, font=entry_font, width=20)
        self.value_entry_text = ttk.Label(self, text='Weight (lbs):', font=label_font)
        # self.measure_entry = ttk.Label(self, text='pounds', font=entry_font)
        # self.measure_entry_text = ttk.Label(self, text='Measure:', font=label_font)
        self.start_date_entry = ttk.Entry(self, font=entry_font, width=20)
        self.start_date_entry_text = ttk.Label(self, text='Start Date:', font=label_font)
        self.target_date_entry = ttk.Entry(self, font=entry_font, width=20)
        self.target_date_entry_text = ttk.Label(self, text='Target Completion Date:', font=label_font)
        self.button_submit = ttk.Button(self, text='Submit')
        self.button_exit = ttk.Button(self, text='Home')

        self.title_text.grid(row=0, column=0, pady=15, columnspan=2, sticky='N')
        self.value_entry_text.grid(row=1, column=0, sticky='E', padx=2, pady=1)
        self.value_entry.grid(row=1, column=1, sticky='W', padx=2, pady=1)
        # self.measure_entry_text.grid(row=2, column=0, sticky='E', padx=2, pady=1)
        # self.measure_entry.grid(row=2, column=1, sticky='W', padx=2, pady=1)
        self.start_date_entry_text.grid(row=2, column=0, sticky='E', padx=2, pady=1)
        self.start_date_entry.grid(row=2, column=1, sticky='W', padx=2, pady=1)
        self.target_date_entry_text.grid(row=3, column=0, sticky='E', padx=2, pady=1)
        self.target_date_entry.grid(row=3, column=1, sticky='W', padx=2, pady=1)


        self.button_exit.grid(row=4, column=0, sticky='E', padx=2, pady=5)
        self.button_submit.grid(row=4, column=1, sticky='W', padx=2, pady=5)

        # Presenter Bindings
        self.button_submit.bind('<Button-1>', presenter.submit_form)
        self.button_exit.bind('<Button-1>', presenter.show_start_view)


class GlossaryView(tk.Frame):
    """The window where a user may enter a new exercise into the database.

    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

    def init_ui(self, presenter):
        term1 = 'Workout: A single continuous session encompassing a series of exercises.'
        term2 = 'Exercise: A particular movement performed singularly or in repetition. For the sake of this program,\n'\
                ' an exercise is also defined by a measure (number of repetitions, distance, etc.) so that you can \n' \
                'track your progress for that particular task over time.'
        term3 = 'Workout Class: A broad classification of similar exercises.'
        term4 = 'Workout Type: A more specific classification of exercises belonging to the same workout class.'
        term5 = ''

        # Widget settings
        title_font= font.Font(family='Segoe UI', size=15, weight='bold')
        label_font = font.Font(family='Segoe UI', size=12, weight='normal')
        entry_font = font.Font(family='Segoe UI', size=11, weight='normal')
        button_font = font.Font(family='Segoe UI', size=11, weight='normal')

        # Create Widgets
        self.title_text = ttk.Label(self, text='Glossary', font=title_font)
        self.term1_text = ttk.Label(self, text=term1, font=label_font)
        self.term2_text = ttk.Label(self, text=term2, font=label_font)
        self.term3_text = ttk.Label(self, text=term3, font=label_font)
        self.term4_text = ttk.Label(self, text=term4, font=label_font)
        self.term5_text = ttk.Label(self, text=term5, font=label_font)

        self.button_exit = ttk.Button(self, text='Home')

        self.title_text.grid(row=0, column=0, pady=15, columnspan=2, sticky='N')
        self.term1_text.grid(row=1, column=0, sticky='W', padx=2, pady=1)
        self.term2_text.grid(row=2, column=0, sticky='W', padx=2, pady=1)
        self.term3_text.grid(row=3, column=0, sticky='W', padx=2, pady=1)
        self.term4_text.grid(row=4, column=0, sticky='W', padx=2, pady=1)
        self.term5_text.grid(row=5, column=0, sticky='W', padx=2, pady=1)

        self.button_exit.grid(row=6, column=0, sticky='N', padx=2, pady=5)

        # Presenter Bindings
        self.button_exit.bind('<Button-1>', presenter.show_start_view)


class ProgramInfoView(tk.Frame):
    """The window where a user may enter a new exercise into the database.

    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

    def init_ui(self, presenter):
        line1 = 'Last updated: 4/13/2023'
        line2 = 'Version: Beta 4.0'
        line3 = 'Author: Austin M Puckett'
        line4 = ''
        line5 = ''

        # Widget settings
        title_font= font.Font(family='Segoe UI', size=15, weight='bold')
        label_font = font.Font(family='Segoe UI', size=12, weight='normal')
        entry_font = font.Font(family='Segoe UI', size=11, weight='normal')
        button_font = font.Font(family='Segoe UI', size=11, weight='normal')

        # Create Widgets
        self.title_text = ttk.Label(self, text='Program Info', font=title_font)
        self.line1_text = ttk.Label(self, text=line1, font=label_font)
        self.line2_text = ttk.Label(self, text=line2, font=label_font)
        self.line3_text = ttk.Label(self, text=line3, font=label_font)
        self.line4_text = ttk.Label(self, text=line4, font=label_font)
        self.line5_text = ttk.Label(self, text=line5, font=label_font)

        self.button_exit = ttk.Button(self, text='Home')

        self.title_text.grid(row=0, column=0, pady=15, columnspan=2, sticky='N')
        self.line1_text.grid(row=1, column=0, sticky='W', padx=2, pady=1)
        self.line2_text.grid(row=2, column=0, sticky='W', padx=2, pady=1)
        self.line3_text.grid(row=3, column=0, sticky='W', padx=2, pady=1)
        self.line4_text.grid(row=4, column=0, sticky='W', padx=2, pady=1)
        self.line5_text.grid(row=5, column=0, sticky='W', padx=2, pady=1)

        self.button_exit.grid(row=6, column=0, sticky='N', padx=2, pady=5)

        # Presenter Bindings
        self.button_exit.bind('<Button-1>', presenter.show_start_view)


class FAQView(tk.Frame):
    """The window where a user may enter a new exercise into the database.

    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

    def init_ui(self, presenter):
        line1 = ''
        line2 = ''
        line3 = ''
        line4 = ''
        line5 = ''

        # Widget settings
        title_font= font.Font(family='Segoe UI', size=15, weight='bold')
        label_font = font.Font(family='Segoe UI', size=12, weight='normal')
        entry_font = font.Font(family='Segoe UI', size=11, weight='normal')
        button_font = font.Font(family='Segoe UI', size=11, weight='normal')

        # Create Widgets
        self.title_text = ttk.Label(self, text='FAQ', font=title_font)
        self.line1_text = ttk.Label(self, text=line1, font=label_font)
        self.line2_text = ttk.Label(self, text=line2, font=label_font)
        self.line3_text = ttk.Label(self, text=line3, font=label_font)
        self.line4_text = ttk.Label(self, text=line4, font=label_font)
        self.line5_text = ttk.Label(self, text=line5, font=label_font)

        self.button_exit = ttk.Button(self, text='Home')

        self.title_text.grid(row=0, column=0, pady=15, columnspan=2, sticky='N')
        self.line1_text.grid(row=1, column=0, sticky='W', padx=2, pady=1)
        self.line2_text.grid(row=2, column=0, sticky='W', padx=2, pady=1)
        self.line3_text.grid(row=3, column=0, sticky='W', padx=2, pady=1)
        self.line4_text.grid(row=4, column=0, sticky='W', padx=2, pady=1)
        self.line5_text.grid(row=5, column=0, sticky='W', padx=2, pady=1)

        self.button_exit.grid(row=6, column=0, sticky='N', padx=2, pady=5)

        # Presenter Bindings
        self.button_exit.bind('<Button-1>', presenter.show_start_view)


class TableDataView(tk.Frame):
    """The window where a user may enter a new exercise into the database.

    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

    def init_ui(self, presenter):

        # Widget settings
        title_font= font.Font(family='Segoe UI', size=15, weight='bold')
        label_font = font.Font(family='Segoe UI', size=12, weight='bold')
        entry_font = font.Font(family='Segoe UI', size=11, weight='normal')
        button_font = font.Font(family='Segoe UI', size=11, weight='normal')

        # Create Widgets
        self.title_text = ttk.Label(self, text='View Data', font=title_font)
        self.table_entry = ttk.Combobox(self, font=entry_font, width=20)
        self.table_entry_text = ttk.Label(self, text='Table:', font=label_font)

        self.button_exit = ttk.Button(self, text='Home')

        # Place entry and text widgets
        self.title_text.grid(row=0, column=0, pady=15, columnspan=2, sticky='N')
        self.table_entry.grid(row=1, column=1, sticky='W', padx=2, pady=1)
        self.table_entry_text.grid(row=1, column=0, sticky='E', padx=2, pady=1)

        self.button_exit.grid(row=2, column=0, padx=2, pady=5, columnspan=2)

        # Presenter Bindings
        self.table_entry.bind('<<ComboboxSelected>>', presenter.show_table)
        self.button_exit.bind('<Button-1>', presenter.show_start_view)
        
    def show_table(self, table_data):
        self.table_data = table_data
        self.columns = table_data['columns']
        self.rows = table_data['entry_data']
        self.root = tk.Toplevel()
        self.tree = ttk.Treeview(self.root, columns=self.columns, show="headings")

        for col in self.columns:
            self.tree.heading(col, text=col.title())

        for row in self.rows:
            self.tree.insert('', 'end', values=row)


