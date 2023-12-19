from PyQGLViewer import QGLViewer, Vec
from CGAL import CGAL_Convex_hull_2
from CGAL.CGAL_Kernel import Point_2, Point_3
from CGAL.CGAL_Polyhedron_3 import Polyhedron_3
from CGAL import CGAL_Convex_hull_3
import random as rn
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from OpenGL.GL import *


class MyViewer(QGLViewer):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.points = []
        self.result = []
        self.task = None
        self.resize(1280, 720)


    def shell_2D(self):
        self.points = []
        self.result = []
        for i in range(20):
            x = np.sin(rn.uniform(0, 2*np.pi))
            y = np.cos(rn.uniform(0, 2*np.pi))
            self.points.append(Point_2(x, y))
        CGAL_Convex_hull_2.convex_hull_2(self.points, self.result)
        
        vertices = self.result
        self.vertices_in_shell = [i for i, p in enumerate(self.points) if p in vertices]


    def shell_3D(self):
        self.points = [Point_3(rn.uniform(-1, 1), rn.uniform(-1, 1), rn.uniform(-1, 1)) for i in range(300)]
        self.polyhedron = Polyhedron_3()
        CGAL_Convex_hull_3.convex_hull_3(self.points, self.polyhedron)


    def shell_3D_ex(self):
        self.points = []
        self.points.append(Point_3(0, 0, 0))
        self.points.append(Point_3(0, 1, 0))
        self.points.append(Point_3(1, 1, 0))
        self.points.append(Point_3(1, 0, 0))
        self.points.append(Point_3(0, 0, 1))
        self.points.append(Point_3(0, 1, 1))
        self.points.append(Point_3(1, 1, 1))
        self.points.append(Point_3(1, 0, 1))

        self.polyhedron = Polyhedron_3()
        CGAL_Convex_hull_3.convex_hull_3(self.points, self.polyhedron)


    def facet_vertices(self, facet_handle):
        vertices = []
        halfedge = facet_handle.halfedge()
        while True:
            vertex = halfedge.vertex().point()
            vertices.append(Vec(vertex.x(), vertex.y(), vertex.z()))
            halfedge = halfedge.next()
            if halfedge == facet_handle.halfedge():
                break
        return vertices


    def draw_2D(self):
        glPointSize(5.0)
        glBegin(GL_POINTS)
        for i, point in enumerate(self.points):
            if i not in self.vertices_in_shell:
                glColor3f(.0, 1.0, .0)
                glVertex2f(point.x(), point.y())
            else:
                glColor3f(1.0, 1.0, 1.0)
                glVertex2f(point.x(), point.y())
        glEnd()

        glBegin(GL_LINE_LOOP)
        glColor3f(1.0, .0, .0)
        for vertex in self.result:
            glVertex2f(vertex.x(), vertex.y())
        glEnd()


    def draw_3D(self):
        glPointSize(7.0)
        glBegin(GL_POINTS)
        for point in self.points:
            glColor3f(.0, 1.0, .0)
            glVertex3f(point.x(), point.y(), point.z())
        glEnd()

        faces = list(self.polyhedron.facets())
        glBegin(GL_TRIANGLES)
        for face in faces:
            vertices = self.facet_vertices(face)
            glColor3f(1.0, .0, .0)
            for vertex in vertices:
               glVertex3f(*vertex)
        glEnd()


    def draw(self):
        if self.task == 'shell_2D':
            self.draw_2D()
        elif self.task == 'shell_3D':
            self.draw_3D()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_1:
            self.task = 'shell_2D'
            self.shell_2D()
        elif event.key() == Qt.Key_2:
            self.task = 'shell_3D'
            self.shell_3D()
        elif event.key() == Qt.Key_3:
            self.task = 'shell_3D'
            self.shell_3D_ex()

        elif (event.key()==Qt.Key_W):
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        elif (event.key()==Qt.Key_F):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
        self.update()


if __name__ == '__main__':
    app = QApplication([])
    viewer = MyViewer()
    viewer.show()
    app.exec_()
