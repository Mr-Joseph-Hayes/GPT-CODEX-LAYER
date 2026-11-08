using Mesen.Windows;

namespace Mesen.Utilities;

public static class RasterLibrary
{
    private static RasterLibraryWindow? _window;

    public static void Open(MainWindow owner)
    {
        if(_window != null) {
            _window.Activate();
            return;
        }

        _window = new RasterLibraryWindow();
        _window.Closed += (_, _) => _window = null;
        _window.Show(owner);
    }
}
