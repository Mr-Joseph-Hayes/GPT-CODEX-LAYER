#include "RasterAudioProcessor.h"
#include <cassert>
#include <iostream>
#include <vector>
#include <random>
#include <limits>
#include <chrono>
using namespace Raster;
using Samples = std::vector<int16_t>;
Samples signal(size_t frames, double amplitude=.3) {
 Samples b(frames*2);
 for(size_t i=0;i<frames;i++) { b[i*2]=(int16_t)(32767*amplitude*std::sin(i*.071)); b[i*2+1]=(int16_t)(32767*amplitude*std::cos(i*.053)); }
 return b;
}
double rms(const Samples& v) { double s=0;for(auto x:v)s+=(double)x*x;return std::sqrt(s/v.size())/32768; }
int main() {
 int tests=0;
 for(Mode mode : {Mode::Vanilla,Mode::Direct}) {
  Samples v(65536);for(size_t i=0;i<v.size();i++)v[i]=(int16_t)(i-32768);auto original=v;
  AudioProcessor p;AudioSettings s;s.mode=mode;s.bassDb=6;s.width=1.5;
  p.Process(v.data(),v.size()/2,48000,s);assert(v==original);tests++;
 }
 for(unsigned mode=0;mode<7;mode++) {
  auto v=signal(48000); AudioProcessor p;AudioSettings s;s.mode=(Mode)mode;
  p.Process(v.data(),v.size()/2,48000,s);assert(rms(v)>0.015 && rms(v)<.3);
  std::cout<<"mode "<<mode<<" rms="<<rms(v)<<"\n"; tests++;
 }
 // Mono remains mono in every mode, including the wider cinema preset.
 for(unsigned mode=0;mode<7;mode++) {
  auto v=signal(4800);for(size_t i=0;i<v.size();i+=2)v[i+1]=v[i];
  AudioProcessor p;AudioSettings s;s.mode=(Mode)mode;p.Process(v.data(),v.size()/2,48000,s);
  for(size_t i=0;i<v.size();i+=2) { assert(v[i]==v[i+1]); }
  tests++;
 }
 // Audio callback block size cannot alter the stream.
 for(unsigned mode=0;mode<7;mode++) {
  auto all=signal(48000),blocks=all; AudioProcessor a,b;AudioSettings s;s.mode=(Mode)mode;
  a.Process(all.data(),48000,48000,s);
  for(size_t i=0;i<48000;i+=128)b.Process(blocks.data()+i*2,std::min(size_t(128),48000-i),48000,s);
  assert(all==blocks);tests++;
 }
 // Stereo isolation in Reference, crossfeed only when requested.
 for(Mode m : {Mode::Reference,Mode::Headphones}) {
  Samples v(48000*2);for(size_t i=0;i<48000;i++)v[i*2]=(int16_t)(12000*std::sin(i*.01));
  AudioSettings s;s.mode=m;AudioProcessor p;p.Process(v.data(),48000,48000,s);
  bool right=false;for(size_t i=1;i<v.size();i+=2)right=right||v[i]!=0;
  assert(right == (m==Mode::Headphones));tests++;
 }
 // A mute reaches digital silence, unmute stays bounded, invalid tuning is sanitized.
 {
  AudioProcessor p;AudioSettings s;auto v=signal(48000);p.Process(v.data(),48000,48000,s);
  v=signal(48000);p.Process(v.data(),48000,48000,s,0);
  for(size_t i=v.size()-4000;i<v.size();i++) { assert(v[i]==0); }
  tests++;
  s.bassDb=std::numeric_limits<double>::quiet_NaN();s.width=std::numeric_limits<double>::infinity();
  v=signal(48000);p.Process(v.data(),48000,48000,s,1);assert(rms(v)>.05);tests++;
 }
 // No full-scale clipping with maximum legal boost/width in every curated preset.
 for(unsigned mode : {0u,2u,3u,4u,5u}) {
  Samples v(96000);std::mt19937 r(34);for(auto& x:v)x=(int16_t)r();
  AudioProcessor p;AudioSettings s;s.mode=(Mode)mode;s.bassDb=6;s.trebleDb=6;s.width=1.5;
  p.Process(v.data(),48000,48000,s);for(auto x:v)assert(std::abs((int)x)<32767);tests++;
 }
 // Sample-rate changes, repeated mode/volume transitions, and empty buffers.
 {
  AudioProcessor p;AudioSettings s;
  for(unsigned rate : {11025u,22050u,32000u,44100u,48000u,96000u}) {
   for(unsigned mode=0;mode<7;mode++) {auto v=signal(4000);s.mode=(Mode)mode;p.Process(v.data(),4000,rate,s,.8);}
  }
  p.Process(nullptr,0,48000,s);p.Reset();tests++;
 }
 std::cout<<"PASS "<<tests<<" behavioral checks\n";
}
