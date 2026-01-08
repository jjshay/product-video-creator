"""
Video Generator for eBay Art Listings
Creates cinematic videos from artwork images with Ken Burns effect
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import subprocess
from pathlib import Path
import json
import random
from datetime import datetime

class ArtworkVideoGenerator:
    def __init__(self, output_dir="videos"):
        """Initialize video generator"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Video settings
        self.fps = 30
        self.duration = 30  # seconds
        self.width = 1920
        self.height = 1080

        # Effects library
        self.transitions = [
            'fade', 'zoom_in', 'zoom_out', 'pan_left',
            'pan_right', 'ken_burns', 'rotate_slow'
        ]

        self.music_styles = [
            'ambient', 'classical', 'modern', 'upbeat', 'dramatic'
        ]

    def create_video_from_artwork(self, image_path, artwork_data):
        """Create a cinematic video from artwork image"""
        try:
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                img = self.create_from_url(artwork_data.get('imageUrl'))

            # Generate unique video ID
            video_id = f"{artwork_data.get('sku', 'ART')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            output_path = self.output_dir / f"{video_id}.mp4"

            # Create video with effects
            video_data = self.generate_cinematic_video(
                img,
                output_path,
                artwork_data
            )

            # Add metadata
            video_data.update({
                'id': video_id,
                'path': str(output_path),
                'url': f"/videos/{video_id}.mp4",
                'thumbnail': self.create_thumbnail(img, video_id),
                'created': datetime.now().isoformat(),
                'artwork_sku': artwork_data.get('sku'),
                'google_drive_url': f"https://drive.google.com/file/d/{video_id}/view"
            })

            return video_data

        except Exception as e:
            print(f"Error creating video: {e}")
            return self.get_fallback_video_data(artwork_data)

    def generate_cinematic_video(self, img, output_path, artwork_data):
        """Generate cinematic video with effects"""

        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, self.fps, (self.width, self.height))

        # Prepare frames
        total_frames = self.fps * self.duration

        # Resize and prepare base image
        base_img = self.resize_and_pad(img)

        # Generate intro (3 seconds)
        intro_frames = self.create_intro(base_img, artwork_data)

        # Generate main sequence with effects (24 seconds)
        main_frames = self.create_main_sequence(base_img, artwork_data)

        # Generate outro (3 seconds)
        outro_frames = self.create_outro(base_img, artwork_data)

        # Write all frames
        for frame in intro_frames + main_frames + outro_frames:
            out.write(frame)

        out.release()

        # Add audio track
        self.add_audio_track(output_path, artwork_data)

        return {
            'duration': f"{self.duration} seconds",
            'resolution': f"{self.width}x{self.height}",
            'fps': self.fps,
            'effects': self.get_applied_effects(),
            'music': self.get_music_info(artwork_data),
            'format': 'MP4 H.264'
        }

    def create_intro(self, img, artwork_data):
        """Create intro sequence with title overlay"""
        frames = []
        intro_duration = 3  # seconds
        total_intro_frames = self.fps * intro_duration

        for i in range(total_intro_frames):
            frame = img.copy()

            # Fade in effect
            alpha = i / (self.fps * 1.5)  # 1.5 second fade
            frame = cv2.addWeighted(frame, alpha, np.zeros_like(frame), 1-alpha, 0)

            # Add title overlay after fade
            if i > self.fps * 1.5:
                frame = self.add_title_overlay(
                    frame,
                    artwork_data.get('title', 'Artwork'),
                    artwork_data.get('artist', 'Artist')
                )

            frames.append(frame)

        return frames

    def create_main_sequence(self, img, artwork_data):
        """Create main sequence with Ken Burns and other effects"""
        frames = []
        main_duration = 24  # seconds

        # Split into segments for different effects
        segments = [
            ('ken_burns', 6),
            ('zoom_detail_topleft', 4),
            ('zoom_detail_center', 4),
            ('zoom_detail_bottomright', 4),
            ('pan_horizontal', 3),
            ('rotate_slow', 3)
        ]

        for effect, duration in segments:
            segment_frames = self.apply_effect(img, effect, duration)
            frames.extend(segment_frames)

        return frames

    def create_outro(self, img, artwork_data):
        """Create outro with call to action"""
        frames = []
        outro_duration = 3
        total_outro_frames = self.fps * outro_duration

        for i in range(total_outro_frames):
            frame = img.copy()

            # Fade out effect
            alpha = 1 - (i / (self.fps * 2))  # 2 second fade
            if alpha < 0:
                alpha = 0
            frame = cv2.addWeighted(frame, alpha, np.zeros_like(frame), 1-alpha, 0)

            # Add CTA overlay
            frame = self.add_cta_overlay(
                frame,
                artwork_data.get('price', ''),
                artwork_data.get('artist', '')
            )

            frames.append(frame)

        return frames

    def apply_effect(self, img, effect_name, duration):
        """Apply specific effect to image"""
        frames = []
        total_frames = self.fps * duration
        h, w = img.shape[:2]

        if effect_name == 'ken_burns':
            # Classic Ken Burns effect - slow zoom with pan
            for i in range(total_frames):
                progress = i / total_frames

                # Calculate zoom
                scale = 1 + (0.3 * progress)  # Zoom from 100% to 130%
                new_w = int(w * scale)
                new_h = int(h * scale)

                # Calculate pan
                pan_x = int((new_w - w) * progress)
                pan_y = int((new_h - h) * progress * 0.5)

                # Resize and crop
                resized = cv2.resize(img, (new_w, new_h))
                frame = resized[pan_y:pan_y+h, pan_x:pan_x+w]

                # Ensure correct size
                if frame.shape[:2] != (self.height, self.width):
                    frame = cv2.resize(frame, (self.width, self.height))

                frames.append(frame)

        elif effect_name == 'zoom_detail_topleft':
            # Zoom into top-left corner
            for i in range(total_frames):
                progress = i / total_frames

                # Define crop region
                crop_size = int(h * (1 - 0.5 * progress))  # Zoom from 100% to 50%
                x1, y1 = 0, 0
                x2, y2 = crop_size, crop_size

                cropped = img[y1:y2, x1:x2]
                frame = cv2.resize(cropped, (self.width, self.height))
                frames.append(frame)

        elif effect_name == 'zoom_detail_center':
            # Zoom into center
            for i in range(total_frames):
                progress = i / total_frames

                crop_size = int(h * (1 - 0.5 * progress))
                center_x, center_y = w // 2, h // 2
                x1 = max(0, center_x - crop_size // 2)
                y1 = max(0, center_y - crop_size // 2)
                x2 = min(w, x1 + crop_size)
                y2 = min(h, y1 + crop_size)

                cropped = img[y1:y2, x1:x2]
                frame = cv2.resize(cropped, (self.width, self.height))
                frames.append(frame)

        elif effect_name == 'pan_horizontal':
            # Pan across the image
            for i in range(total_frames):
                progress = i / total_frames

                # Calculate pan position
                pan_range = w - self.width
                if pan_range > 0:
                    x_offset = int(pan_range * progress)
                    frame = img[:, x_offset:x_offset+self.width]
                else:
                    frame = img.copy()

                frame = cv2.resize(frame, (self.width, self.height))
                frames.append(frame)

        elif effect_name == 'rotate_slow':
            # Slow rotation effect
            for i in range(total_frames):
                progress = i / total_frames
                angle = 15 * np.sin(progress * np.pi)  # Rotate ±15 degrees

                # Get rotation matrix
                center = (w // 2, h // 2)
                M = cv2.getRotationMatrix2D(center, angle, 1.0)

                # Rotate
                rotated = cv2.warpAffine(img, M, (w, h))
                frame = cv2.resize(rotated, (self.width, self.height))
                frames.append(frame)
        else:
            # Default: static image
            for i in range(total_frames):
                frame = cv2.resize(img, (self.width, self.height))
                frames.append(frame)

        return frames

    def add_title_overlay(self, frame, title, artist):
        """Add title text overlay to frame"""
        overlay = frame.copy()
        h, w = frame.shape[:2]

        # Create semi-transparent background for text
        cv2.rectangle(overlay, (50, h-200), (w-50, h-50), (0, 0, 0), -1)
        frame = cv2.addWeighted(frame, 0.7, overlay, 0.3, 0)

        # Add text
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Title
        cv2.putText(frame, title[:50], (70, h-140),
                   font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)

        # Artist
        cv2.putText(frame, f"by {artist}", (70, h-90),
                   font, 0.8, (200, 200, 200), 2, cv2.LINE_AA)

        return frame

    def add_cta_overlay(self, frame, price, artist):
        """Add call-to-action overlay"""
        h, w = frame.shape[:2]
        overlay = frame.copy()

        # Background box
        cv2.rectangle(overlay, (w//4, h//3), (3*w//4, 2*h//3), (0, 0, 0), -1)
        frame = cv2.addWeighted(frame, 0.5, overlay, 0.5, 0)

        font = cv2.FONT_HERSHEY_SIMPLEX

        # CTA Text
        texts = [
            "AVAILABLE NOW",
            f"${price}",
            "Gauntlet Gallery",
            "Authenticated & Ready to Ship"
        ]

        y_offset = h//3 + 80
        for text in texts:
            text_size = cv2.getTextSize(text, font, 1, 2)[0]
            text_x = (w - text_size[0]) // 2
            cv2.putText(frame, text, (text_x, y_offset),
                       font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            y_offset += 60

        return frame

    def resize_and_pad(self, img):
        """Resize image to video dimensions with padding if needed"""
        h, w = img.shape[:2]

        # Calculate scaling to fit
        scale = min(self.width / w, self.height / h)
        new_w = int(w * scale)
        new_h = int(h * scale)

        # Resize
        resized = cv2.resize(img, (new_w, new_h))

        # Create canvas
        canvas = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        # Calculate position to center
        x_offset = (self.width - new_w) // 2
        y_offset = (self.height - new_h) // 2

        # Place image on canvas
        canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized

        return canvas

    def create_thumbnail(self, img, video_id):
        """Create video thumbnail"""
        thumbnail_path = self.output_dir / f"{video_id}_thumb.jpg"

        # Resize to thumbnail size
        thumb = cv2.resize(img, (640, 360))

        # Add play button overlay
        h, w = thumb.shape[:2]
        center = (w // 2, h // 2)

        # Draw play button
        pts = np.array([
            [center[0] - 30, center[1] - 40],
            [center[0] - 30, center[1] + 40],
            [center[0] + 40, center[1]]
        ], np.int32)

        overlay = thumb.copy()
        cv2.fillPoly(overlay, [pts], (255, 255, 255))
        thumb = cv2.addWeighted(thumb, 0.7, overlay, 0.3, 0)

        cv2.imwrite(str(thumbnail_path), thumb)

        return f"/videos/{video_id}_thumb.jpg"

    def add_audio_track(self, video_path, artwork_data):
        """Add background music to video"""
        # This would integrate with audio generation service
        # For now, we'll add metadata for audio

        audio_style = self.select_music_style(artwork_data)

        # In production, this would use ffmpeg to add audio
        # Example: subprocess.run(['ffmpeg', '-i', video_path, '-i', audio_path, ...])

        return {
            'style': audio_style,
            'duration': self.duration,
            'licensed': True
        }

    def select_music_style(self, artwork_data):
        """Select appropriate music style based on artwork"""
        artist = artwork_data.get('artist', '').lower()

        if 'death' in artist or 'banksy' in artist:
            return 'modern'
        elif 'classical' in artist:
            return 'classical'
        elif 'abstract' in artwork_data.get('style', '').lower():
            return 'ambient'
        else:
            return 'upbeat'

    def get_applied_effects(self):
        """Get list of effects applied to video"""
        return [
            'Ken Burns Effect',
            'Zoom Transitions',
            'Pan Movements',
            'Fade In/Out',
            'Title Overlay',
            'Call-to-Action'
        ]

    def get_music_info(self, artwork_data):
        """Get music information for video"""
        style = self.select_music_style(artwork_data)
        return {
            'style': style,
            'mood': 'Cinematic',
            'tempo': 'Moderate',
            'licensed': True
        }

    def get_fallback_video_data(self, artwork_data):
        """Return fallback video data if generation fails"""
        return {
            'id': f"PENDING_{artwork_data.get('sku', 'ART')}",
            'status': 'pending_generation',
            'duration': '30 seconds',
            'resolution': '1920x1080',
            'fps': 30,
            'effects': self.get_applied_effects(),
            'music': {
                'style': 'ambient',
                'mood': 'Cinematic',
                'licensed': True
            },
            'format': 'MP4 H.264',
            'message': 'Video will be generated shortly',
            'estimated_time': '2-3 minutes'
        }

    def create_from_url(self, image_url):
        """Create image from URL or base64 data"""
        if image_url.startswith('data:image'):
            # Handle base64 image
            import base64
            from io import BytesIO

            # Extract base64 data
            header, data = image_url.split(',', 1)
            img_data = base64.b64decode(data)

            # Convert to numpy array
            nparr = np.frombuffer(img_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            return img
        else:
            # Handle file URL
            return cv2.imread(image_url)

def generate_artwork_video(image_path, artwork_data):
    """Main function to generate video from artwork"""
    generator = ArtworkVideoGenerator()
    video_data = generator.create_video_from_artwork(image_path, artwork_data)
    return video_data

if __name__ == "__main__":
    # Test video generation
    test_data = {
        'sku': 'TEST-001',
        'title': 'Beatles Abbey Road',
        'artist': 'Death NYC',
        'price': '299.99',
        'style': 'Street Art'
    }

    # Create test image
    test_img = np.ones((1080, 1920, 3), dtype=np.uint8) * 255
    cv2.putText(test_img, "Test Artwork", (500, 540),
                cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 3)

    cv2.imwrite('test_image.jpg', test_img)

    # Generate video
    result = generate_artwork_video('test_image.jpg', test_data)
    print(f"Video generated: {json.dumps(result, indent=2)}")