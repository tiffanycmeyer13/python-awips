#
#     SOFTWARE HISTORY
#
#    Date            Ticket#       Engineer       Description
#    ------------    ----------    -----------    --------------------------
#    05/28/13         #2023        dgilling       Initial Creation.
#    05/28/13         #5916        bsteffen       Add includeLatLonData
#
#

from dynamicserialize.dstypes.com.raytheon.uf.common.dataaccess.request import AbstractDataAccessRequest


class GetGridDataRequest(AbstractDataAccessRequest):

    def __init__(self):
        super(GetGridDataRequest, self).__init__()
        self.requestedTimes = None
        self.requestedPeriod = None
        self.includeLatLonData = True

    def getRequestedTimes(self):
        return self.requestedTimes

    def setRequestedTimes(self, requestedTimes):
        self.requestedTimes = requestedTimes

    def getRequestedPeriod(self):
        return self.requestedPeriod

    def setRequestedPeriod(self, requestedPeriod):
        self.requestedPeriod = requestedPeriod

    def getIncludeLatLonData(self):
        return self.includeLatLonData

    def setIncludeLatLonData(self, includeLatLonData):
        self.includeLatLonData = includeLatLonData
