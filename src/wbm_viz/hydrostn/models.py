from .models_abstract import *


# Argentina
class ArgentinaHydrostn30Subbasin(Hydrostn30Subbasin):
    country = 'argentina'
    #class Meta(Hydrostn30Subbasin.Meta):
        #app_label = 'argentina'

class ArgentinaHydrostn30Streamline(Hydrostn30Streamline):
    country ='argentina'
    #class Meta(Hydrostn30Streamline.Meta):
        #app_label = 'argentina'

class ArgentinaCatchmentBasins(CatchmentBasins):
    country ='argentina'
    #class Meta(CatchmentBasins.Meta):
        #app_label = 'argentina'

class ArgentinaCatchmentStatsAirTemperature(CatchmentStatsAirTemperature):
    country ='argentina'
    #class Meta(CatchmentStatsAirTemperature.Meta):
        #app_label = 'argentina'

class ArgentinaCatchmentStatsEvapotranspiration(CatchmentStatsEvapotranspiration):
    country ='argentina'
    #class Meta(CatchmentStatsEvapotranspiration.Meta):
        #app_label = 'argentina'

class ArgentinaCatchmentStatsPrecipitation(CatchmentStatsPrecipitation):
    country ='argentina'
    #class Meta(CatchmentStatsPrecipitation.Meta):
        #app_label = 'argentina'

class ArgentinaCatchmentStatsRunoff(CatchmentStatsRunoff):
    country ='argentina'
    #class Meta(CatchmentStatsRunoff.Meta):
        #app_label = 'argentina'

class ArgentinaCatchmentStatsSoilMoisture(CatchmentStatsSoilMoisture):
    country ='argentina'
    #class Meta(CatchmentStatsSoilMoisture.Meta):
        #app_label = 'argentina'

class ArgentinaConfluenceDischargeMonthly(ConfluenceDischargeMonthly):
    country ='argentina'
    #class Meta(ConfluenceDischargeMonthly.Meta):
        #app_label = 'argentina'

class ArgentinaSubbasinAirTemperatureMonthly(SubbasinAirTemperatureMonthly):
    country ='argentina'
    #class Meta(SubbasinAirTemperatureMonthly.Meta):
        #app_label = 'argentina'

class ArgentinaSubbasinEvapotranspirationMonthly(SubbasinEvapotranspirationMonthly):
    country ='argentina'
    #class Meta(SubbasinEvapotranspirationMonthly.Meta):
        #app_label = 'argentina'

class ArgentinaSubbasinPrecipitationMonthly(SubbasinPrecipitationMonthly):
    country ='argentina'
    #class Meta(SubbasinPrecipitationMonthly.Meta):
        #app_label = 'argentina'

class ArgentinaSubbasinRunoffMonthly(SubbasinRunoffMonthly):
    country ='argentina'
    #class Meta(SubbasinRunoffMonthly.Meta):
        #app_label = 'argentina'

class ArgentinaSubbasinSoilMoistureMonthly(SubbasinSoilMoistureMonthly):
    country ='argentina'
    #class Meta(SubbasinSoilMoistureMonthly.Meta):
        #app_label = 'argentina'

#Peru
class PeruHydrostn30Subbasin(Hydrostn30Subbasin):
    country='peru'
    #class Meta(Hydrostn30Subbasin.Meta):
     #   app_label = 'peru'

class PeruHydrostn30Streamline(Hydrostn30Streamline):
    country='peru'
    #class Meta(Hydrostn30Streamline.Meta):
     #   app_label = 'peru'

class PeruCatchmentBasins(CatchmentBasins):
    country='peru'
    #class Meta(CatchmentBasins.Meta):
     #   app_label = 'peru'

class PeruCatchmentStatsAirTemperature(CatchmentStatsAirTemperature):
    country='peru'
    #class Meta(CatchmentStatsAirTemperature.Meta):
        #app_label = 'peru'

class PeruCatchmentStatsEvapotranspiration(CatchmentStatsEvapotranspiration):
    country='peru'
    #class Meta(CatchmentStatsEvapotranspiration.Meta):
        #app_label = 'peru'

class PeruCatchmentStatsPrecipitation(CatchmentStatsPrecipitation):
    country='peru'
    #class Meta(CatchmentStatsPrecipitation.Meta):
        #app_label = 'peru'

class PeruCatchmentStatsRunoff(CatchmentStatsRunoff):
    country='peru'
    #class Meta(CatchmentStatsRunoff.Meta):
        #app_label = 'peru'

class PeruCatchmentStatsSoilMoisture(CatchmentStatsSoilMoisture):
    country='peru'
    #class Meta(CatchmentStatsSoilMoisture.Meta):
        #app_label = 'peru'

class PeruConfluenceDischargeMonthly(ConfluenceDischargeMonthly):
    country='peru'
    #class Meta(ConfluenceDischargeMonthly.Meta):
        #app_label = 'peru'

class PeruSubbasinAirTemperatureMonthly(SubbasinAirTemperatureMonthly):
    country='peru'
    #class Meta(SubbasinAirTemperatureMonthly.Meta):
        #app_label = 'peru'

class PeruSubbasinEvapotranspirationMonthly(SubbasinEvapotranspirationMonthly):
    country='peru'
    #class Meta(SubbasinEvapotranspirationMonthly.Meta):
        #app_label = 'peru'

class PeruSubbasinPrecipitationMonthly(SubbasinPrecipitationMonthly):
    country='peru'
    #class Meta(SubbasinPrecipitationMonthly.Meta):
        #app_label = 'peru'

class PeruSubbasinRunoffMonthly(SubbasinRunoffMonthly):
    country='peru'
    #class Meta(SubbasinRunoffMonthly.Meta):
        #app_label = 'peru'

class PeruSubbasinSoilMoistureMonthly(SubbasinSoilMoistureMonthly):
    country='peru'
    #class Meta(SubbasinSoilMoistureMonthly.Meta):
        #app_label = 'peru'

# CONSTANTS FOR IMPORT
SUBBASIN = {'argentina': ArgentinaHydrostn30Subbasin, 'peru': PeruHydrostn30Subbasin}
STREAMLINE = {'argentina': ArgentinaHydrostn30Streamline, 'peru': PeruHydrostn30Streamline}
CATCHMENT_BASINS = {'argentina': ArgentinaCatchmentBasins, 'peru': PeruCatchmentBasins}
DISCHARGE = {'argentina': ArgentinaConfluenceDischargeMonthly, 'peru': PeruConfluenceDischargeMonthly}
CATCHMENT_STATS_EVAP = {'argentina': ArgentinaCatchmentStatsEvapotranspiration,
                        'peru': PeruCatchmentStatsEvapotranspiration}
CATCHMENT_STATS_RUNOFF = {'argentina': ArgentinaCatchmentStatsRunoff, 'peru': PeruCatchmentStatsRunoff}
CATCHMENT_STATS_PRECIP = {'argentina': ArgentinaCatchmentStatsPrecipitation, 'peru': PeruCatchmentStatsPrecipitation}
CATCHMENT_STATS_SOIL = {'argentina': ArgentinaCatchmentStatsSoilMoisture, 'peru': PeruCatchmentStatsSoilMoisture}
CATCHMENT_STATS_AIR = {'argentina': ArgentinaCatchmentStatsAirTemperature, 'peru': PeruCatchmentStatsAirTemperature}
SUBBASIN_STATS_EVAP = {'argentina': ArgentinaSubbasinEvapotranspirationMonthly,
                       'peru': PeruSubbasinEvapotranspirationMonthly}
SUBBASIN_STATS_RUNOFF = {'argentina': ArgentinaSubbasinRunoffMonthly, 'peru': PeruSubbasinRunoffMonthly}
SUBBASIN_STATS_PRECIP = {'argentina': ArgentinaSubbasinPrecipitationMonthly, 'peru': PeruSubbasinPrecipitationMonthly}
SUBBASIN_STATS_SOIL = {'argentina': ArgentinaSubbasinSoilMoistureMonthly, 'peru': PeruSubbasinSoilMoistureMonthly}
SUBBASIN_STATS_AIR = {'argentina': ArgentinaSubbasinAirTemperatureMonthly, 'peru': PeruSubbasinAirTemperatureMonthly}

UNITS = {
    'discharge': 'm<sup>3</sup>/s',
    'temp': '&#8451;',
    'evap': 'mm/month',
    'precip': 'mm/month',
    'runoff': 'mm/month',
    'soil': 'mm/month'
}