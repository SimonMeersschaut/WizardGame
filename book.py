from global_variables import GLOBAL


class Book:
    def init():
        Book.x, Book.y = (170, 5)
        Book.open = False
        Book.page = 1

    def render():
        screen = GLOBAL.variables['screen']
        width, height = (104, 129)
        if screen.mouseDown:
            if Book.x < screen.mousePos[0] < Book.x + width and Book.y < screen.mousePos[1] < Book.y+height:
                Book.open = True
            else:
                Book.open = False
        if Book.open:
            screen.renderIMG(f'page{Book.page}.png', (500, 50))
        else:
            screen.renderIMG('book.png', (Book.x, Book.y))
