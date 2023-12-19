from PyQGLViewer import QGLViewer
from CGAL.CGAL_Kernel import Point_3
from CGAL.CGAL_Polyhedron_3 import Polyhedron_3
from CGAL import CGAL_Convex_hull_3
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from OpenGL.GL import *

from CGAL.CGAL_Mesh_3 import Polyhedral_mesh_domain_3
from CGAL.CGAL_Mesh_3 import Default_mesh_criteria
from CGAL.CGAL_Mesh_3 import make_mesh_3
from CGAL.CGAL_Mesh_3 import Mesh_3_parameters
from CGAL.CGAL_Mesh_3 import refine_mesh_3


class Viewer(QGLViewer):
    def __init__(self, parent=None):
        QGLViewer.__init__(self, parent)
        self.vertices = [Point_3(-0.5, -0.5, -0.5),
                         Point_3(0.5, -0.5, -0.5),
                         Point_3(0.5, 0.5, -0.5),
                         Point_3(-0.5, 0.5, -0.5),
                         Point_3(-0.5, -0.5, 0.5),
                         Point_3(0.5, -0.5, 0.5),
                         Point_3(0.5, 0.5, 0.5),
                         Point_3(-0.5, 0.5, 0.5)]
        self.resize(1280, 720)
        self.vertex = []
        self.mas = []
        self.polyhedron = Polyhedron_3()
        CGAL_Convex_hull_3.convex_hull_3(self.vertices, self.polyhedron)

        domain = Polyhedral_mesh_domain_3(self.polyhedron)
        params = Mesh_3_parameters()
        criteria = Default_mesh_criteria()
        criteria.facet_angle(25).facet_size(0.15).facet_distance(0.008).cell_radius_edge_ratio(3)
        
        self.c3t3 = make_mesh_3(domain, criteria, params)
        new_criteria = Default_mesh_criteria()
        new_criteria.cell_radius_edge_ratio(3).cell_size(0.1)

        refine_mesh_3(self.c3t3, domain, new_criteria, params)

        for cell in self.c3t3.cells():
            for i in range(4):
                vertex = cell.vertex(i)
                self.vertex.append(Point_3(vertex.point().x(), vertex.point().y(), vertex.point().z()))


    def draw(self):
        glPointSize(7.0)
        glBegin(GL_POINTS)
        for point in self.vertex:
            glColor3f(.0, 1.0, .0)
            glVertex3f(point.x(), point.y(), point.z())
        glEnd()


    def keyPressEvent(self, event):
        if (event.key()==Qt.Key_W):
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        elif (event.key()==Qt.Key_F):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        self.update()


if __name__ == '__main__':
    app = QApplication([])
    viewer = Viewer()
    viewer.show()
    app.exec_()