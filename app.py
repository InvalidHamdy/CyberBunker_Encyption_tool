from LogIn import LoginApp
import sys

def main():
    login_app = LoginApp()
    try:
        login_app.show_login()
    except KeyboardInterrupt:
        login_app.root.destroy()
        sys.exit(0)

if __name__ == "__main__":
    main()