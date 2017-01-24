import numpy as np

class CartesianCoordinates(object):
    def __init__(self, nx, ny, origin=[0.,0.], scale=[1.,1.], mask=None):
        '''
        Encapsulate the method and attributes associated with a cartesian coordinate
        system.
        '''
        self.origin = origin
        self.xx, self.yy = self._compute_coords(nx, ny, origin, scale)
        self.shape = self.xx.shape

    def _compute_coords(self, nx, ny, origin, scale):
        '''Initializes coordinate system by translation THEN scaling (the order matters).'''
        xy = np.ogrid[0.:nx, 0.:ny]

        # Translate.
        x = xy[0] - origin[0]
        y = xy[1] - origin[1]
        
        # Scale.
        x *= scale[0]
        y *= scale[1]
        
        return np.meshgrid(x, y)

    def scale(self, factor = 1, x_factor = 1, y_factor = 1):
        '''Scales the coordinates by an amount factor.'''
        self.xx *= factor*x_factor
        self.yy *= factor*y_factor
    
    def translate(self, x_shift, y_shift):
        '''Translate the coordinate system by an amount (x_shift, y_shift).'''
        self.xx -= x_shift
        self.yy -= y_shift
        self.origin -= (x_shift, y_shift)

    def extrema(self):
        return (self.xx.min(), self.yy.min(), self.xx.max(), self.yy.max())

class SphericalCoordinates(object):
    def __init__(self, cart):
        xx = cart.xx
        yy = cart.yy
        r_squared = xx**2 + yy**2
        #inds = np.where((r_squared-0.5)**2 < .25) # Keep r_squared between 0 and 1.
        inds = np.where(r_squared > 0.0)

        self.costheta = np.sqrt(1. - r_squared)
        self.sintheta = np.sqrt(r_squared)
        # Make sure there are not nans
        self.costheta[r_squared > 1] = 0
        
        self.cosphi = np.ones(r_squared.shape)
        self.sinphi = np.zeros(r_squared.shape)

        self.cosphi[inds] = xx[inds]/self.sintheta[inds]
        self.sinphi[inds] = yy[inds]/self.sintheta[inds]

class VectorField(object):
    def __init__(self, coordinates, dim):
        self.coords = coordinates
        self.dim = dim
        self.shape = (dim, coordinates.shape[0], coordinates.shape[1])

    def evaluate_field(self, function):
        '''
        Evaluate field over coordinates.
        '''
        pass


class SphericalVectorField(VectorField):
    def __init__(self, coordinates, dim):
        VectorField.__init__(self, coordinates, dim)
    

def spherical_to_cartesian(es_cam, sph_coords):
    sintheta = sph_coords.sintheta
    costheta = sph_coords.costheta
    sinphi = sph_coords.sinphi
    cosphi = sph_coords.cosphi

    es_cam_cart = np.zeros(es_cam.shape, dtype = complex)
    es_cam_cart += es_cam
    
    es_cam_cart[0,:,:] =  es_cam[0,:,:] * sintheta * cosphi
    es_cam_cart[0,:,:] += es_cam[1,:,:] * costheta * cosphi
    es_cam_cart[0,:,:] -= es_cam[2,:,:] * sinphi
    
    es_cam_cart[1,:,:] =  es_cam[0,:,:] * sintheta * sinphi
    es_cam_cart[1,:,:] += es_cam[1,:,:] * costheta * sinphi
    es_cam_cart[1,:,:] += es_cam[2,:,:] * cosphi
    
    es_cam_cart[2,:,:] =  es_cam[0,:,:] * costheta - es_cam[1,:,:] * sintheta
    
    return es_cam_cart

if __name__ == '__main__':
    xy = np.ogrid[0:10,0:10]
    origin = [0.0, 0.0]
    cart = CartesianCoordinates(xy, origin, units = [1.0, 'um'])
    
    x = np.tile(np.arange(10, dtype = float), 10)
    y = np.repeat(np.arange(10, dtype = float), 10)
    
    print cart.xx
    print cart.x
    print x
    print cart.y
    print y
    print cart.units
    
    
