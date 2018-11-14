# cartesianPlotFunction2D
 Inkscape extension to plot functions of one independent variable

<img src="docs/images/Examples.png" width="900px"/>

This extension was inspired by Tavmjong Bah's (and collaborators) extension **Function Plotter** already presented in Inkscape. Function Plotter extension is not required here.

### main features

The main features are

 - linear and log10 scales
 - optional grid lines in X and Y directions
 - adjustable tick mark intervals and sizes
 - LaTeX support

# Installation and requirements

This extension was partially developed in Inkscape 0.48 and partially in 0.91 in Linux (Kubuntu 12.04 and 14.04). It should work on both versions of Inkscape. Also, they should work in different OSs too as long as all requirements are installed.

This extension requires another extension to run, inkscapeMadeEasy <https://github.com/fsmMLK/inkscapeMadeEasy>, which contains several backstage methods and classes.

In order to use cartesianPlotFunction2D extension, you must also download inkscapeMadeEasy files and put them inside Inkscape's extension directory. Please refer to inkscapeMadeEasy installation instructions. In the end you must have the following files and directories in your Inkscape extension directory.

```
inkscape/extensions/
            |-- inkscapeMadeEasy_Base.py
            |-- inkscapeMadeEasy_Draw.py
            |-- inkscapeMadeEasy_Plot.py
            |-- textextLib
            |   |-- __init__.py
            |   |-- basicLatexPackages.tex
            |   |-- textext.inx
            |   |-- textext.py
            |
            |-- cartesianPlotFunction2D.py
            `-- cartesianPlotFunction2D.inx
```

**Disabling LaTeX support of inkscapeMadeEasy**

Many of the methods implemented in inkscapeMadeEasy project use LaTeX to generate text. To this end I decided to employ the excellent extension **textext** from Pauli Virtanen  <https://pav.iki.fi/software/textext/>. 

LaTeX support via textext extension requires LaTeX typesetting system in your computer (it's free and awesome! =] ), together with a few python modules (pygtk and Tkinter among others). The later might be a problem for non-Linux systems (precompiled inkscape for Windows as OS X don't come with them).

Since many people don't use LaTeX and/or don't have it installed, inkscapeMadeEasy's LaTeX support is now optional. **By default, LaTeX support is ENABLED.**

Please refer to <https://fsmmlk.github.io/inkscapeMadeEasy/#installation-and-requirements> on how to easily disable LaTeX support.

.. warning:: Since disabling LaTeX support is a new feature, this project was not yet extensively checked for misplacements/errors when this support is disabled. Please report any issues you find.

# Usage

The extension can be found under `extensions > fsmMLK > Plot 2D > Cartesian` menu.

This extension is presented in two tabs, **Function Definition** and  **Axes configuration**. The first is used to define the function and input/output ranges. The second is used to configure the axes.

<img src="docs/images/Config_Function.png" width="600px"/>

<img src="docs/images/Config_Axes.png" width="600px"/>

### The Function Definition tab

Here you can define your function and set both the input and output ranges. 

**Function:** Function definition. This must be a python compatible expression. Your independent variable **MUST** be `x`.

> Tip: This extension imports all method from 'math' module from python. Therefore you don have to specify the module name math.<some_method>.

> Example: to generate a sine function, just type `sin(x)`. You don't have to type `math.sin(x)`

**Number of points:** Number of points where the function will be evaluated within the limits (see below)

  - If logarithmic scale is not checked for X axis, then the points will be uniformly distributed within the limits
  - If logarithmic scale is     checked for X axis, then the points will be logarithmically distributed within the limits


**Use ellipsis marks at the ends:** Use ellipsis marks at the end of the plots to indicate continuation

<img src="docs/images/ellipsis.png" width="300px"/>

**Draw Cartesian plane:** Toggle to generate the cartesian axes. Usually you want this to be checked. =)

<img src="docs/images/drawAxes.png" width="600px"/>

**General aspect factor:** General aspect ratio between line widths and text width. I designed this extension to have an overall aspect ratio that looked nice to my eyes. It is a function of X and Y tick lengths. With this control you can scale both line widths and text height to fit your needs.

<img src="docs/images/generalAspectRatio.png" width="700px"/>

**X min and max:** Set the limits of the X axis. The extension will inform if these limits are invalid.
  
  - The upper limits must be greater than the lower limits
  - If logarithmic scale is checked, then the lower limit will be rounded down to the nearest power of 10 and the upper rounded up to the nearest power of 10 in order to complete the decades. Ex: 0.2 to 12, then the limits will be rounded to 0.1 to 100. **Attention:** This will not change the range of values in which the function will be evaluated. The limits will be rounded only to produce the Cartesian axes with complete decades.
  - If logarithmic scale is checked:
    * if xMin<=0.0 then the lower limit xMin will be set to 0.001.
    * if xMax<=0.0 then the upper limit xMax will be set to 100 times xMin.

<img src="docs/images/xMin_xMax.png" width="500px"/>

**Y min and max:** (linear scale only) Set the limits of the Y axis. The extension will inform if these limits are invalid. These values are used to limit the solution, that is, if `f(x)` does not lie within Ymin and Ymax, then the solution will be clipped at these values.

<img src="docs/images/yMin_yMax.png" width="600px"/>


**multiply X by pi:** Multiply the limits by pi. Ex: `xMin=-2` ans `xMax=2`, with this checkbox selected results in x limits of `xMin=-2pi` ans `xMax=2pi`. This is specially useful for trigonometric functions.

>  If this checkbox is selected, *X tick step* (see below) will be also multiplied  by pi.

<img src="docs/images/multiply_X_ByPi.png" width="600px"/>

### The Axes Configuration tab


**X/Y axis label:** label of the axes. This string must be LaTeX compatible. Any LaTeX commands or environments are valid. If you want to write in mathematical environment, enclose your text with $...$. You don't have to escape any backslashes.

> Tip: Since `siunitx` package is included in basicLatexPackages.tex file by default in inkscapeMadeEasy, you can use any unit command available there 

Ex: `Foobar $\sqrt{x^2}$ so fancy! (\si{\newton\per\squaremetre})`

<img src="docs/images/Legend_01.png" width="400px"/>

**Logarithmic scale:** Set the axis to be represented in log10 scale.

**Add grid to X/Y axis:** Draw grid lines in X or Y axes.
   - *linear scale:* The grid lines will be placed at each tick mark
   - *logarithmic scale:* The grid lines will be placed dividing each decade in 10 parts

**Add ticks to X/Y axis:** Draw tick marks with associated values in X or Y axes.

**X/Y tick step:** Tick marks interval  in units of your chart. This value is not referenced to  in logarithmic scale

Ex: limits from -1 to 1, with tick step of 0.5 will produce ticks at -1, -0.5, 0, 0.5, 1

> Note: The ticks will radiate from the origin x=0 or y=0 unless the origin does not lie within the limits. In such cases, the ticks will radiate starting from the  limit closest to the origin.
>
> Examples in x direction. The same rules apply to Y direction
>
> <img src="docs/images/TickStep.png" width="600px"/>


**X/Y tick length** The distance between the tick marks, in px.
   - *linear scale:* The distance between ticks in px.
   - *logarithmic scale:* The size of each decade in px.

<img src="docs/images/TickLength.png" width="350px"/>

**X/Y tick suffix value:** Optional extra suffix to be added to the tick values. You can use any LaTeX text/commands valid in mathematical environment $...$. You don't have to enclose your text between $...$. You don't have to escape any backslashes.

<img src="docs/images/TickSuffix.png" width="800px"/>

# Observations

 - Since the plot is generated by evaluating the function along the input range and connecting the points by a polyline, if your function is discontinuous your plot will present a line connecting both sides of the discontinuity. **In such cases, please check your plot!**  ;)

<img src="docs/images/Obs_discontinuous.png" width="600px"/>

 - The axes will be placed crossing the origin (0,0) or crossing the coordinate (x,y) closest to the origin if the origin does not lies within the limits.
 - The axes will be created at the center of your screen.

# Special functions

Together with the extension I also pre defined 3 new functions:

 - **Heaviside step function**

Calling: `u(x)`

Examples:

<img src="docs/images/heaviside.png" width="800px"/>

 - **Rectangular pulse**

Calling: `rectPulse(x,amplitude=1.0,length=1.0,offset=0.0,delay=0.0)`

<img src="docs/images/rectPulse.png" width="800px"/>

 - **Square wave**

Calling: `squareWave(x,amplitude=1.0,offset=0,period=1.0,delay=0.0)`

<img src="docs/images/squareWave.png" width="700px"/>

> Tip: You can define your own functions at the beginning of the file `cartesianPlotFunction2D.py`


# Examples

<img src="docs/images/Examples.png" width="900px"/>



