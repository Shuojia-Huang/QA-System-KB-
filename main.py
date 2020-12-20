from core import Core

if __name__ == "__main__":
    app = Core()
    while True:
        question = input('请输入问题:')
        if question == 'quit':
            break
        app.run(question)