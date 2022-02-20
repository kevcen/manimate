import sys
import signal
import PySide2
import moderngl
from manim import *
from manim.opengl import *
from manim.renderer.opengl_renderer import OpenGLRenderer

from PySide6.QtGui import QOpenGLContext, QSurfaceFormat
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Qt, Slot, QTimer, QTranslator, QObject, QThread, Signal
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
    QLineEdit,
    QMainWindow,
    QMenuBar,
    QMenu,
    QWidgetAction
)
from __feature__ import true_property
from fsm.state_handler import StateHandler
import scene.manim_scene as manim_scene 
from pathlib import Path
import moderngl_window as mglw
from moderngl_window.context.pyside2.window import Window as PySideWindow
from moderngl_window.timers.clock import Timer
from scene.scene_handler import SceneHandler
from view.objects_bar import ObjectsBar

from view.state_bar import StateWidget
from view.manim_window import ManimPreview

from threading import Thread

import moderngl as mgl

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.windowTitle = "Manimate"
        self.setStyleSheet("background-color: #232326; color: white")
        self.openWindows = set()
        self.app = app


        button_action = QWidgetAction(QLabel("lol"))
        # button_action.triggered.connect(self.export)

        bar = self.menuBar()
        file_menu = bar.addMenu("File")
        file_menu.addAction("Export")

        
        # QApplication.instance().focusChanged.connect(self.raiseWidgets)

    def raise_(self):
        pass
    
    def raiseWidgets(self):
        for window in self.openWindows:
            window.raise_()

    def addWindow(self, window, show=False):
        # window.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.openWindows.add(window)

        if show:
            window.show()
            self.app.processEvents()


    def export(self):
        pass

    def setupManimGui(self):
        with tempconfig( {
            "input_file": Path("scene/manim_scene.py").absolute(), "renderer": "opengl", "preview": True, "write_to_movie": False, "format": None
        }):           
            # self.openWindows.add(self.manim_window)
            # self.addWindow(self.manim_window.wnd)
            # self.layout().addWidget(self.manim_window._widget)

           
            

            self.scene_handler = SceneHandler()
            state_handler = StateHandler(self.scene_handler)

            objects_bar = ObjectsBar(state_handler)
            self.addWindow(objects_bar, show=True)

            state_bar = StateWidget(self.scene_handler, state_handler)
            self.addWindow(state_bar, show=True)

            
            # self.app.processEvents()
            # self.app.processEvents()
            # self.app.processEvents()
            # self.app.processEvents()
            # self.app.processEvents()
            # self.app.processEvents()

            
            # self.app.processEvents()



            renderer = OpenGLRenderer()
            self.manim_window = ManimPreview(self.app, renderer)
            # self.manim_window.resize(900, 400)

            self.worker = Worker(renderer, self.manim_window)
            self.worker.finished.connect(self.worker.deleteLater)
            self.worker.scene_set.connect(self.setScene)

            self.worker.start()


    def setScene(self, scene):
        self.scene = scene 
        self.scene_handler.setScene(scene)

    def closeEvent(self, event):
        super().closeEvent(event)
        for window in self.openWindows:
            window.close()

class Worker(QThread):
    finished = Signal()
    scene_set = Signal(Scene)

    def __init__(self, renderer, manim_window):
        super().__init__()
        self.renderer = renderer 
        self.manim_window = manim_window

    def run(self):
        with tempconfig( {
            "input_file": Path("scene/manim_scene.py").absolute(), "renderer": "opengl", "preview": True, "write_to_movie": False, "format": None
        }):  
            # self.manim_window.resize(900, 400)
            scene = manim_scene.Test(self.renderer)
            self.renderer.scene = scene
            self.scene_set.emit(scene)

            scene.render()
            self.finished.emit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)

    mainWindow = MainWindow(app)
    app.processEvents()
    mainWindow.showMaximized()
    app.processEvents()
    mainWindow.setupManimGui()

    while True:
        app.processEvents()

    # QTimer.singleShot(0, mainWindow.close)
    # thread = Thread(target=app.exec)
    # thread.start()


    # with tempconfig( {
    #     "input_file": Path("scene/manim_scene.py").absolute(), "renderer": "opengl", "preview": True, "write_to_movie": False, "format": None
    # }):    
    #     mainWindow.scene.render()
    # sys.exit(app.exec())
    # thread.join()
    # app.exec()