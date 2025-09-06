# Gemini Interactive Image Recreation Tool

This repository contains two implementations of a tool that uses Google's Gemini AI to recreate and enhance images. Both versions provide an interactive interface for image processing with support for reference images and custom prompts.

## Files

- `interactive_recreation.py` - Python implementation
- `interactive-recreation.sh` - Bash script implementation

## Features

- **Interactive Image Selection**: Choose input images from current directory, Documents folder, or specify custom paths
- **Reference Images**: Add up to 2 reference images to guide the recreation process
- **Customizable Prompts**: Use the default prompt for realistic recreation or create your own custom prompt
- **Flexible Output**: Configure output location and naming patterns
- **API Key Management**: Support for environment variables or user input
- **Cross-platform Compatibility**: Works on Windows, macOS, and Linux

## Requirements

### Python Version (`interactive_recreation.py`)

**Required Python modules:**
- `requests` (install with: `pip install requests`)

**System requirements:**
- Python 3.6+
- Internet connection for Gemini API access

### Bash Version (`interactive-recreation.sh`)

**System tools:**
- `bash` (Unix/Linux shell)
- `curl` (for API requests)
- `base64` (for image encoding)
- `grep` (for response parsing)
- Internet connection for Gemini API access

## Installation

### Python Setup
1. Ensure Python 3.6+ is installed
2. Install required module:
   ```bash
   pip install requests
   ```

### Bash Setup
1. Ensure bash is available (typically pre-installed on Linux/macOS)
2. Verify required tools are installed (curl, base64, grep)
3. Make script executable:
   ```bash
   chmod +x interactive-recreation.sh
   ```

## Usage

Both versions provide interactive menus for configuration. Run either script and follow the prompts.

### Python Version
```bash
python3 interactive_recreation.py
```

### Bash Version
```bash
./interactive-recreation.sh
```

## How It Works

1. **Input Selection**: Choose the source image to recreate
2. **Reference Images**: Optionally add 1-2 reference images for style guidance
3. **Prompt Configuration**: Select default prompt or enter custom instructions
4. **Output Setup**: Configure where and how to save the recreated image
5. **Processing**: Images are encoded to base64, sent to Gemini API, and response is decoded back to image format

## API Key Configuration

### Environment Variable (Recommended for Bash)
```bash
export GEMINI_API_KEY="your-api-key-here"
```

### Interactive Input
You can enter the API key when prompted by the script.

### Default Key
Both scripts include a default API key for testing purposes.

## Examples

### Default Demonstration
For a realistic, high-quality image recreation:
- Select any input image
- Use 0 reference images
- Choose option 1 for "Use default prompt"
- Output will be saved as `{input_name}_recreated_{timestamp}.jpg`

### Custom Style Transformation
To apply artistic effects:
1. Select input image
2. Choose "Enter custom prompt" (option 2)
3. Enter a prompt like: "Transform into artistic watercolor style"
4. Configure output path
5. Process the image

## Supported Image Formats

**Input formats:**
- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- BMP (.bmp)
- WebP (.webp)

**Output format:**
- JPEG (.jpg)

## Error Handling

Both implementations include comprehensive error handling for:
- Missing or invalid image files
- API connection issues
- Failed image encoding/decoding
- Invalid user inputs

## Troubleshooting

### Python Issues
- **ImportError**: Install missing modules with `pip install requests`
- **File not found**: Ensure image paths are correct and accessible

### Bash Issues
- **Command not found**: Ensure curl, base64, and grep are installed
- **Permission denied**: Make script executable with `chmod +x`

### Common API Issues
- **Invalid API key**: Verify your Gemini API key is valid and has proper permissions
- **Rate limiting**: Wait a moment before retrying if you hit API rate limits
- **Network errors**: Ensure stable internet connection

## License

This project is licensed under the GNU General Public License v2.0 - see the [GPL-2.0](https://www.gnu.org/licenses/gpl-2.0.html) for details.

```
Copyright (C) 2025 Emilo Petrozzi

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
```

## Author

**Emilo Petrozzi**
- Website: [https://mrtux.it](https://mrtux.it)

## Contributing

Feel free to submit issues and enhancement requests.

## Disclaimer

This tool uses Google's Gemini API. Ensure you comply with their terms of service and usage policies. The default API key provided is for demonstration purposes only - use your own API key for production use.
