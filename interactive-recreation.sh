#!/bin/bash

# ======================================================
# Gemini Interactive Image Recreation Tool
# Interactive version of your working script
# ======================================================

echo "======================================="
echo "  Gemini Image Recreation Tool"
echo "======================================="

# API Key Configuration
read -rp "🔑 Enter your Gemini API key (leave empty to use the default one): " USER_API_KEY
if [[ -n "$USER_API_KEY" ]]; then
    API_KEY="$USER_API_KEY"
elif [[ -n "$GEMINI_API_KEY" ]]; then
    API_KEY="$GEMINI_API_KEY"
else
    API_KEY="your-api-key-here"  # Your default key
fi

# Input image file selection
echo ""
echo "📁 Input image file selection:"
echo "1) Enter path manually"
echo "2) Select from current directory"
echo "3) Select from Documents directory"

read -rp "➡ Choose an option (1-3): " INPUT_OPTION

case $INPUT_OPTION in
    1)
        read -rp "📂 Enter the full image file path: " IMG_PATH
        ;;
    2)
        echo "📂 Image files in current directory:"
        ls -1 *.{jpg,jpeg,png,gif,bmp,webp} 2>/dev/null | nl -w2 -s') ' || echo "No image files found"
        echo ""
        read -rp "📝 Enter the filename: " FILENAME
        IMG_PATH="./$FILENAME"
        ;;
    3)
        DOCS_DIR="$HOME/Documents"
        if [[ -d "$DOCS_DIR" ]]; then
            echo "📂 Image files in $DOCS_DIR:"
            ls -1 "$DOCS_DIR"/*.{jpg,jpeg,png,gif,bmp,webp} 2>/dev/null | xargs -I {} basename {} | nl -w2 -s') ' || echo "No image files found"
            echo ""
            read -rp "📝 Enter the filename: " FILENAME
            IMG_PATH="$DOCS_DIR/$FILENAME"
        else
            echo "❌ Documents directory not found"
            read -rp "📂 Enter the full path: " IMG_PATH
        fi
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

# Verify the image file exists
if [[ ! -f "$IMG_PATH" ]]; then
    echo "❌ Error: The image file $IMG_PATH does not exist!"
    exit 1
fi

echo "✅ Selected file: $IMG_PATH"

# Reference images selection
echo ""
echo "📸 Reference images selection:"
echo "0) No reference images"
echo "1) One reference image"
echo "2) Two reference images"

read -rp "➡ Enter number of reference images (0-2): " NUM_REF

REF1_PATH=""
REF2_PATH=""
REF1_BASE64=""
REF2_BASE64=""

for i in $(seq 1 $NUM_REF); do
    echo ""
    echo "📁 Reference image $i file selection:"
    echo "1) Enter path manually"
    echo "2) Select from current directory"
    echo "3) Select from Documents directory"

    read -rp "➡ Choose an option (1-3): " REF_OPTION

    case $REF_OPTION in
        1)
            read -rp "📂 Enter the full image file path: " REF_PATH
            ;;
        2)
            echo "📂 Image files in current directory:"
            ls -1 *.{jpg,jpeg,png,gif,bmp,webp} 2>/dev/null | nl -w2 -s') ' || echo "No image files found"
            echo ""
            read -rp "📝 Enter the filename: " FILENAME
            REF_PATH="./$FILENAME"
            ;;
        3)
            DOCS_DIR="$HOME/Documents"
            if [[ -d "$DOCS_DIR" ]]; then
                echo "📂 Image files in $DOCS_DIR:"
                ls -1 "$DOCS_DIR"/*.{jpg,jpeg,png,gif,bmp,webp} 2>/dev/null | xargs -I {} basename {} | nl -w2 -s') ' || echo "No image files found"
                echo ""
                read -rp "📝 Enter the filename: " FILENAME
                REF_PATH="$DOCS_DIR/$FILENAME"
            else
                echo "❌ Documents directory not found"
                read -rp "📂 Enter the full path: " REF_PATH
            fi
            ;;
        *)
            echo "❌ Invalid option"
            exit 1
            ;;
    esac

    # Verify the reference image file exists
    if [[ ! -f "$REF_PATH" ]]; then
        echo "❌ Error: The reference image file $REF_PATH does not exist!"
        exit 1
    fi

    echo "✅ Selected reference $i: $REF_PATH"

    if [[ $i -eq 1 ]]; then
        REF1_PATH="$REF_PATH"
    elif [[ $i -eq 2 ]]; then
        REF2_PATH="$REF_PATH"
    fi
done

# Output file configuration
echo ""
echo "💾 Output file configuration:"
echo "1) Auto-generate name in the same directory as input"
echo "2) Auto-generate name in current directory"
echo "3) Enter custom path"

read -rp "➡ Choose an option (1-3): " OUTPUT_OPTION

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
INPUT_DIR=$(dirname "$IMG_PATH")
INPUT_NAME=$(basename "$IMG_PATH" | cut -d. -f1)

case $OUTPUT_OPTION in
    1)
        OUTPUT_FILE="${INPUT_DIR}/${INPUT_NAME}_recreated_${TIMESTAMP}.jpg"
        ;;
    2)
        OUTPUT_FILE="./${INPUT_NAME}_recreated_${TIMESTAMP}.jpg"
        ;;
    3)
        read -rp "📂 Enter the full output file path: " OUTPUT_FILE
        # Add extension if missing
        if [[ "$OUTPUT_FILE" != *.jpg && "$OUTPUT_FILE" != *.jpeg ]]; then
            OUTPUT_FILE="${OUTPUT_FILE}.jpg"
        fi
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo "✅ Output file: $OUTPUT_FILE"

# Prompt customization
echo ""
echo "📝 Prompt customization:"
echo "1) Use default prompt (realistic recreation)"
echo "2) Enter custom prompt"

read -rp "➡ Choose an option (1-2): " PROMPT_OPTION

case $PROMPT_OPTION in
    1)
        CUSTOM_PROMPT="Recreate a new very realistic, sharp and defined color image, high resolution, with current quality standards. As if it was taken by a digital reflex camera."
        ;;
    2)
        echo "💡 Prompt examples:"
        echo "   - 'Transform into artistic watercolor style'"
        echo "   - 'Recreate in vintage black and white'"
        echo "   - 'Enhance quality and increase sharpness'"
        echo "   - 'Transform into modern digital illustration'"
        echo ""
        read -rp "📝 Enter your prompt: " CUSTOM_PROMPT
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

# Configuration summary
echo ""
echo "📋 CONFIGURATION SUMMARY:"
echo "   Input:  $IMG_PATH"
if [[ -n "$REF1_PATH" ]]; then
    echo "   Reference 1: $REF1_PATH"
fi
if [[ -n "$REF2_PATH" ]]; then
    echo "   Reference 2: $REF2_PATH"
fi
echo "   Output: $OUTPUT_FILE"
echo "   Prompt: $CUSTOM_PROMPT"
echo ""

read -rp "🚀 Proceed with generation? (y/N): " CONFIRM
if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
    echo "❌ Operation cancelled"
    exit 0
fi

echo ""
echo "🔄 Starting recreation process..."

# System detection for base64 flags
if [[ "$(base64 --version 2>&1)" = *"FreeBSD"* ]]; then
    B64FLAGS="--input"
else
    B64FLAGS="-w0"
fi

# Image base64 encoding
echo "📸 Encoding image to base64..."
IMG_BASE64=$(base64 $B64FLAGS "$IMG_PATH" 2>&1)

# Verify encoding succeeded
if [[ $? -ne 0 ]]; then
    echo "❌ Error during base64 encoding!"
    exit 1
fi

# Encode reference images if selected
if [[ -n "$REF1_PATH" ]]; then
    echo "📸 Encoding reference 1 to base64..."
    REF1_BASE64=$(base64 $B64FLAGS "$REF1_PATH" 2>&1)
    if [[ $? -ne 0 ]]; then
        echo "❌ Error during base64 encoding for reference 1!"
        exit 1
    fi
fi

if [[ -n "$REF2_PATH" ]]; then
    echo "📸 Encoding reference 2 to base64..."
    REF2_BASE64=$(base64 $B64FLAGS "$REF2_PATH" 2>&1)
    if [[ $? -ne 0 ]]; then
        echo "❌ Error during base64 encoding for reference 2!"
        exit 1
    fi
fi

# Create JSON payload in temporary file
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

# API call to Gemini using temporary file
echo "🚀 Sending request to Gemini API..."
RESPONSE=$(curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image-preview:generateContent" \
    -H "x-goog-api-key: $API_KEY" \
    -H 'Content-Type: application/json' \
    -d @"$TEMP_JSON")

# Cleanup temporary file
rm -f "$TEMP_JSON"

# Verify curl succeeded
if [[ $? -ne 0 ]]; then
    echo "❌ Error during API call!"
    exit 1
fi

# Optional debug
if [[ "${DEBUG:-}" == "1" ]]; then
    echo "🔍 Full API response:"
    echo "$RESPONSE"
    echo ""
fi

# Extract and decode image from response
echo "🔄 Processing response..."

# First try with grep (original method)
IMG_DATA=$(echo "$RESPONSE" | grep -o '"data": "[^"]*"' | cut -d'"' -f4)

if [[ -n "$IMG_DATA" ]]; then
    echo "$IMG_DATA" | base64 --decode > "$OUTPUT_FILE"
else
    # If grep fails, try alternative approach
    echo "⚠️ Grep method failed, trying alternative approach..."
    
    # Check for error response or text-only response
    if echo "$RESPONSE" | grep -q '"text":'; then
        echo "📝 Text response received:"
        echo "$RESPONSE" | grep -o '"text": "[^"]*"' | cut -d'"' -f4
        echo ""
        echo "💡 The model responded with text instead of generating an image."
        echo "   This could mean:"
        echo "   - The request couldn't be processed"
        echo "   - Model has limitations for this content type"
        echo "   - API key might not have image generation access"
    fi
    
    echo "❌ Could not extract image from response"
    echo "Full API response:"
    echo "$RESPONSE"
    exit 1
fi

# Verify output file was created
if [[ -f "$OUTPUT_FILE" && -s "$OUTPUT_FILE" ]]; then
    echo ""
    echo "🎉 SUCCESS!"
    echo "✅ Recreated image saved as: $OUTPUT_FILE"
    
    # Show file information
    if command -v du >/dev/null 2>&1; then
        echo "📊 File size: $(du -h "$OUTPUT_FILE" | cut -f1)"
    fi
    
    if command -v identify >/dev/null 2>&1; then
        echo "📊 Image details: $(identify "$OUTPUT_FILE" 2>/dev/null || echo 'N/A')"
    fi
    
    # Suggestion to open file
    echo ""
    echo "👁️  To view the image:"
    echo "   xdg-open \"$OUTPUT_FILE\""
    echo "   or"
    echo "   eog \"$OUTPUT_FILE\""
    xdg-open "$OUTPUT_FILE"
    
else
    echo "❌ Error: Could not create output file or file is empty"
    echo "API response received:"
    echo "$RESPONSE"
    exit 1
fi
