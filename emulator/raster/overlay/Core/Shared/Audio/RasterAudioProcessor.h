// Raster audio presentation layer. GPL-3.0-or-later.
// No emulated APU state is modified. Stereo PCM in, stereo PCM out.
#pragma once
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>

namespace Raster {
enum class Mode : uint32_t { Reference, Vanilla, LivingRoom, Headphones, Night, Cinema, Direct };
struct AudioSettings {
    Mode mode = Mode::Reference;
    double bassDb = 0, trebleDb = 0, width = 1, trimDb = 0;
    bool peakProtection = true;
};
class AudioProcessor {
    std::array<double, 2> _low{}, _highLow{}, _crossLow{}, _roomLow{};
    double _bass = 1, _treble = 1, _width = 1, _cross = 0, _room = 0;
    double _gain = 1, _night = 0, _wet = 0, _guard = 1, _envelope = 0;
    double _master = 1;
    bool _initialized = false;
    static double finite(double v, double fallback) { return std::isfinite(v) ? v : fallback; }
    static double db(double v) { return std::pow(10.0, v / 20.0); }
    static void chase(double& v, double target, double amount) {
        v += (target - v) * amount;
        if(std::abs(v - target) < 1e-9) v = target;
    }
public:
    void Reset() { *this = AudioProcessor(); }
    void Process(int16_t* samples, uint32_t frames, uint32_t sampleRate,
                 const AudioSettings& settings, double master = 1) {
        if(!samples || !frames || sampleRate < 8000 || sampleRate > 192000) return;
        Mode mode = settings.mode;
        if(static_cast<uint32_t>(mode) > 6) mode = Mode::Reference;
        bool bypass = mode == Mode::Vanilla || mode == Mode::Direct;
        double bass = 0, treble = 0, width = 1, cross = 0, room = 0, night = 0;
        switch(mode) {
            case Mode::LivingRoom: bass = .5; treble = -2; width = .85; room = 1; break;
            case Mode::Headphones: treble = -.5; cross = .12; break;
            case Mode::Night: bass = -2; treble = -1; night = 1; break;
            case Mode::Cinema: bass = 2; treble = .5; width = 1.12; break;
            default: break;
        }
        bass += std::clamp(finite(settings.bassDb, 0), -6.0, 6.0);
        treble += std::clamp(finite(settings.trebleDb, 0), -6.0, 6.0);
        width *= std::clamp(finite(settings.width, 1), 0.0, 1.5);
        double trim = std::clamp(finite(settings.trimDb, 0), -12.0, 0.0);
        // Reserve headroom for tone/width boosts; never increase the default loudness.
        double gain = bypass ? 1 : db(-3 - std::max({0.0, bass, treble}) + trim);
        if(bypass) { bass = treble = cross = room = night = 0; width = 1; }
        double bassGain = db(bass), trebleGain = db(treble);
        master = std::clamp(finite(master, 0), 0.0, 1.0);
        const double pi = 3.14159265358979323846;
        double lowA = 1 - std::exp(-2*pi*160 / sampleRate);
        double highA = 1 - std::exp(-2*pi*4000 / sampleRate);
        double crossA = 1 - std::exp(-2*pi*700 / sampleRate);
        double roomA = 1 - std::exp(-2*pi*8000 / sampleRate);
        double smooth = 1 - std::exp(-1.0 / (.008 * sampleRate));
        double volumeSmooth = 1 - std::exp(-1.0 / (.003 * sampleRate));
        double release = std::exp(-1.0 / (.12 * sampleRate));
        if(!_initialized) {
            _bass = bassGain; _treble = trebleGain; _width = width; _cross = cross;
            _room = room; _night = night; _wet = bypass ? 0 : 1; _gain = gain;
            _master = master; _initialized = true;
        }
        for(uint32_t i=0; i<frames; i++) {
            chase(_bass, bassGain, smooth); chase(_treble, trebleGain, smooth);
            chase(_width, width, smooth); chase(_cross, cross, smooth);
            chase(_room, room, smooth); chase(_night, night, smooth);
            chase(_gain, gain, smooth); chase(_wet, bypass ? 0 : 1, smooth);
            chase(_master, master, volumeSmooth);
            double dry[2] = { samples[i*2] / 32768.0, samples[i*2+1] / 32768.0 };
            double v[2];
            for(int ch=0; ch<2; ch++) {
                _low[ch] += lowA * (dry[ch] - _low[ch]);
                _highLow[ch] += highA * (dry[ch] - _highLow[ch]);
                v[ch] = dry[ch] + (_bass-1)*_low[ch] + (_treble-1)*(dry[ch]-_highLow[ch]);
                _roomLow[ch] += roomA * (v[ch] - _roomLow[ch]);
                v[ch] += _room * (_roomLow[ch] - v[ch]);
                _crossLow[ch] += crossA * (v[ch] - _crossLow[ch]);
            }
            double left = v[0] + _cross * (_crossLow[1] - _crossLow[0]);
            double right = v[1] + _cross * (_crossLow[0] - _crossLow[1]);
            double mid = (left+right)*.5, side = (left-right)*.5*_width;
            v[0] = mid+side; v[1] = mid-side;
            double peak = std::max(std::abs(v[0]), std::abs(v[1]));
            _envelope = std::max(peak, _envelope * release);
            double compression = _envelope > .126 ? std::pow(.126/_envelope, 2.0/3.0) : 1;
            double dynamics = 1 + _night * (compression - 1);
            for(int ch=0; ch<2; ch++) v[ch] = dry[ch] + _wet*(v[ch]*_gain*dynamics - dry[ch]);
            peak = std::max(std::abs(v[0]), std::abs(v[1]));
            double targetGuard = (!bypass && settings.peakProtection && peak > .944) ? .944/peak : 1;
            _guard = targetGuard < _guard ? targetGuard : 1 - (1-_guard)*release;
            // Guard fades out in bypass; this is a sample-peak safeguard, not a true-peak limiter.
            double outputGain = _master * (1 + _wet*(_guard-1));
            for(int ch=0; ch<2; ch++) {
                double out = std::clamp(v[ch] * outputGain, -1.0, 32767.0/32768.0);
                samples[i*2+ch] = static_cast<int16_t>(std::lround(out*32768.0));
            }
        }
    }
};
}
