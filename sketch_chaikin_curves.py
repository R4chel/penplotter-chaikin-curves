import vsketch
from shapely.geometry import Point
import math
import vpype as vp

def draw_path(vsk:vsketch.Vsketch, points):
    if len(points) < 2:
        return
    p0 = points[0]
    for p in points[1:]:
        vsk.line(p0.x,p0.y, p.x,p.y)
        p0 = p
            

class ChaikinCurvesSketch(vsketch.SketchClass):
    # Sketch parameters:
    num_points = vsketch.Param(5)
    iterations = vsketch.Param(7)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a6", landscape=True)
        scale = "mm"
        vsk.scale(scale)
        factor = 1 / vp.convert_length(scale)
        width, height = factor * vsk.width, factor * vsk.height

        points = [Point(vsk.random(width), vsk.random(height)) for _ in range(self.num_points)]
        points.sort(key=lambda p : p.x)
        draw_path(vsk, points)

        for _ in range(self.iterations):
            new_points = []
            p0 = points[0]
            for p in points[1:]:
                new_points.append(Point(p0.x*.75+p.x*.25,p0.y*.75+p.y*.25))
                new_points.append(Point(p0.x*.25+p.x*.75,p0.y*.25+p.y*.75))
                p0 = p
            draw_path(vsk, new_points)
            points = new_points

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    ChaikinCurvesSketch.display()
