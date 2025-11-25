"""Notification service for Count-Cups."""

from typing import Optional

from app.core.logging import get_logger

logger = get_logger(__name__)


class NotificationService:
    """Handles desktop notifications."""
    
    def __init__(self):
        """Initialize notification service."""
        self.enabled = True
        self._init_notifier()
    
    def _init_notifier(self) -> None:
        """Initialize platform-specific notifier."""
        try:
            from plyer import notification
            self.notification = notification
            logger.info("Notification service initialized successfully")
        except ImportError:
            logger.warning("Plyer not available, notifications disabled")
            self.enabled = False
        except Exception as e:
            logger.error(f"Failed to initialize notification service: {e}")
            self.enabled = False
    
    def show_notification(
        self, 
        title: str, 
        message: str, 
        timeout: int = 5,
        app_icon: Optional[str] = None
    ) -> bool:
        """Show desktop notification.
        
        Args:
            title: Notification title
            message: Notification message
            timeout: Notification timeout in seconds
            app_icon: Path to app icon
            
        Returns:
            True if notification was shown successfully, False otherwise
        """
        if not self.enabled:
            logger.debug("Notifications disabled, skipping notification")
            return False
        
        try:
            self.notification.notify(
                title=title,
                message=message,
                timeout=timeout,
                app_icon=app_icon
            )
            logger.debug(f"Notification shown: {title}")
            return True
        except Exception as e:
            logger.error(f"Failed to show notification: {e}")
            return False
    
    def show_goal_achieved(self, ml_consumed: float, goal_ml: float) -> bool:
        """Show goal achieved notification.
        
        Args:
            ml_consumed: Milliliters consumed
            goal_ml: Goal in milliliters
            
        Returns:
            True if notification was shown successfully, False otherwise
        """
        title = "🎉 Goal Achieved!"
        message = f"You've reached your daily goal of {goal_ml}ml! Great job!"
        
        return self.show_notification(title, message, timeout=10)
    
    def show_goal_reminder(self, remaining_ml: float, goal_ml: float) -> bool:
        """Show goal reminder notification.
        
        Args:
            remaining_ml: Remaining milliliters to reach goal
            goal_ml: Goal in milliliters
            
        Returns:
            True if notification was shown successfully, False otherwise
        """
        title = "💧 Hydration Reminder"
        message = f"You have {remaining_ml:.0f}ml left to reach your daily goal of {goal_ml}ml."
        
        return self.show_notification(title, message, timeout=8)
    
    def show_sip_detected(self, ml_amount: float) -> bool:
        """Show sip detected notification.
        
        Args:
            ml_amount: Amount of water in milliliters
            
        Returns:
            True if notification was shown successfully, False otherwise
        """
        title = "💧 Sip Detected"
        message = f"Detected {ml_amount:.0f}ml sip. Keep hydrating!"
        
        return self.show_notification(title, message, timeout=3)
    
    def show_error(self, error_message: str) -> bool:
        """Show error notification.
        
        Args:
            error_message: Error message to display
            
        Returns:
            True if notification was shown successfully, False otherwise
        """
        title = "⚠️ Error"
        message = f"An error occurred: {error_message}"
        
        return self.show_notification(title, message, timeout=10)
    
    def show_info(self, title: str, message: str) -> bool:
        """Show info notification.
        
        Args:
            title: Notification title
            message: Notification message
            
        Returns:
            True if notification was shown successfully, False otherwise
        """
        return self.show_notification(title, message, timeout=5)
    
    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable notifications.
        
        Args:
            enabled: Whether to enable notifications
        """
        self.enabled = enabled
        logger.info(f"Notifications {'enabled' if enabled else 'disabled'}")
    
    def is_enabled(self) -> bool:
        """Check if notifications are enabled.
        
        Returns:
            True if notifications are enabled, False otherwise
        """
        return self.enabled and self.notification is not None


# Global notification service instance
notification_service = NotificationService()
