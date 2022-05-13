class EmailError(Exception):
    pass
class PasswordError(Exception):
    pass
class NameValueError(Exception):
    pass

class Student():
    def __init__(self, name, email, password):

        if not type(name)==str: raise NameValueError
        else: self.name=name

        if not type(email)==str: raise EmailError
        else:
            try:
                email_at=email.find('@')
                email_com=email.find('.com')
                if email_at>0 and email_com>0 and email_at < email_com: self.email=email
                else: raise EmailError
            except: raise EmailError

        if password is None: raise PasswordError
        else: self.password=password

    def to_dict(self):
        """passes student to dictionary"""
        student_dict={"name":self.name, "email":self.email, "password":self.password}
        return student_dict

