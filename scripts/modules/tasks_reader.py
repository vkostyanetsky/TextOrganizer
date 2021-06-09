def get_tasks_from_file(path, current_date):

    def get_new_task(title = ''):

        return {
            'title':        title,
            'notes':        [],
            'datetime':     current_date,
            'completed':    False,
            'recurrence':   '',            
        }

    def add_task():

        if is_task():
            tasks.append(task)            

    def is_task():

        return task['title'] != ''

    tasks = []

    with open(path, encoding = 'utf-8-sig') as handle:
        
        lines   = handle.read().splitlines()
        task    = get_new_task()
            
        for line in lines:
                
            if line.startswith('-') or line.startswith('+'):
                    
                add_task()

                parts       = line[1:].strip().split('     ')
                title_date  = parts[0].strip()
                title_name  = parts[1].strip()

                title_date_parts = title_date.strip().split(':')

                hour    = int(title_date_parts[0])
                minute  = int(title_date_parts[1])

                task = get_new_task()

                task['title']       = title_name
                task['datetime']    = current_date.replace(hour = hour, minute = minute)
                task['completed']   = line.startswith('+')
                
            elif line.startswith('#'):

                add_task()

                task = get_new_task()

            else:

                if is_task():
                    task['notes'].append(line)

        add_task()
    
    return tasks