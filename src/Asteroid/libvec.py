#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
# Autores: Ricardo Lenz & Daniel Siqueira
# Versão em Python baseada em: euclid.py
#
# Data: 3-dez-2010 - essa é a versão mais corrigida até essa data.
#
# Obs.: - Parte de Quaternions levemente alterada [Set-Out/2010].
#       - Rotina Matrix.look_at modificada+corrigida [Out/2010]
#       - Adicionados mul_with, translation etc. em Matrix.
#       - Adicionado point_distance.
#       - Modificado __eq__ de Point e Vector; agora pode comparar com None.
#       - Vector agora descende de object pra poder fazer: hashtable[vec] = xx.
#         Isso modifica a questão do __slots__, que passa a ser rigoroso e não
#         aceita mais v.seila = x. Por causa disso, o slots foi comentado no vec.
#       - Corrigido metodo matrix.rotation(): adicionado 'self'.
#       - Adicionado rotação com pivô e relacionados [Nov/2010].
#       - Otimização na transposta da matriz.
#       - Ao calcular o ângulo com base no arc cos (dotproduct), levar em conta
#         que o dotproduct pode ter dado 1.004 no lugar do 1.0 (máximo), então
#         devemos arredondar pra 1.0 nesses casos.
#       - Agora é possível fazer Matrix[i][j], e tb foi adicionado Matrix.set_values.



import math


DEG_TO_RAD = 3.14159265 / 180.0
RAD_TO_DEG = 180.0 / 3.14159265 


def f_is_zero(f, e = 0.0001):
    return abs(f) <= e



def point_distance(p1, p2):
    dx = float(p2.x - p1.x)
    dy = float(p2.y - p1.y)    
    return math.sqrt( dx*dx + dy*dy )
    



class Point:
    __slots__ = ['x', 'y']

    def __init__(self, x=0, y=0):
        self.x = int( x )
        self.y = int( y )

    def __copy__(self):
        return Point( self.x, self.y )

    copy = __copy__


    def __repr__(self):
        return '(%d, %d)' % (self.x, self.y)

    def __eq__(self, a):
        if isinstance(a, Point):
            return self.x == a.x and self.y == a.y
        else:
            return False


    def __add__(self, a):
        return Point( self.x + a.x, self.y + a.y )
                    
    def __sub__(self, a):
        return Point( self.x - a.x, self.y - a.y )
   
    def __mul__(self, i):
        return Point( self.x * i, self.y * i )
    

    __pos__ = __copy__

    def __neg__(self):
        return Point( -self.x, -self.y )



class Vector(object):
    #__slots__ = ['x', 'y', 'z', 'w']

    def __init__(self, x=0.0, y=0.0, z=0.0, w=1.0):
        self.set_values( x, y, z, w )  
    
    def set_values(self, x=0.0, y=0.0, z=0.0, w=1.0):
        self.x = float( x )
        self.y = float( y )
        self.z = float( z )
        self.w = float( w )
    
    
    def to_array(self):
        return [self.x, self.y, self.z, self.w]
    
    
    def copy_from(self, v):
        self.x = v.x
        self.y = v.y
        self.z = v.z
        self.w = v.w
    

    def __copy__(self):
        return Vector( self.x, self.y, self.z, self.w )

    copy = __copy__
    
    dup = __copy__


    def __repr__(self):
        return '(%.2f, %.2f, %.2f, %.2f)' % (self.x, self.y, self.z, self.w)


    def __eq__(self, other):
        if isinstance(other, Vector):
            return self.x == other.x and \
                   self.y == other.y and \
                   self.z == other.z and \
                   self.w == other.w
        else:
            return False


    def __add__(self, other):
        return Vector( self.x + other.x,
                       self.y + other.y,
                       self.z + other.z,
                       self.w + other.w )

    def __sub__(self, other):
        return Vector( self.x - other.x,
                       self.y - other.y,
                       self.z - other.z,
                       self.w - other.w )
   
    def __mul__(self, other):
        if isinstance(other, Vector):
            return Vector( self.x * other.x,
                           self.y * other.y,
                           self.z * other.z,
                           self.w * other.w )
        else:
            return Vector(  self.x * other, \
                            self.y * other, \
                            self.z * other, \
                            self.w * other )


    __pos__ = __copy__

    def __neg__(self):
        return Vector( -self.x, -self.y, -self.z, -self.w )


   
    def length3(self):
        return math.sqrt( self.x * self.x + \
                          self.y * self.y + \
                          self.z * self.z )


    def length4(self):
        return math.sqrt( self.x * self.x + \
                          self.y * self.y + \
                          self.z * self.z + \
                          self.w * self.w )


    def normalize3(self):
        m = self.length3()
        if not f_is_zero(m):
            self.x /= m
            self.y /= m
            self.z /= m


    def normalize4(self):
        m = self.length4()
        if not f_is_zero(m):
            self.x /= m
            self.y /= m
            self.z /= m
            self.w /= m


    def dp3(self, other):
        return self.x * other.x + \
               self.y * other.y + \
               self.z * other.z


    def dp4(self, other):
        return self.x * other.x + \
               self.y * other.y + \
               self.z * other.z + \
               self.w * other.w


    def angle(self, other):
        v1 = self.copy()
        v1.normalize3()
        
        v2 = other.copy()
        v2.normalize3()
        
        # acos() só é definida para -1..+1. fora disso dá "math domain error".
        # porém, às vezes uma conta com float que daria 1.0 dá 1.0004 por ex.
        # então arredondamos para 1.0 para não quebrar a execução por isso.
        #
        dot = v1.dp3(v2)
        if abs(dot - 1.0) < 0.001: dot = 1.0
        
        a = RAD_TO_DEG * math.acos( dot )
        return a 


    def on_left_of(self, other):
        return self.cross( other ).y <= 0.0
    

    def cross(self, other):
        return Vector( self.y * other.z - self.z * other.y,
                       self.z * other.x - self.x * other.z,
                       self.x * other.y - self.y * other.x,
                       self.w )
    
    
    def almost_equals(self, other, e = 0.00001):
        return  abs(self.x - other.x) <= e and \
                abs(self.y - other.y) <= e and \
                abs(self.z - other.z) <= e





class Matrix:

    def __init__(self):
        self.zero()
    
    def zero(self):
        self.m = []
        for i in range(4):
            self.m.append( [0.0, 0.0, 0.0, 0.0] )

    def identity(self):
        self.zero()
        for i in range(4):
            self.m[i][i] = 1.0

    
    def __getitem__(self, i):
        return self.m[i]
    
    
    def set_values(self, *linhas):
        for i in range(4):
            for j in range(4):
                self.m[i][j] = float( linhas[i][j] )


    def __copy__(self):
        M = Matrix()
        for i in range(4):
            for j in range(4):
                M.m[i][j] = self.m[i][j]
        return M

    copy = __copy__
    
    dup = __copy__


    def __repr__(self):
        return ('(%5.2f %5.2f %5.2f %5.2f\n'  \
                ' %5.2f %5.2f %5.2f %5.2f\n'  \
                ' %5.2f %5.2f %5.2f %5.2f\n'  \
                ' %5.2f %5.2f %5.2f %5.2f )') \
                % ( self.m[0][0], self.m[0][1], self.m[0][2], self.m[0][3],
                    self.m[1][0], self.m[1][1], self.m[1][2], self.m[1][3],
                    self.m[2][0], self.m[2][1], self.m[2][2], self.m[2][3],
                    self.m[3][0], self.m[3][1], self.m[3][2], self.m[3][3] )

    
    def copy_from_float_array(self, f):
        k = 0
        for i in range(4):
            for j in range(4):
                self.m[i][j] = f[k]
                k += 1


    def copy_from_float_matrix(self, fm):
        for i in range(4):
            for j in range(4):
                self.m[i][j] = fm[i, j]


    def mul_with(self, other):
        r = self * other
        self.m = r.m


    def __mul__(self, other):
        if isinstance(other, Matrix):
            R = Matrix()
            R.zero()
            
            for i in range(4):
                for j in range(4):
                    for k in range(4):
                        R.m[i][j] += self.m[i][k] * other.m[k][j]
            
            return R
        
        elif isinstance(other, Vector):
            r = Vector( \
                self.m[0][0] * other.x + \
                self.m[0][1] * other.y + \
                self.m[0][2] * other.z + \
                self.m[0][3] * other.w,
                
                self.m[1][0] * other.x + \
                self.m[1][1] * other.y + \
                self.m[1][2] * other.z + \
                self.m[1][3] * other.w,

                self.m[2][0] * other.x + \
                self.m[2][1] * other.y + \
                self.m[2][2] * other.z + \
                self.m[2][3] * other.w,

                self.m[3][0] * other.x + \
                self.m[3][1] * other.y + \
                self.m[3][2] * other.z + \
                self.m[3][3] * other.w )
                 
            return r
            
        else:
            R = Matrix()
            
            for i in range(4):
                for j in range(4):
                    R.m[i][j] = self.m[i][j] * other
            
            return R

             
             
    def transpose(self):
        #
        # x = fica
        # o = troca [i,j] -> [j,i]
        #
        # x o o o
        # o x o o
        # o o x o
        # o o o x
        #
        # forma otimizada de fazer transposta 
        #
        self.m[0][1], self.m[0][2], self.m[0][3], \
        self.m[1][0], self.m[1][2], self.m[1][3], \
        self.m[2][0], self.m[2][1], self.m[2][3], \
        self.m[3][0], self.m[3][1], self.m[3][2] = \
            self.m[1][0], self.m[2][0], self.m[3][0], \
            self.m[0][1], self.m[2][1], self.m[3][1], \
            self.m[0][2], self.m[1][2], self.m[3][2], \
            self.m[0][3], self.m[1][3], self.m[2][3]
        
#        bak = self.copy()        
#        for i in range(4):
#            for j in range(4):
#                self.m[i][j] = bak.m[j][i]


    # gera matriz de rotação
    #
    def rotation(self, a, x, y, z):
        self.identity()
                
        a = a * DEG_TO_RAD
        c = math.cos( a )
        s = math.sin( a )
        
        v = Vector(x,y,z)
        v.normalize3()
        x, y, z = v.x, v.y, v.z
    
        # primeira linha
        self.m[0][0] = x*x*(1 - c) + c
        self.m[0][1] = x*y*(1 - c) - z*s
        self.m[0][2] = x*z*(1 - c) + y*s
 
        # segunda linha
        self.m[1][0] = y*x*(1 - c) + z*s
        self.m[1][1] = y*y*(1 - c) + c
        self.m[1][2] = y*z*(1 - c) - x*s

        # terceira linha
        self.m[2][0] = z*x*(1 - c) - y*s
        self.m[2][1] = z*y*(1 - c) + x*s
        self.m[2][2] = z*z*(1 - c) + c


    # gera matriz de translação
    #
    def translation(self, x, y, z):
        self.identity()
        self.m[0][3] = x
        self.m[1][3] = y
        self.m[2][3] = z


    # gera matriz de rotação em torno de um ponto.
    # equivale ao resultado de Trans[piv] x Rot x Trans[-piv].
    #
    def rotation_around_pivot(self, a, x, y, z, pivot):        
        self.translation( pivot.x, pivot.y, pivot.z )
        
        m = Matrix()
        m.rotation( a, x, y, z )
        self.mul_with( m )
        
        m.translation( -pivot.x, -pivot.y, -pivot.z )
        self.mul_with( m )



    #################################
    
    
    # transforma a matriz atual por uma rotação
    #
    def rotate(self, a, x, y, z):
        m = Matrix()
        m.rotation( a, x, y, z )
        self.mul_with( m )
    
    
    # transforma a matriz atual por uma translação
    #
    def translate(self, x, y, z):
        mt = Matrix()
        mt.translation(x, y, z)
        self.mul_with( mt )


    # transforma a matriz atual por uma rotação com pivot
    #
    def rotate_around_pivot(self, a, x, y, z, pivot):
        m = Matrix()
        m.rotation_around_pivot( a, x, y, z, pivot )
        self.mul_with( m )
    
    
    #################################
    
        
    def swap_lines(self, i, j):
        for k in range(4):
            self.m[i][k], self.m[j][k] = self.m[j][k], self.m[i][k]
        
    def line_mul(self, i, f):
        for k in range(4):
            self.m[i][k] *= f
        
    def line_add(self, dest, src, src_factor = 1.0):
        for k in range(4):
            self.m[dest][k] += src_factor * self.m[src][k]


    def inverse(self):
        m = self.dup()        
        resp = Matrix()
        resp.identity()
        
        for k in range(4):
            pivo = k
            
            if f_is_zero( m.m[pivo][pivo] ):
                
                linha = k
                while linha <= 3:
                    if not f_is_zero( m.m[linha][k] ):
                        pivo = linha
                        break
                    linha += 1
                
                m.swap_lines( pivo, k )                
                resp.swap_lines( pivo, k )
                
                if f_is_zero( m.m[pivo][pivo] ):
                    # matriz singular
                    return None                
            
            valor_pra_tornar1 = 1.0 / m.m[pivo][pivo]
            m.line_mul( pivo, valor_pra_tornar1 )
            resp.line_mul( pivo, valor_pra_tornar1 )
            
            for i in range(4):
                if i == pivo: continue
                
                valor_na_coluna_do_pivo = m.m[i][pivo]
                valor_pra_zerar = -valor_na_coluna_do_pivo / m.m[pivo][pivo]
                
                m.line_add( i, pivo, valor_pra_zerar )
                resp.line_add( i, pivo, valor_pra_zerar )
        
        return resp
    
    
            
        
    def look_at(self, eye, center, up):
        #
        # eye = camera pos
        # center = obj/target pos
        #
        #
        # podemos fazer look_at de 2 modos diferentes (mas que dão iguais):
        #  versão 1: look = eye - center;  my_right = up x look;  my_up = look x my_right
        #  versão 2: look = center - eye;  my_right = look x up;  my_up = my_right x look
        #
        #  versão 1: na 3a linha da matriz, fica o vetor look
        #  versão 2: na 3a linha da matriz, fica o vetor -look
        #
        #  obs.: optamos pela versão 1 por evitar o NEG (-) na 3a linha da matriz.
        #  obs.: na documentação de gluLookAt(), usa-se a versão 2 e os seguintes nomes:
        #        f = forward   =>  look
        #        s = side      =>  my_right
        #        u = up
        #
        # é importante normalizar os resultados vetoriais: look, up, my_right, my_up.
        # 
        #
        
        look = eye - center
        look.normalize3()
        
        up.normalize3()
        my_right = up.cross( look )
        my_right.normalize3()
        
        my_up = look.cross( my_right )
        
        self.identity()
        
        self.m[0][0] = my_right.x
        self.m[0][1] = my_right.y
        self.m[0][2] = my_right.z
        
        self.m[1][0] = my_up.x
        self.m[1][1] = my_up.y
        self.m[1][2] = my_up.z

        self.m[2][0] = look.x
        self.m[2][1] = look.y
        self.m[2][2] = look.z
        
        self.translate( -eye.x, -eye.y, -eye.z )
        # obs.: esse último translate() aqui NÃO é a mesma
        # coisa que simplesmente fazer: 
        #   self.m[0][3] = -eye.x
        #   self.m[1][3] = -eye.y
        #   self.m[2][3] = -eye.z
        # pois a matriz de translação gerada é pos-multiplicada
        # com a matriz atual e a 4a coluna NÃO é -eye, mas
        # cada linha dotProduct4 -eye.
    
    
    
    def from_dir_up_right(self, vec_dir, vec_up, vec_right):
        r = vec_right
        r.normalize3()
        
        u = vec_up
        u.normalize3()
        
        d = vec_dir
        d.normalize3()
        
        self.identity()
        
        self.m[0][0] = r.x
        self.m[1][0] = r.y
        self.m[2][0] = r.z
        
        self.m[0][1] = u.x
        self.m[1][1] = u.y
        self.m[2][1] = u.z
        
        self.m[0][2] = d.x
        self.m[1][2] = d.y
        self.m[2][2] = d.z
        
        

        


class Quaternion:
    __slots__ = ['s', 'x', 'y', 'z']

    def __init__(self, s=0.0, x=0.0, y=0.0, z=0.0):
        self.s = float( s )
        self.x = float( x )
        self.y = float( y )
        self.z = float( z )


    def __copy__(self):
        Q = Quaternion()
        Q.s = self.s
        Q.x = self.x
        Q.y = self.y
        Q.z = self.z
        return Q

    copy = __copy__
    
    dup = __copy__


    def __repr__(self):
        return 'Q(s = %.2f, x = %.2f, y = %.2f, z = %.2f)' % \
            (self.s, self.x, self.y, self.z)


    def conjugate(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z


    def __add__(self, other):
        if isinstance(other, Quaternion):
            
            Q = Quaternion()
            Q.s = self.s + other.s
            Q.x = self.x + other.x
            Q.y = self.y + other.y
            Q.z = self.z + other.z
            return Q
    
        else:
            raise Exception("*** Erro: Quaternion __add__: tipo <%s> inválido" % \
                str(type(other)) )


    def __sub__(self, other):
        if isinstance(other, Quaternion):
            
            Q = Quaternion()
            Q.s = self.s - other.s
            Q.x = self.x - other.x
            Q.y = self.y - other.y
            Q.z = self.z - other.z
            return Q
    
        else:
            raise Exception("*** Erro: Quaternion __sub__: tipo <%s> inválido" % \
                str(type(other)) )
            


    def __mul__(self, other):
        if isinstance(other, Quaternion):
            As = self.s
            Ax = self.x
            Ay = self.y
            Az = self.z
            
            Bs = other.s
            Bx = other.x
            By = other.y
            Bz = other.z
            
            Q = Quaternion()
            Q.s = -Ax * Bx - Ay * By - Az * Bz + As * Bs
            Q.x =  Ax * Bs + Ay * Bz - Az * By + As * Bx    
            Q.y = -Ax * Bz + Ay * Bs + Az * Bx + As * By
            Q.z =  Ax * By - Ay * Bx + Az * Bs + As * Bz
            return Q
        
        elif isinstance(other, Vector):
            # rotaciona v: q x v x q'
            vn = other.dup()
            vn.normalize3()

            a = self.dup()
            b = Quaternion( 0.0, vn.x, vn.y, vn.z )
            c = self.dup()
            c.conjugate()
            
            r = a * b * c
            return Vector( r.x, r.y, r.z )
    
        elif isinstance(other, int) or isinstance(other, float):
        
            Q = Quaternion()
            Q.s = self.s * other
            Q.x = self.x * other
            Q.y = self.y * other
            Q.z = self.z * other 
            return Q
    
        else:
            raise Exception("*** Erro: Quaternion __mul__: tipo <%s> inválido" % \
                str(type(other)) )



    def __div__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            
            Q = Quaternion()
            Q.s = self.s / other
            Q.x = self.x / other
            Q.y = self.y / other
            Q.z = self.z / other 
            return Q
    
        else:
            raise Exception("*** Erro: Quaternion __div__: tipo <%s> inválido" % \
                str(type(other)) )



    def length(self):
        return math.sqrt( self.s * self.s + \
                          self.x * self.x + \
                          self.y * self.y + \
                          self.z * self.z )

    def identity(self):
        self.s = 1.0
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0


    def normalize(self):
        m = self.length()
        if not f_is_zero(m):
            self.s /= m
            self.x /= m
            self.y /= m
            self.z /= m


    def dp4(self, q):
        return self.s * q.s + self.x * q.x + self.y * q.y + self.z * q.z


    def angle(self, q):
        q1 = self
        q1.normalize()
        q2 = q
        q2.normalize()
        return RAD_TO_DEG * math.acos( q1.dp4( q2 ) )



    def to_matrix(self):
        
        xx = self.x * self.x
        xy = self.x * self.y
        xz = self.x * self.z
        xs = self.x * self.s
        
        yy = self.y * self.y
        yz = self.y * self.z
        ys = self.y * self.s
        
        zz = self.z * self.z
        zs = self.z * self.s
        
        M = Matrix()
        M.m[0][0] = 1.0 - 2.0 * (yy + zz)
        M.m[0][1] =       2.0 * (xy - zs)
        M.m[0][2] =       2.0 * (xz + ys)
        M.m[0][3] = 0.0
        
        M.m[1][0] =       2.0 * (xy + zs)
        M.m[1][1] = 1.0 - 2.0 * (xx + zz)
        M.m[1][2] =       2.0 * (yz - xs)
        M.m[1][3] = 0.0
        
        M.m[2][0] =       2.0 * (xz - ys)
        M.m[2][1] =       2.0 * (yz + xs)
        M.m[2][2] = 1.0 - 2.0 * (xx + yy)
        M.m[2][3] = 0.0
        
        M.m[3][0] = M.m[3][1] = M.m[3][2] = 0.0
        M.m[3][3] = 1.0
        return M


    def from_angle_axis(self, angle, axis):
        
        # converte de graus para radianos
        angle = angle * DEG_TO_RAD

        axis.normalize3()
        
        seno = math.sin( angle * 0.5 )
        self.s = math.cos( angle * 0.5 )
        self.x = axis.x * seno
        self.y = axis.y * seno
        self.z = axis.z * seno
    
    
    
    def lerp(self, q1, q2, t):
        self.s = q1.s*(1-t) + q2.s*(t)
        self.x = q1.x*(1-t) + q2.x*(t)
        self.y = q1.y*(1-t) + q2.y*(t)
        self.z = q1.z*(1-t) + q2.z*(t)        


    def slerp(self, q1, q2, t):
        theta = q1.angle( q2 ) * DEG_TO_RAD
        
        # pra evitar divisão de zero: se são muito parecidos, retorna q1 logo.
        if theta < 0.001:
            return q1
        
        a = math.sin( (1-t)*theta ) / math.sin(theta)
        b = math.sin( (t)*theta ) / math.sin(theta)
        
        self.s = q1.s*(a) + q2.s*(b)
        self.x = q1.x*(a) + q2.x*(b)
        self.y = q1.y*(a) + q2.y*(b)
        self.z = q1.z*(a) + q2.z*(b)




def QuaternionFromAngleAxis(angle, x, y, z):
    q = Quaternion()
    q.from_angle_axis( angle, Vector(x,y,z) )
    return q
    

if __name__ == '__main__':
    print "Testando libvec..."

    print "Quaternion ------------------"

    q = QuaternionFromAngleAxis( 45, 0, 1, 0 )
    v = Vector(0,0,1,0)
    vq = q * v
    print vq
    
    m = q.to_matrix()    
    vq = m * v
    print vq
    
    m.transpose()
    vq = m * v
    print vq
    

    print
    print "Vector ----------------------"
    

    v = Vector(1,0,1,1)
    print "v:", v, " length3=", v.length3()
    v.normalize3()
    print "normalize3:", v, " length3=", v.length3()
    
    v = Vector(1,0,1,1)
    print "v:", v, " length4=", v.length4()
    v.normalize4()
    print "normalize4:", v, " length4=", v.length4()
    
    
    print
    print "Matrix ----------------------"
    
    
    m = Matrix()
    m.identity()
    print m
    
    i = m.inverse()
    print "inverse..."
    print i
    print
    
    print "set_values..."
    m.set_values( [1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,16] )
    m[0][0] = 1.1
    m[0][1] = 1.2
    m[3][2] = 1.3
    print m
    print

    print
    print "translate( 1, 2, 3 )..."
    m.translate(1,2,3)
    print m
    print

    print "rotate( 90, 0, 0, 1 )..."
    m.rotate( 90, 0,0,1 )
    print m
    print

    m.identity()
    print "rotate_around_pivot( 90, 0, 0, 1, pivo[1,1,0] )..."
    m.rotate_around_pivot( 90, 0,0,1, Vector(1,1,0) )
    print m
    print
    v = m * Vector(1,1,0)
    print "vetor [1,1,0] rotacionado por essa matriz: %s" % str(v)
    print    
    
    print "look_at( 0.5,2,2,  0.3,0,-1,  0,1,0 )..."
    m.look_at( eye=Vector(0.5,2,2), center=Vector(0.3,0,-1), up=Vector(0,1,0) )
    print m    
    # resultado:
    # ( 1.00  0.00 -0.07 -0.37
    #  -0.04  0.83 -0.55 -0.54
    #   0.06  0.55  0.83 -2.80
    #   0.00  0.00  0.00  1.00 )


    a = {}
    v = Vector(1,2,3)
    a[v] = 4
    print a[v]

    a = Vector(1,2,3)
    b = a
    print "hash(vec b), hash(vec a) = ", hash(b), hash(a)

    print
    print "Testando arredondamento em Vector.angle()..."
    
    v1 = Vector( 0.22, 0.98, 0.00, 0.00 )
    v2 = v1.copy()
    print v1
    v1.normalize3()
    print v1
    print v1.angle(v2) # isso só funciona por causa do arredondamento que fazemos em angle().
    print "OK"
    
    v1 = Vector( -0.00, -1.00, 0.00, 0.00 )
    v2 = Vector( -0.73, -0.69, 0.00, 0.00 )
    print v1.angle(v2)

