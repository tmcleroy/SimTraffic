
from Config import *

class Analytics():
    
    def __init__(self):
        self.data = {   "Total Vehicles Passed":0.0, 
                        "Total Time Passed (mins)":0.0,
                        "Average Throughput (vehics/min)":0.0, 
                        "Average Trip Time":0.0,
                        "Weighted Average Trip Time":0.0,
                        "Weighted Effectiveness Metric": 0.0,
                        "Weighted Average Throughput": 0.0,
                        "Status": 'BASELINE WARMUP'
                    }

        self.averageThroughput = 0.0
        self.averageTripTime = 0.0
        self.totalTripTime = 0.0
        self.totalTimePassed = 0.0
        self.totalFramesPassed = 0
        self.totalVehiclesPassed = 0
        self.weightedTotalVehiclesPassed = 0
        self.weightedEffectivenessMetric = 0.0
        self.weightedAverageThroughput = 0.0
        self.weightedAverageTripTime = 0.0
        self.baselineWeightedEffectivenessMetric = 0.0
        self.status = 'BASELINE WARMUP'

        self.isBaselineEstablished = False
        
    def auto(self):
        self.totalFramesPassed += 1
        #gather baseline states when time elapsed is greater than warmup and less than baseline time
        if self.getTimePassed() >= BASELINE_WARMUP_TIME and self.getTimePassed() < (BASELINE_WARMUP_TIME + BASELINE_TIME):
            self.status = 'BASELINE'
            self.data["Status"] = self.status

        #establish the baseline stats and begin to gather real stats
        elif self.getTimePassed() >= (BASELINE_WARMUP_TIME + BASELINE_TIME) and self.getTimePassed() < (BASELINE_WARMUP_TIME + BASELINE_TIME + WARMUP_TIME):
            if not self.isBaselineEstablished : self.establishBaseline()
            self.status = 'WARMUP'
            self.data["Status"] = self.status

        elif self.getTimePassed() >= (BASELINE_WARMUP_TIME + BASELINE_TIME + WARMUP_TIME):
            self.status = 'RUNNING'
            self.data["Status"] = self.status



    #returns the number of minutes passed since the program was started
    def getTimePassed(self):
        return (self.totalFramesPassed/FRAMERATE)/60

    def establishBaseline(self):
        self.baselineWeightedEffectivenessMetric = self.data["Weighted Effectiveness Metric"]

        self.averageThroughput = 0.0
        self.weightedAverageThroughput = 0.0
        self.weightedEffectivenessMetric = 0.0
        self.totalVehiclesPassed = 0
        self.weightedTotalVehiclesPassed = 0
        self.totalTripTime = 0.0
        self.averageTripTime = 0.0
        self.weightedAverageTripTime = 0.0
    
        self.data["Total Vehicles Passed"] = 0.0
        self.data["Total Time Passed (mins)"] = 0.0
        self.data["Average Throughput (vehics/min)"] = 0.0
        self.data["Average Trip Time"] = 0.0
        self.data["Weighted Average Trip Time"] = 0.0
        self.data["Weighted Effectiveness Metric"] = 0.0
        self.data["Weighted Average Throughput"] = 0.0

        self.totalVehiclesPassed = 0
        self.weightedTotalVehiclesPassed = 0
        self.totalTripTime = 0
        self.averageTripTime = 0

        self.isBaselineEstablished = True

        
    def getData(self):

        self.data["Total Time Passed (mins)"] = self.getTimePassed() - BASELINE_WARMUP_TIME - BASELINE_TIME - WARMUP_TIME


        if self.status == 'BASELINE WARMUP' or self.status == 'WARMUP':

            #warmup time is not taken into account when calculating stats
            #self.totalTimePassed = self.getTimePassed() - BASELINE_WARMUP_TIME
            #self.data["Total Time Passed (mins)"] = self.totalTimePassed
            return self.data


        #update best case scenario statistics (all lights green)
        elif self.status == 'BASELINE':

            #warmup time is not taken into account when calculating stats
            self.totalTimePassed = self.getTimePassed() - BASELINE_WARMUP_TIME# - BASELINE_TIME

            if self.averageTripTime and self.totalTimePassed > 0.0:
                self.averageThroughput = self.totalVehiclesPassed/self.totalTimePassed
                self.weightedAverageThroughput = self.weightedTotalVehiclesPassed/self.totalTimePassed
                self.weightedEffectivenessMetric = self.weightedAverageThroughput/self.weightedAverageTripTime
            self.data["Total Vehicles Passed"] = self.totalVehiclesPassed
            self.data["Average Throughput (vehics/min)"] = self.averageThroughput
            self.data["Average Trip Time"] = self.averageTripTime
            self.data["Weighted Average Trip Time"] = self.weightedAverageTripTime
            self.data["Weighted Effectiveness Metric"] = self.weightedEffectivenessMetric
            self.data["Weighted Average Throughput"] = self.weightedAverageThroughput
            self.data["Status"] = self.status
            return self.data


        elif self.status == 'RUNNING':

            #warmup time is not taken into account when calculating stats
            self.totalTimePassed = self.getTimePassed() - BASELINE_WARMUP_TIME - BASELINE_TIME - WARMUP_TIME

            if self.averageTripTime and self.totalTimePassed > 0.0:
                self.averageThroughput = self.totalVehiclesPassed/self.totalTimePassed
                self.weightedAverageThroughput = self.weightedTotalVehiclesPassed/self.totalTimePassed
                self.weightedEffectivenessMetric = self.weightedAverageThroughput/self.weightedAverageTripTime
            self.data["Total Vehicles Passed"] = self.totalVehiclesPassed
            self.data["Average Throughput (vehics/min)"] = self.averageThroughput
            self.data["Average Trip Time"] = self.averageTripTime
            self.data["Weighted Average Trip Time"] = self.weightedAverageTripTime
            self.data["Weighted Effectiveness Metric"] = self.weightedEffectivenessMetric/self.baselineWeightedEffectivenessMetric
            self.data["Weighted Average Throughput"] = self.weightedAverageThroughput
            self.data["Status"] = self.status
            return self.data

        else : return self.data
        
    def vehicPassed(self, vehic):
        #don't start keeping track until warmup time has elapsed
        if not 'WARMUP' in self.status:
            self.totalVehiclesPassed += 1
            #apply scoring weights (high traffic roads may be more important than normal ones)
            if vehic.isHighTraffic():
                self.weightedTotalVehiclesPassed += 1*HT_SCORING_WEIGHT
            elif not vehic.isHighTraffic():
                self.weightedTotalVehiclesPassed += 1
            self.totalTripTime += vehic.tripTime
            self.averageTripTime = self.totalTripTime/self.totalVehiclesPassed
            self.weightedAverageTripTime = self.totalTripTime/self.weightedTotalVehiclesPassed


        