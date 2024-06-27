def signup_status(errors):
  username_errors = ['']
  email_errors = ['']
  password_errors = ['']
  try:
    username_errors = errors['username']
  except KeyError:
    pass

  try:
    email_errors = errors['email']
  except KeyError:
    pass

  try:
    password_errors = errors['password']
  except KeyError:
    pass

  if username_errors[0] == 'Username must have a length of 1-40 characters.' or email_errors[0] == 'Please enter a valid email.' or password_errors[0] == 'Password must have a minimum length of 8 characters.':
    return 400 # BAD REQUEST
  if username_errors[0] == 'Username is already in use.' or email_errors[0] == 'Email address is already in use.':
    return 409 # CONFLICT
