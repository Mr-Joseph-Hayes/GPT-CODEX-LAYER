using System;
using System.ComponentModel;
using System.Linq;
using System.Collections.Generic;
using Avalonia;
using Avalonia.Controls;
using Avalonia.Input;
using Avalonia.Interactivity;
using Avalonia.Markup.Xaml;
using Avalonia.Threading;
using Avalonia.VisualTree;
using Mesen.Config;
using Mesen.Interop;
using Mesen.Utilities;

namespace Mesen.Windows;

public class RasterSoundWindow : Window
{
    private readonly AudioConfig _config;
    private readonly DispatcherTimer _saveTimer = new() { Interval = TimeSpan.FromMilliseconds(350) };
    private readonly DispatcherTimer _padTimer = new() { Interval = TimeSpan.FromMilliseconds(50) };
    private HashSet<ushort> _previousKeys = new();
    private bool _ready, _applying;
    private ushort _up, _down, _left, _right, _a, _b, _l, _r;
    private static readonly string[] Names = { "Reference", "Vanilla", "CRT / Living Room", "Headphones", "Night", "Cinema", "Direct" };
    private static readonly string[] Descriptions = {
        "Faithful stereo, neutral tone, and 3 dB of headroom. Our everyday default.",
        "Unprocessed emulator audio. Tone, dynamics, crossfeed, and legacy effects are bypassed. Volume remains active.",
        "A softer top end and slightly narrower image for a warm, intimate living-room presentation.",
        "Gentle, low-frequency crossfeed eases hard stereo separation. No simulated surround.",
        "Linked stereo compression keeps loud events in check. Turn the master up or down to suit your room.",
        "Subtle bass weight and a little extra stereo width. No added echo or artificial surround.",
        "Clean stereo for an external receiver or your operating system's spatial renderer. All presentation effects bypassed."
    };
    public RasterSoundWindow()
    {
        _config = ConfigManager.Config.Audio;
        DataContext = _config;
        AvaloniaXamlLoader.Load(this);
        var devices = ConfigApi.GetAudioDevices();
        var list = this.GetControl<ComboBox>("DeviceList");
        list.ItemsSource = devices;
        list.SelectedItem = devices.Contains(_config.AudioDevice) ? _config.AudioDevice : devices.FirstOrDefault();
        _config.PropertyChanged += OnChanged;
        _saveTimer.Tick += (_, _) => { _saveTimer.Stop(); ConfigManager.Config.Save(); };
        _padTimer.Tick += (_, _) => PollGamepad();
        _up=InputApi.GetKeyCode("Pad1 Up"); _down=InputApi.GetKeyCode("Pad1 Down");
        _left=InputApi.GetKeyCode("Pad1 Left"); _right=InputApi.GetKeyCode("Pad1 Right");
        _a=InputApi.GetKeyCode("Pad1 A"); _b=InputApi.GetKeyCode("Pad1 B");
        _l=InputApi.GetKeyCode("Pad1 L1"); _r=InputApi.GetKeyCode("Pad1 R1");
        KeyDown += (_, e) => {
            if(e.Key == Key.Escape) { Close(); e.Handled=true; }
            if(e.KeyModifiers == KeyModifiers.Control && e.Key == Key.M) { OnMute(null, new RoutedEventArgs()); e.Handled=true; }
        };
        Opened += (_, _) => {
            this.GetControl<StackPanel>("PresetPanel").Children.OfType<Button>().First().Focus();
            _padTimer.Start();
        };
        Closed += (_, _) => {
            _config.PropertyChanged -= OnChanged; _saveTimer.Stop(); _padTimer.Stop();
            ConfigManager.Config.Save();
        };
        _ready = true;
        Refresh();
    }
    private void PollGamepad()
    {
        if(!IsActive) return;
        var keys = InputApi.GetPressedKeys().ToHashSet();
        bool pressed(ushort key) => key != 0 && keys.Contains(key) && !_previousKeys.Contains(key);
        if(pressed(_b)) Close();
        if(pressed(_l)) _config.MasterVolume = (uint)Math.Max(0, (int)_config.MasterVolume-5);
        if(pressed(_r)) _config.MasterVolume = Math.Min(100u, _config.MasterVolume+5);
        var focused = FocusManager?.GetFocusedElement() as Control;
        if(focused is TextBox textBox && textBox.FindAncestorOfType<NumericUpDown>() is NumericUpDown parentNumber) focused = parentNumber;
        var controls = this.GetVisualDescendants().OfType<Control>().Where(c =>
            c.IsEffectivelyVisible && c.IsEffectivelyEnabled && c.FindAncestorOfType<NumericUpDown>() == null && c.FindAncestorOfType<ComboBox>() == null && (c is Button || c is Slider || c is ComboBox || c is CheckBox || c is NumericUpDown)).ToList();
        if((pressed(_up) || pressed(_down)) && controls.Count>0) {
            int i=focused == null ? -1 : controls.IndexOf(focused);
            controls[(i + (pressed(_up) ? controls.Count-1 : 1) + controls.Count) % controls.Count].Focus();
        }
        if(focused is Slider slider) {
            if(pressed(_left)) slider.Value = Math.Max(slider.Minimum,slider.Value-slider.TickFrequency);
            if(pressed(_right)) slider.Value = Math.Min(slider.Maximum,slider.Value+slider.TickFrequency);
        } else if(focused is NumericUpDown number) {
            if(pressed(_left)) number.Value = Math.Max(number.Minimum, (number.Value ?? number.Minimum)-number.Increment);
            if(pressed(_right)) number.Value = Math.Min(number.Maximum, (number.Value ?? number.Minimum)+number.Increment);
        } else if(focused is ComboBox combo) {
            if(pressed(_left)) combo.SelectedIndex = Math.Max(0, combo.SelectedIndex-1);
            if(pressed(_right)) combo.SelectedIndex = Math.Min(combo.ItemCount-1,combo.SelectedIndex+1);
        }
        if(pressed(_a)) {
            if(focused is CheckBox check) check.IsChecked = check.IsChecked != true;
            else if(focused is Button button) button.RaiseEvent(new RoutedEventArgs(Button.ClickEvent));
        }
        _previousKeys=keys;
    }
    private void OnPreset(object? sender, RoutedEventArgs e)
    {
        if(sender is not Button button || !uint.TryParse(button.Tag?.ToString(), out uint mode)) return;
        _applying = true;
        _config.RasterMode = Math.Min(6u,mode);
        _config.RasterBassDb=0; _config.RasterTrebleDb=0; _config.RasterWidth=1; _config.RasterTrimDb=0;
        _config.RasterPeakProtection=true;
        _config.EnableEqualizer=false; _config.ReverbEnabled=false; _config.CrossFeedEnabled=false;
        _applying=false;
        Apply("MODE");
    }
    private void OnResetTone(object? sender, RoutedEventArgs e)
    {
        _applying=true;
        _config.RasterBassDb=0; _config.RasterTrebleDb=0; _config.RasterWidth=1; _config.RasterTrimDb=0; _config.RasterPeakProtection=true;
        _applying=false; Apply("TUNING RESET");
    }
    private void OnMute(object? sender, RoutedEventArgs e) => _config.EnableAudio = !_config.EnableAudio;
    private void OnDone(object? sender, RoutedEventArgs e) => Close();
    private void OnDeviceChanged(object? sender, SelectionChangedEventArgs e)
    {
        if(_ready && sender is ComboBox list && list.SelectedItem is string device) _config.AudioDevice=device;
    }
    private void OnChanged(object? sender, PropertyChangedEventArgs e)
    {
        if(!_ready || _applying) return;
        Apply(e.PropertyName == nameof(AudioConfig.MasterVolume) || e.PropertyName == nameof(AudioConfig.EnableAudio) ? "VOLUME" : "SOUND");
    }
    private void Apply(string change)
    {
        _config.ApplyConfig(); Refresh();
        RasterSound.ShowStatus(change);
        _saveTimer.Stop(); _saveTimer.Start();
    }
    private void Refresh()
    {
        int mode = (int)Math.Min(6u, _config.RasterMode);
        this.GetControl<TextBlock>("ModeName").Text = Names[mode].ToUpperInvariant();
        this.GetControl<TextBlock>("Description").Text = Descriptions[mode];
        this.GetControl<TextBlock>("VolumeReadout").Text = _config.MasterVolume.ToString("000");
        this.GetControl<TextBlock>("PlaybackStatus").Text = !_config.EnableAudio || _config.MasterVolume == 0 ? "MUTED" : "SOUND ON";
        this.GetControl<Button>("MuteButton").Content = _config.EnableAudio ? "Mute" : "Unmute";
        this.GetControl<StackPanel>("TonePanel").IsVisible = mode != 1 && mode != 6;
        this.GetControl<TextBlock>("BypassNote").IsVisible = mode == 1 || mode == 6;
        this.GetControl<TextBlock>("OutputStatus").Text = $"{(uint)_config.SampleRate / 1000.0:0.0} kHz / stereo PCM / requested buffer {_config.AudioLatency} ms";
        foreach(var button in this.GetControl<StackPanel>("PresetPanel").Children.OfType<Button>()) {
            button.Classes.Set("active", button.Tag?.ToString() == mode.ToString());
        }
    }
}
