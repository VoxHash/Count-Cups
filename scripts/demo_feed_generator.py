#!/usr/bin/env python3
"""Demo feed generator for Count-Cups testing and demonstration.

This script generates synthetic video frames that simulate drinking gestures
for testing the detection system without requiring a real camera.
"""

import argparse
import time

import cv2
import numpy as np

from app.core.detection.heuristics import AdvancedHeuristicDetector
from app.core.models import DetectionResult


class DemoFeedGenerator:
    """Generates synthetic video frames for testing detection."""

    def __init__(self, width: int = 640, height: int = 480):
        """Initialize demo feed generator.

        Args:
            width: Frame width
            height: Frame height
        """
        self.width = width
        self.height = height
        self.frame_count = 0
        self.detector = AdvancedHeuristicDetector()

        # Animation parameters
        self.head_angle = 0.0
        self.hand_x = width // 2
        self.hand_y = height // 2
        self.drinking_phase = (
            0  # 0: not drinking, 1: approaching, 2: drinking, 3: leaving
        )

    def generate_frame(self) -> np.ndarray:
        """Generate a synthetic video frame.

        Returns:
            Generated frame as numpy array
        """
        # Create base frame
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        frame.fill(50)  # Dark background

        # Add some background noise
        noise = np.random.randint(0, 30, (self.height, self.width, 3), dtype=np.uint8)
        frame = cv2.add(frame, noise)

        # Draw face
        face_center = (self.width // 2, self.height // 3)
        face_size = 120
        self._draw_face(frame, face_center, face_size)

        # Draw hand
        hand_center = (self.hand_x, self.hand_y)
        hand_size = 40
        self._draw_hand(frame, hand_center, hand_size)

        # Update animation
        self._update_animation()

        self.frame_count += 1
        return frame

    def _draw_face(self, frame: np.ndarray, center: tuple[int, int], size: int) -> None:
        """Draw a synthetic face.

        Args:
            frame: Frame to draw on
            center: Face center coordinates
            size: Face size
        """
        x, y = center

        # Face outline
        cv2.ellipse(
            frame, (x, y), (size, int(size * 1.2)), 0, 0, 360, (200, 180, 160), -1
        )

        # Eyes
        eye_y = y - size // 4
        cv2.circle(frame, (x - size // 3, eye_y), 8, (255, 255, 255), -1)
        cv2.circle(frame, (x + size // 3, eye_y), 8, (255, 255, 255), -1)
        cv2.circle(frame, (x - size // 3, eye_y), 4, (0, 0, 0), -1)
        cv2.circle(frame, (x + size // 3, eye_y), 4, (0, 0, 0), -1)

        # Nose
        cv2.circle(frame, (x, y), 5, (180, 160, 140), -1)

        # Mouth
        mouth_y = y + size // 3
        cv2.ellipse(
            frame, (x, mouth_y), (size // 4, size // 8), 0, 0, 180, (100, 50, 50), 2
        )

        # Head tilt effect
        if abs(self.head_angle) > 5:
            # Draw tilted face
            pass  # Simplified for demo

    def _draw_hand(self, frame: np.ndarray, center: tuple[int, int], size: int) -> None:
        """Draw a synthetic hand.

        Args:
            frame: Frame to draw on
            center: Hand center coordinates
            size: Hand size
        """
        x, y = center

        # Hand (skin color)
        cv2.ellipse(
            frame, (x, y), (size, int(size * 0.8)), 0, 0, 360, (200, 180, 160), -1
        )

        # Fingers
        finger_positions = [
            (x - size // 2, y - size // 3),
            (x - size // 4, y - size // 2),
            (x, y - size // 2),
            (x + size // 4, y - size // 2),
            (x + size // 2, y - size // 3),
        ]

        for fx, fy in finger_positions:
            cv2.circle(frame, (fx, fy), 8, (200, 180, 160), -1)

        # Cup (if drinking)
        if self.drinking_phase == 2:
            cup_x = x + size
            cup_y = y
            cv2.rectangle(
                frame,
                (cup_x - 10, cup_y - 20),
                (cup_x + 10, cup_y + 20),
                (100, 100, 100),
                -1,
            )
            cv2.rectangle(
                frame,
                (cup_x - 10, cup_y - 20),
                (cup_x + 10, cup_y + 20),
                (255, 255, 255),
                2,
            )

    def _update_animation(self) -> None:
        """Update animation parameters."""
        # Simple drinking animation
        if self.frame_count % 200 < 50:  # Not drinking
            self.drinking_phase = 0
            self.head_angle = 0
            self.hand_x = self.width // 2 + 100
            self.hand_y = self.height // 2
        elif self.frame_count % 200 < 100:  # Approaching
            self.drinking_phase = 1
            self.head_angle = 0
            progress = (self.frame_count % 200 - 50) / 50
            self.hand_x = int(self.width // 2 + 100 - progress * 80)
            self.hand_y = int(self.height // 2 - progress * 30)
        elif self.frame_count % 200 < 150:  # Drinking
            self.drinking_phase = 2
            self.head_angle = 20 + 10 * np.sin((self.frame_count % 200 - 100) * 0.2)
            self.hand_x = self.width // 2 + 20
            self.hand_y = self.height // 2 - 30
        else:  # Leaving
            self.drinking_phase = 3
            self.head_angle = 0
            progress = (self.frame_count % 200 - 150) / 50
            self.hand_x = int(self.width // 2 + 20 + progress * 80)
            self.hand_y = int(self.height // 2 - 30 + progress * 30)

    def generate_detection_result(self, frame: np.ndarray) -> DetectionResult | None:
        """Generate a detection result for the frame.

        Args:
            frame: Input frame

        Returns:
            Detection result or None
        """
        # Simulate detection based on animation state
        if self.drinking_phase == 2:  # Drinking phase
            confidence = 0.7 + 0.2 * np.random.random()
            head_tilt = self.head_angle
            hand_distance = 50 + 20 * np.random.random()

            return DetectionResult(
                has_sip=True,
                confidence=confidence,
                head_tilt_angle=head_tilt,
                hand_face_distance=hand_distance,
                face_center=(self.width // 2, self.height // 3),
                hand_center=(self.hand_x, self.hand_y),
                detection_data={
                    "demo": True,
                    "phase": self.drinking_phase,
                    "frame": self.frame_count,
                },
            )

        return None


def main():
    """Main function for demo feed generator."""
    parser = argparse.ArgumentParser(
        description="Generate demo video feed for Count-Cups"
    )
    parser.add_argument("--width", type=int, default=640, help="Frame width")
    parser.add_argument("--height", type=int, default=480, help="Frame height")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second")
    parser.add_argument("--duration", type=int, default=60, help="Duration in seconds")
    parser.add_argument("--output", type=str, help="Output video file")
    parser.add_argument(
        "--display", action="store_true", help="Display video in window"
    )
    parser.add_argument("--detect", action="store_true", help="Run detection on frames")

    args = parser.parse_args()

    # Create generator
    generator = DemoFeedGenerator(args.width, args.height)

    # Setup video writer if output specified
    video_writer = None
    if args.output:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        video_writer = cv2.VideoWriter(
            args.output, fourcc, args.fps, (args.width, args.height)
        )

    # Setup detection if requested
    detector = None
    if args.detect:
        detector = AdvancedHeuristicDetector()

    print(f"Generating demo feed: {args.width}x{args.height} @ {args.fps}fps")
    if args.duration:
        print(f"Duration: {args.duration} seconds")
    if args.output:
        print(f"Output: {args.output}")
    if args.display:
        print("Display: Enabled")
    if args.detect:
        print("Detection: Enabled")

    # Generate frames
    start_time = time.time()
    frame_count = 0
    detection_count = 0

    try:
        while True:
            # Check duration
            if args.duration and (time.time() - start_time) >= args.duration:
                break

            # Generate frame
            frame = generator.generate_frame()

            # Run detection if requested
            if detector:
                result = detector.detect(frame)
                if result and result.has_sip:
                    detection_count += 1
                    print(
                        f"Detection #{detection_count}: confidence={result.confidence:.2f}"
                    )

            # Display frame
            if args.display:
                cv2.imshow("Count-Cups Demo Feed", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            # Write frame
            if video_writer:
                video_writer.write(frame)

            frame_count += 1

            # Control frame rate
            time.sleep(1.0 / args.fps)

    except KeyboardInterrupt:
        print("\nStopped by user")

    finally:
        # Cleanup
        if video_writer:
            video_writer.release()
        if args.display:
            cv2.destroyAllWindows()

        # Print statistics
        elapsed = time.time() - start_time
        print(f"\nGenerated {frame_count} frames in {elapsed:.1f} seconds")
        print(f"Average FPS: {frame_count / elapsed:.1f}")
        if detector:
            print(f"Detections: {detection_count}")


if __name__ == "__main__":
    main()
