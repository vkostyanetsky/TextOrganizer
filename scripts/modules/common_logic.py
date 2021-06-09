import os
import datetime

def get_paths(script_dirpath):

    parameters_filepath     = os.path.join(script_dirpath, 'params.yaml')
    tasks_dirpath           = os.path.split(script_dirpath)[0]

    current_tasks_filepath  = os.path.join(tasks_dirpath, 'today.md')
    planned_tasks_filepath  = os.path.join(tasks_dirpath, 'draft.md')
    history_tasks_dirpath   = os.path.join(tasks_dirpath, 'history')
    
    return {
        'parameters_filepath':      parameters_filepath,
        'tasks_dirpath':            tasks_dirpath,
        'current_tasks_filepath':   current_tasks_filepath,
        'planned_tasks_filepath':   planned_tasks_filepath,
        'history_tasks_dirpath':    history_tasks_dirpath
    }

def get_current_date():

    current_date = datetime.datetime.today()

    return current_date.replace(hour = 0, minute = 0, second = 0, microsecond = 0)