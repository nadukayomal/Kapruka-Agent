"""
Logistics specialist: Sri Lankan district delivery feasibility.

Implemented in Phase 4.
"""

from __future__ import annotations

from typing import Any


class LogisticsSpecialist:
    """
    Checks whether a product can be delivered to a district.
    """

    def check_delivery(self, product: dict[str, Any], district: str) -> dict[str, Any]:
        """
        Assess delivery feasibility.

        Args:
            product: Catalog record.
            district: Canonical Sri Lankan district name.

        Returns:
            dict: Feasibility result with reason.

        Raises:
            NotImplementedError: Until Phase 4 is implemented.
        """
        raise NotImplementedError(
            "LogisticsSpecialist.check_delivery is implemented in Phase 4."
        )
