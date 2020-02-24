from .models_abstract import *

# Argentina
class ArgentinaHydrostn30Subbasin(Hydrostn30Subbasin):
    class Meta(Hydrostn30Subbasin.Meta):
        app_label = 'argentina'

class ArgentinaHydrostn30Streamline(Hydrostn30Streamline):
    class Meta(Hydrostn30Streamline.Meta):
        app_label = 'argentina'

class ArgentinaCatchmentBasins(CatchmentBasins):
    class Meta(CatchmentBasins.Meta):
        app_label = 'argentina'

class ArgentinaCatchmentStatsAirTemperature(CatchmentStatsAirTemperature):
    class Meta(CatchmentStatsAirTemperature.Meta):
        app_label = 'argentina'

class ArgentinaCatchmentStatsEvapotranspiration(CatchmentStatsEvapotranspiration):
    class Meta(CatchmentStatsEvapotranspiration.Meta):
        app_label = 'argentina'

class ArgentinaCatchmentStatsPrecipitation(CatchmentStatsPrecipitation):
    class Meta(CatchmentStatsPrecipitation.Meta):
        app_label = 'argentina'

class ArgentinaCatchmentStatsRunoff(CatchmentStatsRunoff):
    class Meta(CatchmentStatsRunoff.Meta):
        app_label = 'argentina'

class ArgentinaCatchmentStatsSoilMoisture(CatchmentStatsSoilMoisture):
    class Meta(CatchmentStatsSoilMoisture.Meta):
        app_label = 'argentina'

class ArgentinaConfluenceDischargeMonthly(ConfluenceDischargeMonthly):
    class Meta(ConfluenceDischargeMonthly.Meta):
        app_label = 'argentina'

class ArgentinaSubbasinAirTemperatureMonthly(SubbasinAirTemperatureMonthly):
    class Meta(SubbasinAirTemperatureMonthly.Meta):
        app_label = 'argentina'

class ArgentinaSubbasinEvapotranspirationMonthly(SubbasinEvapotranspirationMonthly):
    class Meta(SubbasinEvapotranspirationMonthly.Meta):
        app_label = 'argentina'

class ArgentinaSubbasinPrecipitationMonthly(SubbasinPrecipitationMonthly):
    class Meta(SubbasinPrecipitationMonthly.Meta):
        app_label = 'argentina'

class ArgentinaSubbasinRunoffMonthly(SubbasinRunoffMonthly):
    class Meta(SubbasinRunoffMonthly.Meta):
        app_label = 'argentina'

class ArgentinaSubbasinSoilMoistureMonthly(SubbasinSoilMoistureMonthly):
    class Meta(SubbasinSoilMoistureMonthly.Meta):
        app_label = 'argentina'
