import math
import random
from math import sqrt
from operator import attrgetter
import matplotlib.pyplot as plt


N = 100
K = 5


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def set_distance(self, dist):
        self.dist = dist

    def set_classter(self, claster):
        self.claster = claster

    def set_color(self, color):
        self.color = color


def init_point(color):
    rand_x = random.randrange(0, N + 1)
    rand_y = random.randrange(0, N + 1)
    rand_z = random.randrange(0, N + 1)
    p = Point(rand_x, rand_y, rand_z)
    p.set_color(color)

    return p


def init_all_points():
    points = []
    for i in range(0, N):
        a = init_point(color="black")
        points.append(a)

    return points


def generate_k(points):
    """
    :param points: list of objects
    find the minimum and maximum for each coordinate.
    Generate K random points between the ranges.
    :return list of the random points.
    """
    colors = ["blue", "red", "green", "violet", "yellow"]
    centers = []

    # for x dimension
    min_num = min(points, key=attrgetter('x'))
    max_num = max(points, key=attrgetter('x'))

    # for y dimension
    min_num2 = min(points, key=attrgetter('y'))
    max_num2 = max(points, key=attrgetter('y'))

    # for z dimension
    min_num3 = min(points, key=attrgetter('z'))
    max_num3 = max(points, key=attrgetter('z'))

    for k in range(K):
        centroid = Point(round(random.uniform(min_num.x, max_num.x)),
                         round(random.uniform(min_num2.y, max_num2.y)),
                         round(random.uniform(min_num3.z, max_num3.z)))
        rand_col = random.randrange(0, 5)
        centroid.set_color(colors[rand_col])
        centroid.claster = k
        centers.append(centroid)

    return centers


def find_distance(points, centroids):
    """
    :params points: list of N points
            centroids: list of K centroids
    K distance values for each data point.
    Choose the closest center and assign relevant data point to center.
    """
    assignments = []
    for point in points:
        shortest = math.inf
        shortest_index = 0
        new_color = ''
        for i in centroids:
            val = distance(point, i)
            if val < shortest:
                shortest = val
                shortest_index = i.claster
                new_color = i.color
        point.dist = shortest
        point.claster = shortest_index
        point.set_color(new_color)
        assignments.append(shortest_index)

    return assignments, points


def distance(point, centroid):
    sum = 0
    difference_sq = (point.x - centroid.x) ** 2
    difference_sq2 = (point.y - centroid.y) ** 2
    difference_sq3 = (point.z - centroid.z) ** 2
    sum = difference_sq + difference_sq2 + difference_sq3

    return sqrt(sum)


def calculate_avg(points, center):
    Si = float(len(points) + 0.00001)
    dim_sum, dim_sum2, dim_sum3 = 0, 0, 0
    for p in points:
        dim_sum += p.x
        dim_sum2 += p.y
        dim_sum3 += p.z
    # average of each dimension
    center.x = dim_sum / Si
    center.y = dim_sum2 / Si
    center.z = dim_sum3 / Si

    return center


def update_centers(points, centroids):
    """
    :param points: list of all points
    :return list of updates K centers
    """
    new_means = dict()
    for c in centroids:
        new_means[c] = []
        for point in points:
            if point.claster == c.claster:
                new_means[c].append(point)
    for centroida, points_list in new_means.items():
        centroida = calculate_avg(points_list, centroida)

    return list(new_means.keys())


def connect_points(centres, points):
    for centr in centres:
        x1 = centr.x
        y1 = centr.y
        z1 = centr.z
        for point in points:
            if point.claster == centr.claster:
                x2 = point.x
                y2 = point.y
                z2 = point.z
                plt.plot([x1, x2], [y1, y2], [z1, z2], color=centr.color)


if __name__ == "__main__":
    old_assignments = None
    points_list = init_all_points()
    centroids_list = generate_k(points_list)

    # show start
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    fig.suptitle("Start K-means")
    for i in points_list:
        ax.scatter(i.x, i.y, i.z, c=i.color)
    for i in centroids_list:
        ax.scatter(i.x, i.y, i.z, c=i.color, marker='o', s=120)
    plt.show()

    assignments_list, clasterized_points = find_distance(points_list, centroids_list)
    new_centers_list = []
    while assignments_list != old_assignments:
        new_centers_list = update_centers(clasterized_points, centroids_list)
        old_assignments = assignments_list
        assignments_list = find_distance(clasterized_points, new_centers_list)
        # for showing iterating plots
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for i in clasterized_points:
            ax.scatter(i.x, i.y, i.z, c=i.color)
        for i in new_centers_list:
            ax.scatter(i.x, i.y, i.z, c=i.color, marker='o', s=120)
        connect_points(new_centers_list, clasterized_points)
        plt.show()

    # RES
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    fig.suptitle("RESULT K-means")
    for i in clasterized_points:
        ax.scatter(i.x, i.y, i.z, c=i.color)
    for i in new_centers_list:
        ax.scatter(i.x, i.y, i.z, c=i.color, marker='o', s=120)
    connect_points(new_centers_list, clasterized_points)
    plt.show()

