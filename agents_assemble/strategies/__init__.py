"""Trading strategy personas: generic, famous investors, themes, recession."""
from agents_assemble.strategies.generic import (
    BasePersona, PersonaConfig, ALL_PERSONAS,
    get_persona, list_personas,
    BuffettValue, MomentumTrader, MemeStockTrader, DividendInvestor,
    QuantStrategist, FixedIncomeStrat, GrowthInvestor,
    SectorRotation, PairsTrader, EnsembleStrategist,
)
from agents_assemble.strategies.famous import (
    FAMOUS_INVESTORS, get_famous_investor, list_famous_investors,
    PeterLynch, RayDalio, GeorgeSoros, MichaelBurry, JimSimons, CarlIcahn,
    MasayoshiSon, LiKaShing, NassefSawiris, JorgePauloLemann,
    PrinceAlwaleed, HowardMarks, SupportResistanceCommodity,
)
from agents_assemble.strategies.themes import (
    THEME_STRATEGIES, get_theme_strategy, list_theme_strategies,
    AIRevolution, CleanEnergy, DefenseAerospace, BiotechBreakout,
    ChinaTechRebound, LatAmGrowth, InfrastructureBoom, SmallCapValue,
    CryptoEcosystem, AgingPopulation,
)
from agents_assemble.strategies.recession import (
    RECESSION_STRATEGIES, get_recession_strategy,
    detect_recession_regime,
    RecessionDetector, TreasurySafe, DefensiveRotation, GoldBug,
)
