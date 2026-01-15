# [SARAH_CORE_STUB]: SECURITY_SHROUD
# LOGIC: PHYSICAL_PERIMETER_ENFORCEMENT
class SecurityShroud:
    def __init__(self):
        self.PERIMETER = "7467_HAGAR_SHORE"
        self.ENCRYPTION_MODE = "OMEGA-SHARD"

    def check_location(self, current_node):
        return current_node == self.PERIMETER

shroud = SecurityShroud()
