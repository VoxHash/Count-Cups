"""Dashboard screen for Count-Cups."""

from datetime import date

from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.core.db import Database
from app.core.logging import get_logger

logger = get_logger(__name__)


class DashboardScreen(QWidget):
    """Dashboard screen showing daily statistics and quick actions."""

    # Signals
    sip_detected = pyqtSignal(float)  # Emitted when sip is detected

    def __init__(self, database: Database | None, parent=None):
        """Initialize dashboard screen.

        Args:
            database: Database instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.database = database
        self.parent_window = parent

        self._init_ui()
        self._init_timer()

        # Load initial data
        self.refresh_data()

    def _init_ui(self) -> None:
        """Initialize UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)

        # Header section
        header_layout = QHBoxLayout()

        # Title
        title = QLabel("Hydration Dashboard")
        title.setProperty("class", "title")
        title.setStyleSheet(
            "font-size: 28px; font-weight: bold; color: #ffffff; margin-bottom: 8px;"
        )
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Quick actions
        quick_actions = QHBoxLayout()
        quick_actions.setSpacing(12)

        self.add_sip_btn = QPushButton("+ Add Sip")
        self.add_sip_btn.setProperty("class", "button-primary")
        self.add_sip_btn.clicked.connect(self._add_sip)
        quick_actions.addWidget(self.add_sip_btn)

        self.add_cup_btn = QPushButton("+ Add Cup")
        self.add_cup_btn.setProperty("class", "button-primary")
        self.add_cup_btn.clicked.connect(self._add_cup)
        quick_actions.addWidget(self.add_cup_btn)

        header_layout.addLayout(quick_actions)
        layout.addLayout(header_layout)

        # Stats grid with modern cards
        stats_layout = QGridLayout()
        stats_layout.setSpacing(16)

        # Today's Progress Card
        progress_card = self._create_card(
            "Today's Progress", "Track your daily hydration goal"
        )
        # Get the layout from the card (it already has one)
        progress_layout = progress_card.layout()

        # Progress bar
        self.goal_progress = QProgressBar()
        self.goal_progress.setRange(0, 100)
        self.goal_progress.setValue(0)
        self.goal_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #404040;
                border-radius: 8px;
                text-align: center;
                font-weight: bold;
                height: 24px;
                background-color: #2a2a2a;
            }
            QProgressBar::chunk {
                background-color: #3b82f6;
                border-radius: 6px;
            }
        """)
        progress_layout.addWidget(self.goal_progress)

        self.goal_label = QLabel("0% of daily goal")
        self.goal_label.setStyleSheet(
            "color: #d0d0d0; font-size: 14px; margin-top: 8px;"
        )
        progress_layout.addWidget(self.goal_label)

        stats_layout.addWidget(progress_card, 0, 0)

        # Today's Stats Card
        stats_card = self._create_card("Today's Stats", "Your hydration summary")
        # Get the layout from the card and add a grid layout to it
        card_layout = stats_card.layout()
        stats_card_layout = QGridLayout()
        card_layout.addLayout(stats_card_layout)

        # ML consumed
        ml_label = QLabel("ML Consumed")
        ml_label.setStyleSheet("color: #d0d0d0; font-size: 12px;")
        stats_card_layout.addWidget(ml_label, 0, 0)

        self.today_ml_label = QLabel("0 ml")
        self.today_ml_label.setStyleSheet(
            "color: #ffffff; font-size: 24px; font-weight: bold;"
        )
        stats_card_layout.addWidget(self.today_ml_label, 1, 0)

        # Cups consumed
        cups_label = QLabel("Cups Consumed")
        cups_label.setStyleSheet("color: #d0d0d0; font-size: 12px;")
        stats_card_layout.addWidget(cups_label, 0, 1)

        self.today_cups_label = QLabel("0.0 cups")
        self.today_cups_label.setStyleSheet(
            "color: #ffffff; font-size: 24px; font-weight: bold;"
        )
        stats_card_layout.addWidget(self.today_cups_label, 1, 1)

        # Sips taken
        sips_label = QLabel("Sips Taken")
        sips_label.setStyleSheet("color: #d0d0d0; font-size: 12px;")
        stats_card_layout.addWidget(sips_label, 0, 2)

        self.today_sips_label = QLabel("0 sips")
        self.today_sips_label.setStyleSheet(
            "color: #ffffff; font-size: 24px; font-weight: bold;"
        )
        stats_card_layout.addWidget(self.today_sips_label, 1, 2)

        stats_layout.addWidget(stats_card, 0, 1)

        layout.addLayout(stats_layout)

    def _create_card(self, title: str, subtitle: str) -> QFrame:
        """Create a modern card widget.

        Args:
            title: Card title
            subtitle: Card subtitle

        Returns:
            QFrame configured as a card
        """
        card = QFrame()
        card.setProperty("class", "card")
        card.setStyleSheet("""
            QFrame.card {
                background-color: #1e1e1e;
                border: 1px solid #333333;
                border-radius: 8px;
                padding: 16px;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #ffffff; font-size: 18px; font-weight: bold;")
        layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("color: #d0d0d0; font-size: 12px;")
        layout.addWidget(subtitle_label)

        return card

        # Recent activity section
        activity_card = self._create_card(
            "Recent Activity", "Your latest hydration events"
        )
        # Get the layout from the card
        activity_layout = activity_card.layout()

        self.activity_list = QScrollArea()
        self.activity_list.setWidgetResizable(True)
        self.activity_list.setMaximumHeight(200)
        self.activity_list.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)

        self.activity_widget = QWidget()
        self.activity_layout = QVBoxLayout(self.activity_widget)
        self.activity_layout.setContentsMargins(0, 0, 0, 0)
        self.activity_list.setWidget(self.activity_widget)

        activity_layout.addWidget(self.activity_list)
        layout.addWidget(activity_card)

        # Initialize activity list
        self.activity_list = QLabel("No recent activity")
        self.activity_list.setStyleSheet(
            "color: #d0d0d0; font-size: 14px; padding: 8px;"
        )
        self.activity_list.setWordWrap(True)
        self.activity_layout.addWidget(self.activity_list)

    def _init_timer(self) -> None:
        """Initialize refresh timer."""
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_data)
        self.refresh_timer.start(30000)  # Refresh every 30 seconds

    def refresh_data(self) -> None:
        """Refresh dashboard data."""
        if not self.database or not self.database.ensure_connection():
            logger.warning("Database not available for refresh")
            return

        try:
            # Get today's stats
            today = date.today()
            daily_stats = self.database.get_daily_stats(today)

            # Update labels
            self.today_ml_label.setText(f"{daily_stats.total_ml:.0f} ml")
            self.today_cups_label.setText(f"{daily_stats.total_cups:.1f} cups")
            self.today_sips_label.setText(f"{daily_stats.total_sips} sips")

            # Update progress bar
            self.goal_progress.setValue(int(daily_stats.progress_percentage))
            self.goal_label.setText(
                f"{daily_stats.progress_percentage:.0f}% of daily goal"
            )

            # Update recent activity
            self._update_activity_list(daily_stats.events)

        except Exception as e:
            logger.error(f"Failed to refresh dashboard data: {e}")

    def _update_activity_list(self, events) -> None:
        """Update the recent activity list.

        Args:
            events: List of recent sip events
        """
        if not hasattr(self, "activity_layout"):
            return

        # Clear existing activity items
        for i in reversed(range(self.activity_layout.count())):
            child = self.activity_layout.itemAt(i).widget()
            if child:
                child.setParent(None)

        if not events:
            no_activity = QLabel("No recent activity")
            no_activity.setStyleSheet("color: #d0d0d0; font-size: 14px; padding: 8px;")
            self.activity_layout.addWidget(no_activity)
            return

        # Add recent events
        for event in events[-5:]:  # Show last 5 events
            event_text = (
                f"{event.timestamp.strftime('%H:%M')} - {event.ml_estimate:.0f}ml sip"
            )
            event_label = QLabel(event_text)
            event_label.setStyleSheet(
                "color: #ffffff; font-size: 12px; padding: 4px; background-color: #2a2a2a; border-radius: 4px; margin: 2px;"
            )
            self.activity_layout.addWidget(event_label)

    def _add_sip(self) -> None:
        """Add a sip manually."""
        if self.database:
            # Create manual sip event
            from datetime import datetime

            from app.core.models import EventSource, SipEvent

            sip_event = SipEvent(
                timestamp=datetime.now(),
                profile_id=1,  # Default profile
                ml_estimate=20.0,  # 20ml per sip
                source=EventSource.MANUAL,
                confidence=1.0,
            )

            try:
                self.database.create_sip_event(sip_event)
                self.refresh_data()
                self.sip_detected.emit(20.0)
                logger.info("Manual sip added: 20ml")
            except Exception as e:
                logger.error(f"Failed to add manual sip: {e}")

    def _add_cup(self) -> None:
        """Add a cup manually."""
        if self.database:
            # Create manual sip event
            from datetime import datetime

            from app.core.models import EventSource, SipEvent

            sip_event = SipEvent(
                timestamp=datetime.now(),
                profile_id=1,  # Default profile
                ml_estimate=250.0,  # 250ml per cup
                source=EventSource.MANUAL,
                confidence=1.0,
            )

            try:
                self.database.create_sip_event(sip_event)
                self.refresh_data()
                self.sip_detected.emit(250.0)
                logger.info("Manual cup added: 250ml")
            except Exception as e:
                logger.error(f"Failed to add manual cup: {e}")

    def _reset_today(self) -> None:
        """Reset today's statistics."""
        from PyQt6.QtWidgets import QMessageBox

        reply = QMessageBox.question(
            self,
            "Reset Today",
            "Are you sure you want to reset today's statistics? This action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            # This would reset today's stats in a real implementation
            self.refresh_data()
            logger.info("Today's statistics reset")

    def cleanup(self) -> None:
        """Clean up resources."""
        if hasattr(self, "refresh_timer"):
            self.refresh_timer.stop()
