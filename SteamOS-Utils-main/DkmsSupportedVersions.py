'''
    MIT License

    Copyright (c) 2025 InnoVision Games

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

    file: SupportedVersions.py
'''

import os
import platform
import urllib.request

WORKING_MIRROR = None
WORKING_FILENAME = None
WORKING_HEADERS_FILENAME = None

def get_os_version():
    temp = platform.release().split('-')
    return {
        'os_name': 'linux',
        'kernel_type': 'neptune',
        '_raw_temp': temp
    }

def get_kernel_modules_filename(os_version):
    global WORKING_MIRROR, WORKING_FILENAME, WORKING_HEADERS_FILENAME
    
    print('\n[Scanner] Generating filename and scanning ALL Valve mirrors...')
    
    temp = os_version.get('_raw_temp', [])
    if len(temp) > 5 and temp[4] == 'neptune':
        pkgname = f"linux-neptune-{temp[5]}"
        version = temp[0]
        pkgrel = temp[3]
        formats = [
            f"{temp[1]}.{temp[2]}",
            f"{temp[1]}_{temp[2]}",
            f"{temp[1]}-{temp[2]}"
        ]
    else:
        pkgname = "linux-neptune"
        version = temp[0]
        pkgrel = temp[2]
        formats = [temp[1]]

    # List of all possible active Valve repositories
    mirrors = [
        'https://steamdeck-packages.steamos.cloud/archlinux-mirror/jupiter-main/os/x86_64/',
        'https://steamdeck-packages.steamos.cloud/archlinux-mirror/jupiter-beta/os/x86_64/',
        'https://steamdeck-packages.steamos.cloud/archlinux-mirror/jupiter/os/x86_64/',
        'https://steamdeck-packages.steamos.cloud/archlinux-mirror/holo-main/os/x86_64/',
        'https://steamdeck-packages.steamos.cloud/archlinux-mirror/holo-beta/os/x86_64/',
        'https://steamdeck-packages.steamos.cloud/archlinux-mirror/holo/os/x86_64/'
    ]

    for fmt in formats:
        mod_filename = f"{pkgname}-{version}.{fmt}-{pkgrel}-x86_64.pkg.tar.zst"
        head_filename = f"{pkgname}-headers-{version}.{fmt}-{pkgrel}-x86_64.pkg.tar.zst"
        
        for mirror in mirrors:
            url = mirror + mod_filename
            try:
                req = urllib.request.Request(url, method='HEAD')
                with urllib.request.urlopen(req) as response:
                    if response.status == 200:
                        print(f"-> SUCCESS: Found package on {mirror}")
                        WORKING_MIRROR = mirror
                        WORKING_FILENAME = mod_filename
                        WORKING_HEADERS_FILENAME = head_filename
                        return WORKING_FILENAME
            except Exception:
                pass

    # Absolute fallback (will likely trigger a 404 in the main script)
    WORKING_MIRROR = 'https://steamdeck-packages.steamos.cloud/archlinux-mirror/jupiter-main/os/x86_64/'
    WORKING_FILENAME = f"{pkgname}-{version}.{formats[0]}-{pkgrel}-x86_64.pkg.tar.zst"
    WORKING_HEADERS_FILENAME = f"{pkgname}-headers-{version}.{formats[0]}-{pkgrel}-x86_64.pkg.tar.zst"
    print(f"-> WARNING: Package not found! Valve likely purged it.")
    return WORKING_FILENAME

def get_kernel_headers_filename(os_version):
    global WORKING_HEADERS_FILENAME
    return WORKING_HEADERS_FILENAME

def get_remote_kernel_modules_path(filename):
    global WORKING_MIRROR, WORKING_FILENAME
    return WORKING_MIRROR + WORKING_FILENAME

def get_remote_kernel_headers_path(filename):
    global WORKING_MIRROR, WORKING_HEADERS_FILENAME
    return WORKING_MIRROR + WORKING_HEADERS_FILENAME