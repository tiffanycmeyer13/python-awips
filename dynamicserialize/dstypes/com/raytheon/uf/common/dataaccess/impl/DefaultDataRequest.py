##
##

# File auto-generated against equivalent DynamicSerialize Java class
# and then modified post-generation to sub-class IDataRequest.
#
#     SOFTWARE HISTORY
#
#    Date            Ticket#       Engineer       Description
#    ------------    ----------    -----------    --------------------------
#    05/28/13         2023         dgilling       Initial Creation.
#
#


from awips.dataaccess import IDataRequest

from dynamicserialize.dstypes.com.vividsolutions.jts.geom import Envelope
from dynamicserialize.dstypes.com.raytheon.uf.common.dataplugin.level import Level


class DefaultDataRequest(IDataRequest):

    def __init__(self):
        self.datatype = None
        self.identifiers = {}
        self.parameters = []
        self.levels = []
        self.locationNames = []
        self.envelope = None

    def setDatatype(self, datatype):
        self.datatype = str(datatype)

    def addIdentifier(self, key, value):
        self.identifiers[key] = value

    def removeIdentifier(self, key):
        del self.identifiers[key]

    def setParameters(self, *params):
        self.parameters = list(map(str, params))

    def setLevels(self, *levels):
        self.levels = list(map(self.__makeLevel, levels))

    def __makeLevel(self, level):
        if type(level) is Level:
            return level
        elif type(level) is str:
            return Level(level)
        else:
            raise TypeError("Invalid object type specified for level.")

    def setEnvelope(self, env):
        self.envelope = Envelope(env.envelope)

    def setLocationNames(self, *locationNames):
        self.locationNames = list(map(str, locationNames))

    def getDatatype(self):
        return self.datatype

    def getIdentifiers(self):
        return self.identifiers

    def getParameters(self):
        return self.parameters

    def getLevels(self):
        return self.levels

    def getEnvelope(self):
        return self.envelope

    def getLocationNames(self):
        return self.locationNames
