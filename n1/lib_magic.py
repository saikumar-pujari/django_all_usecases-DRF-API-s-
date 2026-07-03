import magic

# ============================================================
# File Paths
# ============================================================

Payment = r"C:\skippers\skipper\Desktop\vsc\django\python_magic\Payment.pdf"
FAKE_PDF = r"C:\skippers\skipper\Desktop\vsc\django\python_magic\na.pdf"
ZIP_FILE = r"C:\skippers\skipper\Desktop\vsc\django\python_magic\sa.zip"

# ============================================================
# Basic Usage
# ============================================================

print("=" * 50)
print("Basic File Detection")
print("=" * 50)

print(magic.from_file(Payment))
print(magic.from_file(Payment, mime=True))

with open(Payment, "rb") as file:
    print(magic.from_buffer(file.read(2048)))
print()

# ============================================================
# Magic Object
# ============================================================

magic_detector = magic.Magic(
    mime=True,
    uncompress=True
)

print("=" * 50)
print("Magic Object Detection")
print("=" * 50)

print(magic_detector.from_file(Payment))
print(magic_detector.from_file(FAKE_PDF))
print(magic_detector.from_file(ZIP_FILE))

print()

# ============================================================
# Allowed MIME Types
# ============================================================

ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/zip",
    "image/jpeg",
    "image/png",
    "text/plain",
    "text/csv",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

# ============================================================
# Validation Function
# ============================================================


def validate_file(file_path: str) -> bool:
    """
    Validate a file using python-magic.
    Returns True if the file is allowed.
    """

    detected_type = magic_detector.from_file(file_path)

    print(f"Detected MIME Type : {detected_type}")

    if detected_type in ALLOWED_MIME_TYPES:
        print("✅ File is allowed")
        return True

    print("❌ File is NOT allowed")
    return False


print("=" * 50)
print("Validation")
print("=" * 50)

validate_file(Payment)

print("=" * 50)
print("Validation")
print("=" * 50)

try:
    print(magic.from_file("C:/Users/SKIPPER/Desktop/vsc/django/final/manage.pdf"))
except magic.MagicException as e:
    print(e)

with open("C:/Users/SKIPPER/Desktop/vsc/django/final/manage.pdf", "rb") as f:
    fd = f.fileno()
    print(magic.from_descriptor(fd))
