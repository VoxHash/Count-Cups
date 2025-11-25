"""Sip detection logic and aggregation."""

import time
from datetime import datetime, timedelta

from app.core.logging import get_logger
from app.core.models import CupProfile, DetectionResult, EventSource, SipEvent

logger = get_logger(__name__)


class SipAggregator:
    """Aggregates detection results into sip events."""

    def __init__(
        self,
        sip_duration_min: float = 0.8,
        sip_duration_max: float = 3.5,
        cooldown_duration: float = 1.0,
        confidence_threshold: float = 0.5,
    ):
        """Initialize sip aggregator.

        Args:
            sip_duration_min: Minimum duration for a valid sip (seconds)
            sip_duration_max: Maximum duration for a valid sip (seconds)
            cooldown_duration: Cooldown period between sips (seconds)
            confidence_threshold: Minimum confidence for sip detection
        """
        self.sip_duration_min = sip_duration_min
        self.sip_duration_max = sip_duration_max
        self.cooldown_duration = cooldown_duration
        self.confidence_threshold = confidence_threshold

        # State tracking
        self.sip_start_time: float | None = None
        self.sip_detections: list[DetectionResult] = []
        self.last_sip_time: float = 0.0
        self.is_sip_in_progress = False

    def process_detection(self, detection: DetectionResult) -> SipEvent | None:
        """Process a detection result and return a sip event if complete.

        Args:
            detection: Detection result from detection engine

        Returns:
            SipEvent if sip is complete, None otherwise
        """
        current_time = time.time()

        # Check cooldown period
        if current_time - self.last_sip_time < self.cooldown_duration:
            return None

        # Check confidence threshold
        if detection.confidence < self.confidence_threshold:
            return None

        if detection.has_sip:
            if not self.is_sip_in_progress:
                # Start new sip
                self.sip_start_time = current_time
                self.sip_detections = [detection]
                self.is_sip_in_progress = True
                logger.debug("Sip detection started")
            else:
                # Continue existing sip
                self.sip_detections.append(detection)
        else:
            # No sip detected, check if we should complete current sip
            if self.is_sip_in_progress:
                return self._complete_sip()

        # Check if sip duration exceeds maximum
        if self.is_sip_in_progress and self.sip_start_time:
            sip_duration = current_time - self.sip_start_time
            if sip_duration > self.sip_duration_max:
                return self._complete_sip()

        return None

    def _complete_sip(self) -> SipEvent | None:
        """Complete current sip and return SipEvent."""
        if not self.is_sip_in_progress or not self.sip_start_time:
            return None

        current_time = time.time()
        sip_duration = current_time - self.sip_start_time

        # Check if sip duration is sufficient
        if sip_duration < self.sip_duration_min:
            logger.debug(f"Sip duration too short: {sip_duration:.2f}s")
            self._reset_sip()
            return None

        # Calculate average confidence and other metrics
        avg_confidence = sum(d.confidence for d in self.sip_detections) / len(
            self.sip_detections
        )
        avg_head_tilt = sum(
            d.head_tilt_angle for d in self.sip_detections if d.head_tilt_angle
        ) / len(self.sip_detections)
        avg_hand_distance = sum(
            d.hand_face_distance for d in self.sip_detections if d.hand_face_distance
        ) / len(self.sip_detections)

        # Create sip event
        sip_event = SipEvent(
            timestamp=datetime.fromtimestamp(self.sip_start_time),
            profile_id=1,  # Default profile, will be updated by caller
            ml_estimate=self._estimate_ml_from_detection(avg_confidence, sip_duration),
            source=EventSource.AUTO,
            confidence=avg_confidence,
            detection_data={
                "duration": sip_duration,
                "detection_count": len(self.sip_detections),
                "avg_head_tilt": avg_head_tilt,
                "avg_hand_distance": avg_hand_distance,
                "detections": [
                    {
                        "timestamp": d.timestamp.isoformat(),
                        "confidence": d.confidence,
                        "head_tilt": d.head_tilt_angle,
                        "hand_distance": d.hand_face_distance,
                    }
                    for d in self.sip_detections
                ],
            },
        )

        # Update state
        self.last_sip_time = current_time
        self._reset_sip()

        logger.info(
            f"Sip event created: {sip_event.ml_estimate:.1f}ml, confidence: {avg_confidence:.2f}"
        )
        return sip_event

    def _reset_sip(self) -> None:
        """Reset sip tracking state."""
        self.sip_start_time = None
        self.sip_detections = []
        self.is_sip_in_progress = False

    def _estimate_ml_from_detection(self, confidence: float, duration: float) -> float:
        """Estimate milliliters from detection parameters.

        Args:
            confidence: Detection confidence (0-1)
            duration: Sip duration in seconds

        Returns:
            Estimated milliliters
        """
        # Base estimation: 15-25ml per sip
        base_ml = 20.0

        # Adjust based on confidence
        confidence_factor = 0.5 + (confidence * 0.5)  # 0.5 to 1.0

        # Adjust based on duration
        duration_factor = min(1.5, max(0.5, duration / 2.0))  # 0.5 to 1.5

        estimated_ml = base_ml * confidence_factor * duration_factor

        return round(estimated_ml, 1)

    def reset(self) -> None:
        """Reset all state."""
        self._reset_sip()
        self.last_sip_time = 0.0


class CupConverter:
    """Converts sips to cups using cup profiles."""

    def __init__(self, default_profile: CupProfile | None = None):
        """Initialize cup converter.

        Args:
            default_profile: Default cup profile to use
        """
        self.default_profile = default_profile or CupProfile(
            name="Default", size_ml=250, sips_per_cup=10, is_default=True
        )

    def sips_to_cups(self, sips: int, profile: CupProfile | None = None) -> float:
        """Convert number of sips to cups.

        Args:
            sips: Number of sips
            profile: Cup profile to use (defaults to default profile)

        Returns:
            Number of cups
        """
        profile = profile or self.default_profile
        return sips / profile.sips_per_cup

    def ml_to_cups(self, ml: float, profile: CupProfile | None = None) -> float:
        """Convert milliliters to cups.

        Args:
            ml: Milliliters
            profile: Cup profile to use (defaults to default profile)

        Returns:
            Number of cups
        """
        profile = profile or self.default_profile
        return ml / profile.size_ml

    def cups_to_ml(self, cups: float, profile: CupProfile | None = None) -> float:
        """Convert cups to milliliters.

        Args:
            cups: Number of cups
            profile: Cup profile to use (defaults to default profile)

        Returns:
            Milliliters
        """
        profile = profile or self.default_profile
        return cups * profile.size_ml

    def estimate_sip_ml(
        self, sip_event: SipEvent, profile: CupProfile | None = None
    ) -> float:
        """Estimate milliliters for a sip event.

        Args:
            sip_event: Sip event
            profile: Cup profile to use (defaults to default profile)

        Returns:
            Estimated milliliters
        """
        profile = profile or self.default_profile

        # Use detection-based estimate if available
        if sip_event.ml_estimate > 0:
            return sip_event.ml_estimate

        # Fallback to profile-based estimate
        return profile.size_ml / profile.sips_per_cup


class SipTracker:
    """Main sip tracking coordinator."""

    def __init__(
        self,
        sip_aggregator: SipAggregator | None = None,
        cup_converter: CupConverter | None = None,
    ):
        """Initialize sip tracker.

        Args:
            sip_aggregator: Sip aggregator instance
            cup_converter: Cup converter instance
        """
        self.sip_aggregator = sip_aggregator or SipAggregator()
        self.cup_converter = cup_converter or CupConverter()

        # Statistics
        self.total_sips_today = 0
        self.total_ml_today = 0.0
        self.sip_events_today: list[SipEvent] = []

        # Daily reset tracking
        self.last_reset_date = datetime.now().date()

    def process_detection(
        self, detection: DetectionResult, profile: CupProfile | None = None
    ) -> SipEvent | None:
        """Process detection and return sip event if complete.

        Args:
            detection: Detection result
            profile: Cup profile to use for conversion

        Returns:
            SipEvent if sip is complete, None otherwise
        """
        # Check for daily reset
        self._check_daily_reset()

        # Process detection
        sip_event = self.sip_aggregator.process_detection(detection)

        if sip_event:
            # Update profile ID if provided
            if profile:
                sip_event.profile_id = profile.id or 1

            # Estimate ML if not set
            if sip_event.ml_estimate <= 0:
                sip_event.ml_estimate = self.cup_converter.estimate_sip_ml(
                    sip_event, profile
                )

            # Update statistics
            self.total_sips_today += 1
            self.total_ml_today += sip_event.ml_estimate
            self.sip_events_today.append(sip_event)

            logger.info(
                f"Sip tracked: {sip_event.ml_estimate:.1f}ml (Total today: {self.total_ml_today:.1f}ml)"
            )

        return sip_event

    def add_manual_sip(self, ml: float, profile: CupProfile | None = None) -> SipEvent:
        """Add a manual sip event.

        Args:
            ml: Milliliters to add
            profile: Cup profile to use

        Returns:
            Created sip event
        """
        # Check for daily reset
        self._check_daily_reset()

        # Create manual sip event
        sip_event = SipEvent(
            timestamp=datetime.now(),
            profile_id=profile.id if profile else 1,
            ml_estimate=ml,
            source=EventSource.MANUAL,
            confidence=1.0,
            detection_data={"manual": True},
        )

        # Update statistics
        self.total_sips_today += 1
        self.total_ml_today += ml
        self.sip_events_today.append(sip_event)

        logger.info(
            f"Manual sip added: {ml:.1f}ml (Total today: {self.total_ml_today:.1f}ml)"
        )
        return sip_event

    def get_daily_stats(self) -> dict:
        """Get daily statistics.

        Returns:
            Dictionary with daily statistics
        """
        self._check_daily_reset()

        total_cups = self.cup_converter.ml_to_cups(self.total_ml_today)

        return {
            "date": self.last_reset_date,
            "total_sips": self.total_sips_today,
            "total_ml": self.total_ml_today,
            "total_cups": total_cups,
            "sip_events": self.sip_events_today.copy(),
        }

    def _check_daily_reset(self) -> None:
        """Check if daily reset is needed."""
        current_date = datetime.now().date()

        if current_date > self.last_reset_date:
            # Reset daily statistics
            self.total_sips_today = 0
            self.total_ml_today = 0.0
            self.sip_events_today = []
            self.last_reset_date = current_date

            logger.info("Daily statistics reset")

    def reset_daily_stats(self) -> None:
        """Manually reset daily statistics."""
        self.total_sips_today = 0
        self.total_ml_today = 0.0
        self.sip_events_today = []
        self.last_reset_date = datetime.now().date()

        logger.info("Daily statistics manually reset")

    def get_sip_rate(self, window_minutes: int = 60) -> float:
        """Get sip rate (sips per hour) for the specified window.

        Args:
            window_minutes: Time window in minutes

        Returns:
            Sips per hour
        """
        if not self.sip_events_today:
            return 0.0

        cutoff_time = datetime.now() - timedelta(minutes=window_minutes)
        recent_sips = [
            event for event in self.sip_events_today if event.timestamp >= cutoff_time
        ]

        if not recent_sips:
            return 0.0

        time_span_hours = window_minutes / 60.0
        return len(recent_sips) / time_span_hours
