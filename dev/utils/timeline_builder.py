from dev.renderers.basic_renderer import BasicRenderer

class TimelineBuilder:
    def __init__(self, persons, events, renderer=None):
        self.persons = persons
        self.events = events
        self.renderer = renderer or BasicRenderer()

    def build(self, output_path="timeline.png"):
        self.renderer.render(self.persons, self.events, output_path)
