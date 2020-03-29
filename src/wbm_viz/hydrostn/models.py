from .models_abstract import *

class GlobalCountries(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    recordname = models.CharField(db_column='RecordName', max_length=15, blank=True, null=True)
    gridvalue = models.IntegerField(db_column='GridValue', blank=True, null=True)
    gridarea = models.FloatField(db_column='GridArea', blank=True, null=True)
    gridpercent = models.FloatField(db_column='GridPercent', blank=True, null=True)
    adm0_code = models.IntegerField(blank=True, null=True)
    adm0_name = models.CharField(max_length=64, blank=True, null=True)
    geom = models.GeometryField(srid=0, blank=True, null=True)
    scolor = models.IntegerField(db_column='SColor', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'global_countries'

    country = 'argentina'# Arbitrarily chosen for convenience

# Argentina
class ArgentinaHydrostn30Subbasin(Hydrostn30Subbasin):
    country = 'argentina'


class ArgentinaHydrostn30Streamline(Hydrostn30Streamline):
    country = 'argentina'


class ArgentinaCatchmentBasins(CatchmentBasins):
    country = 'argentina'


class ArgentinaCatchmentStatsAirTemperature(CatchmentStatsAirTemperature):
    country = 'argentina'


class ArgentinaCatchmentStatsEvapotranspiration(CatchmentStatsEvapotranspiration):
    country = 'argentina'


class ArgentinaCatchmentStatsPrecipitation(CatchmentStatsPrecipitation):
    country = 'argentina'


class ArgentinaCatchmentStatsRunoff(CatchmentStatsRunoff):
    country = 'argentina'


class ArgentinaCatchmentStatsSoilMoisture(CatchmentStatsSoilMoisture):
    country = 'argentina'


class ArgentinaConfluenceDischargeMonthly(ConfluenceDischargeMonthly):
    country = 'argentina'


class ArgentinaSubbasinAirTemperatureMonthly(SubbasinAirTemperatureMonthly):
    country = 'argentina'


class ArgentinaSubbasinEvapotranspirationMonthly(SubbasinEvapotranspirationMonthly):
    country = 'argentina'


class ArgentinaSubbasinPrecipitationMonthly(SubbasinPrecipitationMonthly):
    country = 'argentina'


class ArgentinaSubbasinRunoffMonthly(SubbasinRunoffMonthly):
    country = 'argentina'


class ArgentinaSubbasinSoilMoistureMonthly(SubbasinSoilMoistureMonthly):
    country = 'argentina'


#### Peru ####

class PeruHydrostn30Subbasin(Hydrostn30Subbasin):
    country = 'peru'


class PeruHydrostn30Streamline(Hydrostn30Streamline):
    country = 'peru'


class PeruCatchmentBasins(CatchmentBasins):
    country = 'peru'


class PeruCatchmentStatsAirTemperature(CatchmentStatsAirTemperature):
    country = 'peru'


class PeruCatchmentStatsEvapotranspiration(CatchmentStatsEvapotranspiration):
    country = 'peru'


class PeruCatchmentStatsPrecipitation(CatchmentStatsPrecipitation):
    country = 'peru'


class PeruCatchmentStatsRunoff(CatchmentStatsRunoff):
    country = 'peru'


class PeruCatchmentStatsSoilMoisture(CatchmentStatsSoilMoisture):
    country = 'peru'


class PeruConfluenceDischargeMonthly(ConfluenceDischargeMonthly):
    country = 'peru'


class PeruSubbasinAirTemperatureMonthly(SubbasinAirTemperatureMonthly):
    country = 'peru'


class PeruSubbasinEvapotranspirationMonthly(SubbasinEvapotranspirationMonthly):
    country = 'peru'


class PeruSubbasinPrecipitationMonthly(SubbasinPrecipitationMonthly):
    country = 'peru'


class PeruSubbasinRunoffMonthly(SubbasinRunoffMonthly):
    country = 'peru'


class PeruSubbasinSoilMoistureMonthly(SubbasinSoilMoistureMonthly):
    country = 'peru'


# CONSTANTS for filtering correct models
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
