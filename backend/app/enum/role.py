from enum import Enum

class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    CARE_GIVER = "care_giver"
    USER = "user"

class RequestType(str, Enum):
    MEDICAL= "medical"
    NON_MEDICAL = "non_medical"
    EMERGENCY = "emergency" 
    
class RequestCategory(str, Enum):
    BABY_SITTING = "baby_sitting"
    ELDERLY = "elderly"
    # MENTAL = "mental"
    # category = Column(Enum('RequestCategory', values=(
    #     'physical', 'mental', 'social', 'other'), 
    #     name='request_category'), nullable=False)

class DurationType(str, Enum):
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"