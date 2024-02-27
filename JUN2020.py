import math
import time

class RingStartAngle:
    Standard = 0  # 0 Percent
    Angled = 1    # 30 Percent

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Circle:
    def __init__(self, center=Point(), radius=0):
        self.center = center
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius

    def crosses_other_circle(self, other):
        distance_between_circles = math.sqrt((self.center.x - other.center.x) ** 2 + (self.center.y - other.center.y) ** 2)
        return distance_between_circles < (self.radius + other.radius)

class Ring:
    def __init__(self, center=Point(), side_length=0, ring_start_angle=RingStartAngle.Standard):
        self.center = center
        self.side_length = side_length
        self.ring_start_angle = ring_start_angle
        self.circles = []
        self.create_rings()

    def create_rings(self):
        self.circles.clear()
        for i in range(6):
            radius = self.side_length / 2
            x_point = self.side_length * math.cos(i * math.pi / 3 + int(self.ring_start_angle) * math.pi / 6)
            y_point = self.side_length * math.sin(i * math.pi / 3 + int(self.ring_start_angle) * math.pi / 6)
            self.circles.append(Circle(Point(x_point, y_point), radius))

    def occupying_area(self):
        return self.circles[0].area() * 6

    def ring_fits_snugly_above_another_ring(self, other):
        for circle1 in self.circles:
            for circle2 in other.circles:
                if circle1.crosses_other_circle(circle2):
                    return False
        return True

    def decrement_side_length(self, increment):
        self.side_length -= increment
        self.create_rings()

    def perimeter(self):
        return 2 * math.pi * self.side_length * 1.5

def work_inwards_solution():
    C_radius = 1.5
    total_area = 0
    initial_start_angle = 0
    previous_ring = Ring(Point(), 1, RingStartAngle.Standard)
    while True:
        adding_area = previous_ring.occupying_area()
        if adding_area < 0.0000001:
            break
        total_area += adding_area
        initial_start_angle += 1
        new_ring = Ring(Point(), previous_ring.side_length - 0.0000001, RingStartAngle(initial_start_angle % 2))
        while not new_ring.ring_fits_snugly_above_another_ring(previous_ring):
            new_ring.decrement_side_length(0.0000001)
        print("Found the next hexagon's best-fit radius:", new_ring.side_length, ". Are we angled?", int(new_ring.ring_start_angle))
        previous_ring = new_ring
    return total_area / (math.pi * C_radius ** 2)

if __name__ == "__main__":
    t1 = time.time()
    solution_tuple = work_inwards_solution()
    t2 = time.time()
    print("The efficient solution takes (in microseconds):", (t2 - t1) * 1e6)
    print("Area proportion:", solution_tuple)
