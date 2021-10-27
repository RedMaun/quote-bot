import json
config = 'config.json'

with open(config, 'r') as f:
    data = json.load(f)

default = data["default"]

class AbstractCommand():
    def __init__(self, handler = [], description = None):
        self.handler = handler
        self.description = description
        
    def hdl(self):
        return self.handler
    
    def dsc(self):
        return self.description

    @staticmethod
    async def ans_up(ans, m):
        if (m.text.count(' ') == 0):
            if (m.text == m.text.upper()):
                up = True
            else:
                up = False
        else:
            ind = m.text.index(' ')
            text = m.text[:ind]
            if (text == text.upper()):
                up = True
            else:
                up = False

        if (ans != ''):
            if (up):
                await m.answer(default["prefix"] + ans.upper())
                return True
            else:
                await m.answer(ans)
                return True