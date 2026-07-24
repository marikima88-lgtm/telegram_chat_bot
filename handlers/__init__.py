from .start import router as start_router
from .rates import router as rates_router
from .services import router as services_router
from .alerts import router as alerts_router
from .contacts import router as contacts_router
from .faq import router as faq_router

__all__ = [
    "start_router",
    "rates_router",
    "services_router",
    "alerts_router",
    "contacts_router",
    "faq_router",
]
