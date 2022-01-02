import time
from global_variables import GLOBAL


class Message:
    font_size = 26
    width = 1600-50

    def __init__(self, message, person):
        self.person = person
        self.animation_start = time.time()

        i = 0
        self.message = []
        current_text = ""
        for word in message.split(' '):
            if (i+len(word))*Message.font_size > Message.width+1500:
                self.message.append(current_text)
                current_text = ''
                i = 0
            i += len(word)+1
            current_text += " "+word
        self.message.append(current_text)

    def render(self):
        GLOBAL.variables['screen'].draw_rect(
            320, 20, 1600-50, 70+len(self.message)*Message.font_size, color=(255, 255, 255))
        GLOBAL.variables['screen'].render_text(self.person, 1900-len(self.person)*Message.font_size, 20, color=(
            0, 0, 0), fontsize=Message.font_size+2, bold=True)

        animation_text = self.message[0:min(int(
            (time.time()-self.animation_start)*40), len(self.message))]
        total = 0
        for i, text in enumerate(self.message):

            GLOBAL.variables['screen'].render_text(
                text[0:max(0, min(int((time.time()-self.animation_start)*80)-total, len(text)-1))], 350, 60+i*30, color=(0, 0, 0), fontsize=Message.font_size)
            total += len(text)


class Cut_Scene:
    class Animation:
        def __init__(self, image):
            self.image = image

    def __init__(self):
        pass


class Story_telling:
    messages = []

    def init():
        Story_telling.messages.append(Message(
            "Hello, welcome, this is a super random message that nobody cares about, but it has to be as long as I can, so I will use Lorem Ipsoum, who dolors sid amet: loremipsum dolors sit amet in a box wayfarerer blijft ma gaan . . . test test Hello, welcome, this is a super random message that nobody cares about, but it has to be as long as I can, so I will use Lorem Ipsoum, who dolors sid amet: loremipsum dolors sit amet in a box wayfarerer blijft ma gaan . . . test test", "een zeer lange naam"))
        pass  # necessary!

    def render():
        for message in Story_telling.messages:
            message.render()

    def tell(person, title, message):
        pass
