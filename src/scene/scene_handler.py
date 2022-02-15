

class SceneHandler:
    def __init__(self, scene):
        self.scene = scene

    def playFast(self, state):
        for animation in state.animations:
            animation.run_time = 0
        self.scene.play(*state.animations)

    def reset(self):
        self.scene.clear()
        self.scene.render()
            