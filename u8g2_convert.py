# Repository for this tool: https://github.com/mahbird/u8g2-chinese-convert-tool-py/
# This is a modified version of the powershell tool from https://blog.darkthread.net/blog/u8g2-cht-font-tool/
# If you download the whole u8g2 library, put this in tool/font
# Otherwise, just copy the tool/font/bdfconv folder to the directory this file is in (The whole foler as is)

import argparse
import pathlib
import re
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(
        description=" Creates font.c files from .bdf and source characters.\n\n"
                    " Usage example:\n"
                    " python convert.py -i path/to/font.bdf -s path/to/include_char.txt -n fontname\n\n"
                    " Font.c is output in: converted_fonts/u8g2_font_<fontname>.c"
    )
    parser.add_argument("-i", "--input", required=True, help="Input BDF font path")
    parser.add_argument("-s", "--source", required=True, help="Source text file for characters")
    parser.add_argument("-n", "--name", required=True, help="Font name for bdfconv")
    args = parser.parse_args()

    # Output file is at converted_fonts/u8g2_font_<fontname>.c
    build_dir = pathlib.Path("./converted_fonts")
    build_dir.mkdir(parents=True, exist_ok=True)
    output_font_c = build_dir / f"u8g2_font_{args.name}.c"

    bdf_font = pathlib.Path(args.input)
    src_file = pathlib.Path(args.source)
    map_file = pathlib.Path("bdfconv/chinesemap.map")
    bdfconv_exe = pathlib.Path("bdfconv/bdfconv.exe")

    # Extract non-ASCII characters from -s source file
    try:
        src_text = src_file.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"ERROR: Source file {src_file} not found.")
        sys.exit(1)

    uni_chars = sorted(set(re.findall(r"[^\x0a-\x7f]", src_text)))
    print(f"發現中文字元 ({len(uni_chars)} 個): {', '.join(uni_chars)}")

    # Generate mapping file (bdfconv/chinesemap.map)
    with map_file.open("w", encoding="utf-8") as f:
        f.write("32-128,\n")
        for ch in uni_chars:
            f.write(f"${ord(ch):04X},\n")
    print(f"Mapping file written to {map_file}")

    # Runs bdfconv.exe with the following presets, configure as needed

    print("Running bdfconv...")
    subprocess.run([
        str(bdfconv_exe),
        "-v", str(bdf_font),
        "-b", "1",
        "-f", "1",
        "-M", str(map_file),
        "-n", args.name,
        "-o", str(output_font_c)
    ], check=True)
    print(f"Font file generated: {output_font_c}")

    # Post-processing .c file
    content = output_font_c.read_text(encoding="utf-8")

    # Remove #ifdef U8G2_USE_LARGE_FONTS and #endif if presence for convenience use, otherwise just use 
    content = re.sub(r'^\s*#ifdef U8G2_USE_LARGE_FONTS\s*$', '', content, flags=re.M)
    content = re.sub(r'^\s*#endif(?:\s*/\*.*\*/)?\s*$', '', content, flags=re.M)

    # Add header guard and include u8g2 header
    guard = output_font_c.stem.upper() + "_H"
    header = f"#ifndef {guard}\n#define {guard}\n#include <u8g2_fonts.h>\n\n"
    footer = "\n#endif\n"
    content = header + content + footer

    output_font_c.write_text(content, encoding="utf-8")

    print("Output file:")
    print(f"  converted_fonts/{output_font_c.name}")

if __name__ == "__main__":
    main()