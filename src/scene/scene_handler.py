

from fsm.reverser import Reverser


class SceneHandler:
    def __init__(self, scene):
        self.scene = scene
        self.reverser = Reverser()

    def play(self, state):
        forward_anim = [self.reverser.forward(anim) for anim in state.animations]

        if forward_anim:
            self.scene.play(*forward_anim)
            # self.scene.wait()


    def playFast(self, state):
        forward_anim = [self.reverser.forward(anim) for anim in state.animations]
        for animation in forward_anim:
            animation.run_time = 0

        if forward_anim:
            self.scene.play(*forward_anim)

    def playRev(self, state):
        reversed_anim = [self.reverser.reverse(instr) for instr in state.animations]
        
        for animation in reversed_anim:
            animation.run_time = 0

        if reversed_anim:
            self.scene.play(*reversed_anim)

    def reset(self):
        self.scene.clear()
        self.scene.render()
            