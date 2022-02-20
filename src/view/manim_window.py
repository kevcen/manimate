import sys
import moderngl
from manim import *
from manim.opengl import *
from manim.renderer.opengl_renderer import OpenGLRenderer

from PySide6.QtGui import QOpenGLContext, QSurfaceFormat
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Qt, Slot, QRect, QEventLoop
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
    QLineEdit,
)

from PySide2.QtWidgets import (
    QToolBar,
    QAction,
    QMenuBar,
    QMenu
)
from __feature__ import true_property
from pathlib import Path
import moderngl_window as mglw
from moderngl_window.context.pyside2.window import Window as PySideWindow
from moderngl_window.timers.clock import Timer
import moderngl as mgl

class ManimPreview(QOpenGLWidget):
    def __init__(self, app, renderer) -> None:
        super().__init__()
        self.geometry = QRect(900, 250, 900, 500)
        self.title = f"Preview"

        # self._widget.layout().setMenuBar(menu)
        format = QSurfaceFormat()
        format.setDepthBufferSize(24)
        format.setStencilBufferSize(8)
        format.setVersion(3, 3)
        format.setProfile(QSurfaceFormat.CoreProfile)
        QSurfaceFormat.setDefaultFormat(format)
        self.setFormat(format)

        # self.size = size
        self.renderer = renderer

        # mglw.activate_context(window=self)
        # self.timer = Timer()
        # self.config = mglw.WindowConfig(ctx=self.ctx, wnd=self, timer=self.timer)
        # self.timer.start()

        # self.ctx = None
        self.is_closing = False

        self.app = app

        self.swap_buffers()
        # self.makeCurrent()
        # self.ctx = None
        # print("created")

    def init(self):
        ctx = self.renderer.context 
        assert ctx, 'context is not initialized'
        self.fb = ctx.detect_framebuffer(self.defaultFramebufferObject())
    
    # def render(self):
    #     self.makeCurrent()
    #     # render smth

    def initializeGL(self):
        # super().initializeGL()
        self.renderer.context = mgl.create_context(require=330)
        self.renderer.window = self
        self.renderer.frame_buffer_object = self.renderer.context.detect_framebuffer(self.manim_window.defaultFramebufferObject())
        # self.renderer.context = self.manim_window.ctx
        self.renderer.context.enable(moderngl.BLEND)
        self.renderer.context.wireframe = config["enable_wireframe"]
        self.renderer.context.blend_func = (
            moderngl.SRC_ALPHA,
            moderngl.ONE_MINUS_SRC_ALPHA,
            moderngl.ONE,
            moderngl.ONE,
        )
        self.init()
        # self.preload()
    
    def swap_buffers(self):
        # self.swapBuffers()
        # self.set_default_viewport()
        # self.app.processEvents()
        pass

    # def paintGL(self):
    #     self.makeCurrent()
    #     self.render()

    # def resizeEvent(self, evt):
    #     QOpenGLWidget.resizeEvent(self, evt)
    #     self.init()
    #     self.update()
    
    # # Delegate event handling to scene.
    def mouseMoveEvent(self, event):
        pass
    #     # super().mouse_move_event(event)
    #     x, y = event.x(), event.y()
    #     dx, dy = self._calc_mouse_delta(x, y)
    #     point = self.renderer.pixel_coords_to_space_coords(x, y)
    #     d_point = self.renderer.pixel_coords_to_space_coords(dx, dy, relative=True)
    #     self.renderer.scene.mouse_move_event(point, d_point)

    # # def key_pressed_event(self, event):
    # #     key = event.key()
    # #     self.renderer.pressed_keys.add(key)
    # #     super().key_pressed_event(event)
    # #     self.renderer.scene.on_key_press(key, None)

    # # def key_release_event(self, event):
    # #     key = event.key()
    # #     if key in self.renderer.pressed_keys:
    # #         self.renderer.pressed_keys.remove(key)
    # #     super().key_release_event(event)
    #     # self.renderer.scene.on_key_release(key, None)

    def mousePressEvent(self, event):
        pass
    #     # super().mouse_press_event(event)
    #     x, y = event.x(), event.y()
    #     button = self._mouse_button_map.get(event.button())
    #     modifiers = event.modifiers()
    #     point = self.renderer.pixel_coords_to_space_coords(x, y)
    #     mouse_button_map = {
    #         1: "LEFT",
    #         2: "MOUSE",
    #         4: "RIGHT",
    #     }
    #     self.renderer.scene.on_mouse_press(point, mouse_button_map[button], modifiers)

    def mouseReleaseEvent(self, event):
        pass
    #     # super().mouse_press_event(event)
    #     x, y = event.x(), event.y()
    #     button = self._mouse_button_map.get(event.button())
    #     modifiers = event.modifiers()
    #     point = self.renderer.pixel_coords_to_space_coords(x, y)
    #     mouse_button_map = {
    #         1: "LEFT",
    #         2: "MOUSE",
    #         4: "RIGHT",
    #     }
    #     self.renderer.scene.on_mouse_release(point, mouse_button_map[button], modifiers)


    # def mouse_drag_event(self, event):
    #     super().on_mouse_drag(x, y, dx, dy, buttons, modifiers)
    #     point = self.renderer.pixel_coords_to_space_coords(x, y)
    #     d_point = self.renderer.pixel_coords_to_space_coords(dx, dy, relative=True)
    #     self.renderer.scene.on_mouse_drag(point, d_point, buttons, modifiers)
    # def swap_buffers(self):
    #     # self.widget.update()
    #     pass
