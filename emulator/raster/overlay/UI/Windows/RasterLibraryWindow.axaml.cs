using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
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

public class RasterLibraryWindow : Window
{
    private readonly DispatcherTimer _padTimer = new() { Interval = TimeSpan.FromMilliseconds(50) };
    private HashSet<ushort> _previousKeys = new();
    private ushort _up, _down, _left, _right, _a, _b;
    private readonly string _libraryRoot;

    private const string ShadowgateRomHash = "F3EEEEFB3A1359CF45AD8A5033525AE4BE050B9FB9CBE2105E09637AAD00A9BE";
    private const string ShadowgateGuideHash = "A6386C222A8DA2A13A6ABF1222FDC7A61880C38E9C6ABF894F5DB7DAF3BC7164";
    private const string Icarus10ExeHash = "10B6077E3F42BDB0C6E7CCF63E11351598BD665253979D2BDDE0642E06248ECB";
    private const string Icarus20ExeHash = "4F346907B5D7A960080689EFDBBF4F08A052EC97D3D31DD0AD241EB6284AEFEC";

    private string ShadowgateRom => Path.Combine(_libraryRoot, "Shadowgate", "Shadowgate (USA).nes");
    private string ShadowgateGuide => Path.Combine(_libraryRoot, "Shadowgate", "Shadowgate-NES-Guide.pdf");
    private string Icarus10Exe => Path.Combine(_libraryRoot, "Kid Icarus Infinite Underworld 1.0", "Infinite Underworld.exe");
    private string Icarus20Exe => Path.Combine(_libraryRoot, "Kid Icarus Infinite Underworld 2.0", "Infinite Underworld.exe");

    public RasterLibraryWindow()
    {
        AvaloniaXamlLoader.Load(this);
        _libraryRoot = ResolveLibraryRoot();
        Directory.CreateDirectory(_libraryRoot);
        this.GetControl<TextBlock>("LibraryPath").Text = _libraryRoot;

        _up = InputApi.GetKeyCode("Pad1 Up");
        _down = InputApi.GetKeyCode("Pad1 Down");
        _left = InputApi.GetKeyCode("Pad1 Left");
        _right = InputApi.GetKeyCode("Pad1 Right");
        _a = InputApi.GetKeyCode("Pad1 A");
        _b = InputApi.GetKeyCode("Pad1 B");

        _padTimer.Tick += (_, _) => PollGamepad();
        Opened += (_, _) => {
            RefreshStatus();
            this.GetControl<Button>("ShadowgatePlay").Focus();
            _padTimer.Start();
        };
        Closed += (_, _) => _padTimer.Stop();
        KeyDown += (_, e) => {
            if(e.Key == Key.Escape) {
                Close();
                e.Handled = true;
            }
        };
    }

    private static string ResolveLibraryRoot()
    {
        string portable = Path.Combine(AppContext.BaseDirectory, "RasterLibrary");
        if(Directory.Exists(portable)) {
            return portable;
        }
        return Path.Combine(ConfigManager.HomeFolder, "RasterLibrary");
    }

    private void PollGamepad()
    {
        if(!IsActive) return;
        var keys = InputApi.GetPressedKeys().ToHashSet();
        bool pressed(ushort key) => key != 0 && keys.Contains(key) && !_previousKeys.Contains(key);

        if(pressed(_b)) {
            Close();
            _previousKeys = keys;
            return;
        }

        var buttons = this.GetVisualDescendants().OfType<Button>()
            .Where(x => x.IsEffectivelyVisible && x.IsEffectivelyEnabled)
            .ToList();
        var focused = FocusManager?.GetFocusedElement() as Button;

        bool previous = pressed(_up) || pressed(_left);
        bool next = pressed(_down) || pressed(_right);
        if((previous || next) && buttons.Count > 0) {
            int index = focused == null ? -1 : buttons.IndexOf(focused);
            int delta = previous ? buttons.Count - 1 : 1;
            buttons[(index + delta + buttons.Count) % buttons.Count].Focus();
        }
        if(pressed(_a) && focused != null) {
            focused.RaiseEvent(new RoutedEventArgs(Button.ClickEvent));
        }

        _previousKeys = keys;
    }

    private void RefreshStatus()
    {
        this.GetControl<TextBlock>("ShadowgateStatus").Text =
            DescribePair(ShadowgateRom, ShadowgateRomHash, ShadowgateGuide, ShadowgateGuideHash);
        this.GetControl<TextBlock>("Icarus10Status").Text =
            DescribeFile(Icarus10Exe, Icarus10ExeHash, "READY / VERIFIED", "FOUND / DIFFERENT 1.0 BUILD");
        this.GetControl<TextBlock>("Icarus20Status").Text =
            DescribeFile(Icarus20Exe, Icarus20ExeHash, "READY / VERIFIED", "FOUND / DIFFERENT 2.0 BUILD");

        this.GetControl<Button>("ShadowgatePlay").IsEnabled = File.Exists(ShadowgateRom);
        this.GetControl<Button>("ShadowgateGuide").IsEnabled = File.Exists(ShadowgateGuide);
        this.GetControl<Button>("Icarus10Play").IsEnabled = File.Exists(Icarus10Exe);
        this.GetControl<Button>("Icarus20Play").IsEnabled = File.Exists(Icarus20Exe);
    }

    private static string DescribePair(string first, string firstHash, string second, string secondHash)
    {
        bool game = File.Exists(first);
        bool guide = File.Exists(second);
        if(!game && !guide) return "MISSING / install the local RasterLibrary content pack";
        string gameState = game ? (Verify(first, firstHash) ? "GAME VERIFIED" : "GAME FOUND") : "GAME MISSING";
        string guideState = guide ? (Verify(second, secondHash) ? "GUIDE VERIFIED" : "GUIDE FOUND") : "GUIDE MISSING";
        return gameState + " / " + guideState;
    }

    private static string DescribeFile(string path, string expectedHash, string verified, string different)
    {
        if(!File.Exists(path)) return "MISSING / install the local RasterLibrary content pack";
        return Verify(path, expectedHash) ? verified : different;
    }

    private static bool Verify(string path, string expectedHash)
    {
        try {
            using FileStream stream = File.OpenRead(path);
            using SHA256 sha = SHA256.Create();
            return Convert.ToHexString(sha.ComputeHash(stream)).Equals(expectedHash, StringComparison.OrdinalIgnoreCase);
        } catch {
            return false;
        }
    }

    private void OnShadowgatePlay(object? sender, RoutedEventArgs e)
    {
        if(File.Exists(ShadowgateRom)) {
            LoadRomHelper.LoadFile(ShadowgateRom);
            Close();
        }
    }

    private void OnShadowgateGuide(object? sender, RoutedEventArgs e) => OpenShell(ShadowgateGuide);
    private void OnIcarus10Play(object? sender, RoutedEventArgs e) => LaunchExternal(Icarus10Exe);
    private void OnIcarus20Play(object? sender, RoutedEventArgs e) => LaunchExternal(Icarus20Exe);
    private void OnOpenFolder(object? sender, RoutedEventArgs e) => OpenShell(_libraryRoot);
    private void OnDone(object? sender, RoutedEventArgs e) => Close();

    private static void LaunchExternal(string exe)
    {
        if(!File.Exists(exe)) return;
        Process.Start(new ProcessStartInfo {
            FileName = exe,
            WorkingDirectory = Path.GetDirectoryName(exe) ?? AppContext.BaseDirectory,
            UseShellExecute = true
        });
    }

    private static void OpenShell(string path)
    {
        if(!File.Exists(path) && !Directory.Exists(path)) return;
        Process.Start(new ProcessStartInfo { FileName = path, UseShellExecute = true });
    }
}
