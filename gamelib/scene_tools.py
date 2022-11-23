class FrameCounter:
    def __init__(self, fps: int):
        self.fps = fps
        self.frame: int = 0
        self.milliseconds: int = 0
        self.seconds: int = 0
        self.minutes: int = 0
        self.new_second = False
        self.new_minute = False

    def tick(self, delta_time: int):
        self.new_second = False
        self.new_minute = False
        self.frame += 1
        self.milliseconds += delta_time
        if self.milliseconds >= 1000:
            self.milliseconds -= 1000
            self.seconds += 1
            self.new_second = True
        if self.seconds >= 60:
            self.seconds -= 60
            self.minutes += 1
            self.new_minute = True


__all__ = ["FrameCounter"]
