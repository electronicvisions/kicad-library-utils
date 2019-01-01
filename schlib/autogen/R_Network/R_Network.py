#!/usr/bin/env python3

import math
import os
import sys

sys.path.append(os.path.join(sys.path[0], '..'))

from KiCadSymbolGenerator import *

def roundG(x, g):
    if x > 0:
        return math.ceil(x / g) * g
    else:
        return math.floor(x / g) * g

generator = SymbolGenerator('R_Network')

def generateResistorNetwork(count):
    name = 'R_Network{:02d}'.format(count)
    refdes = 'RN'
    footprint = 'Resistor_THT:R_Array_SIP{0}'.format(count + 1)
    footprint_filter = 'R?Array?SIP*'
    description = '{0} resistor network, star topology, bussed resistors, small symbol'.format(count)
    keywords = 'R network star-topology'
    datasheet = 'http://www.vishay.com/docs/31509/csc.pdf'

    dp = 100
    junction_diameter = 20
    pin_length = 100
    resistor_length = 160
    resistor_width = 60
    W_dist = 30
    box_l_offset = 50
    left = -math.floor(count / 2) * dp
    body_x = left - box_l_offset
    body_y = -125
    body_height = 250
    body_width = (count - 1) * dp + 2 * box_l_offset
    top = -200
    bottom = 200

    symbol = generator.addSymbol(name,
        dcm_options = {
            'datasheet': datasheet,
            'description': description,
            'keywords': keywords
        },
        footprint_filter = footprint_filter,
        offset = 0,
        pin_name_visibility = Symbol.PinMarkerVisibility.INVISIBLE
    )
    symbol.setReference(refdes,
        at = {'x': body_x - 50, 'y': 0},
        orientation = SymbolField.FieldOrientation.VERTICAL
    )
    symbol.setValue(
        at = {'x': body_x + body_width + 50, 'y': 0},
        orientation = SymbolField.FieldOrientation.VERTICAL
    )
    symbol.setDefaultFootprint(
        at = {'x': body_x + body_width + 50 + 75, 'y': 0},
        orientation = SymbolField.FieldOrientation.VERTICAL,
        value = footprint
    )

    # Symbol body
    symbol.drawing.append(DrawingRectangle(
        end = {'x': body_x + body_width, 'y': body_y + body_height},
        fill = ElementFill.FILL_BACKGROUND,
        start = {'x': body_x, 'y': body_y},
        unit_idx = 0
    ))

    pin_left = left

    # Common pin
    symbol.drawing.append(DrawingPin(
        at = {'x': pin_left, 'y': -top},
        name = 'common',
        number = 1,
        orientation = DrawingPin.PinOrientation.DOWN,
        pin_length = pin_length
    ))

    # First top resistor lead
    symbol.drawing.append(DrawingPolyline(
        line_width = 0,
        points = [
            {'x': pin_left, 'y': -(top + pin_length)},
            {'x': pin_left, 'y': -(bottom - pin_length - resistor_length)}
        ],
        unit_idx = 0
    ))

    for s in range(1, count + 1):
        # Resistor pins
        symbol.drawing.append(DrawingPin(
            at = {'x': pin_left, 'y': -bottom},
            name = 'R{0}'.format(s),
            number = s + 1,
            orientation = DrawingPin.PinOrientation.UP,
            pin_length = pin_length
        ))
        # Resistor bodies
        symbol.drawing.append(DrawingRectangle(
            end = {'x': pin_left + resistor_width / 2, 'y': -(bottom - pin_length)},
            start = {'x': pin_left - resistor_width / 2, 'y': -(bottom - pin_length - resistor_length)},
            unit_idx = 0
        ))

        if s < count:
            # Top resistor leads
            symbol.drawing.append(DrawingPolyline(
                line_width = 0,
                points = [
                    {'x': pin_left, 'y': -(bottom - pin_length - resistor_length)},
                    {'x': pin_left, 'y': -(bottom - pin_length - resistor_length - W_dist)},
                    {'x': pin_left + dp, 'y': -(bottom - pin_length - resistor_length - W_dist)},
                    {'x': pin_left + dp, 'y': -(bottom - pin_length - resistor_length)}
                ],
                unit_idx = 0
            ))
            # Junctions
            symbol.drawing.append(DrawingCircle(
                at = {'x': pin_left, 'y': -(bottom - pin_length - resistor_length - W_dist)},
                fill = ElementFill.FILL_FOREGROUND,
                line_width = 0,
                radius = junction_diameter / 2,
                unit_idx = 0
            ))

        pin_left = pin_left + dp

def generateSIPNetworkDividers(count):
    name = 'R_Network_Dividers_x{:02d}_SIP'.format(count)
    refdes = 'RN'
    footprint = 'Resistor_THT:R_Array_SIP{0}'.format(count + 2)
    footprint_filter = 'R?Array?SIP*'
    description = '{0} voltage divider network, dual terminator, SIP package'.format(count)
    keywords = 'R network divider topology'
    datasheet = 'http://www.vishay.com/docs/31509/csc.pdf'

    dp = 200
    junction_diameter = 20
    pin_length = 100
    resistor_length = 100
    resistor_width = 40
    box_l_offset = 50
    left = -math.floor(count / 2) * dp
    top = -300
    bottom = 300
    body_x = left - box_l_offset
    body_y = top + pin_length
    body_height = abs(bottom - pin_length - body_y)
    body_width = (count - 1) * dp + dp / 2 + 2 * box_l_offset
    R_dist = (body_height - 2 * resistor_length) / 3

    symbol = generator.addSymbol(name,
        dcm_options = {
            'datasheet': datasheet,
            'description': description,
            'keywords': keywords
        },
        footprint_filter = footprint_filter,
        offset = 0,
        pin_name_visibility = Symbol.PinMarkerVisibility.INVISIBLE
    )
    symbol.setReference(refdes,
        at = {'x': body_x - 50, 'y': 0},
        orientation = SymbolField.FieldOrientation.VERTICAL
    )
    symbol.setValue(
        at = {'x': body_x + body_width + 50, 'y': 0},
        orientation = SymbolField.FieldOrientation.VERTICAL
    )
    symbol.setDefaultFootprint(
        at = {'x': body_x + body_width + 50 + 75, 'y': 0},
        orientation = SymbolField.FieldOrientation.VERTICAL,
        value = footprint
    )

    # Symbol body
    symbol.drawing.append(DrawingRectangle(
        end = {'x': body_x + body_width, 'y': body_y + body_height},
        fill = ElementFill.FILL_BACKGROUND,
        start = {'x': body_x, 'y': body_y},
        unit_idx = 0
    ))

    pin_left = left

    # Common 1 pin
    symbol.drawing.append(DrawingPin(
        at = {'x': pin_left, 'y': -top},
        name = 'COM1',
        number = 1,
        orientation = DrawingPin.PinOrientation.DOWN,
        pin_length = pin_length
    ))
    # Common 2 pin
    symbol.drawing.append(DrawingPin(
        at = {'x': left + (count - 1) * dp + dp / 2, 'y': -top},
        name = 'COM2',
        number = count + 2,
        orientation = DrawingPin.PinOrientation.DOWN,
        pin_length = pin_length
    ))
    # Vertical COM2 lead
    symbol.drawing.append(DrawingPolyline(
        line_width = 0,
        points = [
            {'x': left + (count - 1) * dp + dp / 2, 'y': -(bottom - pin_length - R_dist / 2)},
            {'x': left + (count - 1) * dp + dp / 2, 'y': -(top + pin_length)}
        ],
        unit_idx = 0
    ))

    for s in range(1, count + 1):
        # Voltage divider center pins
        symbol.drawing.append(DrawingPin(
            at = {'x': pin_left, 'y': -bottom},
            name = 'R{0}'.format(s),
            number = s + 1,
            orientation = DrawingPin.PinOrientation.UP,
            pin_length = pin_length
        ))
        # Top resistor bodies
        symbol.drawing.append(DrawingRectangle(
            end = {'x': pin_left + resistor_width / 2, 'y': -(top + pin_length + R_dist + resistor_length)},
            start = {'x': pin_left - resistor_width / 2, 'y': -(top + pin_length + R_dist)},
            unit_idx = 0
        ))
        # Bottom resistor bodies
        symbol.drawing.append(DrawingRectangle(
            end = {'x': pin_left + 3 * resistor_width / 2 + resistor_width / 2, 'y': -(bottom - pin_length - R_dist - resistor_length)},
            start = {'x': pin_left + 3 * resistor_width / 2 - resistor_width / 2, 'y': -(bottom - pin_length - R_dist)},
            unit_idx = 0
        ))
        # Horizontal COM2 leads
        symbol.drawing.append(DrawingPolyline(
            line_width = 0,
            points = [
                {'x': pin_left + 3 * resistor_width / 2, 'y': -(bottom - pin_length - R_dist)},
                {'x': pin_left + 3 * resistor_width / 2, 'y': -(bottom - pin_length - R_dist / 2)},
                {'x': left + (count - 1) * dp + dp / 2, 'y': -(bottom - pin_length - R_dist / 2)}
            ],
            unit_idx = 0
        ))

        if s == 1:
            # First resistor top lead
            symbol.drawing.append(DrawingPolyline(
                line_width = 0,
                points = [
                    {'x': pin_left, 'y': -(top + pin_length)},
                    {'x': pin_left, 'y': -(top + pin_length + R_dist)}
                ],
                unit_idx = 0
            ))

        if s > 1:
            # Top resistor top leads
            symbol.drawing.append(DrawingPolyline(
                line_width = 0,
                points = [
                    {'x': pin_left - dp, 'y': -(top + pin_length + R_dist / 2)},
                    {'x': pin_left, 'y': -(top + pin_length + R_dist / 2)},
                    {'x': pin_left, 'y': -(top + pin_length + R_dist)}
                ],
                unit_idx = 0
            ))

        # Top resistor bottom leads
        symbol.drawing.append(DrawingPolyline(
            line_width = 0,
            points = [
                {'x': pin_left, 'y': -(bottom - pin_length)},
                {'x': pin_left, 'y': -(top + pin_length + R_dist + resistor_length)}
            ],
            unit_idx = 0
        ))
        # Bottom resistor top leads
        symbol.drawing.append(DrawingPolyline(
            line_width = 0,
            points = [
                {'x': pin_left, 'y': -(top + pin_length + R_dist + resistor_length + R_dist / 2)},
                {'x': pin_left + 3 * resistor_width / 2, 'y': -(top + pin_length + R_dist + resistor_length + R_dist / 2)},
                {'x': pin_left + 3 * resistor_width / 2, 'y': -(bottom - pin_length - R_dist - resistor_length)}
            ],
            unit_idx = 0
        ))
        # Center junctions
        symbol.drawing.append(DrawingCircle(
            at = {'x': pin_left, 'y': 0},
            fill = ElementFill.FILL_FOREGROUND,
            line_width = 0,
            radius = junction_diameter / 2,
            unit_idx = 0
        ))

        if s > 1:
            # Bottom junctions
            symbol.drawing.append(DrawingCircle(
                at = {'x': pin_left + 3 * resistor_width / 2, 'y': -(bottom - pin_length - R_dist / 2)},
                fill = ElementFill.FILL_FOREGROUND,
                line_width = 0,
                radius = junction_diameter / 2,
                unit_idx = 0
            ))

        if s < count:
            # Top junctions
            symbol.drawing.append(DrawingCircle(
                at = {'x': pin_left, 'y': -(top + pin_length + R_dist / 2)},
                fill = ElementFill.FILL_FOREGROUND,
                line_width = 0,
                radius = junction_diameter / 2,
                unit_idx = 0
            ))

        pin_left = pin_left + dp

def generateResistorPack(count):
    name = 'R_Pack{:02d}'.format(count)
    refdes = 'RN'
    footprint = ''
    footprint_filter = ['DIP*', 'SOIC*']
    description = '{0} resistor network, parallel topology, DIP package'.format(count)
    keywords = 'R network parallel topology isolated'
    datasheet = '~'

    dp = 100
    pin_length = 100
    resistor_length = 150
    resistor_width = 50
    box_l_offset = 50
    box_t_offset = 20
    left = -roundG(((count - 1) * dp) / 2, 100)
    body_x = left - box_l_offset
    body_height = resistor_length + 2 * box_t_offset
    body_y = -body_height / 2
    body_width = ((count - 1) * dp) + 2 * box_l_offset
    top = -200
    bottom = 200

    symbol = generator.addSymbol(name,
        dcm_options = {
            'datasheet': datasheet,
            'description': description,
            'keywords': keywords
        },
        footprint_filter = footprint_filter,
        offset = 0,
        pin_name_visibility = Symbol.PinMarkerVisibility.INVISIBLE
    )
    symbol.setReference(refdes,
        at = {'x': body_x - 50, 'y': 0},
        orientation = SymbolField.FieldOrientation.VERTICAL
    )
    symbol.setValue(
        at = {'x': body_x + body_width + 50, 'y': 0},
        orientation = SymbolField.FieldOrientation.VERTICAL
    )
    symbol.setDefaultFootprint(
        at = {'x': body_x + body_width + 50 + 75, 'y': 0},
        orientation = SymbolField.FieldOrientation.VERTICAL,
        value = footprint
    )

    # Symbol body
    symbol.drawing.append(DrawingRectangle(
        end = {'x': body_x + body_width, 'y': body_y + body_height},
        fill = ElementFill.FILL_BACKGROUND,
        start = {'x': body_x, 'y': body_y},
        unit_idx = 0
    ))

    pin_left = left

    for s in range(1, count + 1):
        # Resistor bottom pins
        symbol.drawing.append(DrawingPin(
            at = {'x': pin_left, 'y': -bottom},
            name = 'R{0}.1'.format(s),
            number = s,
            orientation = DrawingPin.PinOrientation.UP,
            pin_length = pin_length
        ))
        # Resistor top pins
        symbol.drawing.append(DrawingPin(
            at = {'x': pin_left, 'y': -top},
            name = 'R{0}.2'.format(s),
            number = 2 * count - s + 1,
            orientation = DrawingPin.PinOrientation.DOWN,
            pin_length = pin_length
        ))
        # Resistor bodies
        symbol.drawing.append(DrawingRectangle(
            end = {'x': pin_left + resistor_width / 2, 'y': -(resistor_length / 2)},
            start = {'x': pin_left - resistor_width / 2, 'y': -(-resistor_length / 2)},
            unit_idx = 0
        ))
        # Resistor bottom leads
        symbol.drawing.append(DrawingPolyline(
            line_width = 0,
            points = [
                {'x': pin_left, 'y': -(bottom - pin_length)},
                {'x': pin_left, 'y': -(resistor_length / 2)}
            ],
            unit_idx = 0
        ))
        # Resistor top leads
        symbol.drawing.append(DrawingPolyline(
            line_width = 0,
            points = [
                {'x': pin_left, 'y': -(-resistor_length / 2)},
                {'x': pin_left, 'y': -(top + pin_length)}
            ],
            unit_idx = 0
        ))

        pin_left = pin_left + dp

def generateSIPResistorPack(count):
    name = 'R_Pack{:02d}_SIP'.format(count)
    refdes = 'RN'
    footprint = 'Resistor_THT:R_Array_SIP{0}'.format(count * 2)
    footprint_filter = 'R?Array?SIP*'
    description = '{0} resistor network, parallel topology, SIP package'.format(count)
    keywords = 'R network parallel topology isolated'
    datasheet = 'http://www.vishay.com/docs/31509/csc.pdf'

    dp = 100
    dR = 300
    pin_length = 150
    resistor_length = 160
    resistor_width = 60
    W_dist = 30
    box_l_offset = 50
    left = -roundG(((count - 1) * dR) / 2, 100)
    body_x = left - box_l_offset
    body_y = -75
    body_height = 250
    body_width = ((count - 1) * dR + dp) + 2 * box_l_offset
    bottom = 200

    symbol = generator.addSymbol(name,
        dcm_options = {
            'datasheet': datasheet,
            'description': description,
            'keywords': keywords
        },
        footprint_filter = footprint_filter,
        offset = 0,
        pin_name_visibility = Symbol.PinMarkerVisibility.INVISIBLE
    )
    symbol.setReference(refdes,
        at = {'x': body_x - 50, 'y': 0},
        orientation = SymbolField.FieldOrientation.VERTICAL
    )
    symbol.setValue(
        at = {'x': body_x + body_width + 50, 'y': 0},
        orientation = SymbolField.FieldOrientation.VERTICAL
    )
    symbol.setDefaultFootprint(
        at = {'x': body_x + body_width + 50 + 75, 'y': 0},
        orientation = SymbolField.FieldOrientation.VERTICAL,
        value = footprint
    )

    # Symbol body
    symbol.drawing.append(DrawingRectangle(
        end = {'x': body_x + body_width, 'y': body_y + body_height},
        fill = ElementFill.FILL_BACKGROUND,
        start = {'x': body_x, 'y': body_y},
        unit_idx = 0
    ))

    pin_left = left

    for s in range(1, count + 1):
        # Resistor short pins
        symbol.drawing.append(DrawingPin(
            at = {'x': pin_left, 'y': -bottom},
            name = 'R{0}.1'.format(s),
            number = 2 * s - 1,
            orientation = DrawingPin.PinOrientation.UP,
            pin_length = pin_length
        ))
        # Resistor long pins
        symbol.drawing.append(DrawingPin(
            at = {'x': pin_left + dp, 'y': -bottom},
            name = 'R{0}.2'.format(s),
            number = 2 * s,
            orientation = DrawingPin.PinOrientation.UP,
            pin_length = pin_length
        ))
        # Resistor bodies
        symbol.drawing.append(DrawingRectangle(
            end = {'x': pin_left + resistor_width / 2, 'y': -(bottom - pin_length)},
            start = {'x': pin_left - resistor_width / 2, 'y': -(bottom - pin_length - resistor_length)},
            unit_idx = 0
        ))
        # Resistor long leads
        symbol.drawing.append(DrawingPolyline(
            line_width = 0,
            points = [
                {'x': pin_left, 'y': -(bottom - pin_length - resistor_length)},
                {'x': pin_left, 'y': -(bottom - pin_length - resistor_length - W_dist)},
                {'x': pin_left + dp, 'y': -(bottom - pin_length - resistor_length - W_dist)},
                {'x': pin_left + dp, 'y': -(bottom - pin_length)}
            ],
            unit_idx = 0
        ))

        pin_left = pin_left + dR

if __name__ == '__main__':
    for i in range(3, 14):
        generateResistorNetwork(i)

    for i in range(2, 12):
        generateSIPNetworkDividers(i)

    for i in range(2, 8):
        generateResistorPack(i)
        generateSIPResistorPack(i)

    for i in range(8, 12):
        generateResistorPack(i)

    generator.writeFiles()
