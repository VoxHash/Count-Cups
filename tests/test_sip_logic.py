"""Tests for sip logic and aggregation."""

from datetime import datetime

from app.core.models import CupProfile, DetectionResult, EventSource, SipEvent
from app.core.sip_logic import CupConverter, SipAggregator, SipTracker


class TestSipAggregator:
    """Test sip aggregator functionality."""

    def test_init(self):
        """Test sip aggregator initialization."""
        aggregator = SipAggregator()
        assert aggregator.sip_duration_min == 0.8
        assert aggregator.sip_duration_max == 3.5
        assert aggregator.cooldown_duration == 1.0
        assert aggregator.confidence_threshold == 0.5

    def test_process_detection_no_sip(self):
        """Test processing detection with no sip."""
        aggregator = SipAggregator()

        detection = DetectionResult(
            has_sip=False, confidence=0.8, head_tilt_angle=30.0, hand_face_distance=50.0
        )

        result = aggregator.process_detection(detection)
        assert result is None

    def test_process_detection_low_confidence(self):
        """Test processing detection with low confidence."""
        aggregator = SipAggregator(confidence_threshold=0.9)

        detection = DetectionResult(
            has_sip=True,
            confidence=0.5,  # Below threshold
            head_tilt_angle=30.0,
            hand_face_distance=50.0,
        )

        result = aggregator.process_detection(detection)
        assert result is None

    def test_process_detection_cooldown(self):
        """Test processing detection during cooldown."""
        aggregator = SipAggregator()

        # First detection
        detection1 = DetectionResult(
            has_sip=True, confidence=0.8, head_tilt_angle=30.0, hand_face_distance=50.0
        )

        result1 = aggregator.process_detection(detection1)
        assert result1 is None  # Not enough duration yet

        # Second detection during cooldown
        detection2 = DetectionResult(
            has_sip=True, confidence=0.8, head_tilt_angle=30.0, hand_face_distance=50.0
        )

        result2 = aggregator.process_detection(detection2)
        assert result2 is None  # Still in cooldown


class TestCupConverter:
    """Test cup converter functionality."""

    def test_init(self):
        """Test cup converter initialization."""
        converter = CupConverter()
        assert converter.default_profile.name == "Default"
        assert converter.default_profile.size_ml == 250
        assert converter.default_profile.sips_per_cup == 10

    def test_sips_to_cups(self):
        """Test converting sips to cups."""
        converter = CupConverter()

        # Test with default profile
        cups = converter.sips_to_cups(20)
        assert cups == 2.0

        # Test with custom profile
        profile = CupProfile(name="Test", size_ml=500, sips_per_cup=5)
        cups = converter.sips_to_cups(15, profile)
        assert cups == 3.0

    def test_ml_to_cups(self):
        """Test converting milliliters to cups."""
        converter = CupConverter()

        # Test with default profile
        cups = converter.ml_to_cups(500)
        assert cups == 2.0

        # Test with custom profile
        profile = CupProfile(name="Test", size_ml=200, sips_per_cup=4)
        cups = converter.ml_to_cups(600, profile)
        assert cups == 3.0

    def test_cups_to_ml(self):
        """Test converting cups to milliliters."""
        converter = CupConverter()

        # Test with default profile
        ml = converter.cups_to_ml(2.5)
        assert ml == 625.0

        # Test with custom profile
        profile = CupProfile(name="Test", size_ml=300, sips_per_cup=6)
        ml = converter.cups_to_ml(2.0, profile)
        assert ml == 600.0

    def test_estimate_sip_ml(self):
        """Test estimating sip milliliters."""
        converter = CupConverter()

        # Test with sip event that has ml_estimate
        sip_event = SipEvent(
            timestamp=datetime.now(),
            profile_id=1,
            ml_estimate=25.0,
            source=EventSource.AUTO,
        )

        ml = converter.estimate_sip_ml(sip_event)
        assert ml == 25.0

        # Test with sip event without ml_estimate
        sip_event_no_ml = SipEvent(
            timestamp=datetime.now(),
            profile_id=1,
            ml_estimate=0.0,
            source=EventSource.AUTO,
        )

        ml = converter.estimate_sip_ml(sip_event_no_ml)
        assert ml == 25.0  # Default profile: 250ml / 10 sips = 25ml


class TestSipTracker:
    """Test sip tracker functionality."""

    def test_init(self):
        """Test sip tracker initialization."""
        tracker = SipTracker()
        assert tracker.total_sips_today == 0
        assert tracker.total_ml_today == 0.0
        assert len(tracker.sip_events_today) == 0

    def test_add_manual_sip(self):
        """Test adding manual sip."""
        tracker = SipTracker()

        sip_event = tracker.add_manual_sip(50.0)

        assert sip_event.ml_estimate == 50.0
        assert sip_event.source == EventSource.MANUAL
        assert tracker.total_sips_today == 1
        assert tracker.total_ml_today == 50.0
        assert len(tracker.sip_events_today) == 1

    def test_get_daily_stats(self):
        """Test getting daily statistics."""
        tracker = SipTracker()

        # Add some sips
        tracker.add_manual_sip(20.0)
        tracker.add_manual_sip(30.0)

        stats = tracker.get_daily_stats()

        assert stats["total_sips"] == 2
        assert stats["total_ml"] == 50.0
        assert stats["total_cups"] == 0.2  # 50ml / 250ml per cup
        assert len(stats["sip_events"]) == 2

    def test_reset_daily_stats(self):
        """Test resetting daily statistics."""
        tracker = SipTracker()

        # Add some sips
        tracker.add_manual_sip(20.0)
        tracker.add_manual_sip(30.0)

        # Reset
        tracker.reset_daily_stats()

        assert tracker.total_sips_today == 0
        assert tracker.total_ml_today == 0.0
        assert len(tracker.sip_events_today) == 0

    def test_get_sip_rate(self):
        """Test getting sip rate."""
        tracker = SipTracker()

        # Add some sips
        tracker.add_manual_sip(20.0)
        tracker.add_manual_sip(30.0)

        # Get sip rate for last hour
        rate = tracker.get_sip_rate(60)
        assert rate > 0  # Should have some sips in the last hour
