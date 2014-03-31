#! /usr/bin/python

from xbee import ZigBee
import serial

R1_ADDR_LONG = b'\x00\x13\xA2\x00\x40\xB4\x10\x3b'
R1_ADDR_SHORT = b'\xff\xfe' 
"""
serial_example.py
By Paul Malmsten, 2010

Demonstrates reading the low-order address bits from an XBee Series 1
device over a serial port (USB) in API-mode.
"""

def main():
    """
    Sends an API AT command to read the lower-order address bits from 
    an XBee Series 1 and looks for a response
    """
    try:
        # Open serial port
        ser = serial.Serial('COM17', 9600)
        
        # Create XBee Series 1 object
        xbee = ZigBee(ser)

        # Send AT packet
        xbee.send('at', frame_id='A', dest_addr_long=R1_ADDR_LONG, dest_addr=R1_ADDR_SHORT, command='MY')
        # Wait for response
        response = xbee.wait_read_frame()
        print response
        
        # Send AT packet
        xbee.send('tx', frame_id='B', dest_addr_long=R1_ADDR_LONG, dest_addr=R1_ADDR_SHORT, data='0123')
        
        # Wait for response
        response = xbee.wait_read_frame()
        print response
        
        # Send AT packet
        xbee.send('tx', frame_id='C', dest_addr_long=R1_ADDR_LONG, dest_addr=R1_ADDR_SHORT, data='H:60.21')
        
        # Wait for response
        response = xbee.wait_read_frame()
        print response
        
        # Send AT packet
        xbee.send('remote_at', frame_id='D', dest_addr_long=R1_ADDR_LONG, dest_addr=R1_ADDR_SHORT, command='NI', \
                  parameter='R1')
        
        # Wait for response
        response = xbee.wait_read_frame()
        print response

         # Send AT packet
        xbee.send('remote_at', frame_id='E', dest_addr_long=R1_ADDR_LONG, dest_addr=R1_ADDR_SHORT, command='NI')
        
        # Wait for response
        response = xbee.wait_read_frame()
        print response
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()
    
if __name__ == '__main__':
    main()
