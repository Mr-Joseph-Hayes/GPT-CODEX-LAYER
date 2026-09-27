using System;
using Mesen.Config;
using Mesen.Interop;
using Mesen.Windows;

namespace Mesen.Utilities;
public static class RasterSound
{
    private static RasterSoundWindow? _window;
    public static void Open(MainWindow owner)
    {
        if(_window != null) { _window.Activate(); return; }
        _window = new RasterSoundWindow();
        _window.Closed += (_, _) => _window=null;
        _window.Show(owner);
    }
    public static void ShowStatus(string change = "VOLUME")
    {
        var c=ConfigManager.Config.Audio;
        string[] modes={"REFERENCE","VANILLA","LIVING ROOM","HEADPHONES","NIGHT","CINEMA","DIRECT"};
        string level = !c.EnableAudio || c.MasterVolume==0 ? "MUTED" : c.MasterVolume + "%";
        EmuApi.DisplayMessage("RASTER SOUND", change + " / " + level + " / " + modes[Math.Min(6u,c.RasterMode)]);
    }
}
