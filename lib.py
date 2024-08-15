from pathlib import Path
import subprocess
import schemdraw
import schemdraw.elements as elm
import matplotlib
import warnings
import os
from pysvgexport import SVGExport

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning, message="FigureCanvasAgg is non-interactive, and thus cannot be shown")

matplotlib.use('Agg')

def drawSchematics(inductor_low, capacitor_low, resistor_high1, capacitor_high, inductor_high, resistor_high2):
    # Create the Drawing object for low pass filter
    d_low = schemdraw.Drawing()
    
    # Draw the Low Pass Filter
    with d_low:
        # Voltage Source
        vsource = d_low.add(elm.SourceV().label('V1').at((0, 0)))
        
        # Ground for voltage source
        d_low.add(elm.Ground().left().flip().at(vsource.start))
        
        # Inductor
        ind = d_low.add(elm.Inductor().right(9).at(vsource.end).label(inductor_low))
        
        # Dot and Capacitor
        dot = (ind.end)
        d_low.add(elm.Dot().at(dot))
        cap = d_low.add(elm.Capacitor().down().at(dot).label(capacitor_low))
        
        # Ground for Capacitor
        d_low.add(elm.Ground().at(cap.end))
        
        # Load (Speaker)
        d_low.add(elm.Line().right().at(dot))
        speaker_low = d_low.add(elm.Speaker().label('Low frequency'))
        d_low.add(elm.Ground().at((speaker_low.in2)))
        
        d_low.add(elm.Label('Low Pass Filter').at((12, -0.2)))

    # Create the Drawing object for high pass filter
    d_high = schemdraw.Drawing()
    
    # Draw the High Pass Filter
    with d_high:
        # Voltage Source
        vsource = d_high.add(elm.SourceV().label('V2').at((0, 0)))
        
        # Ground for voltage source
        d_high.add(elm.Ground().flip().left().at(vsource.start))
        
        # Resistor 1
        res1 = d_high.add(elm.Resistor().right().at(vsource.end).label(resistor_high1))
        
        # Capacitor
        cap = d_high.add(elm.Capacitor().right().at(res1.end).label(capacitor_high))
        
        # Dot 1 and Inductor
        dot1 = (cap.end)
        d_high.add(elm.Dot().at(dot1))
        ind = d_high.add(elm.Inductor().down().at(dot1).label(inductor_high))
        
        # Ground for Inductor
        d_high.add(elm.Ground().right().at(ind.end))
        
        # Dot 2 and Resistor 2
        d_high.add(elm.Line().right().at(dot1))
        d_high.add(elm.Dot().right())
        res2 = d_high.add(elm.Resistor().down().label(resistor_high2))
        
        # Ground for Resistor 2
        d_high.add(elm.Ground().right().at(res2.end))
        dot2 = (res2.start)
        d_high.add(elm.Line().right().at(dot2))
        speaker_high = d_high.add(elm.Speaker().label('High Frequency'))
        d_high.add(elm.Ground().at(speaker_high.in2))
        
        d_high.add(elm.Label('High Pass Filter').at((12, -0.2)))

    d_low.draw()
    d_high.draw()

    saveInOutDir(d_low, 'low_pass_filter')
    saveInOutDir(d_high, 'high_pass_filter')

    return formatSvg(d_low), formatSvg(d_high)


def formatSvg(svg):
    svg_bytes = svg.get_imagedata('svg')
    svg_string = svg_bytes.decode('utf-8')
    return svg_string


def saveInOutDir(svg, filename):
    if not os.path.exists('out'):
        os.makedirs('out')
    svg.save('out/{filename}.svg'.format(filename=filename))


def getDesktopPath():
    home = Path.home()
    desktop = home / "Desktop"
    # desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    print("desktop: ", desktop)
    return desktop


def exportPng():
    out = os.path.abspath('out')

    low_pass_source = os.path.join(out, 'low_pass_filter.svg')
    low_pass_target = os.path.join(out, 'low_pass_filter.png')

    subprocess.run(['svgexport', '-f', low_pass_source, '-s', '20', '-o', low_pass_target])

    high_pass_source = os.path.join(out, 'high_pass_filter.svg')
    high_pass_target = os.path.join(out, 'high_pass_filter.png')

    subprocess.run(['svgexport', '-f', high_pass_source, '-s', '20', '-o', high_pass_target])

