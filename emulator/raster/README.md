# Raster — MesenCE build overlay

This directory contains the native audio/display milestone for the NES/SNES console project.
It adds seven listening modes and a compact Raster interface to the user's uploaded MesenCE
source while retaining upstream emulation. It is isolated from the existing repository game.

The exact upstream revision is in `manifest.json`. `apply_overlay.py` validates every touched
source file against the baseline before writing. New UI files and native audio code are
included in full; font bytes are stored as base64 solely for transport.

## Reproduce

1. Check out `nesdev-org/MesenCE` at `a60e79feb4d6dcced5922d636f9211837d01e381`.
2. Run `python apply_overlay.py /path/to/MesenCE`.
3. Build with the pinned source's `COMPILING.md` instructions (.NET 10 + C++17).
4. The repository workflow `.github/workflows/raster-windows.yml` builds Windows x64,
   runs behavioral DSP checks, packages corresponding source, and captures the UI.

Run native DSP checks locally:

```sh
g++ -std=c++17 -O2 -Ioverlay/Core/Shared/Audio tests/audio_test.cpp -o audio-test
./audio-test
```

The current font builder and development integration scripts assume this workspace layout:
`work/MesenCE-base`, `work/MesenCE-master`, and `raster-overlay`. End users and CI need only
`apply_overlay.py`, `manifest.json`, and `overlay/`; development scripts document construction.

See `QUICKSTART.txt` and `docs/RELEASE-NOTES.md` for controls and exact feature boundaries.
The source is GPL-3.0-or-later. No copyrighted game files are included.
