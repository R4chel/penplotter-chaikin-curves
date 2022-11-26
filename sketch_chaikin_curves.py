import vsketch
from shapely.geometry import Point
import math
import vpype as vp

def draw_path(vsk:vsketch.Vsketch, points):
    if len(points) < 2:
        return
    p0 = points[0]
    p0x, p0y = points[0].x, points[0].y
    for p in points[1:]:
        vsk.line(p0.x,p0.y, p.x,p.y)
        p0 = p
            

class ChaikinCurvesSketch(vsketch.SketchClass):
    # Sketch parameters:
    num_points = vsketch.Param(5)
    # iterations = vsketch.Param(7)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a6", landscape=True)
        scale = "mm"
        vsk.scale(scale)
        factor = 1 / vp.convert_length(scale)
        width, height = factor * vsk.width, factor * vsk.height

        points = [Point(vsk.random(width), vsk.random(height)) for _ in range(self.num_points)]
        draw_path(vsk, points)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    ChaikinCurvesSketch.display()
