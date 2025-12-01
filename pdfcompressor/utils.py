import subprocess
import os
import uuid
import platform
import shutil
import pikepdf


TMP_DIR = '/tmp' if platform.system() != 'Windows' else os.environ.get('TEMP', 'C:\\Temp')


def find_ghostscript():
    gs = shutil.which('gs') or shutil.which('gswin64c') or shutil.which('gswin32c')
    if gs:
        return gs
    raise FileNotFoundError("Ghostscript executable not found")


def compress_with_ghostscript(input_path, quality='ebook'):
    """
    Compress PDF using Ghostscript with aggressive settings.
    quality: 'screen', 'ebook', 'printer'
    """
    output_path = os.path.join(TMP_DIR, f"compressed_{uuid.uuid4().hex}.pdf")
    gs = find_ghostscript()

    # Définir la résolution d'image selon le niveau
    dpi_map = {
        'screen': 72,
        'ebook': 150,
        'printer': 300
    }
    dpi = dpi_map.get(quality, 150)

    command = [
        gs,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS=/{quality}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        "-dDetectDuplicateImages=true",
        "-dCompressFonts=true",
        "-dDownsampleColorImages=true",
        "-dDownsampleGrayImages=true",
        "-dDownsampleMonoImages=true",
        f"-dColorImageResolution={dpi}",
        f"-dGrayImageResolution={dpi}",
        f"-dMonoImageResolution={dpi}",
        f"-sOutputFile={output_path}",
        input_path
    ]

    subprocess.run(command, check=True)
    return output_path


def compress_with_pikepdf(input_path):
    """
    Fallback PDF compression using pikepdf.
    Simply rewrites the PDF; does not aggressively compress images.
    """
    output_path = os.path.join(TMP_DIR, f"compressed_{uuid.uuid4().hex}.pdf")
    pdf = pikepdf.open(input_path)
    pdf.save(output_path)
    return output_path


def compress_pdf(input_path, quality='scree'):
    """
    Main compression function.
    Tries Ghostscript first, falls back to PikePDF if an error occurs.
    """
    try:
        return compress_with_ghostscript(input_path, quality)
    except Exception as e:
        print(f"Ghostscript compression failed: {e}. Falling back to PikePDF.")
        return compress_with_pikepdf(input_path)



# def compress_with_ghostscript(input_path, quality='ebook'):
#     """
#     Compress PDF using Ghostscript with different quality levels:
#     /screen -> lowest, smallest size
#     /ebook   -> medium quality
#     /printer -> higher quality, larger file
#     """
#     output_path = os.path.join(TMP_DIR, f"compressed_{uuid.uuid4().hex}.pdf")
#     gs = find_ghostscript()

#     # Ghostscript quality mapping
#     valid_qualities = ['screen', 'ebook', 'printer', 'prepress', 'default']
#     if quality not in valid_qualities:
#         quality = 'ebook'

#     # Paramètres optimisés
#     command = [
#         gs,
#         "-sDEVICE=pdfwrite",
#         "-dCompatibilityLevel=1.4",
#         f"-dPDFSETTINGS=/{quality}",
#         "-dNOPAUSE",
#         "-dQUIET",
#         "-dBATCH",
#         "-dDetectDuplicateImages=true",   # supprime les images dupliquées
#         "-dCompressFonts=true",           # compresse les polices intégrées
#         "-dDownsampleColorImages=true",   # rééchantillonne les images couleur
#         "-dColorImageDownsampleType=/Bicubic",
#         "-dColorImageResolution=72",     # réduire la résolution des images (screen/ebook)
#         f"-sOutputFile={output_path}",
#         input_path,
#     ]


#     subprocess.run(command, check=True)
#     return output_path

