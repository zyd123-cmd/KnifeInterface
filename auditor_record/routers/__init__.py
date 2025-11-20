from .replenish_record_router import router as replenish_record_router
from .lend_record_router import router as lend_record_router
from .storage_record_router import router as storage_record_router
from .alarm_router import router as alarm_router

__all__ = ['replenish_record_router', 'lend_record_router', 'storage_record_router', 'alarm_router']