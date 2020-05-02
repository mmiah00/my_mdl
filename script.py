import mdl
from display import *
from matrix import *
from draw import *
import copy

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print("Parsing failed.")
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    print(symbols)
    for command in commands:
        op = command['op']
        args = command['args']
        if op == 'pop':
            stack.pop ()
        elif op == 'push':
            c = copy.deepcopy (stack[-1])
            stack.append (c)
        elif op == 'move':
            make_translate (args[0], args[1], args[2])
        elif op == 'rotate':
            xyz = args[0]
            degree = args[1]
            if xyz == 'x':
                make_rotX (degree)
            elif xyz == 'y':
                make_rotY (degree)
            else:
                make_rotZ (degree)
        elif op == 'scale':
            make_scale (args[0], args[1], args[2])
        elif op == 'box':
            constant = command['constants']
            add_box(tmp,
                    float(args[0]), float(args[1]), float(args[2]),
                    float(args[3]), float(args[4]), float(args[5]))
            matrix_mult( stack[-1], coords )
            if constant == None:
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
            else:
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, constant)
            tmp = []
        elif op == 'sphere':
            constant = command['constants']
            add_sphere(tmp,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step_3d)
            matrix_mult( stack[-1], coords )
            if constant == None:
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
            else:
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, constant)
            tmp = []
        elif op == 'torus':
            constant = command['constants']
            add_torus(tmp,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), step_3d)
            matrix_mult( stack[-1], coords )
            if constant == None:
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
            else:
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, constant)
            tmp = []
        elif op == 'line':
            print (line)
            add_edge( tmp,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), float(args[5]) )
            matrix_mult( stack[-1], edges )
            draw_lines(tmp, screen, zbuffer, color)
            tmp = []
        elif(op == 'save'):
            save_extension(screen, args[0] + '.png')

        elif(op == 'display'):
            display(screen)
