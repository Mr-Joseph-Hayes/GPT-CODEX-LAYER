from pathlib import Path
p=Path('work/MesenCE-master')
def edit(path, old, new):
 f=p/path
 s=f.read_text(encoding='utf-8-sig')
 assert old in s, path+': anchor missing'
 f.write_text(s.replace(old,new),encoding='utf-8')
fields='''
    // Raster presentation parameters; appended to preserve earlier field offsets.
    uint32_t RasterMode = 0;
    double RasterBassDb = 0;
    double RasterTrebleDb = 0;
    double RasterWidth = 1;
    double RasterTrimDb = 0;
    bool RasterPeakProtection = true;
'''
edit('Core/Shared/SettingTypes.h','uint32_t AudioPlayerSilenceDelay = 3;','uint32_t AudioPlayerSilenceDelay = 3;'+fields)
edit('Core/Shared/Audio/SoundMixer.h','#include "Utilities/Audio/HermiteResampler.h"','#include "Utilities/Audio/HermiteResampler.h"\n#include "Shared/Audio/RasterAudioProcessor.h"')
edit('Core/Shared/Audio/SoundMixer.h','Emulator* _emu;','Emulator* _emu;\n\tRaster::AudioProcessor _rasterAudio;')
edit('Core/Shared/Audio/SoundMixer.cpp','if(cfg.EnableEqualizer) {','if(cfg.RasterMode != 1 && cfg.RasterMode != 6 && cfg.EnableEqualizer) {')
edit('Core/Shared/Audio/SoundMixer.cpp','if(cfg.ReverbEnabled) {','if(cfg.RasterMode != 1 && cfg.RasterMode != 6 && cfg.ReverbEnabled) {')
edit('Core/Shared/Audio/SoundMixer.cpp','if(cfg.CrossFeedEnabled) {','if(cfg.RasterMode != 1 && cfg.RasterMode != 6 && cfg.CrossFeedEnabled) {')
edit('Core/Shared/Audio/SoundMixer.cpp','''	if(masterVolume < 100) {
		//Apply volume if not using the default value
		for(uint32_t i = 0; i < count * 2; i++) {
			out[i] = (int32_t)out[i] * (int32_t)masterVolume / 100;
		}
	}''','''	Raster::AudioSettings rasterSettings;
	rasterSettings.mode = static_cast<Raster::Mode>(cfg.RasterMode);
	rasterSettings.bassDb = cfg.RasterBassDb;
	rasterSettings.trebleDb = cfg.RasterTrebleDb;
	rasterSettings.width = cfg.RasterWidth;
	rasterSettings.trimDb = cfg.RasterTrimDb;
	rasterSettings.peakProtection = cfg.RasterPeakProtection;
	_rasterAudio.Process(out, count, cfg.SampleRate, rasterSettings, cfg.EnableAudio ? masterVolume / 100.0 : 0.0);''')
# Feed silence when muted; preserves a smooth gain ramp and a stable device clock.
edit('Core/Shared/Audio/SoundMixer.cpp','if(cfg.EnableAudio) {','if(true) { // Raster mute is applied with a short gain ramp above.')
edit('Core/Shared/Audio/SoundMixer.cpp','if(clearBuffer) {','if(clearBuffer) {\n\t\t\t_rasterAudio.Reset();')
# Interop fields are deliberately appended in exactly the same order on both sides.
edit('UI/Config/AudioConfig.cs','public partial class AudioConfig : BaseConfig<AudioConfig>','public partial class AudioConfig : BaseConfig<AudioConfig>')
edit('UI/Config/AudioConfig.cs','\t\tpublic void ApplyConfig()', '''		[ObservableProperty] public partial uint RasterMode { get; set; } = 0;
		[ObservableProperty][MinMax(-6.0, 6.0)] public partial double RasterBassDb { get; set; } = 0;
		[ObservableProperty][MinMax(-6.0, 6.0)] public partial double RasterTrebleDb { get; set; } = 0;
		[ObservableProperty][MinMax(0.0, 1.5)] public partial double RasterWidth { get; set; } = 1;
		[ObservableProperty][MinMax(-12.0, 0.0)] public partial double RasterTrimDb { get; set; } = 0;
		[ObservableProperty] public partial bool RasterPeakProtection { get; set; } = true;

		public void ApplyConfig()''')
edit('UI/Config/AudioConfig.cs','AudioPlayerSilenceDelay = AudioPlayerSilenceDelay','''AudioPlayerSilenceDelay = AudioPlayerSilenceDelay,
                RasterMode = RasterMode, RasterBassDb = RasterBassDb, RasterTrebleDb = RasterTrebleDb,
                RasterWidth = RasterWidth, RasterTrimDb = RasterTrimDb, RasterPeakProtection = RasterPeakProtection''')
edit('UI/Config/AudioConfig.cs','\t\tpublic UInt32 AudioPlayerSilenceDelay;','''		public UInt32 AudioPlayerSilenceDelay;
        public UInt32 RasterMode;
        public double RasterBassDb;
        public double RasterTrebleDb;
        public double RasterWidth;
        public double RasterTrimDb;
        [MarshalAs(UnmanagedType.I1)] public bool RasterPeakProtection;''')
# Shared upstream defaults are unchanged; this fork uses separate settings.
edit('UI/Config/ConfigManager.cs','Path.Combine(BaseDocumentsFolder, "MesenCE")','Path.Combine(BaseDocumentsFolder, "Raster")')
edit('UI/Config/ConfigManager.cs','return File.Exists(Path.Combine(path, "settings.json")) ? path : null;','return null; // Do not import or overwrite the user\'s Mesen settings.')
edit('UI/Config/VideoConfig.cs','partial bool VerticalSync { get; set; } = false','partial bool VerticalSync { get; set; } = true')
edit('UI/Config/VideoConfig.cs','partial int ScanlineIntensity { get; set; } = 0','partial int ScanlineIntensity { get; set; } = 15')
# 80 percent initial volume; output rate/latency stay at 48 kHz / 30 ms.
edit('UI/Config/AudioConfig.cs','partial UInt32 MasterVolume { get; set; } = 100','partial UInt32 MasterVolume { get; set; } = 80')
