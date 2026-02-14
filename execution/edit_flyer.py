#!/usr/bin/env python3
"""
Flyer Editing Tool
==================
Edit existing flyers by adding text overlays, contact info blocks, and QR codes.

Usage:
    # Add contact info to a flyer
    python edit_flyer.py input.heic output.png --contact-block \
        --name "Carson Goff" \
        --phone "(208) 353-0597" \
        --email "vibenthrivevibroacoustics@gmail.com" \
        --address "10580 SW McDonald St. Suite #205, Tigard, OR 97224"

    # Add custom text overlays
    python edit_flyer.py input.jpg output.png --overlay "Hello World" --x 100 --y 50 --font-size 24

    # Use a config file for complex edits
    python edit_flyer.py input.heic output.png --config edits.json

Dependencies:
    pip install Pillow pillow-heif qrcode
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Pillow is required. Install with: pip install Pillow")
    sys.exit(1)

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
    HEIF_SUPPORT = True
except ImportError:
    HEIF_SUPPORT = False
    print("Warning: pillow-heif not installed. HEIC files won't be supported.")
    print("Install with: pip install pillow-heif")


# Default fonts to try (in order of preference)
DEFAULT_FONTS = [
    # macOS fonts
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/SFNSText.ttf",
    "/Library/Fonts/Arial.ttf",
    # Linux fonts
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/TTF/DejaVuSans.ttf",
    # Windows fonts
    "C:/Windows/Fonts/arial.ttf",
    # Fallback
    None  # Will use default bitmap font
]

# Brand colors for Vibe'N Thrive
BRAND_COLORS = {
    "navy": "#1a5276",
    "teal": "#148f77",
    "dark_teal": "#0d6655",
    "gray": "#5d6d7e",
    "dark_gray": "#2c3e50",
    "black": "#000000",
}


def find_font(font_path: Optional[str] = None, font_size: int = 14) -> ImageFont.FreeTypeFont:
    """Find and load a font, with fallbacks."""
    if font_path and Path(font_path).exists():
        try:
            return ImageFont.truetype(font_path, font_size)
        except Exception:
            pass

    for font in DEFAULT_FONTS:
        if font is None:
            # Use default bitmap font
            return ImageFont.load_default()
        try:
            if Path(font).exists():
                return ImageFont.truetype(font, font_size)
        except Exception:
            continue

    return ImageFont.load_default()


def hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def load_image(path: str) -> Image.Image:
    """Load an image file, supporting HEIC, JPEG, PNG, etc."""
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")

    suffix = path.suffix.lower()

    if suffix in ['.heic', '.heif'] and not HEIF_SUPPORT:
        raise ImportError(
            "HEIC support requires pillow-heif. Install with: pip install pillow-heif"
        )

    img = Image.open(path)

    # Convert to RGB if necessary (e.g., from RGBA or palette mode)
    if img.mode not in ['RGB', 'RGBA']:
        img = img.convert('RGB')

    return img


def add_text_overlay(
    img: Image.Image,
    text: str,
    x: int,
    y: int,
    font_size: int = 14,
    font_path: Optional[str] = None,
    color: str = "#000000",
    align: str = "left",
    max_width: Optional[int] = None,
) -> Image.Image:
    """Add a text overlay to an image."""
    img = img.copy()
    draw = ImageDraw.Draw(img)
    font = find_font(font_path, font_size)

    # Resolve color
    if color in BRAND_COLORS:
        color = BRAND_COLORS[color]
    rgb_color = hex_to_rgb(color) if color.startswith('#') else color

    # Handle text wrapping if max_width is specified
    if max_width:
        lines = wrap_text(text, font, max_width, draw)
        text = '\n'.join(lines)

    # Calculate text bounding box for alignment
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]

    # Adjust x position based on alignment
    if align == "center":
        x = x - text_width // 2
    elif align == "right":
        x = x - text_width

    draw.text((x, y), text, font=font, fill=rgb_color)

    return img


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.Draw) -> list:
    """Wrap text to fit within max_width."""
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        width = bbox[2] - bbox[0]

        if width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]

    if current_line:
        lines.append(' '.join(current_line))

    return lines


def add_contact_block(
    img: Image.Image,
    name: Optional[str] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    address: Optional[str] = None,
    x: int = None,
    y: int = None,
    align: str = "right",
    font_path: Optional[str] = None,
    name_color: str = "navy",
    phone_color: str = "teal",
    email_color: str = "gray",
    address_color: str = "gray",
    line_spacing: int = None,
    name_size: int = None,
    detail_size: int = None,
    auto_scale: bool = True,
) -> Image.Image:
    """Add a contact information block to the flyer."""

    # Auto-scale font sizes based on image dimensions
    if auto_scale:
        scale = img.width / 600  # Base scale on 600px width
        if name_size is None:
            name_size = int(20 * scale)
        if detail_size is None:
            detail_size = int(16 * scale)
        if line_spacing is None:
            line_spacing = int(24 * scale)
    else:
        name_size = name_size or 14
        detail_size = detail_size or 12
        line_spacing = line_spacing or 18

    # Default position: top-right area (typical for business flyers)
    if x is None:
        x = img.width - int(25 * (img.width / 600)) if align == "right" else 20
    if y is None:
        y = int(150 * (img.height / 1000))  # Below typical header area

    current_y = y

    if name:
        img = add_text_overlay(
            img, name, x, current_y,
            font_size=name_size, font_path=font_path,
            color=name_color, align=align
        )
        current_y += line_spacing

    if phone:
        img = add_text_overlay(
            img, phone, x, current_y,
            font_size=detail_size, font_path=font_path,
            color=phone_color, align=align
        )
        current_y += line_spacing

    if email:
        img = add_text_overlay(
            img, email, x, current_y,
            font_size=detail_size - 1, font_path=font_path,
            color=email_color, align=align
        )
        current_y += line_spacing

    if address:
        img = add_text_overlay(
            img, address, x, current_y,
            font_size=detail_size - 2, font_path=font_path,
            color=address_color, align=align
        )

    return img


def add_qr_code(
    img: Image.Image,
    data: str,
    x: int,
    y: int,
    size: int = 100,
    border: int = 2,
) -> Image.Image:
    """Add or replace a QR code on the flyer."""
    try:
        import qrcode
    except ImportError:
        print("Warning: qrcode not installed. Skipping QR code.")
        print("Install with: pip install qrcode")
        return img

    img = img.copy()

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img = qr_img.resize((size, size), Image.Resampling.LANCZOS)

    # Paste QR code onto flyer
    if qr_img.mode != 'RGB':
        qr_img = qr_img.convert('RGB')

    img.paste(qr_img, (x, y))

    return img


def process_config(img: Image.Image, config: dict) -> Image.Image:
    """Process a config dictionary with multiple edits."""

    # Add contact block if specified
    if 'contact_block' in config:
        cb = config['contact_block']
        img = add_contact_block(
            img,
            name=cb.get('name'),
            phone=cb.get('phone'),
            email=cb.get('email'),
            address=cb.get('address'),
            x=cb.get('x'),
            y=cb.get('y'),
            align=cb.get('align', 'right'),
            font_path=cb.get('font_path'),
            name_color=cb.get('name_color', 'navy'),
            phone_color=cb.get('phone_color', 'teal'),
            email_color=cb.get('email_color', 'gray'),
            address_color=cb.get('address_color', 'gray'),
            line_spacing=cb.get('line_spacing', 18),
            name_size=cb.get('name_size', 14),
            detail_size=cb.get('detail_size', 12),
        )

    # Add text overlays
    for overlay in config.get('overlays', []):
        img = add_text_overlay(
            img,
            text=overlay['text'],
            x=overlay['x'],
            y=overlay['y'],
            font_size=overlay.get('font_size', 14),
            font_path=overlay.get('font_path'),
            color=overlay.get('color', '#000000'),
            align=overlay.get('align', 'left'),
            max_width=overlay.get('max_width'),
        )

    # Add QR codes
    for qr in config.get('qr_codes', []):
        img = add_qr_code(
            img,
            data=qr['data'],
            x=qr['x'],
            y=qr['y'],
            size=qr.get('size', 100),
            border=qr.get('border', 2),
        )

    return img


def save_image(img: Image.Image, path: str, quality: int = 95):
    """Save image to file, determining format from extension."""
    path = Path(path)
    suffix = path.suffix.lower()

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    if suffix == '.jpg' or suffix == '.jpeg':
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        img.save(path, 'JPEG', quality=quality)
    elif suffix == '.png':
        img.save(path, 'PNG')
    elif suffix == '.pdf':
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        img.save(path, 'PDF', resolution=300)
    else:
        img.save(path)

    print(f"Saved: {path}")


def main():
    parser = argparse.ArgumentParser(
        description='Edit flyers by adding text overlays, contact info, and QR codes.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add contact info to a flyer
  python edit_flyer.py input.heic output.png --contact-block \\
      --name "Carson Goff" --phone "(208) 353-0597"

  # Add a single text overlay
  python edit_flyer.py input.jpg output.png --overlay "Sale!" --x 50 --y 100

  # Use a JSON config file
  python edit_flyer.py input.heic output.png --config edits.json
        """
    )

    parser.add_argument('input', help='Input image file (HEIC, JPEG, PNG)')
    parser.add_argument('output', help='Output image file (JPEG, PNG, PDF)')

    # Contact block options
    contact_group = parser.add_argument_group('Contact Block')
    contact_group.add_argument('--contact-block', action='store_true',
                               help='Add a contact information block')
    contact_group.add_argument('--name', help='Contact name')
    contact_group.add_argument('--phone', help='Phone number')
    contact_group.add_argument('--email', help='Email address')
    contact_group.add_argument('--address', help='Physical address')
    contact_group.add_argument('--contact-x', type=int, help='X position for contact block')
    contact_group.add_argument('--contact-y', type=int, help='Y position for contact block')
    contact_group.add_argument('--contact-align', choices=['left', 'center', 'right'],
                               default='right', help='Contact block alignment')

    # Text overlay options
    overlay_group = parser.add_argument_group('Text Overlay')
    overlay_group.add_argument('--overlay', help='Text to overlay')
    overlay_group.add_argument('--x', type=int, help='X position')
    overlay_group.add_argument('--y', type=int, help='Y position')
    overlay_group.add_argument('--font-size', type=int, default=14, help='Font size')
    overlay_group.add_argument('--color', default='#000000', help='Text color (hex or name)')
    overlay_group.add_argument('--align', choices=['left', 'center', 'right'],
                               default='left', help='Text alignment')

    # Config file
    parser.add_argument('--config', help='JSON config file with multiple edits')

    # Output options
    parser.add_argument('--quality', type=int, default=95, help='JPEG quality (1-100)')

    args = parser.parse_args()

    # Load image
    print(f"Loading: {args.input}")
    img = load_image(args.input)
    print(f"Image size: {img.width}x{img.height}")

    # Process config file if provided
    if args.config:
        with open(args.config) as f:
            config = json.load(f)
        img = process_config(img, config)

    # Add contact block if requested
    if args.contact_block or any([args.name, args.phone, args.email, args.address]):
        img = add_contact_block(
            img,
            name=args.name,
            phone=args.phone,
            email=args.email,
            address=args.address,
            x=args.contact_x,
            y=args.contact_y,
            align=args.contact_align,
        )

    # Add text overlay if provided
    if args.overlay:
        if args.x is None or args.y is None:
            parser.error("--overlay requires --x and --y positions")
        img = add_text_overlay(
            img,
            text=args.overlay,
            x=args.x,
            y=args.y,
            font_size=args.font_size,
            color=args.color,
            align=args.align,
        )

    # Save output
    save_image(img, args.output, quality=args.quality)


if __name__ == '__main__':
    main()
