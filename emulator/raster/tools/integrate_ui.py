from pathlib import Path
p=Path('work/MesenCE-master')
def edit(path,old,new):
 f=p/path;s=f.read_text(encoding='utf-8-sig');assert old in s,path;f.write_text(s.replace(old,new))
edit('UI/Windows/MainWindow.axaml','\t<DockPanel>','''	<DockPanel>
        <Border DockPanel.Dock="Top" Background="#111A1E" Padding="12 6" IsVisible="{Binding IsMenuVisible}">
            <Grid ColumnDefinitions="*,Auto,Auto,Auto">
                <TextBlock Text="RASTER" FontFamily="avares://Mesen/Assets/RasterDisplay.ttf#Raster Display" FontSize="17" Foreground="#AFF2DA" VerticalAlignment="Center" />
                <Button Grid.Column="1" Content="Sound" Click="OpenRasterSound" Margin="0 0 8 0" ToolTip.Tip="Ctrl Shift A" />
                <Slider Grid.Column="2" Width="110" Minimum="0" Maximum="100" TickFrequency="1" IsSnapToTickEnabled="True" Value="{Binding Config.Audio.MasterVolume, Mode=TwoWay}" PropertyChanged="RasterVolumeChanged" AutomationProperties.Name="Master volume" />
                <Button Grid.Column="3" Content="Mute / Unmute" Click="ToggleRasterMute" Margin="8 0 0 0" ToolTip.Tip="Ctrl M" />
            </Grid>
        </Border>''')
# PropertyChanged is not a routed XAML event in every Avalonia version; use a config observer in constructor instead.
edit('UI/Windows/MainWindow.axaml',' PropertyChanged="RasterVolumeChanged"','')
edit('UI/Windows/MainWindow.axaml.cs','\t\tprivate void OnPreviewKeyDown(object? sender, KeyEventArgs e)\n\t\t{','''        private void OpenRasterSound(object? sender, RoutedEventArgs e) => RasterSound.Open(this);
        private void ToggleRasterMute(object? sender, RoutedEventArgs e)
        {
            ConfigManager.Config.Audio.EnableAudio = !ConfigManager.Config.Audio.EnableAudio;
            ConfigManager.Config.Audio.ApplyConfig();
            RasterSound.ShowStatus();
        }

		private void OnPreviewKeyDown(object? sender, KeyEventArgs e)
		{
            if(e.Key == Key.A && e.KeyModifiers == (KeyModifiers.Control | KeyModifiers.Shift)) {
                RasterSound.Open(this); e.Handled = true; return;
            }''')
# Observe only top-level audio changes needed by the bar. Full settings window applies other changes.
edit('UI/Windows/MainWindow.axaml.cs','\t\t\tConsole.CancelKeyPress += Console_CancelKeyPress;','''			Console.CancelKeyPress += Console_CancelKeyPress;
            ConfigManager.Config.Audio.PropertyChanged += (_, e) => {
                if(e.PropertyName == nameof(AudioConfig.MasterVolume) || e.PropertyName == nameof(AudioConfig.EnableAudio)) {
                    ConfigManager.Config.Audio.ApplyConfig();
                    RasterSound.ShowStatus();
                }
            };''')
edit('UI/Utilities/ShortcutHandler.cs','ConfigManager.Config.AudioPlayer.ApplyConfig();\n\t\t\t}\n\t\t}', 'ConfigManager.Config.AudioPlayer.ApplyConfig();\n\t\t\t}\n            RasterSound.ShowStatus();\n\t\t}')
# Insert default mute shortcut, using existing rebinding infrastructure.
edit('UI/Config/PreferencesConfig.cs','\t\t\tAddShortcut(new ShortcutKeyInfo { Shortcut = EmulatorShortcut.IncreaseVolume,', '\t\t\tAddShortcut(new ShortcutKeyInfo { Shortcut = EmulatorShortcut.ToggleAudio, KeyCombination = new KeyCombination() { Key1 = ctrl, Key2 = InputApi.GetKeyCode("M") } });\n\t\t\tAddShortcut(new ShortcutKeyInfo { Shortcut = EmulatorShortcut.IncreaseVolume,')
# Dedicated sound entry in the existing full audio settings.
edit('UI/Views/AudioConfigView.axaml','<c:SystemSpecificSettings ConfigType="Audio" />','''<c:SystemSpecificSettings ConfigType="Audio" />
                    <Border Background="#162621" Padding="14" CornerRadius="8" Margin="0 0 0 10">
                        <StackPanel Spacing="8">
                            <TextBlock Text="RASTER SOUND" Foreground="#AFF2DA" FontFamily="avares://Mesen/Assets/RasterDisplay.ttf#Raster Display" FontSize="18" />
                            <TextBlock Text="Open the Sound button in the main window for the seven listening modes. Vanilla and Direct bypass the effects below." TextWrapping="Wrap" />
                        </StackPanel>
                    </Border>''')
