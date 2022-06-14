from PySide6.QtGui import QColor, QPainter
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QSlider,
    QStyleOptionSlider,
)


class TimeSlider(QSlider):
    """
    Styled QSlider for the time slider.
    """

    def paintEvent(self, ev):
        super(TimeSlider, self).paintEvent(ev)

        style = QApplication.style()
        opt = QStyleOptionSlider()
        handle = style.subControlRect(style.CC_Slider, opt, style.SC_SliderHandle)

        p = QPainter(self)

        # custom ticks to make discreteness obvious
        interval = self.tickInterval()
        if interval == 0:
            interval = self.pageStep()

        tp = self.tickPosition()
        if tp != QSlider.TickPosition.NoTicks:
            for i in range(self.minimum(), self.maximum() + 1, interval):
                if self.minimum() == self.maximum():
                    return

                x = (
                    round(
                        (i - self.minimum())
                        / (self.maximum() - self.minimum())
                        * (self.width() - handle.width())
                        + (handle.width() / 2.0)
                    )
                    - 1
                )
                h = 2
                p.setPen(QColor("#ffffff"))
                if (
                    tp == QSlider.TickPosition.TicksBothSides
                    or tp == QSlider.TickPosition.TicksAbove
                ):
                    y = self.rect().top()
                    p.drawLine(x, y, x, y + h)

                if (
                    tp == QSlider.TickPosition.TicksBothSides
                    or tp == QSlider.TickPosition.TicksBelow
                ):
                    y = self.rect().bottom()
                    p.drawLine(x, y, x, y - h)


class StateWidget(QWidget):
    """
    The bottom widget which controls the the state machine.
    """

    def __init__(self, scene_controller, fsm_controller, close_handler):
        def time_change_handler(value):
            scene_controller.unselect_mobjects()
            label.setText(f"{value}/{time_slider.maximum()}")
            fsm_controller.set_state_number(value)

        def state_change_handler(value, length):
            time_slider.setMaximum(length)
            time_slider.setValue(value)
            label.setText(f"{value}/{length}")

        super().__init__()

        self.close_handler = close_handler

        self.setWindowTitle(" ")
        self.setGeometry(550, 800, 900, 100)

        # button1 = QPushButton("manim it")
        # button1.clicked.connect(lambda : self.manim_run())
        layout = QVBoxLayout()

        video_buttons = QHBoxLayout()
        slider_buttons = QHBoxLayout()

        run_btn = QPushButton("Play")
        run_btn.clicked.connect(fsm_controller.run)

        stop_btn = QPushButton("Pause")
        stop_btn.clicked.connect(fsm_controller.stop)

        video_buttons.addStretch()
        video_buttons.addWidget(run_btn)
        video_buttons.addWidget(stop_btn)
        video_buttons.addStretch()

        add_frame_btn = QPushButton("+")
        add_frame_btn.clicked.connect(fsm_controller.add_state)
        del_frame_btn = QPushButton("-")
        del_frame_btn.clicked.connect(fsm_controller.del_state)

        export_btn = QPushButton("Export")
        export_btn.clicked.connect(lambda: fsm_controller.export())

        time_slider = TimeSlider()
        time_slider.setOrientation(Qt.Horizontal)
        time_slider.setTickInterval(1)
        time_slider.setMinimum(1)
        time_slider.setMaximum(1)
        time_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        time_slider.setValue(1)
        time_slider.valueChanged.connect(time_change_handler)

        label = QLabel("1/1")

        fsm_controller.stateChange.connect(state_change_handler)

        for w in (time_slider, label, add_frame_btn, del_frame_btn, export_btn):
            slider_buttons.addWidget(w)

        layout.addLayout(video_buttons)
        layout.addLayout(slider_buttons)
        self.setLayout(layout)

    def close_event(self, e):
        self.close_handler()
        e.accept()
