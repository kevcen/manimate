from PySide6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QWidget,
    QTabWidget,
    QGroupBox,
    QFileDialog,
    QMessageBox,
)
import importlib.util
import sys
import inspect
from intermediate.imobject import ICircle, IMobject, ISquare, IStar, ITriangle
from intermediate.itext import IMarkupText, IMathTex
from intermediate.itree import INode
from manim import Mobject

class ObjectsBar(QTabWidget):
    """
    The left widget which controls adding objects to the scene...

    also can control admin related objects.
    """

    def __init__(self, fsm_controller, close_handler):
        super().__init__()

        self.fsm_controller = fsm_controller
        self.close_handler = close_handler

        self.setWindowTitle(" ")

        self.setGeometry(250, 250, 300, 600)

        self.addTab(self.file_tab(), "File")
        self.addTab(self.object_tab(), "Add Objects")
        self.addTab(self.animation_tab(), "Animation")

        self.setTabPosition(QTabWidget.West)
        self.setCurrentIndex(1)

        self.user_defined_mobjects = {}

    def file_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(self.close_handler)
        export_script = QPushButton("Export As Python Script")
        export_script.clicked.connect(lambda: self.fsm_controller.export())
        import_mobject = QPushButton("Import A MObject Class")
        import_mobject.clicked.connect(self.import_mobject_handler)
        export_mp4 = QPushButton("TODO: Export As MP4")
        export_mp4.setEnabled(False)
        import_btn = QPushButton("TODO: Import Script As State")
        import_btn.setEnabled(False)

        for w in (export_script, import_mobject, export_mp4, import_btn):
            layout.addWidget(w)

        # layout.addStretch()
        layout.addWidget(exit_btn)

        tab.setLayout(layout)
        return tab
    
    def import_mobject_handler(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open File', '/home', 'Python Files (*.py)')[0]
        module_name = file_name.split('/')[-1][:-3]
    
        spec = importlib.util.spec_from_file_location(module_name, file_name)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        

        # classes = inspect.getmembers(sys.modules[module_name], inspect.isclass)
        classes = {}
        for name, obj in inspect.getmembers(sys.modules[module_name]):
            if inspect.isclass(obj) and obj.__module__ == module.__name__:
                classes[name] = obj

        msg = QMessageBox()
        msg.setWindowTitle("Manimate")
        msg.setText(f"Are you sure you want to import this file?")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        msg.setDetailedText(f"You will be importing {', '.join(classes.keys())} from {module_name}.py.")
        ret = msg.exec_()
        if ret == QMessageBox.Ok:
            for class_name, mobject_class in classes.items():
                addMobject = QPushButton(f"add {class_name}")
                addMobject.clicked.connect(
                    self.imobject_add(mobject_class)
                )

                if not self.user_defined_mobjects:
                    self.user_defined_mobjects['hji'] = 'h'
                    self.user_mobjects = QGroupBox("User Defined")
                    self.user_layout = QVBoxLayout()
                    self.user_mobjects.setLayout(self.user_layout)
                else:
                    self.user_mobjects.setParent(None)

                self.user_layout.addWidget(addMobject)

            self.objects_layout.insertWidget(0, self.user_mobjects, self.user_layout.count())

            self.fsm_controller.add_python_to_writer(file_name)



    def imobject_add(self, mobject_class):
        return lambda: self.fsm_controller.instant_add_object_to_curr(IMobject(mobject_class(), user_defined=True))

    def animation_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        addFrame = QPushButton("New Frame (+)")
        addFrame.clicked.connect(self.fsm_controller.add_state)
        delFrame = QPushButton("Delete Current Frame (-)")
        delFrame.clicked.connect(self.fsm_controller.del_state)

        for w in (addFrame, delFrame):
            layout.addWidget(w)

        tab.setLayout(layout)
        return tab

    def object_tab(self):
        tab = QWidget()
        self.objects_layout = QVBoxLayout()

        addTree = QPushButton("add tree")
        addTree.clicked.connect(self.add_tree)

        addCircle = QPushButton("add circle")
        addCircle.clicked.connect(
            lambda: self.fsm_controller.instant_add_object_to_curr(ICircle())
        )

        addSquare = QPushButton("add square")
        addSquare.clicked.connect(
            lambda: self.fsm_controller.instant_add_object_to_curr(ISquare())
        )

        addStar = QPushButton("add star")
        addStar.clicked.connect(
            lambda: self.fsm_controller.instant_add_object_to_curr(IStar())
        )

        addTriangle = QPushButton("add triangle")
        addTriangle.clicked.connect(
            lambda: self.fsm_controller.instant_add_object_to_curr(ITriangle())
        )

        addMarkupText = QPushButton("add text")
        addMarkupText.clicked.connect(
            lambda: self.fsm_controller.instant_add_object_to_curr(
                IMarkupText(
                    """click to add text"""
                    # mergeHeaps h1@(t1 : h) h2@(t2 : h')
                    #     | r < r'    = t1 : mergeHeaps h h2
                    #     | r' < r    = t2 : mergeHeaps h1 h'
                    #     | otherwise = mergeHeaps [combineTrees t1 t2] (mergeHeaps h h')
                    #     where
                    #         r  = rank t1
                    #         r' = rank t2"""
                    ,
                    fsm_controller=self.fsm_controller,
                )
            )
        )

        addMathTex = QPushButton("add latex")
        addMathTex.clicked.connect(
            lambda: self.fsm_controller.instant_add_object_to_curr(
                IMathTex(r"\xrightarrow{x^6y^8}", fsm_controller=self.fsm_controller)
            )
        )

        self.simple_mobjects = QGroupBox("Simple Shapes")
        self.complex_mobjects = QGroupBox("Complex Data Structures")
        self.text_mobjects = QGroupBox("Text")
        
        simple_layout = QVBoxLayout()
        complex_layout = QVBoxLayout()
        text_layout = QVBoxLayout()

        for w in (addCircle, addSquare, addTriangle, addStar):
            simple_layout.addWidget(w)

        for w in (addTree, ):
            complex_layout.addWidget(w)

        for w in (addMarkupText, addMathTex):
            text_layout.addWidget(w)

        self.simple_mobjects.setLayout(simple_layout)
        self.complex_mobjects.setLayout(complex_layout)
        self.text_mobjects.setLayout(text_layout)

        for w, l in (
            (self.simple_mobjects, 4),
            (self.text_mobjects, 2),
            (self.complex_mobjects, 1),
        ):
            self.objects_layout.addWidget(w, l)

        tab.setLayout(self.objects_layout)
        return tab

    def add_tree(self):
        node = INode(self.fsm_controller)
        node.show_node()  # can also use instant_add

    def closeEvent(self, e):
        self.close_handler()
        e.accept()
