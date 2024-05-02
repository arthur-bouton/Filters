""" 
Recursive filters

Author: Arthur Bouton [arthur.bouton@gadz.org]
"""
import collections.abc
import math


class LP_first_order() :
	"""
	First order low-pass filter

	Parameters
	----------
	Te : float
		Sampling period in seconds.
	wc : float
		Cut-off frequency in rad/s.
	transform : string, optional, default: 'bilinear'
		Type of discrete time approximation to use.

	"""

	def __init__( self, Te, wc, transform='bilinear' ) :
		self.reset()

		getattr( self, 'init_' + transform )( Te, wc )

	def reset( self ) :
		self._y_k1 = 0
		self._x_k1 = 0

	def init_bilinear( self, Te, wc ) :

		self._Cy1 = ( 2 - wc*Te )/( 2 + wc*Te )
		self._Cx0 = wc*Te/( 2 + wc*Te )
		self._Cx1 = self._Cx0

		return self

	def init_homographic( self, Te, wc ) :

		twt = math.tan( wc*Te/2 )
		self._Cy1 = ( 1 - twt )/( 1 + twt )
		self._Cx0 = twt/( 1 + twt )
		self._Cx1 = self._Cx0

		return self

	def init_step_matching( self, Te, wc ) :

		ewt = math.exp( -wc*Te )
		self._Cy1 = ewt
		self._Cx0 = 0
		self._Cx1 = 1 - ewt

		return self

	def init_impulse_matching( self, Te, wc ) :

		ewt = math.exp( -wc*Te )
		self._Cy1 = ewt
		self._Cx0 = 1 - ewt
		self._Cx1 = 0

		return self

	def _feed( self, x_k0 ) :

		y_k0 = self._Cy1*self._y_k1 + self._Cx0*x_k0 + self._Cx1*self._x_k1
		self._y_k1 = y_k0
		self._x_k1 = x_k0

		return y_k0

	def __call__( self, input ) :

		if isinstance( input, collections.abc.Iterable ) :
			return [ self._feed( x ) for x in input ]
		else :
			return self._feed( input )


class LP_second_order() :
	"""
	Second order low-pass filter

	Parameters
	----------
	Te : float
		Sampling period in seconds.
	w0 : float
		Resonant frequency in rad/s.
	Q : float
		Quality factor.
	transform : string, optional, default: 'bilinear'
		Type of discrete time approximation to use.

	"""

	def __init__( self, Te, w0, Q, transform='bilinear' ) :
		self.reset()

		getattr( self, 'init_' + transform )( Te, w0, Q )

	def reset( self ) :
		self._y_k1 = 0
		self._x_k1 = 0
		self._y_k2 = 0
		self._x_k2 = 0

	def init_bilinear( self, Te, w0, Q ) :

		w2T2 = ( w0*Te )**2
		den = 2*w0*Te + 4*Q + Q*w2T2
		self._Cy1 = 2*Q*( 4 - w2T2 )/den
		self._Cy2 = ( 2*w0*Te - 4*Q - Q*w2T2 )/den
		self._Cx0 = Q*w2T2/den
		self._Cx1 = 2*self._Cx0
		self._Cx2 = self._Cx0

		return self

	def reset( self ) :
		self._y_k1 = 0
		self._x_k1 = 0
		self._y_k2 = 0
		self._x_k2 = 0

	def _feed( self, x_k0 ) :

		y_k0 = self._Cy1*self._y_k1 + self._Cy2*self._y_k2 + self._Cx0*x_k0 + self._Cx1*self._x_k1 + self._Cx2*self._x_k2
		self._y_k2 = self._y_k1
		self._y_k1 = y_k0
		self._x_k2 = self._x_k1
		self._x_k1 = x_k0

		return y_k0

	def __call__( self, input ) :

		if isinstance( input, collections.abc.Iterable ) :
			return [ self._feed( x ) for x in input ]
		else :
			return self._feed( input )


class Moving_average() :
	"""
	Moving average filter

	Parameter
	---------
	N : int
		Number of elements used to compute the average.

	"""

	def __init__( self, N ) :
		self._N = N

		self.reset()

	def reset( self ) :
		self._buffer = [ 0 ]*self._N
		self._i = 0
		self._y_k0 = 0

	def _feed( self, x_k0 ) :

		self._y_k0 -= self._buffer[self._i]
		self._buffer[self._i] = x_k0/self._N
		self._y_k0 += self._buffer[self._i]

		self._i += 1
		if self._i >= self._N :
			self._i = 0

		return self._y_k0

	def __call__( self, input ) :

		if isinstance( input, collections.abc.Iterable ) :
			return [ self._feed( x ) for x in input ]
		else :
			return self._feed( input )
