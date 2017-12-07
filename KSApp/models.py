from KSApp import app, db

user_roles = db.table('user_roles',
                      db.Column('user_id', db.INTEGER(), db.ForeignKey('user_id')),
                      db.Column('role_id', db.INTEGER(), db.ForeignKey('role_id'))
                      )

class Role(db.Model, RoleMixin):
    role_id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

class User(db.Model, RoleMixin):
    user_id = db.Column(db.INTEGER, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(255))
    roles = db.relationship('role',
                            secondary=user_roles,
                            backref=db.backref('users', lazy='dynamic')
                            )

    class UserAdmin(sqla.ModelView):
        # Don't display the password on the list of Users
        column_exclude_list = list = ('password',)

        # Don't include the standard password field when creating or editing a User (but see below)
        form_excluded_columns = ('password',)

        # Automatically display human-readable names for the current and available Roles when creating or editing a User
        column_auto_select_related = True

        # Prevent administration of Users unless the currently logged-in user has the "admin" role
        def is_accessible(self):
            return current_user.has_role('admin')

        # On the form for creating or editing a User, don't display a field corresponding to the model's password field.
        # There are two reasons for this. First, we want to encrypt the password before storing in the database. Second,
        # we want to use a password field (with the input masked) rather than a regular text field.
        def scaffold_form(self):
            # Start with the standard form as provided by Flask-Admin. We've already told Flask-Admin to exclude the
            # password field from this form.
            form_class = super(UserAdmin, self).scaffold_form()

            # Add a password field, naming it "password2" and labeling it "New Password".
            form_class.password2 = PasswordField('New Password')
            return form_class

        # This callback executes when the user saves changes to a newly-created or edited User -- before the changes are
        # committed to the database.
        def on_model_change(self, form, model, is_created):
            # If the password field isn't blank...
            if len(model.password2):
                # ... then encrypt the new password prior to storing it in the database. If the password field is blank,
                # the existing password in the database will be retained.
                model.password = utils.encrypt_password(model.password2)

    # Customized Role model for SQL-Admin
    class RoleAdmin(sqla.ModelView):
        # Prevent administration of Roles unless the currently logged-in user has the "admin" role
        def is_accessible(self):
            return current_user.has_role('admin')



