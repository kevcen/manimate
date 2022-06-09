from PySide6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QWidget,
    QTabWidget,
)
from intermediate.imobject import ICircle, ISquare, IStar, ITriangle
from intermediate.itext import IMarkupText, IMathTex
from intermediate.itree import INode


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

    def file_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(self.close_handler)
        export_script = QPushButton("Export As Python Script")
        export_script.clicked.connect(self.fsm_controller.export)
        export_mp4 = QPushButton("TODO: Export As MP4")
        export_mp4.setEnabled(False)
        import_btn = QPushButton("TODO: Import Script As State")
        import_btn.setEnabled(False)

        for w in (export_script, export_mp4, import_btn):
            layout.addWidget(w)

        layout.addStretch()
        layout.addWidget(exit_btn)

        tab.setLayout(layout)
        return tab

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
        layout = QVBoxLayout()

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

        for w in (
            addTree,
            addCircle,
            addSquare,
            addTriangle,
            addStar,
            addMarkupText,
            addMathTex,
        ):
            layout.addWidget(w)

        tab.setLayout(layout)
        return tab

    def add_tree(self):
        node = INode(self.fsm_controller)
        node.show_node()  # can also use instant_add

    def closeEvent(self, e):
        self.close_handler()
        e.accept()
