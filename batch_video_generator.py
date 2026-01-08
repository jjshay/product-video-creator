#!/usr/bin/env python3
"""
Batch Video Generator
Processes all SKUs in output_clean to create product videos
"""

import sys
from pathlib import Path
from create_product_videos import (
    create_product_video,
    upload_to_drive,
    OUTPUT_DIR
)
from pathlib import Path
CROPS_DIR = Path("/Users/johnshay/3DSELLERS/processed_crops")

def batch_generate_videos():
    """Generate videos for all SKUs"""
    print(f"\n{'='*70}")
    print("BATCH VIDEO GENERATOR")
    print(f"{'='*70}\n")

    # Get all SKU folders
    sku_folders = [d for d in CROPS_DIR.iterdir() if d.is_dir()]
    sku_folders = sorted(sku_folders)

    print(f"Found {len(sku_folders)} SKUs to process\n")

    successful = 0
    failed = 0
    skipped = 0

    for idx, sku_folder in enumerate(sku_folders, 1):
        sku_name = sku_folder.name

        print(f"\n[{idx}/{len(sku_folders)}] Processing: {sku_name}")
        print(f"{'='*70}")

        # Check if video already exists
        video_path = OUTPUT_DIR / f"{sku_name}.mp4"
        if video_path.exists():
            print(f"⏭️  Video already exists, skipping...")
            skipped += 1
            continue

        try:
            # Generate video
            print("🎬 Generating video...")
            video_file = create_product_video(sku_name)

            if not video_file or not Path(video_file).exists():
                print(f"❌ Video generation failed")
                failed += 1
                continue

            video_size = Path(video_file).stat().st_size / (1024 * 1024)
            print(f"✅ Video created: {video_size:.1f} MB")

            # Upload to Google Drive
            print("📤 Uploading to Google Drive...")
            file_id = upload_to_drive(video_file, sku_name)

            if file_id:
                print(f"✅ Uploaded: File ID {file_id}")
                successful += 1
            else:
                print("⚠️  Upload failed, but video saved locally")
                successful += 1  # Still count as success since video was created

        except Exception as e:
            print(f"❌ Error: {e}")
            failed += 1
            import traceback
            traceback.print_exc()

    # Final summary
    print(f"\n\n{'='*70}")
    print("BATCH PROCESSING COMPLETE")
    print(f"{'='*70}")
    print(f"✅ Successful: {successful}/{len(sku_folders)}")
    print(f"⏭️  Skipped: {skipped}")
    print(f"❌ Failed: {failed}")
    print(f"📁 Output: {OUTPUT_DIR}")
    print(f"{'='*70}\n")

    return successful, failed, skipped


if __name__ == "__main__":
    successful, failed, skipped = batch_generate_videos()
    sys.exit(0 if failed == 0 else 1)
