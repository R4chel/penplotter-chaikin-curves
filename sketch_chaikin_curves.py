import vsketch
from shapely.geometry import Point
import math
import vpype as vp

def to_cartesian(r, theta):
    return Point(r * math.cos(theta), r * math.sin(theta))


def draw_path(vsk:vsketch.Vsketch, points, closed):
    if len(points) < 2:
        return
    p0 = points[0]
    i = 1
    for p in points[1:]:
        vsk.strokeWeight(i)
        i += 1
        vsk.line(p0.x,p0.y, p.x,p.y)
        p0 = p
    if closed:
        vsk.line(p0.x, p0.y, points[0].x,points[0].y)

def to_polar(center, p):
    r = center.distance(p)
    theta = math.acos((p.x-center.x)/r)
    print(p, r, theta)
    return (r, theta)

class ChaikinCurvesSketch(vsketch.SketchClass):
    # Sketch parameters:
    num_points = vsketch.Param(5)
    iterations = vsketch.Param(4)
    closed = vsketch.Param(False)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a6", landscape=True)
        scale = "mm"
        vsk.scale(scale)
        factor = 1 / vp.convert_length(scale)
        width, height = factor * vsk.width, factor * vsk.height

        points = [Point(vsk.random(width), vsk.random(height)) for _ in range(self.num_points)]
        # center = Point(sum([p.x for p in points])/len(points), sum([p.y for p in points])/len(points))
        center = Point(width/2,height/2)
        # vsk.circle(center.x,center.y, 20)
        print([(p.x, p.y) for p in points])
        points.sort(key=lambda p : to_polar(center, p)[::-1])
        print([(p.x, p.y) for p in points])
        draw_path(vsk, points, self.closed)

        for _ in range(self.iterations):
            new_points = []
            p0 = points[0]
            for p in points[1:]:
                new_points.append(Point(p0.x*.75+p.x*.25,p0.y*.75+p.y*.25))
                new_points.append(Point(p0.x*.25+p.x*.75,p0.y*.25+p.y*.75))
                p0 = p
            draw_path(vsk, new_points, self.closed)
            points = new_points
            points.sort(key=lambda p : to_polar(center, p)[::-1])

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    ChaikinCurvesSketch.display()
