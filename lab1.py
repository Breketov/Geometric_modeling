from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQGLViewer import QGLViewer
from OpenGL.GL import *
import numpy as np
import random as rn
from CGAL.CGAL_Kernel import Point_3, Vector_3


class Viewer(QGLViewer):
    def __init__(self, parent=None):
        QGLViewer.__init__(self, parent)
        self.task = None
        self.points = []
        self.resize(1280, 720)


    def randPoint(self):
        self.points = []
        num_point = 400
        
        if self.task == 'cube':
            n = 6
            x = np.linspace(-1, 1, n)
            for i in x:
                for j in x:
                    for k in x:
                        point = Point_3(i, j, k)
                        self.points.append(point)

        elif self.task == 'cube_rand':
            n = 1
            for _ in range(num_point):
                random_point = Vector_3(np.random.uniform(-n, n),
                                        np.random.uniform(-n, n),
                                        np.random.uniform(-n, n))
                self.points.append(random_point)

        elif self.task == 'rand_sphere':
            rad = 1
            for _ in range(num_point):
                random_point = Vector_3(np.random.uniform(-rad, rad),
                                        np.random.uniform(-rad, rad),
                                        np.random.uniform(-rad, rad))
                random_point.normalize()
                scaled_vector = random_point * np.random.uniform(-rad, rad)
                point = scaled_vector
                self.points.append(point)

        elif self.task == 'rand_shell_sphere':
            rad = 1
            for _ in range(num_point):
                theta = rn.uniform(0, 2 * np.pi)
                phi = rn.uniform(0, np.pi)

                epsilon = np.pi/100
                x = rad * np.sin(phi) * np.cos(theta) + rn.uniform(-epsilon, epsilon)
                y = rad * np.sin(phi) * np.sin(theta) + rn.uniform(-epsilon, epsilon)
                z = rad * np.cos(phi) + rn.uniform(-epsilon, epsilon)
                point = Point_3(x, y, z)
                self.points.append(point)


    def draw(self):
        glPointSize(5.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glColor3f(.0, .0, 1.0)
        for point in self.points:
            glBegin(GL_POINTS)
            glVertex3d(point.x(), point.y(), point.z())
            glEnd()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_1:
            self.task = 'cube'
        elif event.key() == Qt.Key_2:
            self.task = 'cube_rand'
        elif event.key() == Qt.Key_3:
            self.task = 'rand_sphere'
        elif event.key() == Qt.Key_4:
            self.task = 'rand_shell_sphere'
        elif event.key() == Qt.Key_0:
            self.task = None
            self.points = []
        
        self.randPoint()
        self.update()


if __name__ == '__main__':
    app = QApplication([])
    viewer = Viewer()
    viewer.show()
    app.exec_()