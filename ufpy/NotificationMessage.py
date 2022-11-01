##
# This software was developed and / or modified by Raytheon Company,
# pursuant to Contract DG133W-05-CQ-1067 with the US Government.
# 
# U.S. EXPORT CONTROLLED TECHNICAL DATA
# This software product contains export-restricted data whose
# export/transfer/disclosure is restricted by U.S. law. Dissemination
# to non-U.S. persons whether in the United States or abroad requires
# an export license or other authorization.
# 
# Contractor Name:        Raytheon Company
# Contractor Address:     6825 Pine Street, Suite 340
#                         Mail Stop B8
#                         Omaha, NE 68106
#                         402.291.0100
# 
# See the AWIPS II Master Rights File ("Master Rights File.pdf") for
# further licensing information.
##

from string import Template

import ctypes
import stomp
import socket
import sys
import time
import threading
import xml.etree.ElementTree as ET 

import ThriftClient
from dynamicserialize.dstypes.com.raytheon.uf.common.alertviz import AlertVizRequest
from dynamicserialize import DynamicSerializationManager

#
# Provides a capability of constructing notification messages and sending 
# them to a STOMP data source.
#  
#    
#     SOFTWARE HISTORY
#    
#    Date            Ticket#       Engineer       Description
#    ------------    ----------    -----------    --------------------------
#    09/30/08                      chammack       Initial Creation.
#    11/03/10        5849          cjeanbap       Moved to ufpy package from
#                                                     com.raytheon.uf.tools.cli
#    01/07/11        5645          cjeanbap       Added audio file to Status Message.
#    05/27/11        3050          cjeanbap       Added if-statement to check Priority
#                                                 value
#    07/27/15        4654          skorolev       Added filters
#    11/11/15        5120          rferrel        Cannot serialize empty filters.
#
class NotificationMessage:
  
   priorityMap = { 
             0: 'CRITICAL',
             1: 'SIGNIFICANT',
             2: 'PROBLEM',
             3: 'EVENTA',
             4: 'EVENTB',
             5: 'VERBOSE'}

   def __init__(self, host='localhost', port=61999, message='', priority='PROBLEM', category="LOCAL", source="ANNOUNCER", audioFile="NONE", filters=None):
      self.host = host
      self.port = port
      self.message = message
      self.audioFile = audioFile
      self.source = source
      self.category = category 
      self.filters = filters

      priorityInt = None

      try:
         priorityInt = int(priority)
      except:
         pass

      if priorityInt is None:
          #UFStatus.java contains mapping of Priority to Logging level mapping
          if priority == 'CRITICAL' or priority == 'FATAL':
            priorityInt = int(0)
          elif priority == 'SIGNIFICANT' or priority == 'ERROR':
              priorityInt = int(1)
          elif priority == 'PROBLEM' or priority == 'WARN':
              priorityInt = int(2)
          elif priority == 'EVENTA' or priority == 'INFO':
              priorityInt = int(3)
          elif priority == 'EVENTB':
              priorityInt = int(4)
          elif priority == 'VERBOSE' or priority == 'DEBUG':
              priorityInt = int(5)       
      
      if (priorityInt < 0 or priorityInt > 5):                  
          print "Error occurred, supplied an invalid Priority value: " + str(priorityInt)
          print "Priority values are 0, 1, 2, 3, 4 and 5."
          sys.exit(1)     

      if priorityInt is not None:
          self.priority = self.priorityMap[priorityInt]
      else:
          self.priority = priority

   def connection_timeout(self, connection):
          if (connection is not None and not connection.is_connected()):
              print "Connection Retry Timeout"
              for tid, tobj in threading._active.items():
                  if tobj.name is "MainThread":
                      res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(SystemExit))
                      if res != 0 and res != 1:
                          # problem, reset state
                          ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)

   def send(self):
       # depending on the value of the port number indicates the distribution
       # of the message to AlertViz   
       # 9581 is global distribution thru ThriftClient to Edex
       # 61999 is local distribution
    if (int(self.port) == 61999):
        # use stomp.py
        conn = stomp.Connection(host_and_ports=[(self.host, 61999)])
        timeout = threading.Timer(5.0, self.connection_timeout, [conn])

        try:
            timeout.start();
            conn.start()
        finally:
            timeout.cancel()

        conn.connect()

        sm = ET.Element("statusMessage")
        sm.set("machine", socket.gethostname())
        sm.set("priority", self.priority)
        sm.set("category", self.category)
        sm.set("sourceKey", self.source)
        sm.set("audioFile", self.audioFile)
        if self.filters is not None and len(self.filters) > 0:
            sm.set("filters", self.filters)
        msg = ET.SubElement(sm, "message")
        msg.text = self.message
        details = ET.SubElement(sm, "details")
        msg = ET.tostring(sm, "UTF-8")
        
        try :
            conn.send(msg, destination='/queue/messages')
            time.sleep(2)
        finally:
            conn.stop()
    else:
        # use ThriftClient
        alertVizRequest = createRequest(self.message, self.priority, self.source, self.category, self.audioFile, self.filters)
        thriftClient = ThriftClient.ThriftClient(self.host, self.port, "/services")
    
        serverResponse = None
        try:
            serverResponse = thriftClient.sendRequest(alertVizRequest)
        except Exception, ex:
            print "Caught exception submitting AlertVizRequest: ", str(ex)    
        
        if (serverResponse != "None"):
            print "Error occurred submitting Notification Message to AlertViz receiver: ", serverResponse
            sys.exit(1)
        else:
            print "Response: " + str(serverResponse)        
        
def createRequest(message, priority, source, category, audioFile, filters):    
    obj = AlertVizRequest()
    
    obj.setMachine(socket.gethostname())    
    obj.setPriority(priority)
    obj.setCategory(category)
    obj.setSourceKey(source)    
    obj.setMessage(message)
    if (audioFile is not None):
        obj.setAudioFile(audioFile)
    else:
        obj.setAudioFile('\0')
    obj.setFilters(filters)
    return obj

if __name__ == '__main__':
    main()