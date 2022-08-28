
Django Shell Notes
- [User Model](#user-model)
  - [Reset User Password](#reset-user-password)

# User Model
## Reset User Password
Retrieve the desired User object and run the set_password with a new password. Do not forget to save the User object.
```python
from django.contrib.auth.models import User
users = User.objects.all().last()   # desired user object
user.set_password('<enter_new_password>')
user.save()
```