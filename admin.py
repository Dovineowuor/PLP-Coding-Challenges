import hashlib

class Admin:
    def __init__(self, name, password):
        self.name = name
        self.password = self.hash_password(password)
        self.profile_picture = None

    def hash_password(self, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

    def authenticate(self):
        entered_password = input("Enter your password: ")
        hashed_password = self.hash_password(entered_password)

        if hashed_password == self.password:
            print("Authentication successful. Access granted.")
            return True
        else:
            print("Authentication failed. Access denied.")
            return False

    def set_profile_picture(self, profile_picture):
        self.profile_picture = profile_picture

    def get_profile_info(self):
        profile_info = f"Name: {self.name}"
        if self.profile_picture:
            profile_info += f"\nProfile Picture: {self.profile_picture}"
        return profile_info

def register():
    name = input("Enter your name: ")
    password = input("Enter your password: ")

    admin = Admin(name, password)
    return admin

def main():
    admin = register()

    if admin.authenticate():
        # UI code here
        profile_info = admin.get_profile_info()
        print("Profile Information:")
        print(profile_info)

if __name__ == "__main__":
    main()
