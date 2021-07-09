def write_empty_line(handle):

    handle.write('\n')

def write_title(handle, title, marker = ''):

    if marker == '':
        line = '{0}\n'.format(title)
    else:
        line = '{0} {1}\n'.format(marker, title)

    handle.write(line)

def write_notes(handle, task):

    def is_task_with_notes(task):

        result = False

        for note in task['notes']:

            if note.strip() != '':
                result = True
                break
                    
        return result

    if is_task_with_notes(task):

        notes = '\n'.join(task['notes'])
        handle.write(notes)

        write_empty_line(handle)