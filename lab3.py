from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQGLViewer import QGLViewer
from OpenGL.GL import *


def clamp(value, minval, maxval):
    return max(minval, min(value, maxval))


class BSpline3:
    def __init__(self, reference_points, discrete_num = 10, closed = False):
        self.points = reference_points
        self.d_num = int(discrete_num)
        self.closed = closed
        
        self.coefs = [];
        for i in range(self.d_num):
            spline_segm_coef = self.calc_spline3_coef(i/self.d_num)
            self.coefs.append(spline_segm_coef)


    def calc_spline3_coef(self, t):
        coefs = [0,0,0,0]
        coefs[0] = (1.0-t)*(1.0-t)*(1.0-t)/6.0;
        coefs[1] = (3.0*t*t*t - 6.0*t*t + 4)/6.0;
        coefs[2] = (-3.0*t*t*t + 3*t*t + 3*t+1)/6.0;
        coefs[3] = t*t*t/6.0;
        return coefs


    def draw_spline_curve(self):
        if not self.closed:
            segmentsCount = len(self.points) - 1
            glBegin(GL_LINE_STRIP)
        else:
            segmentsCount = len(self.points)
            glBegin(GL_LINE_LOOP)  
        glColor3f(1.0, 1.0, .0)
        for i in range(segmentsCount):
            self.draw_glvertex_for_one_segment_of_spline(i);
        glEnd()


    def draw_glvertex_for_one_segment_of_spline(self, segment_id):
        pNum = len(self.points)
        if not self.closed:
            p0 = clamp(segment_id - 1, 0, pNum - 1)
            p1 = clamp(segment_id, 0, pNum - 1)
            p2 = clamp(segment_id + 1, 0, pNum - 1)
            p3 = clamp(segment_id + 2, 0, pNum - 1)
        else:
            p0 = (segment_id - 1 + pNum) % pNum
            p1 = (segment_id + pNum) % pNum
            p2 = (segment_id + 1 + pNum) % pNum
            p3 = (segment_id + 2 + pNum) % pNum

        for i in range(self.d_num):
            x = self.coefs[i][0] * self.points[p0][0] \
                + self.coefs[i][1] * self.points[p1][0] \
                + self.coefs[i][2] * self.points[p2][0] \
                + self.coefs[i][3] * self.points[p3][0] 
            y = self.coefs[i][0] * self.points[p0][1] \
                + self.coefs[i][1] * self.points[p1][1] \
                + self.coefs[i][2] * self.points[p2][1] \
                + self.coefs[i][3] * self.points[p3][1]
            z = self.coefs[i][0] * self.points[p0][2] \
            + self.coefs[i][1] * self.points[p1][2] \
            + self.coefs[i][2] * self.points[p2][2] \
            + self.coefs[i][3] * self.points[p3][2] \
 
            glVertex3f(x, y, z)


class BSpline2:
    def __init__(self, reference_points, discrete_num = 10, closed = False):
        self.points = reference_points
        self.d_num = int(discrete_num)
        self.closed = closed
        
        self.coefs = []
        for i in range(self.d_num):
            spline_segm_coef = self.calc_spline2_coef(i/self.d_num)
            self.coefs.append(spline_segm_coef)


    def calc_spline2_coef(self, t):
        coefs = [0, 0, 0]
        coefs[0] = (1 - t) ** 2 / 2
        coefs[1] = (1 + 2 * t - 2 * t ** 2) / 2
        coefs[2] = t ** 2 / 2
        return coefs


    def draw_spline_curve(self):
        if not self.closed:
            segmentsCount = len(self.points) - 2
            glBegin(GL_LINE_STRIP)
        else:
            segmentsCount = len(self.points) - 1  
            glBegin(GL_LINE_LOOP)  
        glColor3f(.0, 1.0, 1.0)
        for i in range(segmentsCount):
            self.draw_glvertex_for_one_segment_of_spline(i)
        glEnd()


    def draw_glvertex_for_one_segment_of_spline(self, segment_id):
        pNum = len(self.points)
        if not self.closed:
            p0 = clamp(segment_id, 0, pNum - 1)
            p1 = clamp(segment_id + 1, 0, pNum - 1)
            p2 = clamp(segment_id + 2, 0, pNum - 1)
        else:
            p0 = (segment_id - 1 + pNum) % pNum
            p1 = (segment_id + pNum) % pNum
            p2 = (segment_id + 1 + pNum) % pNum

        for i in range(self.d_num):
            x = self.coefs[i][0] * self.points[p0][0] \
                + self.coefs[i][1] * self.points[p1][0] \
                + self.coefs[i][2] * self.points[p2][0]
            y = self.coefs[i][0] * self.points[p0][1] \
                + self.coefs[i][1] * self.points[p1][1] \
                + self.coefs[i][2] * self.points[p2][1]
            z = self.coefs[i][0] * self.points[p0][2] \
                + self.coefs[i][1] * self.points[p1][2] \
                + self.coefs[i][2] * self.points[p2][2]
 
            glVertex3f(x, y, z)


class Viewer(QGLViewer):
    def __init__(self,parent = None):
        QGLViewer.__init__(self,parent)
        self.point_A = (0,0,0)
        self.resize(1280, 720)

    def draw(self):
        self.points = (self.point_A, (0,3,0), (1,3,0), (1,1,0), (2,1,0), (3,2,0), (3,0,0))
        glPointSize(5.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glColor3f(.0, 1.0, 0.0)
        for point in self.points:
            glBegin(GL_POINTS)
            glVertex3d(point[0], point[1], point[2])
            glEnd()
        
        glBegin(GL_LINES)
        glColor3f(1.0, 0.0, 0.0)
        for i in range(len(self.points) - 1):
            glVertex3fv(self.points[i])
            glVertex3fv(self.points[i + 1])
        glEnd()

        BSpline2(self.points, 10, False).draw_spline_curve()
        BSpline3(self.points, 10, False).draw_spline_curve()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_1:
            self.point_A = (-1, 0, 0)
        elif event.key() == Qt.Key_2:
            self.point_A = (-3, 2, 0)
        elif event.key() == Qt.Key_3:
            self.point_A = (0, 4, 0)
        elif event.key() == Qt.Key_0:
            self.point_A = (0, 0, 0)
        self.update()


if __name__ == '__main__':
    qapp = QApplication([])
    viewer = Viewer()
    viewer.show()
    qapp.exec_()
