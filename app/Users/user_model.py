class User():

    USERS = [{'id':1, 'email':'ronald@gmail.com', 'password':'123456', 'authenticated':False},
            {'id':2, 'email':'mutebi@gmail.com', 'password':'123hdg', 'authenticated':True}]

    def get_user(self, email, password):
        """This represents a sign/login in"""
        user = [x for x in USERS if x.get('email') ==email if x.get('password')==password]

        if user:
            return user[0]
        return None

    def register_user(self, email, password,passord2):
        """This represents a user registration"""
        for x in self.USERS:
            if x.get('email') == email:
                return "You are already registered"
            else:
                if password == password2:
                    user = {'email': email, 'password':password}
                    self.USERS.append(user)
                    return "You have registered successfully"



