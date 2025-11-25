"""History screen for Count-Cups."""

from datetime import timedelta
from typing import Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTableWidget, QTableWidgetItem, QHeaderView, QDateEdit, QComboBox
)
from PyQt6.QtCore import QDate

from app.core.db import Database
from app.core.logging import get_logger

logger = get_logger(__name__)


class HistoryScreen(QWidget):
    """History screen showing past water intake data."""
    
    def __init__(self, database: Optional[Database], parent=None):
        """Initialize history screen.
        
        Args:
            database: Database instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.database = database
        self.parent_window = parent
        
        self._init_ui()
        self._load_data()
    
    def _init_ui(self) -> None:
        """Initialize UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("History")
        title.setProperty("class", "title")
        layout.addWidget(title)
        
        # Filters
        filters_layout = QHBoxLayout()
        
        filters_layout.addWidget(QLabel("From:"))
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        self.start_date.dateChanged.connect(self._load_data)
        filters_layout.addWidget(self.start_date)
        
        filters_layout.addWidget(QLabel("To:"))
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.dateChanged.connect(self._load_data)
        filters_layout.addWidget(self.end_date)
        
        self.period_combo = QComboBox()
        self.period_combo.addItems(["Last 7 days", "Last 30 days", "Last 90 days", "Custom"])
        self.period_combo.currentTextChanged.connect(self._on_period_changed)
        filters_layout.addWidget(self.period_combo)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self._load_data)
        filters_layout.addWidget(self.refresh_btn)
        
        filters_layout.addStretch()
        layout.addLayout(filters_layout)
        
        # Data table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Date", "Total ML", "Total Cups", "Total Sips", "Goal ML", "Achieved"
        ])
        
        # Set table properties
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        layout.addWidget(self.table)
        
        # Summary
        self.summary_label = QLabel("No data available")
        self.summary_label.setProperty("class", "secondary")
        layout.addWidget(self.summary_label)
    
    def _on_period_changed(self, period: str) -> None:
        """Handle period selection change.
        
        Args:
            period: Selected period
        """
        today = QDate.currentDate()
        
        if period == "Last 7 days":
            self.start_date.setDate(today.addDays(-7))
            self.end_date.setDate(today)
        elif period == "Last 30 days":
            self.start_date.setDate(today.addDays(-30))
            self.end_date.setDate(today)
        elif period == "Last 90 days":
            self.start_date.setDate(today.addDays(-90))
            self.end_date.setDate(today)
        # Custom period - don't change dates
    
    def _load_data(self) -> None:
        """Load historical data."""
        if not self.database:
            return
        
        try:
            start_date = self.start_date.date().toPyDate()
            end_date = self.end_date.date().toPyDate()
            
            # Get daily stats for the period
            daily_stats = []
            current_date = start_date
            
            while current_date <= end_date:
                stats = self.database.get_daily_stats(current_date)
                daily_stats.append(stats)
                current_date += timedelta(days=1)
            
            # Populate table
            self.table.setRowCount(len(daily_stats))
            
            for row, stats in enumerate(daily_stats):
                self.table.setItem(row, 0, QTableWidgetItem(stats.date.strftime("%Y-%m-%d")))
                self.table.setItem(row, 1, QTableWidgetItem(f"{stats.total_ml:.0f}"))
                self.table.setItem(row, 2, QTableWidgetItem(f"{stats.total_cups:.1f}"))
                self.table.setItem(row, 3, QTableWidgetItem(str(stats.total_sips)))
                self.table.setItem(row, 4, QTableWidgetItem(f"{stats.goal_ml}"))
                self.table.setItem(row, 5, QTableWidgetItem("Yes" if stats.goal_achieved else "No"))
            
            # Update summary
            self._update_summary(daily_stats)
            
        except Exception as e:
            logger.error(f"Failed to load historical data: {e}")
            self.summary_label.setText(f"Error loading data: {e}")
    
    def _update_summary(self, daily_stats) -> None:
        """Update summary statistics.
        
        Args:
            daily_stats: List of daily statistics
        """
        if not daily_stats:
            self.summary_label.setText("No data available")
            return
        
        total_ml = sum(stats.total_ml for stats in daily_stats)
        total_cups = sum(stats.total_cups for stats in daily_stats)
        total_sips = sum(stats.total_sips for stats in daily_stats)
        goal_achieved_days = sum(1 for stats in daily_stats if stats.goal_achieved)
        
        avg_daily_ml = total_ml / len(daily_stats)
        goal_achievement_rate = (goal_achieved_days / len(daily_stats)) * 100
        
        summary_text = (
            f"Period Summary: {total_ml:.0f}ml total, {total_cups:.1f} cups, {total_sips} sips | "
            f"Average: {avg_daily_ml:.0f}ml/day | "
            f"Goal Achievement: {goal_achievement_rate:.0f}%"
        )
        
        self.summary_label.setText(summary_text)
    
    def refresh_data(self) -> None:
        """Refresh data (called from parent)."""
        self._load_data()
