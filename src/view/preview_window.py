import moderngl
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import QTimer, Qt


class PreviewWindow(QOpenGLWidget):
    """
    A custom QOpenGLWidget for rendering Manim animations with ModernGL.
    """

    def __init__(self, app, renderer, close_handler, parent=None):
        super().__init__(parent)
        self.app = app
        self.renderer = renderer
        self.close_handler = close_handler
        self.setGeometry(550, 250, 900, 520)
        self.setWindowTitle("Manimate")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)  # ~60 FPS

    def initializeGL(self):
        self.ctx = moderngl.create_context()
        self.renderer.window = self
        self.renderer.frame_buffer_object = self.ctx.detect_framebuffer()
        self.renderer.context = self.ctx
        self.renderer.context.enable(moderngl.BLEND)
        self.renderer.context.wireframe = False
        self.renderer.context.blend_func = (
            moderngl.SRC_ALPHA,
            moderngl.ONE_MINUS_SRC_ALPHA,
            moderngl.ONE,
            moderngl.ONE,
        )

    def paintGL(self):
        self.renderer.render_frame()
        self.update()

    def resizeGL(self, w, h):
        self.ctx.viewport = (0, 0, w, h)

    def mouseMoveEvent(self, event):
        x, y = event.x(), event.y()
        # This is a hack to get the delta, as QMouseEvent does not provide it directly
        if not hasattr(self, "old_x"):
            self.old_x = x
            self.old_y = y
        dx, dy = x - self.old_x, y - self.old_y
        self.old_x, self.old_y = x, y

        point = self.renderer.pixel_coords_to_space_coords(x, y, top_left=True)
        d_point = self.renderer.pixel_coords_to_space_coords(
            dx, dy, relative=True, top_left=True
        )
        self.renderer.scene.mouse_move_event(point, d_point)

    def mousePressEvent(self, event):
        x, y = event.x(), event.y()
        button = "UNKNOWN"
        if event.button() == Qt.LeftButton:
            button = "LEFT"
        elif event.button() == Qt.RightButton:
            button = "RIGHT"

        modifiers = event.modifiers()
        point = self.renderer.pixel_coords_to_space_coords(x, y, top_left=True)
        self.renderer.scene.on_mouse_press(point, button, modifiers)

    def mouseReleaseEvent(self, event):
        x, y = event.x(), event.y()
        button = "UNKNOWN"
        if event.button() == Qt.LeftButton:
            button = "LEFT"
        elif event.button() == Qt.RightButton:
            button = "RIGHT"

        modifiers = event.modifiers()
        point = self.renderer.pixel_coords_to_space_coords(x, y, top_left=True)
        self.renderer.scene.on_mouse_release(point, button, modifiers)

    def closeEvent(self, event):
        self.close_handler()
        event.accept()
