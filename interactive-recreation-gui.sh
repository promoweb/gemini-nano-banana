#!/bin/bash

# ======================================================
# Gemini Interactive Image Recreation Tool (GUI Version)
# Based on working script with Zenity interface
# ======================================================

# GUI Header
zenity --info --title="Gemini Image Recreation Tool" --text="🔄 Starting Gemini Image Recreation Tool..." --width=400

# Check if zenity is available
if ! command -v zenity &> /dev/null; then
    echo "❌ Zenity is required but not installed. Please install it with: sudo apt-get install zenity"
    exit 1
fi

# API Key Configuration
USER_API_KEY=$(zenity --entry --title="API Key Configuration" --text="🔑 Enter your Gemini API key:" --entry-text="$GEMINI_API_KEY" --width=400)

if [[ -n "$USER_API_KEY" ]]; then
    API_KEY="$USER_API_KEY"
else
    API_KEY="your-api-key-here"
fi

# Input image file selection with zenity file browser
IMG_PATH=$(zenity --file-selection --title="Select Input Image" --file-filter="Image files (jpg,jpeg,png,gif,bmp,webp) | *.jpg *.jpeg *.png *.gif *.bmp *.webp" --width=600)

if [[ -z "$IMG_PATH" ]]; then
    zenity --error --text="No input image selected!" --width=300
    exit 1
fi

# Verify the image file exists
if [[ ! -f "$IMG_PATH" ]]; then
    zenity --error --text="❌ Error: The image file $IMG_PATH does not exist!" --width=400
    exit 1
fi

# Reference images selection
NUM_REF=$(zenity --list --title="Reference Images" --text="How many reference images?" --radiolist --column="Select" --column="Number" --column="Description" \
    TRUE "0" "No reference images" \
    FALSE "1" "One reference image" \
    FALSE "2" "Two reference images" --width=400)

if [[ -z "$NUM_REF" ]]; then
    NUM_REF=0
fi

REF1_PATH=""
REF2_PATH=""

for i in $(seq 1 $NUM_REF); do
    REF_PATH=$(zenity --file-selection --title="Select Reference Image $i" --file-filter="Image files | *.jpg *.jpeg *.png *.gif *.bmp *.webp" --width=600)

    if [[ -z "$REF_PATH" ]]; then
        zenity --error --text="No reference image selected!" --width=300
        exit 1
    fi

    # Verify the reference image file exists
    if [[ ! -f "$REF_PATH" ]]; then
        zenity --error --text="❌ Error: The reference image file $REF_PATH does not exist!" --width=400
        exit 1
    fi

    if [[ $i -eq 1 ]]; then
        REF1_PATH="$REF_PATH"
    elif [[ $i -eq 2 ]]; then
        REF2_PATH="$REF_PATH"
    fi
done

# Output file configuration
OUTPUT_OPTION=$(zenity --list --title="Output File Configuration" --text="Choose output location:" --radiolist --column="Select" --column="Option" --column="Description" \
    TRUE "auto_same" "Auto-generate in same directory as input" \
    FALSE "auto_current" "Auto-generate in current directory" \
    FALSE "custom" "Enter custom path" --width=500)

if [[ -z "$OUTPUT_OPTION" ]]; then
    OUTPUT_OPTION="auto_same"
fi

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
INPUT_DIR=$(dirname "$IMG_PATH")
INPUT_NAME=$(basename "$IMG_PATH" | cut -d. -f1)

case $OUTPUT_OPTION in
    "auto_same")
        OUTPUT_FILE="${INPUT_DIR}/${INPUT_NAME}_recreated_${TIMESTAMP}.jpg"
        ;;
    "auto_current")
        OUTPUT_FILE="./${INPUT_NAME}_recreated_${TIMESTAMP}.jpg"
        ;;
    "custom")
        OUTPUT_FILE=$(zenity --file-selection --title="Save Output As" --save --confirm-overwrite --filename="${INPUT_NAME}_recreated_${TIMESTAMP}.jpg" --file-filter="JPEG files | *.jpg *.jpeg" --width=600)
        if [[ -z "$OUTPUT_FILE" ]]; then
            zenity --error --text="No output file selected!" --width=300
            exit 1
        fi
        # Add extension if missing
        if [[ "$OUTPUT_FILE" != *.jpg && "$OUTPUT_FILE" != *.jpeg ]]; then
            OUTPUT_FILE="${OUTPUT_FILE}.jpg"
        fi
        ;;
esac

# Prompt customization
PROMPT_OPTION=$(zenity --list --title="Prompt Configuration" --text="Choose prompt option:" --radiolist --column="Select" --column="Option" --width=400 \
    TRUE "default" \
    FALSE "custom")

case $PROMPT_OPTION in
    "default")
        CUSTOM_PROMPT="Recreate a new very realistic, sharp and defined color image, high resolution, with current quality standards. As if it was taken by a digital reflex camera."
        ;;
    "custom")
        CUSTOM_PROMPT=$(zenity --entry --title="Custom Prompt" --text="💡 Examples:\n• Transform into artistic watercolor style\n• Recreate in vintage black and white\n• Enhance quality and increase sharpness\n• Transform into modern digital illustration" --entry-text="Recreate a new very realistic, sharp and defined color image, high resolution, with current quality standards." --width=500 --height=200)
        if [[ -z "$CUSTOM_PROMPT" ]]; then
            zenity --error --text="No prompt entered!" --width=300
            exit 1
        fi
        ;;
    *)
        CUSTOM_PROMPT="Recreate a new very realistic, sharp and defined color image, high resolution, with current quality standards."
        ;;
esac

# Configuration summary
SUMMARY="📋 CONFIGURATION SUMMARY:\n"
SUMMARY="${SUMMARY}\n   Input: $(basename "$IMG_PATH")"
if [[ -n "$REF1_PATH" ]]; then
    SUMMARY="${SUMMARY}\n   Reference 1: $(basename "$REF1_PATH")"
fi
if [[ -n "$REF2_PATH" ]]; then
    SUMMARY="${SUMMARY}\n   Reference 2: $(basename "$REF2_PATH")"
fi
SUMMARY="${SUMMARY}\n   Output: $(basename "$OUTPUT_FILE")"
SUMMARY="${SUMMARY}\n   Prompt: ${CUSTOM_PROMPT:0:50}..."

if ! zenity --question --title="Confirm Configuration" --text="$SUMMARY" --ok-label="🚀 Proceed" --cancel-label="❌ Cancel" --width=600; then
    zenity --info --text="❌ Operation cancelled" --width=300
    exit 0
fi

# Progress dialog setup
(
echo "10" ; echo "# 🔄 Starting recreation process..."
sleep 0.5

# System detection for base64 flags
if [[ "$(base64 --version 2>&1)" = *"FreeBSD"* ]]; then
    B64FLAGS="--input"
else
    B64FLAGS="-w0"
fi

echo "20" ; echo "# 📸 Encoding image to base64..."
IMG_BASE64=$(base64 $B64FLAGS "$IMG_PATH" 2>&1)

if [[ $? -ne 0 ]]; then
    echo "100" ; echo "# ❌ Error during base64 encoding!"
    exit 1
fi

# Encode reference images if selected
if [[ -n "$REF1_PATH" ]]; then
    echo "30" ; echo "# 📸 Encoding reference 1 to base64..."
    REF1_BASE64=$(base64 $B64FLAGS "$REF1_PATH" 2>&1)
    if [[ $? -ne 0 ]]; then
        echo "100" ; echo "# ❌ Error during base64 encoding for reference 1!"
        exit 1
    fi
fi

if [[ -n "$REF2_PATH" ]]; then
    echo "40" ; echo "# 📸 Encoding reference 2 to base64..."
    REF2_BASE64=$(base64 $B64FLAGS "$REF2_PATH" 2>&1)
    if [[ $? -ne 0 ]]; then
        echo "100" ; echo "# ❌ Error during base64 encoding for reference 2!"
        exit 1
    fi
fi

echo "50" ; echo "# 🚀 Sending request to Gemini API..."

# Create JSON payload in temporary file (same as original)
TEMP_JSON=$(mktemp)
PARTS="        {\"text\": \"$CUSTOM_PROMPT\"},"
PARTS="$PARTS"$'\n'"        {"$'\n'"          \"inline_data\": {"$'\n'"            \"mime_type\":\"image/jpeg\","$'\n'"            \"data\": \"$IMG_BASE64"\"$'\n'"          }"$'\n'"        }"

if [[ -n "$REF1_BASE64" ]]; then
    PARTS="$PARTS"$',\n'"        {"$'\n'"          \"inline_data\": {"$'\n'"            \"mime_type\":\"image/jpeg\","$'\n'"            \"data\": \"$REF1_BASE64"\"$'\n'"          }"$'\n'"        }"
fi

if [[ -n "$REF2_BASE64" ]]; then
    PARTS="$PARTS"$',\n'"        {"$'\n'"          \"inline_data\": {"$'\n'"            \"mime_type\":\"image/jpeg\","$'\n'"            \"data\": \"$REF2_BASE64"\"$'\n'"          }"$'\n'"        }"
fi

cat > "$TEMP_JSON" << EOF
{
  "contents": [{
    "parts":[
${PARTS}
    ]
  }]
}
EOF

echo "60" ; echo "# 🔄 Processing API response..."

# API call to Gemini
RESPONSE=$(curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image-preview:generateContent" \
    -H "x-goog-api-key: $API_KEY" \
    -H 'Content-Type: application/json' \
    -d @"$TEMP_JSON")

# Cleanup temporary file
rm -f "$TEMP_JSON"

# Verify curl succeeded
if [[ $? -ne 0 ]]; then
    echo "100" ; echo "# ❌ Error during API call!"
    exit 1
fi

echo "80" ; echo "# 🔄 Extracting image from response..."

# Extract and decode image from response (same logic)
IMG_DATA=$(echo "$RESPONSE" | grep -o '"data": "[^"]*"' | cut -d'"' -f4)

if [[ -n "$IMG_DATA" ]]; then
    echo "$IMG_DATA" | base64 --decode > "$OUTPUT_FILE"
    echo "95" ; echo "# 📁 File written successfully..."
else
    echo "100" ; echo "# ❌ Could not extract image from response"
    exit 1
fi

# Verify output file was created
if [[ -f "$OUTPUT_FILE" && -s "$OUTPUT_FILE" ]]; then
    echo "100" ; echo "# 🎉 SUCCESS!"
    sleep 0.5
else
    echo "100" ; echo "# ❌ Error: Could not create output file"
    exit 1
fi

) | zenity --progress --title="Gemini Image Recreation" --text="Starting..." --percentage=0 --auto-close --width=400

# Check the exit status of the subshell
if [[ ${PIPESTATUS[0]} -ne 0 ]]; then
    zenity --error --text="❌ Generation failed!" --width=300
    exit 1
fi

# Success notification
zenity --info --title="Success!" --text="🎉 SUCCESS!\n✅ Recreated image saved as: $(basename "$OUTPUT_FILE")\n\n👁️ Opening file..." --width=400

# Open the output file
if command -v xdg-open &> /dev/null; then
    xdg-open "$OUTPUT_FILE" &>/dev/null &
elif command -v eog &> /dev/null; then
    eog "$OUTPUT_FILE" &>/dev/null &
fi

exit 0
