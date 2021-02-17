from app import create_app, db
from app.models import User

app = create_app()

sum = 0;
with app.app_context():
    for user in User.query.all():
        user.popup = True
        sum += 1
    db.session.commit()

print('Updated ' + str(sum) + ' users.')
