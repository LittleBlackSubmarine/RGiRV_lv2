import numpy as np
import cv2 as cv

import random
from random import seed



def in_rect(rect, pt1, pt2, pt3):
    if pt1[0] < rect[0] or pt1[0] > rect[2] or pt1[1] < rect[1] or pt1[1] > rect[3]:
        return False
    elif pt2[0] < rect[0] or pt2[0] > rect[2] or pt2[1] < rect[1] or pt2[1] > rect[3]:
        return False
    elif pt3[0] < rect[0] or pt3[0] > rect[2] or pt3[1] < rect[1] or pt3[1] > rect[3]:
        return False
    else:
        return True


def triangle_draw(img, subdiv, d_color):
    triangle_list = subdiv.getTriangleList()
    rect_ = (0, 0, len(img), len(img[0]))

    for triangle in triangle_list:

        pt1 = (triangle[0], triangle[1])
        pt2 = (triangle[2], triangle[3])
        pt3 = (triangle[4], triangle[5])

        if in_rect(rect_, pt1, pt2, pt3):
            cv.line(img, pt1, pt2, d_color, thickness=1)
            cv.line(img, pt2, pt3, d_color, thickness=1)
            cv.line(img, pt3, pt1, d_color, thickness=1)


def get_triangle(ed_1):

    rect_ = (0, 0, len(img), len(img[0]))

    # Point1
    vtx1 = sub_div.edgeOrg(ed_1)[0]
    pt1 = tuple(map(int, sub_div.getVertex(vtx1)[0]))

    # Point2
    ed_2 = sub_div.getEdge(ed_1, cv.SUBDIV2D_NEXT_AROUND_LEFT)
    vtx2 = sub_div.edgeOrg(ed_2)[0]
    pt2 = tuple(map(int, sub_div.getVertex(vtx2)[0]))

    # Point3
    ed_3 = sub_div.getEdge(ed_2, cv.SUBDIV2D_NEXT_AROUND_LEFT)
    vtx3 = sub_div.edgeOrg(ed_3)[0]
    pt3 = tuple(map(int, sub_div.getVertex(vtx3)[0]))

    triangle = np.array([pt1, pt2, pt3])

    if in_rect(rect_, pt1, pt2, pt3):
        return triangle
    else:
        return np.array([[0, 0], [0, 0], [0, 0]])


def get_neighbours(ed_1):
    ed_1_rot = sub_div.rotateEdge(ed_1, 2)
    neighbour1 = get_triangle(ed_1_rot)

    ed_2 = sub_div.getEdge(ed_1, cv.SUBDIV2D_NEXT_AROUND_LEFT)
    ed_2_rot = sub_div.rotateEdge(ed_2, 2)
    neighbour2 = get_triangle(ed_2_rot)

    ed_3 = sub_div.getEdge(ed_2, cv.SUBDIV2D_NEXT_AROUND_LEFT)
    ed_3_rot = sub_div.rotateEdge(ed_3, 2)
    neighbour3 = get_triangle(ed_3_rot)

    return neighbour1, neighbour2, neighbour3


def color_triangle(event, x, y, flags, subdiv):
    ed_1 = subdiv.locate((x, y))[1]
    triangle = get_triangle(ed_1)

    if (np.all(triangle)):

        neighbour1, neighbour2, neighbour3 = get_neighbours(ed_1)
        neighbours = [neighbour1, neighbour2, neighbour3]

        if event == cv.EVENT_LBUTTONDOWN:
            cv.fillPoly(img, pts=[triangle], color=(0, 0, 255))
            for neighbour in neighbours:
                cv.fillPoly(img, pts=[neighbour], color=(255, 0, 0))
            triangle_draw(img, subdiv, (0, 0, 0))

        elif event == cv.EVENT_LBUTTONUP:
            cv.fillPoly(img, pts=[triangle], color=(255, 255, 255))
            for neighbour in neighbours:
                cv.fillPoly(img, pts=[neighbour], color=(255, 255, 255))
            triangle_draw(img, subdiv, (0, 0, 0))

    else:
        triangle_draw(img, subdiv, (0, 0, 0))


seed(333)
points = []

for i in range(0, 20):
    x = random.randrange(20, 420)
    y = random.randrange(20, 420)
    points.append((x, y))

img = np.empty((440, 440, 3))
img.fill(255)
rect = (0, 0, len(img), len(img[0]))


sub_div = cv.Subdiv2D(rect)
for pt in points:
    sub_div.insert(pt)

triangle_draw(img, sub_div, (0, 0, 0))

cv.namedWindow("dln_triangulation")
cv.setMouseCallback("dln_triangulation", color_triangle, sub_div)

print("Use space button to exit program!")

while True:
    cv.imshow("dln_triangulation", img)
    if cv.waitKey(1) == 32:  # Break on space
        break

cv.destroyAllWindows()
