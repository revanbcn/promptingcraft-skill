"""Original isolated Save fixture; there is no real network or settings store."""


def save_settings(form, send):
    response = send({'settings': dict(form['values'])})
    form['banner'] = 'success'
    form['dirty'] = False
    return response['status']
