# GPT Codex Layer — Raster

Raster is a native NES/SNES emulator audio playtest built on [Mesen Community Edition](https://github.com/nesdev-org/MesenCE).

The source overlay is in `emulator/raster/`. It includes seven listening modes, master volume and mute controls, the Raster Display font, in-game sound status, and audio signal tests.

## Build

The `Raster Windows audio build` workflow builds the pinned upstream source with the Raster overlay on Windows x64. It runs on changes to `main` and can also be started manually from Actions. A successful run provides a portable Windows package and matching source/QA artifacts.

Windows compilation and native UI validation are pending the first successful run. See `emulator/raster/QUICKSTART.txt` for controls and `emulator/raster/docs/RELEASE-NOTES.md` for the current feature boundaries.

No game ROMs are included or downloaded. Use your own game files.

## License

MesenCE and the Raster modifications are GPL-3.0-or-later. The full license is in `emulator/raster/LICENSE`.
