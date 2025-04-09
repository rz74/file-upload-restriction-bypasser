import base64
import math
import zipfile
from datetime import datetime
from pathlib import Path

def shift_obfuscate(data: str, shift: int) -> str:
    return ''.join(chr((ord(c) + shift) % 256) for c in data)

def split_into_segments(text: str, num_segments: int):
    seg_len = math.ceil(len(text) / num_segments)
    return [text[i * seg_len:(i + 1) * seg_len] for i in range(num_segments)]

def save_segments(segments, output_dir):
    filenames = []
    for i, segment in enumerate(segments):
        fname = output_dir / f"part_{i}"
        with open(fname, 'w', encoding='latin1') as f:
            f.write(segment)
        filenames.append(fname.name)
    return filenames

def create_readme(original_filename, shift_value, segment_names, output_dir):
    readme_path = output_dir / "README.txt"
    with open(readme_path, 'w') as f:
        f.write("== File Upload Bypass - Reconstruction Guide ==\n\n")
        f.write(f"Original Filename: {original_filename}\n")
        f.write(f"Character Shift Value: {shift_value}\n")
        f.write(f"Segments ({len(segment_names)} total):\n")
        for name in segment_names:
            f.write(f"  - {name}\n")
        f.write("\nTo reconstruct:\n")
        f.write("1. Concatenate all segments in order.\n")
        f.write("2. Shift characters back by the value above.\n")
        f.write("3. Base64 decode and save as the original file.\n")
    return readme_path.name

def zip_output(folder: Path, zip_name: str):
    zip_path = folder / zip_name
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in folder.iterdir():
            if file.name != zip_name:
                zipf.write(file, arcname=file.name)
    return zip_path

def main():
    file_path = input("Enter the path to the file you want to encode: ").strip()
    try:
        shift_value = int(input("Enter a character shift value (e.g. 3): ").strip())
        num_segments = int(input("Enter number of segments (1–10): ").strip())
        if not (1 <= num_segments <= 10):
            raise ValueError("Segment count must be between 1 and 10.")
    except ValueError as e:
        print(f"Invalid input: {e}")
        return

    file_path = Path(file_path)
    if not file_path.exists():
        print("File not found.")
        return

    with open(file_path, 'rb') as f:
        b64_data = base64.b64encode(f.read()).decode('utf-8')

    obfuscated = shift_obfuscate(b64_data, shift_value)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True, parents=True)

    segments = split_into_segments(obfuscated, num_segments)
    segment_names = save_segments(segments, output_dir)

    create_readme(file_path.name, shift_value, segment_names, output_dir)

    zip_file = zip_output(output_dir, f"{file_path.stem}_obfuscated.zip")

    print(f"✅ Done! Zip created at: {zip_file}")

if __name__ == "__main__":
    main()
