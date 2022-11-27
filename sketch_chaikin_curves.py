import vsketch
from shapely.geometry import Point
import math
import vpype as vp

def to_cartesian(r, theta):
    return Point(r * math.cos(theta), r * math.sin(theta))



def to_polar(center, p):
    r = p.distance(center)
    theta = math.acos((p.x-center.x)/r)
    return (r, theta)



class ChaikinCurvesSketch(vsketch.SketchClass):
    # Sketch parameters:
    num_points = vsketch.Param(5)
    iterations = vsketch.Param(4)
    closed = vsketch.Param(False)
    debug= vsketch.Param(False)
    only_draw_last = vsketch.Param(False)
    always_resort = vsketch.Param(False)
    precision = vsketch.Param(3)

    def sort_points(self, points):
        if self.closed:
            self.center = Point(sum([p.x for p in points])/len(points), sum([p.y for p in points])/len(points))
        # center = Point(self.width/2,self.height/2)
            points.sort(key = lambda p : to_polar(self.center, p)[::-1])
        else:
            points.sort(key = lambda p : ( p.x, p.y ))
        if self.closed and points[-1] != points[0]:
            points.append(points[0])

    def lerp_points(self, p0, p1, pct):
        x = round(p0.x*pct+p1.x*(1-pct), self.precision)
        y = round(p0.y*pct+p1.y*(1-pct), self.precision)
        return Point(x,y)

    def draw_path(self, vsk:vsketch.Vsketch, points):
        if len(points) < 2:
            return
        p0 = points[0]
        i = 1
        for p in points[1:]:
            if self.debug:
                vsk.strokeWeight(i)
                i = i % 10
                i += 1
            vsk.line(p0.x,p0.y, p.x,p.y)
            p0 = p
        # if closed:
        #     vsk.line(p0.x, p0.y, points[0].x,points[0].y)


    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a6", landscape=True)
        scale = "mm"
        vsk.scale(scale)
        factor = 1 / vp.convert_length(scale)
        self.width, self.height = factor * vsk.width, factor * vsk.height

        points = [Point(vsk.random(self.width), vsk.random(self.height)) for _ in range(self.num_points)]
        self.sort_points(points)
        if self.debug:
            vsk.circle(center.x,center.y, 20)
            print([(p.x, p.y) for p in points])
        if not self.only_draw_last:
            self.draw_path(vsk, points)
         
        for _ in range(self.iterations):
            new_points = []
            p0 = points[0]
            for p in points[1:]:
                lerp1 = self.lerp_points(p0, p, 0.25)
                if len(new_points) == 0 or lerp1 != new_points[-1]:
                    new_points.append(lerp1)
                lerp2 = self.lerp_points(p0, p, 0.75)
                if lerp2 != new_points[-1]:
                    
                    new_points.append(lerp2)
                p0 = p
            
            if not self.only_draw_last:
                self.draw_path(vsk, points)
         
            points = new_points
            if self.always_resort:
                self.sort_points(points)

        if self.only_draw_last:
            self.draw_path(vsk, points)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    ChaikinCurvesSketch.display()
