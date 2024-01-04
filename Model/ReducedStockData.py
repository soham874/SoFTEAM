from dataclasses import dataclass

@dataclass
class ReducedStockData:
    Date: str
    Open: float
    High: float
    Low: float
    Close: float
    Volume: float