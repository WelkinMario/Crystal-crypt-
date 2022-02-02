class Text():
    def __init__(self, setting, screen):
        self.screen = screen
        self.setting= setting

        self.instruction = '''
You are invited to {}!
Go to find Key and Chest, and Exit at last
Use Arrow key or w/s/a/d to move
Press Space to enter the crypt
Press C to use potion if you have any
Be careful of your Stamina and Health
And then, Begin Your Advanture!
But if you are stuck, press R at any time to retry
'''.format(setting.caption)

        self.dead_massage = '''
YOU ARE DEAD
Press R to try again
'''
        self.exit_massage = '''
Press Space to leave
'''
