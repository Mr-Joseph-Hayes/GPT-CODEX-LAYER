from pathlib import Path
p=Path('work/MesenCE-master')
def edit(path,old,new):
 f=p/path;s=f.read_text(encoding='utf-8-sig');assert old in s,path;f.write_text(s.replace(old,new))
edit('Core/Shared/SettingTypes.h','\tShortcutCount,','\tOpenRasterSound,\n\tShortcutCount,')
edit('UI/Config/Shortcuts/EmulatorShortcut.cs','\t\tLastValidValue,','\t\tOpenRasterSound,\n\t\tLastValidValue,')
edit('UI/Utilities/ShortcutHandler.cs','case EmulatorShortcut.ToggleAudio:','case EmulatorShortcut.OpenRasterSound: RasterSound.Open(_mainWindow); break;\n\t\t\t\tcase EmulatorShortcut.ToggleAudio:')
edit('UI/Config/PreferencesConfig.cs','AddShortcut(new ShortcutKeyInfo { Shortcut = EmulatorShortcut.ToggleAudio,','AddShortcut(new ShortcutKeyInfo { Shortcut = EmulatorShortcut.OpenRasterSound, KeyCombination = new KeyCombination() { Key1 = ctrl, Key2 = shift, Key3 = InputApi.GetKeyCode("A") }, KeyCombination2 = new KeyCombination() { Key1 = InputApi.GetKeyCode("Pad1 Back"), Key2 = InputApi.GetKeyCode("Pad1 Start") } });\n\t\t\tAddShortcut(new ShortcutKeyInfo { Shortcut = EmulatorShortcut.ToggleAudio,')
edit('UI/Windows/MainWindow.axaml.cs','cmdLine.OnAfterInit(this);','cmdLine.OnAfterInit(this);\n                    if(Environment.GetEnvironmentVariable("RASTER_SOUND_PREVIEW") == "1") RasterSound.Open(this);')
edit('UI/ViewModels/MainWindowViewModel.cs','"MesenCE"','"Raster | MesenCE"')
edit('UI/Config/PreferencesConfig.cs','partial bool AutomaticallyCheckForUpdates { get; set; } = true','partial bool AutomaticallyCheckForUpdates { get; set; } = false')
f=p/'UI/Windows/RasterSoundWindow.axaml.cs';s=f.read_text();s=s.replace('c is ComboBox || c is CheckBox','c is ComboBox || c is CheckBox || c is NumericUpDown')
s=s.replace('} else if(focused is ComboBox combo) {','''} else if(focused is NumericUpDown number) {
            if(pressed(_left)) number.Value = Math.Max(number.Minimum, (number.Value ?? number.Minimum)-number.Increment);
            if(pressed(_right)) number.Value = Math.Min(number.Maximum, (number.Value ?? number.Minimum)+number.Increment);
        } else if(focused is ComboBox combo) {''');f.write_text(s)
f=p/'UI/Windows/RasterSoundWindow.axaml';s=f.read_text();s='\n'.join(l for l in s.split('\n') if 'Button.preset:selected' not in l);f.write_text(s)
# Guard raw config values before looking up string arrays and applying native settings.
f=p/'UI/Config/AudioConfig.cs';s=f.read_text();s=s.replace('RasterMode = RasterMode,','RasterMode = Math.Min(6u, RasterMode),');f.write_text(s)
