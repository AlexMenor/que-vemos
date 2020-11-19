def main(req):
    user = req.params.get('user')
    return f'Hello, {user}!'