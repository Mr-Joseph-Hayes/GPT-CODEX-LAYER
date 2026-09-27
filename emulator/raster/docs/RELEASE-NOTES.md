# Raster 0.1.0 — native audio milestone

Raster is a working-name customization of Mesen Community Edition for Joseph Hayes.
This release adds the approved sound presentation layer to the uploaded source revision
`a60e79feb4d6dcced5922d636f9211837d01e381`. Existing NES/SNES emulation is supplied by MesenCE.

## Implemented

- Reference (default), Vanilla, CRT / Living Room, Headphones, Night, Cinema, Direct.
- One master gain for the mixed emulator/provider stream, with short gain ramps.
- Neutral reference sound with 3 dB headroom; modest tonal/width changes in the named presets.
- Low-frequency headphone crossfeed, stereo-linked night compression, sample-peak guard.
- Fine bass, treble, stereo width, output trim, device, sample-rate and buffer controls.
- Original Raster Display ASCII font and matching in-game HUD glyphs.
- Native settings window, quick volume/mute, keyboard shortcuts, rebindable sound action,
  default Back + Start gamepad chord, and gamepad navigation within the sound window.
- In-game volume bar, mode/status notification, and persistent mute indicator.
- Portable settings isolated from existing Mesen installations.
- VSync on and restrained scanlines on for a fresh installation.
- Windows audio initialization and reset fail gracefully when no output endpoint is available.

## Honest boundaries

Vanilla and Direct bypass the post-mix presentation layer and legacy EQ/reverb/crossfeed.
They still use the emulator's mandatory resampling, operating-system mixer, and master
volume. They do not globally disable game patches, cheats, HD audio, or per-channel
settings. Direct is plain stereo PCM intended for an external/system renderer, not
exclusive-mode bit-perfect hardware output, Dolby encoding, or object-based spatial audio.

The limiter is sample-peak protection, not an oversampled true-peak mastering limiter.
No ambience, echo, mono-to-stereo synthesis, or new surround channels are added.
The requested buffer is not an end-to-end latency measurement. Existing legacy effects
may clip before the presentation layer; choose a preset to clear legacy effects.

Physical Windows device/controller checks and listening evaluation require the owner's
hardware. Synthetic DSP tests cannot certify subjective sound quality or Bluetooth latency.
The console library, polished boot, timed auto-launch, manual/strategy reader,
achievements, broad per-game enhancement manager, and browser release remain future
implementation milestones; this source does not claim those screens or systems exist.

## Certification research — 2026-09-27

THX describes a formal certification program; no free emulator certification path was
found: https://www.thx.com/certification/
Dolby describes licensing, registration, testing, and design approval, not a freely
assignable preset or badge: https://professional.dolby.com/licensing/ and
https://handbook.dolby.com/dsh/product-certification/
No certification application, agreement, or third-party contact was submitted.

## License

MesenCE and these modifications: GPL-3.0-or-later. Keep all upstream notices.
Raster Display is original glyph geometry; the editable builder and glyph data are
included under the same license. No ROMs or private compatibility files are distributed.
