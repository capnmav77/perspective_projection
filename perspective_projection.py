import pygame
import numpy as np
from math import *


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WIDTH, HEIGHT = 800, 600
pygame.display.set_caption("Perspective Projection")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

scale = 100

circle_pos = [WIDTH/2, HEIGHT/2]

anglex = 0
angley = 0
anglez = 0

camera_angle_x=0
camera_angle_y=0
camera_angle_z=0


points = []
points.append(np.array([-1, -1, -1]))
points.append(np.array([1, -1, -1]))
points.append(np.array([1,  1, -1]))
points.append(np.array([-1, 1, -1]))
points.append(np.array([-1, -1, -2]))
points.append(np.array([1, -1, -2]))
points.append(np.array([1, 1, -2]))
points.append(np.array([-1, 1, -2]))


def connect_points(i, j, points):
    pygame.draw.line(
        screen, BLACK, (points[i][0], points[i][1]), (points[j][0], points[j][1]))


def perspective_projection(points, fov, aspect_ratio, near_clip, far_clip):
    f = 1 / tan(radians(fov / 2))
    perspective_matrix = np.array([
        [f / aspect_ratio, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far_clip + near_clip) / (near_clip - far_clip), 2 * far_clip * near_clip / (near_clip - far_clip)],
        [0, 0, -1, 0]
    ])
    points = np.hstack((points, np.ones((len(points), 1))))
    projected_points = np.dot(points,perspective_matrix)
    normalized_points = projected_points[:, :-1] / projected_points[:, -1].reshape((-1, 1))
    return normalized_points.tolist()



def rotate_around_camera(points, angle_x, angle_y, angle_z):
    rotation_x = np.array([
        [1, 0, 0],
        [0, cos(angle_x), -sin(angle_x)],
        [0, sin(angle_x), cos(angle_x)],
    ])

    rotation_y = np.array([
        [cos(angle_y), 0, sin(angle_y)],
        [0, 1, 0],
        [-sin(angle_y), 0, cos(angle_y)],
    ])

    rotation_z = np.array([
        [cos(angle_z), -sin(angle_z), 0],
        [sin(angle_z), cos(angle_z), 0],
        [0, 0, 1],
    ])

    rotation_matrix = np.dot(np.dot(rotation_x, rotation_y), rotation_z)
    return [np.dot(rotation_matrix, i) for i in points]



def rotate_along_axis(points, angle_x, angle_y, angle_z):
    center = np.mean(points, axis=0)
    points=[p - center for p in points]
    rotation_x = np.array([
        [1, 0, 0],
        [0, cos(angle_x), -sin(angle_x)],
        [0, sin(angle_x), cos(angle_x)],
    ])

    rotation_y = np.array([
        [cos(angle_y), 0, sin(angle_y)],
        [0, 1, 0],
        [-sin(angle_y), 0, cos(angle_y)],
    ])

    rotation_z = np.array([
        [cos(angle_z), -sin(angle_z), 0],
        [sin(angle_z), cos(angle_z), 0],
        [0, 0, 1],
    ])

    rotation_matrix = np.dot(np.dot(rotation_x, rotation_y), rotation_z)
    return [center+np.dot(rotation_matrix, i) for i in points]



clock = pygame.time.Clock()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
                #Arrow keys rotation around camera
            elif event.key == pygame.K_UP:
                camera_angle_z += 0.1
            elif event.key == pygame.K_DOWN:
                camera_angle_z -= 0.1
            elif event.key == pygame.K_LEFT:
                camera_angle_y += 0.1
            elif event.key == pygame.K_RIGHT:
                camera_angle_y -= 0.1
            elif event.key == pygame.K_RCTRL:
                camera_angle_x += 0.1
            elif event.key == pygame.K_KP0:
                camera_angle_x -= 0.1

            #numpad keys for object rotation along its axis
            elif event.key == pygame.K_KP8:
                anglez += 0.1
            elif event.key == pygame.K_KP2:
                anglez -= 0.1
            elif event.key == pygame.K_KP4:
                angley += 0.1
            elif event.key == pygame.K_KP6:
                angley -= 0.1
            elif event.key == pygame.K_KP7:
                anglex += 0.1
            elif event.key == pygame.K_KP9:
                anglex -= 0.1

            #WASDQE for translation of object
            #ZX for scaling of object
            


            

    screen.fill(WHITE)
    rotatedPoints=rotate_along_axis(points,anglex,angley,anglez)
    rotatedPoints=rotate_around_camera(rotatedPoints,camera_angle_x,camera_angle_y,camera_angle_z)
    projected_points=[]
    projected2dList =perspective_projection(rotatedPoints,np.radians(75),1,0.25,100.0)

    for projected2d in projected2dList:
        x = int(projected2d[0]) + circle_pos[0]
        y = int(projected2d[1]) + circle_pos[1]

        projected_points.append([x, y])
        pygame.draw.circle(screen, RED, (x, y), 5)

    for p in range(4):
        connect_points(p, (p+1) % 4, projected_points)
        connect_points(p+4, ((p+1) % 4) + 4, projected_points)
        connect_points(p, (p+4), projected_points)

    pygame.display.update()
