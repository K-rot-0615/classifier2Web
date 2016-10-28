# -*- coding:utf-8 -*-

import serial

com_num = 3

def py2ar():
    with serial.Serial(com_num-1,9600,timeout=1) as ser:
        while True:
            # transport from python to arduino
            py2ar_flag = raw_input()
            ser.write(py2ar_flag)
            if (py2ar_flag=='a'):
                break

            # transport from arduino to python
            ar2py_flag = ser.readline()
            if ar2py_flag.rindex == 1:
                print 'ready to vibration!'
                break
            elif ar2py_flag.rindex == 0:
                print 'ready to stop!'
                break

        ser.close()

def ar2py():
    pass

if __name__ == '__main__':
    py2ar()