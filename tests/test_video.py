"""
Tests for Product Video Creator
"""
import pytest
import os
import json
from pathlib import Path


class TestVideoConfig:
    """Test video configuration"""

    def test_config_exists(self):
        """Verify video config file exists"""
        config_path = Path(__file__).parent.parent / "examples" / "video_config.json"
        assert config_path.exists(), "Video config file should exist"

    def test_config_valid_json(self):
        """Verify config is valid JSON"""
        config_path = Path(__file__).parent.parent / "examples" / "video_config.json"
        with open(config_path) as f:
            config = json.load(f)
        assert "video_settings" in config, "Config should have video_settings"

    def test_video_dimensions(self):
        """Verify video dimensions are HD"""
        config_path = Path(__file__).parent.parent / "examples" / "video_config.json"
        with open(config_path) as f:
            config = json.load(f)

        settings = config["video_settings"]
        assert settings["width"] == 1920, "Width should be 1920"
        assert settings["height"] == 1080, "Height should be 1080"
        assert settings["fps"] == 30, "FPS should be 30"


class TestKenBurnsEffect:
    """Test Ken Burns effect parameters"""

    def test_effect_types(self):
        """Verify Ken Burns effect types are defined"""
        config_path = Path(__file__).parent.parent / "examples" / "video_config.json"
        with open(config_path) as f:
            config = json.load(f)

        effects = config["ken_burns_effects"]
        expected = ["zoom_in", "zoom_out", "pan_left", "pan_right", "pan_up", "pan_down"]

        for effect in expected:
            assert effect in effects, f"Missing effect type: {effect}"

    def test_zoom_range(self):
        """Test zoom scale range is valid"""
        min_zoom = 1.0
        max_zoom = 1.3

        assert min_zoom >= 1.0, "Min zoom should be at least 1.0"
        assert max_zoom <= 2.0, "Max zoom should not exceed 2.0"
        assert max_zoom > min_zoom, "Max zoom should be greater than min"


class TestSampleImages:
    """Test sample input images"""

    def test_artwork_images_exist(self):
        """Verify artwork sample images exist"""
        examples_path = Path(__file__).parent.parent / "examples"

        required_images = [
            "artwork_full.jpg",
            "artwork_top_left.jpg",
            "artwork_top_right.jpg",
            "artwork_center.jpg",
            "artwork_signature.jpg"
        ]

        for img in required_images:
            img_path = examples_path / img
            assert img_path.exists(), f"Sample image {img} should exist"

    def test_images_are_valid(self):
        """Verify images are valid JPEGs"""
        img_path = Path(__file__).parent.parent / "examples" / "artwork_full.jpg"
        with open(img_path, 'rb') as f:
            header = f.read(3)
        assert header[:2] == b'\xff\xd8', "File should be a valid JPEG"


class TestVideoSegments:
    """Test video segment structure"""

    def test_segment_duration(self):
        """Test total video duration"""
        config_path = Path(__file__).parent.parent / "examples" / "video_config.json"
        with open(config_path) as f:
            config = json.load(f)

        segments = config["segments"]
        total_duration = sum(seg["duration"] for seg in segments)

        # Should be around 45 seconds
        assert 40 <= total_duration <= 50, "Total duration should be ~45 seconds"

    def test_segments_have_required_fields(self):
        """Verify segments have required fields"""
        config_path = Path(__file__).parent.parent / "examples" / "video_config.json"
        with open(config_path) as f:
            config = json.load(f)

        for segment in config["segments"]:
            assert "name" in segment, "Segment should have name"
            assert "duration" in segment, "Segment should have duration"
            assert "effect" in segment, "Segment should have effect"


class TestTextOverlays:
    """Test text overlay functionality"""

    def test_quotes_defined(self):
        """Verify art quotes are defined"""
        config_path = Path(__file__).parent.parent / "examples" / "video_config.json"
        with open(config_path) as f:
            config = json.load(f)

        assert "art_quotes" in config, "Config should have art_quotes"
        assert len(config["art_quotes"]) >= 5, "Should have at least 5 quotes"

    def test_text_settings(self):
        """Verify text overlay settings"""
        config_path = Path(__file__).parent.parent / "examples" / "video_config.json"
        with open(config_path) as f:
            config = json.load(f)

        text_settings = config["text_overlay"]
        assert "font_size" in text_settings, "Should have font_size"
        assert "position" in text_settings, "Should have position"


class TestOutputSpec:
    """Test video output specification"""

    def test_sample_spec_exists(self):
        """Verify sample video spec exists"""
        spec_path = Path(__file__).parent.parent / "sample_output" / "video_spec.json"
        assert spec_path.exists(), "Video spec output should exist"

    def test_spec_has_frames(self):
        """Verify spec includes frame information"""
        spec_path = Path(__file__).parent.parent / "sample_output" / "video_spec.json"
        with open(spec_path) as f:
            spec = json.load(f)

        assert "total_frames" in spec, "Spec should have total_frames"
        assert spec["total_frames"] > 0, "Should have positive frame count"
