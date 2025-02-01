import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from mouse_recorder import MouseApp

def main():
    app = MouseApp()
    app.run()

if __name__ == "__main__":
    main() 