#!/usr/bin/env python

# Compare the root mean squared errors between these two quantization approaches:
# a) Simple truncation and b) Error diffusion

import random
from math import sqrt

# Generate a pixel vector that has at least this length
minimumNumberOfPixelsToGenerate = 500

# Simulate a smooth gradient by appending uniform chunks of identically-valued pixels
# to the pixel vector.  Each chunk has a random width comprised between 5 and 20 pixels.
# A smooth gradient is simulated by enforcing that the value of these uniform chunks must
# randomly differ by +1 or -1 from the preceding chunk.  As an exception, if the previous
# random chunk contained zero-valued pixels, then, as we don't allow negative pixel
# values, the next chunk must containe pixels with a value of one.

# We start with an empty vector
pixelVector = []

numberOfGeneratedPixels = 0

previousPixelValue = random.randint( 0, 15 )

while numberOfGeneratedPixels < minimumNumberOfPixelsToGenerate:

	widthOfThisChunk = random.randint( 4, 20 )

	# The new chunk must contain values that differ from the previous chunk by -1 or +1
	newPixelValue = previousPixelValue + random.choice( [ -1, 1 ] )

	if newPixelValue < 0:
		# The previous pixel value must then necessarily have been zero
		newPixelValue = 1

	for i in range( widthOfThisChunk ):
		pixelVector.append( newPixelValue )

	previousPixelValue = newPixelValue
	numberOfGeneratedPixels += widthOfThisChunk

errorDiffusedQuantizedVector = [ 0 for i in range( numberOfGeneratedPixels ) ]

truncatedQuantizedVector = map( lambda x: x / 4, pixelVector )

accumulatedError = 0
for i in range( numberOfGeneratedPixels ):

	quantizedPixel = pixelVector[ i ] / 4
	delta = pixelVector[ i ] - quantizedPixel * 4
	accumulatedError += delta

	if accumulatedError > 3:
		quantizedPixel += 1
		accumulatedError -= 4
	elif accumulatedError < -3:
		quantizedPixel -= 1
		accumulatedError += 4

	errorDiffusedQuantizedVector[ i ] = quantizedPixel

accumulatedSquareError = 0
for i in range( numberOfGeneratedPixels ):
	delta = pixelVector[ i ] - truncatedQuantizedVector[ i ] * 4
	accumulatedSquareError += delta * delta

print "RMSE straightforward truncation:", sqrt( float( accumulatedSquareError ) / numberOfGeneratedPixels )

accumulatedSquareError = 0
for i in range( numberOfGeneratedPixels ):
	delta = pixelVector[ i ] - errorDiffusedQuantizedVector[ i ] * 4
	accumulatedSquareError += delta * delta

print "RMSE with error diffusion:", sqrt( float( accumulatedSquareError ) / numberOfGeneratedPixels )
