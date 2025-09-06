#!/usr/bin/env python3

# ======================================================
# Gemini Interactive Image Recreation Tool (Python Version)
# ======================================================

import os
import base64
import json
import datetime
import sys
import subprocess
import binascii
from pathlib import Path

try:
    import requests
except ImportError:
    print("The 'requests' library is not installed. Please install it by running: pip install requests")
    sys.exit(1)

def print_header():
    """Prints the tool's header."""
    print("=======================================")
    print("  Gemini Image Recreation Tool")
    print("=======================================")

def get_api_key():
    """Gets the Gemini API key from user input, environment variable, or default."""
    user_api_key = input("🔑 Enter your Gemini API key (leave empty to use the default one): ")
    if user_api_key:
        return user_api_key
    if os.getenv("GEMINI_API_KEY"):
        return os.getenv("GEMINI_API_KEY")
    return "your-api-key-here"  # Default key

def select_image_path(prompt_message="Input image"):
    """Allows the user to select an image file from various locations."""
    print(f"\n📁 {prompt_message} file selection:")
    print("1) Enter path manually")
    print("2) Select from current directory")
    print("3) Select from Documents directory")

    choice = input("➡ Choose an option (1-3): ")
    
    img_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']

    if choice == '1':
        return input("📂 Enter the full image file path: ")
    elif choice == '2':
        print("📂 Image files in current directory:")
        files = [f for f in os.listdir('.') if os.path.splitext(f)[1].lower() in img_extensions]
        if not files:
            print("No image files found")
            return None
        for i, f in enumerate(files, 1):
            print(f"{i}) {f}")
        filename = input("📝 Enter the filename: ")
        return os.path.join('.', filename)
    elif choice == '3':
        docs_dir = Path.home() / "Documents"
        if not docs_dir.is_dir():
            print("❌ Documents directory not found")
            return input("📂 Enter the full path: ")
        
        print(f"📂 Image files in {docs_dir}:")
        files = [f for f in os.listdir(docs_dir) if os.path.splitext(f)[1].lower() in img_extensions]
        if not files:
            print("No image files found")
            return None
        for i, f in enumerate(files, 1):
            print(f"{i}) {f}")
        filename = input("📝 Enter the filename: ")
        return os.path.join(docs_dir, filename)
    else:
        print("❌ Invalid option")
        return None

def get_output_path(input_path):
    """Determines the output file path based on user's choice."""
    print("\n💾 Output file configuration:")
    print("1) Auto-generate name in the same directory as input")
    print("2) Auto-generate name in current directory")
    print("3) Enter custom path")

    choice = input("➡ Choose an option (1-3): ")
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    input_dir = os.path.dirname(input_path)
    input_name = Path(input_path).stem

    if choice == '1':
        return os.path.join(input_dir, f"{input_name}_recreated_{timestamp}.jpg")
    elif choice == '2':
        return os.path.join('.', f"{input_name}_recreated_{timestamp}.jpg")
    elif choice == '3':
        output_file = input("📂 Enter the full output file path: ")
        if not output_file.lower().endswith(('.jpg', '.jpeg')):
            output_file += ".jpg"
        return output_file
    else:
        print("❌ Invalid option")
        return None

def get_custom_prompt():
    """Gets the generation prompt from the user."""
    print("\n📝 Prompt customization:")
    print("1) Use default prompt (realistic recreation)")
    print("2) Enter custom prompt")

    choice = input("➡ Choose an option (1-2): ")

    if choice == '1':
        return "Recreate a new very realistic, sharp and defined color image, high resolution, with current quality standards. As if it was taken by a digital reflex camera."
    elif choice == '2':
        print("💡 Prompt examples:")
        print("   - 'Transform into artistic watercolor style'")
        print("   - 'Recreate in vintage black and white'")
        print("   - 'Enhance quality and increase sharpness'")
        print("   - 'Transform into modern digital illustration'")
        return input("📝 Enter your prompt: ")
    else:
        print("❌ Invalid option")
        return None

def encode_image_to_base64(file_path):
    """Reads an image file and returns its base64 encoded string."""
    try:
        with open(file_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except IOError as e:
        print(f"❌ Error reading file {file_path}: {e}")
        return None

def main():
    """Main function to run the script."""
    print_header()
    
    api_key = get_api_key()

    # Input image
    img_path = select_image_path("Input image")
    if not img_path or not os.path.isfile(img_path):
        print(f"❌ Error: The image file {img_path} does not exist!")
        sys.exit(1)
    print(f"✅ Selected file: {img_path}")

    # Reference images
    ref_paths = []
    num_ref = input("\n📸 Enter number of reference images (0-2): ")
    if num_ref.isdigit() and 0 < int(num_ref) <= 2:
        for i in range(int(num_ref)):
            ref_path = select_image_path(f"Reference image {i+1}")
            if not ref_path or not os.path.isfile(ref_path):
                print(f"❌ Error: The reference image file {ref_path} does not exist!")
                sys.exit(1)
            print(f"✅ Selected reference {i+1}: {ref_path}")
            ref_paths.append(ref_path)

    # Output file
    output_file = get_output_path(img_path)
    if not output_file:
        sys.exit(1)
    print(f"✅ Output file: {output_file}")

    # Prompt
    custom_prompt = get_custom_prompt()
    if not custom_prompt:
        sys.exit(1)

    # Configuration summary
    print("\n📋 CONFIGURATION SUMMARY:")
    print(f"   Input:  {img_path}")
    for i, ref in enumerate(ref_paths, 1):
        print(f"   Reference {i}: {ref}")
    print(f"   Output: {output_file}")
    print(f"   Prompt: {custom_prompt}\n")

    confirm = input("🚀 Proceed with generation? (y/N): ")
    if confirm.lower() != 'y':
        print("❌ Operation cancelled")
        sys.exit(0)

    print("\n🔄 Starting recreation process...")

    # Image encoding
    print("📸 Encoding image to base64...")
    img_base64 = encode_image_to_base64(img_path)
    if not img_base64:
        sys.exit(1)

    ref_base64_list = []
    for i, ref_path in enumerate(ref_paths, 1):
        print(f"📸 Encoding reference {i} to base64...")
        ref_base64 = encode_image_to_base64(ref_path)
        if not ref_base64:
            sys.exit(1)
        ref_base64_list.append(ref_base64)

    # Build JSON payload
    parts = [
        {"text": custom_prompt},
        {"inlineData": {"mimeType": "image/jpeg", "data": img_base64}}
    ]
    for ref_b64 in ref_base64_list:
        parts.append({"inlineData": {"mimeType": "image/jpeg", "data": ref_b64}})
    
    payload = {"contents": [{"parts": parts}]}
    
    # API call
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image-preview:generateContent"
    headers = {"x-goog-api-key": api_key, "Content-Type": "application/json"}

    print("🚀 Sending request to Gemini API...")
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"❌ Error during API call: {e}")
        sys.exit(1)

    print("🔄 Processing response...")
    try:
        response_data = response.json()
        print(f"🔍 Response data keys: {list(response_data.keys())}")
        
        # Extract the image data from the response - UPDATED CODE
        candidate = response_data['candidates'][0]
        content = candidate['content']
        
        # Search for the image data in all parts
        img_data_b64 = None
        for part in content['parts']:
            if 'inlineData' in part:
                img_data_b64 = part['inlineData']['data']
                break
        
        if not img_data_b64:
            print("❌ No image data found in response")
            print("Full API response:")
            print(json.dumps(response_data, indent=2))
            sys.exit(1)
            
        print(f"📏 Length of base64 data: {len(img_data_b64)}")

        try:
            decoded_img = base64.b64decode(img_data_b64)
            print(f"📏 Length of decoded image: {len(decoded_img)} bytes")
            with open(output_file, "wb") as f:
                f.write(decoded_img)
            print(f"📁 File written to: {output_file}")
        except binascii.Error as decode_e:
            print(f"❌ Error decoding base64 data from API response: {decode_e}")
            print("The API might have returned invalid base64 or text instead of an image.")
            sys.exit(1)
        except IOError as io_e:
            print(f"❌ Error writing to file {output_file}: {io_e}")
            sys.exit(1)

    except (KeyError, IndexError, TypeError) as e:
        print(f"❌ Could not extract image from response. Error: {e}")
        print("Full API response:")
        print(json.dumps(response_data, indent=2))
        sys.exit(1)

    # Verify output
    if os.path.isfile(output_file) and os.path.getsize(output_file) > 0:
        print("\n🎉 SUCCESS!")
        print(f"✅ Recreated image saved as: {output_file}")
        
        # Open file
        if sys.platform == "win32":
            os.startfile(output_file)
        elif sys.platform == "darwin":
            subprocess.run(["open", output_file])
        else:
            try:
                subprocess.run(["xdg-open", output_file])
            except FileNotFoundError:
                print(f"\n👁️ To view the image, open: {output_file}")

    else:
        print("❌ Error: Could not create output file or file is empty")
        print("API response received:")
        print(json.dumps(response.json(), indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()