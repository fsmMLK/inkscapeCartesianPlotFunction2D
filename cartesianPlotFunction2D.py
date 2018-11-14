#!/usr/bin/python

# --------------------------------------------------------------------------------------
#
#    cartesianPlotFunction2D: - Inkscape extension to plot functions of one independent variable
#
#    Copyright (C) 2016 by Fernando Moura
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------------------------

from __future__ import division
import inkex
import inkscapeMadeEasy_Base as inkBase
import inkscapeMadeEasy_Draw as inkDraw
import inkscapeMadeEasy_Plot as inkPlot
from math import *
import numpy
import random

# heaviside function


def u(x):
    if x < 0:
        return 0.0
    else:
        return 1.0


# rectangular Pulse
def rectPulse(x, amplitude=1.0, length=1.0, offset=0.0, delay=0.0):
    return amplitude * (u(x - delay) - u(x - length - delay)) + offset


# square wave, with amplitude -A/2 to A/2, and given period
def squareWave(x, amplitude=1.0, offset=0, period=1.0, delay=0.0):
    return rectPulse((x % period), amplitude, period / 2.0, offset=-amplitude / 2.0 + offset, delay=delay)


def rand():
    return random.random()


#---------------------------------------------
class PlotFunction(inkBase.inkscapeMadeEasy):

    def __init__(self):
        inkBase.inkscapeMadeEasy.__init__(self)

        self.OptionParser.add_option("--tab", action="store", type="string", dest="tab", default="object")

        self.OptionParser.add_option("--function", action="store", type="string", dest="function", default='pow(x,2)')
        self.OptionParser.add_option("--nPoints", action="store", type="int", dest="nPoints", default=20)

        self.OptionParser.add_option("--xMin", action="store", type="float", dest="xMin", default='0.0')
        self.OptionParser.add_option("--xMax", action="store", type="float", dest="xMax", default='0.0')
        self.OptionParser.add_option("--xPi", action="store", type="inkbool", dest="xPi", default=False)
        self.OptionParser.add_option("--yMin", action="store", type="float", dest="yMin", default='0.0')
        self.OptionParser.add_option("--yMax", action="store", type="float", dest="yMax", default='0.0')
        self.OptionParser.add_option("--useElipsis", action="store", type="inkbool", dest="useEllipsis", default=False)
        self.OptionParser.add_option("--drawAxis", action="store", type="inkbool", dest="drawAxis", default=True)

        self.OptionParser.add_option("--xLabel", action="store", type="string", dest="xLabel", default='')
        self.OptionParser.add_option("--xScale", action="store", type="float", dest="xScale", default='5')
        self.OptionParser.add_option("--xLog10scale", action="store", type="inkbool", dest="xLog10scale", default=False)
        self.OptionParser.add_option("--xTicks", action="store", type="inkbool", dest="xTicks", default=False)
        self.OptionParser.add_option("--xTickStep", action="store", type="float", dest="xTickStep", default='1')
        self.OptionParser.add_option("--xGrid", action="store", type="inkbool", dest="xGrid", default=True)
        self.OptionParser.add_option("--xExtraText", action="store", type="string", dest="xExtraText", default='')

        self.OptionParser.add_option("--yLabel", action="store", type="string", dest="yLabel", default='')
        self.OptionParser.add_option("--yScale", action="store", type="float", dest="yScale", default='5')
        self.OptionParser.add_option("--yLog10scale", action="store", type="inkbool", dest="yLog10scale", default=False)
        self.OptionParser.add_option("--yTicks", action="store", type="inkbool", dest="yTicks", default=False)
        self.OptionParser.add_option("--yTickStep", action="store", type="float", dest="yTickStep", default='1')
        self.OptionParser.add_option("--yGrid", action="store", type="inkbool", dest="yGrid", default=True)
        self.OptionParser.add_option("--yExtraText", action="store", type="string", dest="yExtraText", default='')

        self.OptionParser.add_option("--generalAspectFactor", action="store", type="float", dest="generalAspectFactor", default=1.0)

    def effect(self):

        so = self.options

        # sets the position to the viewport center, round to next 10.
        position = [self.view_center[0], self.view_center[1]]
        position[0] = int(ceil(position[0] / 10.0)) * 10
        position[1] = int(ceil(position[1] / 10.0)) * 10

        #root_layer = self.current_layer
        root_layer = self.document.getroot()
        #root_layer = self.getcurrentLayer()

        myLambda = eval('lambda x: ' + so.function)

        # generate x data
        if not so.xLog10scale:
            xData = numpy.linspace(so.xMin, so.xMax, so.nPoints)
        else:
            xMin = so.xMin
            xMax = so.xMax
            # check limits
            if so.xMin <= 0:
                self.displayMsg('Error: xMin=%d is invalid in logarithmic scale\nUsing 0.001 instead' % (so.xMin))
                xMin = 0.001
            # check limits
            if so.xMax <= 0:
                self.displayMsg('Error: xMax=%d is invalid in logarithmic scale\nUsing  100 times xMin instead' % (so.xMax))
                xMax = 100 * xMin

            xData = numpy.logspace(log10(xMin), log10(xMax), so.nPoints)

        if so.xPi:
            xData = [x * pi for x in xData]

        # generate y data
        #yData= map(myLambda, xData)

        yData = []
        for x in xData:
            if myLambda(x) == float('Inf'):
                yData.append(0.0)
                inkDraw.text.write(self, 'Inf result detected: The function at x=%d is infinite.' % x, position, root_layer, fontSize=5)
                inkDraw.text.write(self, 'Setting the point to 0... PLEASE CHECK YOUR PLOT!' % x, [position[0], position[1] + 8], root_layer, fontSize=5)
            else:
                yData.append(myLambda(x))

        # check if limits are valid
        if so.yMin >= so.yMax:
            self.displayMsg('Error: yMin and yMax are invalid.')
            return 0

        # block limits
        yData = [min(y, so.yMax) for y in yData]
        yData = [max(y, so.yMin) for y in yData]

        if so.yLog10scale:
            ylim = None
        else:
            ylim = [so.yMin, so.yMax]

        # x labels if multiply by pi
        if so.xPi:
            xData = numpy.linspace(so.xMin, so.xMax, so.nPoints)
            xExtraText = "\pi " + so.xExtraText
        else:
            xExtraText = so.xExtraText

        # line style
        lineWidthPlot = so.generalAspectFactor * min(so.xScale, so.yScale) / 30.0
        lineColor = inkDraw.color.defined('blue')
        if so.useEllipsis:
            StartLineInf, EndLineInf = inkDraw.marker.createInfLineMarker(self, 'InfiniteLine', RenameMode=1, fillColor=lineColor)
            lineStylePlot = inkDraw.lineStyle.set(lineWidth=lineWidthPlot, lineColor=lineColor, markerStart=StartLineInf, markerEnd=EndLineInf)
        else:
            lineStylePlot = inkDraw.lineStyle.set(lineWidth=lineWidthPlot, lineColor=lineColor)

        inkPlot.plot.cartesian(self, root_layer, xData, yData, position,
                               xLabel=so.xLabel, yLabel=so.yLabel, xlog10scale=so.xLog10scale, ylog10scale=so.yLog10scale,
                               xTicks=so.xTicks, yTicks=so.yTicks, xTickStep=so.xTickStep, yTickStep=so.yTickStep,
                               xScale=so.xScale, yScale=so.yScale, xExtraText=xExtraText, yExtraText=so.yExtraText,
                               xGrid=so.xGrid, yGrid=so.yGrid, generalAspectFactorAxis=so.generalAspectFactor, lineStylePlot=lineStylePlot,
                               forceYlim=ylim, drawAxis=so.drawAxis)

if __name__ == '__main__':
    plot = PlotFunction()
    plot.affect()
