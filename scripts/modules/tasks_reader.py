import re

def get_tasks_from_file(path, current_date):

    def get_new_task(title = ''):

        return {

            'title':            title,
            'original_title':   title,

            'notes':        [],
            'datetime':     current_date,
            'outdated':     False,
            'completed':    False,
            'recurrence':   '',

        }

    def get_new_group(title = ''):

        return {
            'title': title,
            'tasks': []
        }

    def add_group():

        if is_group():
            groups.append(group)

    def add_task():

        if is_task():
            group['tasks'].append(task)            

    def is_group():

        return group['title'] != ''

    def is_task():

        return task['title'] != ''

    groups = []

    with open(path, encoding = 'utf-8-sig') as handle:
        
        lines   = handle.read().splitlines()        
        group   = get_new_group()
        task    = get_new_task()        
                    
        for line in lines:
                
            if line.startswith('-') or line.startswith('+'):
                    
                add_task()

                line_without_mark = line[1:].strip()

                time = re.search(r'[0-9]{1,2}:[0-9]{2}', line_without_mark)

                if time != None:

                    title_date  = time.group(0)
                    title_date_parts = title_date.strip().split(':')

                    hour    = int(title_date_parts[0])
                    minute  = int(title_date_parts[1])                    

                else:

                    hour    = 0
                    minute  = 0

                task = get_new_task()

                task['title']           = line_without_mark
                task['original_title']  = line_without_mark
                
                task['datetime']    = current_date.replace(hour = hour, minute = minute)
                task['outdated']    = False
                task['completed']   = line.startswith('+')

            elif line.startswith('#'):

                add_task()

                task = get_new_task()

                if group['title'] == '':
                    group['title'] = line
                else:
                    add_group()
                    group = get_new_group(line)

            else:

                if is_task():
                    task['notes'].append(line)

        add_task()
        add_group()
    
    return groups