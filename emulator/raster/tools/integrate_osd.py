from pathlib import Path
p=Path('work/MesenCE-master')
f=p/'Core/Shared/Video/SystemHud.cpp';s=f.read_text()
s=s.replace('DrawMessages(hud, width, height);','''DrawMessages(hud, width, height);
    AudioConfig rasterAudio = _emu->GetSettings()->GetAudioConfig();
    if((!rasterAudio.EnableAudio || rasterAudio.MasterVolume == 0) && _emu->IsRunning()) {
        hud->DrawRectangle(25, 6, 39, 13, 0x3010191D, true, 1);
        hud->DrawString(29, 9, "MUTED", 0xA7DCCB, 0xFF000000, 1);
    }''')
s=s.replace('//Get opacity for fade in/out effect','''if(msg.GetTitle() == "RASTER SOUND") {
        AudioConfig c = _emu->GetSettings()->GetAudioConfig();
        const char* names[] = { "REFERENCE", "VANILLA", "CRT / LIVING ROOM", "HEADPHONES", "NIGHT", "CINEMA", "DIRECT" };
        int w = std::min(230, (int)screenWidth - 16);
        int x = ((int)screenWidth-w)/2;
        int y = std::max(4, (int)screenHeight-64);
        int alpha = (int)((1.0f-msg.GetOpacity())*255) << 24;
        hud->DrawRectangle(x, y, w, 54, 0x101A1F | alpha, true, 1);
        hud->DrawRectangle(x, y, w, 54, 0x456B65 | alpha, false, 1);
        string title = names[std::min(6u, c.RasterMode)];
        bool muted = !c.EnableAudio || c.MasterVolume == 0;
        string status = muted ? "MUTED" : "VOLUME " + std::to_string(c.MasterVolume) + "%";
        hud->DrawString(x+10, y+8, title, 0xAFF2DA | alpha, 0xFF000000, 1, -1, w-20);
        hud->DrawString(x+10, y+20, status, 0xE8F1EE | alpha, 0xFF000000, 1, -1, w-20);
        int bars = std::max(1, (w-20)/6);
        int filled = muted ? 0 : (int)(std::min(100u,c.MasterVolume)*bars/100);
        for(int i=0; i<bars; i++) hud->DrawRectangle(x+10+i*6, y+32, 4, 5, (i<filled ? 0x96E4C9 : 0x31434A) | alpha, true, 1);
        hud->DrawString(x+10, y+43, "CTRL +/-   CTRL M", 0x91ADB0 | alpha, 0xFF000000, 1, -1, w-20);
        lastHeight += 64;
        return;
    }
    //Get opacity for fade in/out effect''')
s=s.replace('_messages.push_front(std::make_unique<MessageInfo>(title, message, 3000));','''if(title == "RASTER SOUND") {
        _messages.remove_if([](unique_ptr<MessageInfo>& m) { return m->GetTitle() == "RASTER SOUND"; });
    }
    _messages.push_front(std::make_unique<MessageInfo>(title, message, title == "RASTER SOUND" ? 2200 : 3000));''')
f.write_text(s)
