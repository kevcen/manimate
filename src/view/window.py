import sys
import moderngl
from manim import *
from manim.opengl import *
import moderngl_window as mglw
from moderngl_window.context.pyside2.window import Window as PySideWindow
from moderngl_window.timers.clock import Timer

class QTWindow(PySideWindow):
    def __init__(self, app, renderer) -> None:
        super().__init__()
        self._widget.setGeometry(550, 250, 900, 520)
        self.title = f"Manimate"

        # self.size = size
        self.renderer = renderer

        mglw.activate_context(window=self)
        self.timer = Timer()
        self.config = mglw.WindowConfig(ctx=self.ctx, wnd=self, timer=self.timer)
        self.timer.start()

        self.swap_buffers()


    def export(self):
        pass
    
    # Delegate event handling to scene.
    def mouse_move_event(self, event):
        super().mouse_move_event(event)
        x, y = event.x(), event.y()
        dx, dy = self._calc_mouse_delta(x, y)
        point = self.renderer.pixel_coords_to_space_coords(x, y, top_left=True)
        d_point = self.renderer.pixel_coords_to_space_coords(dx, dy, relative=True, top_left=True)
        self.renderer.scene.mouse_move_event(point, d_point)

    # def key_pressed_event(self, event):
    #     key = event.key()
    #     self.renderer.pressed_keys.add(key)
    #     super().key_pressed_event(event)
    #     self.renderer.scene.on_key_press(key, None)

    # def key_release_event(self, event):
    #     key = event.key()
    #     if key in self.renderer.pressed_keys:
    #         self.renderer.pressed_keys.remove(key)
    #     super().key_release_event(event)
        # self.renderer.scene.on_key_release(key, None)

    def mouse_press_event(self, event):
        super().mouse_press_event(event)
        x, y = event.x(), event.y()
        button = self._mouse_button_map.get(event.button())
        modifiers = event.modifiers()
        point = self.renderer.pixel_coords_to_space_coords(x, y, top_left=True)
        mouse_button_map = {
            1: "LEFT",
            # 2: "MOUSE",
            2: "RIGHT",
        }
        self.renderer.scene.on_mouse_press(point, mouse_button_map[button], modifiers)

    def mouse_release_event(self, event):
        super().mouse_press_event(event)
        x, y = event.x(), event.y()
        button = self._mouse_button_map.get(event.button())
        modifiers = event.modifiers()
        point = self.renderer.pixel_coords_to_space_coords(x, y, top_left=True)
        mouse_button_map = {
            1: "LEFT",
            # 2: "MOUSE",
            2: "RIGHT",
        }
        self.renderer.scene.on_mouse_release(point, mouse_button_map[button], modifiers)


    # def mouse_drag_event(self, event):
    #     super().on_mouse_drag(x, y, dx, dy, buttons, modifiers)
    #     point = self.renderer.pixel_coords_to_space_coords(x, y)
    #     d_point = self.renderer.pixel_coords_to_space_coords(dx, dy, relative=True)
    #     self.renderer.scene.on_mouse_drag(point, d_point, buttons, modifiers)
    # def swap_buffers(self):
    #     # self.widget.update()
    #     pass
