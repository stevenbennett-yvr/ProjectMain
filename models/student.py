class Student():
    def __init__(self, name, email, password):
        # must have a name
        if name is None or not type(name)==str: raise ValueError
        else: self.name=name

        if email is None or not type(email)==str: raise ValueError
        else:
            try:
                email_at=email.find('@')
                email_com=email.find('.com')
                if email_at>0 and email_com>0 and email_at < email_com: self.email=email
                else: raise ValueError
            except: raise ValueError

        if password is None: raise ValueError
        else: self.password=password

    def to_dict(self):
        """passes student to dictionary"""
        student_dict={"name":self.name, "email":self.email, "password":self.password}
        return student_dict