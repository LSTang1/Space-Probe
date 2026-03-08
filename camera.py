from picamera2 import Picamera2, Preview
import time
import os

# Output directory for saved images/video
OUTPUT_DIR = "captures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def take_photo(filename="photo.jpg"):
    picam2 = Picamera2()

    # Configure for still image capture
    config = picam2.create_still_configuration(
        main={"size": (2592, 1944)},  # Full 5MP resolution
        lores={"size": (640, 480)},
        display="lores"
    )
    picam2.configure(config)

    picam2.start()
    time.sleep(2)  # Warm up / allow auto-exposure to settle

    filepath = os.path.join(OUTPUT_DIR, filename)
    picam2.capture_file(filepath)
    print(f"Photo saved: {filepath}")

    picam2.stop()
    picam2.close()


def record_video(filename="video.h264", duration=10):
    picam2 = Picamera2()

    # Configure for video recording
    config = picam2.create_video_configuration(
        main={"size": (1920, 1080)},  # 1080p
        controls={"FrameRate": 30}
    )
    picam2.configure(config)

    from picamera2.encoders import H264Encoder
    encoder = H264Encoder(bitrate=10000000)

    filepath = os.path.join(OUTPUT_DIR, filename)

    picam2.start_recording(encoder, filepath)
    print(f"Recording for {duration} seconds...")
    time.sleep(duration)
    picam2.stop_recording()
    print(f"Video saved: {filepath}")

    picam2.close()


def live_preview(duration=10):
    picam2 = Picamera2()

    config = picam2.create_preview_configuration(
        main={"size": (1280, 720)}
    )
    picam2.configure(config)

    picam2.start_preview(Preview.QTGL)  # Use Preview.NULL if no display attached
    picam2.start()

    print(f"Showing preview for {duration} seconds...")
    time.sleep(duration)

    picam2.stop_preview()
    picam2.stop()
    picam2.close()


def main():
    print("Arducam OV5647 5MP Camera")
    print("=" * 35)
    print("1. Take a photo")
    print("2. Record video")
    print("3. Live preview")
    choice = input("Choose an option (1/2/3): ").strip()

    if choice == "1":
        take_photo("photo.jpg")
    elif choice == "2":
        duration = int(input("Enter recording duration (seconds): "))
        record_video("video.h264", duration)
    elif choice == "3":
        duration = int(input("Enter preview duration (seconds): "))
        live_preview(duration)
    else:
        print("Invalid option.")

if __name__ == "__main__":
    main()