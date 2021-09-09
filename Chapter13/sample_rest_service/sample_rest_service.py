"""Test REST server


This is a simple test REST service implemented in flask
for ABQ Data Entry.  It provides 3 endpoints:

- /auth for authenticating
- /upload for uploading a file
- /files for downloading a file

/files can respond to HEAD requests to simply check the file's
existence and size.
"""

import sys
from pathlib import Path

try:
  import flask as f
except ImportError:
  print(
    'This script requires the Flask library.  '
      'You can install this using the command:  pip3 install --user flask'
  )
  sys.exit()

app = f.Flask(__name__)
app.secret_key = '12345'

#####################
# Wrapper functions #
#####################

def make_error(status_code, message):
  """Create error response with JSON body"""
  response = f.jsonify({
    'status': status_code,
    'message': message
  })
  response.status_code = status_code
  return response

#############
# Endpoints #
#############

@app.route('/auth', methods=['POST'])
def auth():
  """Authenticate the user and set a session cookie"""
  username = f.request.form.get('username')
  password = f.request.form.get('password')
  if username == 'test' and password == 'test':
    f.session['authenticated'] = True
    return f.jsonify({'message': 'Success'})
  return make_error(401, 'The provided credentials were not accepted.')

@app.route('/files', methods=['PUT'])
def upload():
  """Endpoint for file upload"""
  if not f.session.get('authenticated'):
    return make_error(403, 'Access is forbidden')
  filedata = f.request.files.get('file')
  print(f'Uploaded {filedata.filename}')
  filedata.save(filedata.filename)

  return f.jsonify({'message': 'Success'})

@app.route('/files/<filename>', methods=['GET', 'HEAD'])
def files(filename):
  """Endpoint for file download"""
  if not f.session.get('authenticated'):
    return make_error(403, 'Access is forbidden')
  fp = Path(filename)
  if not fp.exists():
    return make_error(404, 'File not found')
  response = f.Response()
  response.headers.add('content-length', fp.stat().st_size)
  if f.request.method == 'HEAD':
    return response
  response.set_data(fp.read_text())
  return response


##################
# Execute script #
##################

if __name__ == '__main__':
  app.run(port=8000)
