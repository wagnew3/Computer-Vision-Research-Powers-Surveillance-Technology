'''Helper for analysis'''

def print_lists(lists):
    print('\n'.join([header + ': ' + ', '.join(lists[header]) + '\n' for header in lists]))