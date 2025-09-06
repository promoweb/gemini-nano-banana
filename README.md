# Gemini Interactive Image Recreation Tool

This repository contains **four implementations** (2 CLI + 2 GUI) of a tool that uses Google's Gemini AI to recreate and enhance images. All versions provide intuitive interfaces for image processing with support for reference images and custom prompts.

## Files

### CLI Versions
- `interactive_recreation.py` - Python CLI implementation
- `interactive-recreation.sh` - Bash CLI script implementation

### GUI Versions
- `interactive_recreation_gui.py` - Python GUI implementation (CustomTkinter)
- `interactive_recreation_gui.sh` - Bash GUI script implementation (Zenity)

## Features

- **Interactive Image Selection**: Choose input images from current directory, Documents folder, or specify custom paths
- **Reference Images**: Add up to 2 reference images to guide the recreation process
- **Customizable Prompts**: Use the default prompt for realistic recreation or create your own custom prompt
- **Flexible Output**: Configure output location and naming patterns
- **API Key Management**: Support for environment variables or user input
- **Cross-platform Compatibility**: Works on Windows, macOS, and Linux

## Requirements

### Python CLI Version (`interactive_recreation.py`)

**Required Python modules:**
- `requests` (install with: `pip install requests`)

**System requirements:**
- Python 3.6+
- Internet connection for Gemini API access

### Python GUI Version (`interactive_recreation_gui.py`)

**Required Python modules:**
- `requests` (install with: `pip install requests`)
- `customtkinter` (install with: `pip install customtkinter`)
- `Pillow` (install with: `pip install Pillow`)

**System requirements:**
- Python 3.6+
- Display server (X11 on Linux)
- Tkinter support
- Internet connection for Gemini API access

### Bash CLI Version (`interactive-recreation.sh`)

**System tools:**
- `bash` (Unix/Linux shell)
- `curl` (for API requests)
- `base64` (for image encoding)
- `grep` (for response parsing)
- Internet connection for Gemini API access

### Bash GUI Version (`interactive-recreation_gui.sh`)

**System tools:**
- `bash` (Unix/Linux shell)
- `curl` (for API requests)
- `base64` (for image encoding)
- `grep` (for response parsing)
- `zenity` (for GUI dialogs)
- Display server (X11 on Linux)
- Internet connection for Gemini API access

## Installation

### Python CLI Setup
1. Ensure Python 3.6+ is installed
2. Install required module:
   ```bash
   pip install requests
   ```

### Python GUI Setup
1. Ensure Python 3.6+ is installed
2. Install required modules:
   ```bash
   pip install requests customtkinter Pillow
   ```
3. Ensure Tkinter is available (usually pre-installed on most systems)

### Bash CLI Setup
1. Ensure bash is available (typically pre-installed on Linux/macOS)
2. Verify required tools are installed (curl, base64, grep)
3. Make script executable:
   ```bash
   chmod +x interactive-recreation.sh
   ```

### Bash GUI Setup
1. Ensure bash is available (typically pre-installed on Linux/macOS)
2. Install Zenity GUI toolkit:
   ```bash
   sudo apt-get install zenity
   ```
3. Verify required tools are installed (curl, base64, grep)
4. Make script executable:
   ```bash
   chmod +x interactive-recreation_gui.sh
   ```

## Usage

### CLI Versions
Both CLI versions provide interactive console menus for configuration. Run either script and follow the prompts.

**Python CLI:**
```bash
python3 interactive_recreation.py
```

**Bash CLI:**
```bash
./interactive-recreation.sh
```

### GUI Versions
Both GUI versions provide modern desktop interfaces with file browsers, progress bars, and visual feedback.

**Python GUI (CustomTkinter):**
```bash
python3 interactive_recreation_gui.py
```

**Bash GUI (Zenity):**
```bash
./interactive-recreation_gui.sh
```

**GUI Features:**
- Native file selection dialogs
- Real-time image preview (Python GUI only)
- Progress bar during processing
- Error messages in popup dialogs
- Automatic file opening after generation

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

### Python CLI Issues
- **ImportError**: Install missing modules with `pip install requests`
- **File not found**: Ensure image paths are correct and accessible

### Python GUI Issues
- **ModuleNotFoundError**: Install required modules with `pip install customtkinter Pillow`
- **tkinter not found**: Ensure Python Tkinter is installed (`sudo apt-get install python3-tk`)
- **Display issues**: Ensure X11/display server is running
- **No GUI appears**: Check if running in headless environment

### Bash CLI Issues
- **Command not found**: Ensure curl, base64, and grep are installed
- **Permission denied**: Make script executable with `chmod +x`

### Bash GUI Issues
- **zenity not found**: Install with `sudo apt-get install zenity`
- **GUI not appearing**: Ensure DISPLAY variable is set and X11 is running
- **zenity command failed**: Check if running in GUI environment

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
