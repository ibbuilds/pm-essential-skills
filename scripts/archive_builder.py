"""Build and verify downloads before replacing an existing output."""

import os
from pathlib import Path, PurePosixPath
import tempfile
import zipfile


def write_archive(output, entries, generated=None):
    output = Path(output)
    generated = generated or {}
    for name in [*entries, *generated]:
        relative = PurePosixPath(name)
        if (relative.is_absolute() or ".." in relative.parts or "\\" in name
                or ":" in name or not relative.parts):
            raise ValueError(f"Unsafe archive entry: {name}")
    if set(entries) & set(generated):
        raise ValueError("Duplicate generated archive entry")
    for source in entries.values():
        if source.is_symlink():
            raise ValueError("Linked package sources are not supported")
        if not source.is_file():
            raise ValueError("Package sources must be regular files")
        if output.resolve() == source.resolve() or (output.exists() and output.samefile(source)):
            raise ValueError("Archive output would overwrite a package source")
    if output.is_symlink():
        raise ValueError("Linked archive outputs are not supported")
    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".pm-archive-", suffix=".zip", dir=output.parent)
    os.close(descriptor)
    temporary = Path(temporary)
    try:
        with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED) as archive:
            # Ignore wall-clock time, source modes, insertion order, and host OS.
            for name in sorted(set(entries) | set(generated)):
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                data = generated[name] if name in generated else entries[name].read_bytes()
                archive.writestr(info, data, compresslevel=9)
        with zipfile.ZipFile(temporary) as archive:
            if archive.testzip() is not None:
                raise ValueError("Archive verification failed")
            for name, source in entries.items():
                if archive.read(name) != source.read_bytes():
                    raise ValueError(f"Packaged content differs: {name}")
            for name, data in generated.items():
                expected = data.encode("utf-8") if isinstance(data, str) else data
                if archive.read(name) != expected:
                    raise ValueError(f"Packaged content differs: {name}")
        os.replace(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)
