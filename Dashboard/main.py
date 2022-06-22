from application import Application

class App:
    def __init__(self):
        self.application = Application()


    def run(self):
        while True:
            self.application.update()


if __name__ == '__main__':
    app = App()
    app.run()

