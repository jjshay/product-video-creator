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
        assert settings["resolution"][0] == 1920, "Width should be 1920"
        assert settings["resolution"][1] == 1080, "Height should be 1080"
        assert settings["fps"] == 30, "FPS should be 30"

    def test_video_duration(self):
        """Verify video duration is set"""
        config_path = Path(__file__).parent.parent / "examples" / "video_config.json"
        with open(config_path) as f:
            config = json.load(f)

        settings = config["video_settings"]
        assert "duration_seconds" in settings, "Should have duration_seconds"
        assert settings["duration_seconds"] == 45, "Duration should be 45 seconds"


class TestKenBurnsEffect:
    """Test Ken Burns effect parameters"""

    def test_ken_burns_settings(self):
        """Verify Ken Burns settings are defined"""
        config_path = Path(__file__).parent.parent / "examples" / "video_config.json"
        with open(config_path) as f:
            config = json.load(f)

        assert "ken_burns_settings" in config, "Config should have ken_burns_settings"
        settings = config["ken_burns_settings"]
        assert "zoom_range" in settings, "Should have zoom_range"
        assert "pan_speed" in settings, "Should have pan_speed"
        assert "easing" in settings, "Should have easing"

    def test_zoom_range(self):
        """Test zoom scale range is valid"""
        config_path = Path(__file__).parent.parent / "examples" / "video_config.json"
        with open(config_path) as f:
            config = json.load(f)

        zoom_range = config["ken_burns_settings"]["zoom_range"]
        min_zoom = zoom_range[0]
        max_zoom = zoom_range[1]

        assert min_zoom >= 1.0, "Min zoom should be at least 1.0"
        assert max_zoom <= 2.0, "Max zoom should not exceed 2.0"
        assert max_zoom > min_zoom, "Max zoom should be greater than min"


class TestInputImages:
    """Test input image configuration"""

    def test_input_images_defined(self):
        """Verify input images are defined in config"""
        config_path = Path(__file__).parent.parent / "examples" / "video_config.json"
        with open(config_path) as f:
            config = json.load(f)

        assert "input_images" in config, "Config should have input_images"
        images = config["input_images"]
        assert len(images) >= 5, "Should have at least 5 input images"

    def test_input_image_properties(self):
        """Verify input images have required properties"""
        config_path = Path(__file__).parent.parent / "examples" / "video_config.json"
        with open(config_path) as f:
            config = json.load(f)

        for image in config["input_images"]:
            assert "file" in image, "Image should have file"
            assert "type" in image, "Image should have type"


class TestBranding:
    """Test branding configuration"""

    def test_branding_defined(self):
        """Verify branding is defined"""
        config_path = Path(__file__).parent.parent / "examples" / "video_config.json"
        with open(config_path) as f:
            config = json.load(f)

        assert "branding" in config, "Config should have branding"
        branding = config["branding"]
        assert "quotes" in branding, "Branding should have quotes"
        assert "website_url" in branding, "Branding should have website_url"

    def test_quotes_defined(self):
        """Verify quotes are defined"""
        config_path = Path(__file__).parent.parent / "examples" / "video_config.json"
        with open(config_path) as f:
            config = json.load(f)

        quotes = config["branding"]["quotes"]
        assert len(quotes) >= 3, "Should have at least 3 quotes"


class TestProductInfo:
    """Test product information"""

    def test_product_defined(self):
        """Verify product info is defined"""
        config_path = Path(__file__).parent.parent / "examples" / "video_config.json"
        with open(config_path) as f:
            config = json.load(f)

        assert "product" in config, "Config should have product"
        product = config["product"]
        assert "name" in product, "Product should have name"
        assert "sku" in product, "Product should have sku"


class TestOutputConfig:
    """Test output configuration"""

    def test_output_defined(self):
        """Verify output configuration is defined"""
        config_path = Path(__file__).parent.parent / "examples" / "video_config.json"
        with open(config_path) as f:
            config = json.load(f)

        assert "output" in config, "Config should have output"
        output = config["output"]
        assert "filename" in output, "Output should have filename"
        assert "upload_to_drive" in output, "Output should have upload_to_drive"


class TestVideoSpec:
    """Test video specification output"""

    def test_sample_spec_exists(self):
        """Verify sample video spec exists"""
        spec_path = Path(__file__).parent.parent / "sample_output" / "video_spec.json"
        assert spec_path.exists(), "Video spec output should exist"

    def test_spec_has_video_settings(self):
        """Verify spec has video settings"""
        spec_path = Path(__file__).parent.parent / "sample_output" / "video_spec.json"
        with open(spec_path) as f:
            spec = json.load(f)

        assert "video_settings" in spec, "Spec should have video_settings"
        settings = spec["video_settings"]
        assert "total_frames" in settings, "Settings should have total_frames"
        assert settings["total_frames"] > 0, "Should have positive frame count"

    def test_spec_has_timeline(self):
        """Verify spec has timeline"""
        spec_path = Path(__file__).parent.parent / "sample_output" / "video_spec.json"
        with open(spec_path) as f:
            spec = json.load(f)

        assert "timeline" in spec, "Spec should have timeline"
        timeline = spec["timeline"]
        assert len(timeline) >= 5, "Timeline should have at least 5 segments"

    def test_timeline_segment_properties(self):
        """Verify timeline segments have required properties"""
        spec_path = Path(__file__).parent.parent / "sample_output" / "video_spec.json"
        with open(spec_path) as f:
            spec = json.load(f)

        for segment in spec["timeline"]:
            assert "segment" in segment, "Segment should have segment name"
            assert "start" in segment, "Segment should have start time"
            assert "end" in segment, "Segment should have end time"
            assert "source" in segment, "Segment should have source"
            assert "effect" in segment, "Segment should have effect"


class TestTextOverlays:
    """Test text overlay functionality"""

    def test_text_overlays_in_spec(self):
        """Verify text overlays are in the spec"""
        spec_path = Path(__file__).parent.parent / "sample_output" / "video_spec.json"
        with open(spec_path) as f:
            spec = json.load(f)

        assert "text_overlays" in spec, "Spec should have text_overlays"
        overlays = spec["text_overlays"]
        assert len(overlays) >= 3, "Should have at least 3 text overlays"

    def test_overlay_properties(self):
        """Verify text overlays have required properties"""
        spec_path = Path(__file__).parent.parent / "sample_output" / "video_spec.json"
        with open(spec_path) as f:
            spec = json.load(f)

        for overlay in spec["text_overlays"]:
            assert "text" in overlay, "Overlay should have text"
            assert "start" in overlay, "Overlay should have start time"
            assert "end" in overlay, "Overlay should have end time"
            assert "position" in overlay, "Overlay should have position"


class TestInputSpec:
    """Test input specification in output"""

    def test_input_in_spec(self):
        """Verify input info is in the spec"""
        spec_path = Path(__file__).parent.parent / "sample_output" / "video_spec.json"
        with open(spec_path) as f:
            spec = json.load(f)

        assert "input" in spec, "Spec should have input"
        assert "images" in spec["input"], "Input should have images"


class TestMetadata:
    """Test spec metadata"""

    def test_metadata_present(self):
        """Verify metadata is included"""
        spec_path = Path(__file__).parent.parent / "sample_output" / "video_spec.json"
        with open(spec_path) as f:
            spec = json.load(f)

        assert "metadata" in spec, "Spec should have metadata"
        metadata = spec["metadata"]
        assert "processing_time_seconds" in metadata, "Metadata should have processing_time_seconds"
        assert "timestamp" in metadata, "Metadata should have timestamp"

    def test_output_info(self):
        """Verify output info is included"""
        spec_path = Path(__file__).parent.parent / "sample_output" / "video_spec.json"
        with open(spec_path) as f:
            spec = json.load(f)

        assert "output" in spec, "Spec should have output"
        output = spec["output"]
        assert "filename" in output, "Output should have filename"
        assert "file_size_mb" in output, "Output should have file_size_mb"
