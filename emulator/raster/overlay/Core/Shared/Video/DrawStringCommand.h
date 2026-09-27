#pragma once
#include "pch.h"
#include "Shared/Video/DrawCommand.h"

class DrawStringCommand : public DrawCommand
{
private:
	int _x, _y, _color, _backColor;
	int _maxWidth = 0;
	string _text;

	//Taken from FCEUX's LUA code
	static constexpr int _tabSpace = 4;

	static unordered_map<int, char const*> _jpFont;

	// clang-format off
	static constexpr uint8_t _font[768] = {
        6, 0, 0, 0, 0, 0, 0, 0,
        6, 32, 32, 32, 32, 32, 0, 32,
        6, 80, 80, 80, 0, 0, 0, 0,
        6, 80, 80, 248, 80, 248, 80, 80,
        6, 32, 120, 160, 112, 40, 240, 32,
        6, 200, 208, 16, 32, 64, 88, 152,
        6, 96, 144, 160, 64, 168, 144, 104,
        6, 32, 32, 32, 0, 0, 0, 0,
        6, 16, 32, 64, 64, 64, 32, 16,
        6, 64, 32, 16, 16, 16, 32, 64,
        6, 0, 168, 112, 248, 112, 168, 0,
        6, 0, 32, 32, 248, 32, 32, 0,
        6, 0, 0, 0, 0, 48, 32, 64,
        6, 0, 0, 0, 248, 0, 0, 0,
        6, 0, 0, 0, 0, 0, 48, 48,
        6, 8, 8, 16, 32, 64, 128, 128,
        6, 112, 136, 152, 168, 200, 136, 112,
        6, 32, 96, 32, 32, 32, 32, 112,
        6, 112, 136, 8, 48, 64, 128, 248,
        6, 240, 8, 8, 112, 8, 8, 240,
        6, 16, 48, 80, 144, 248, 16, 16,
        6, 248, 128, 128, 240, 8, 8, 240,
        6, 112, 128, 128, 240, 136, 136, 112,
        6, 248, 8, 16, 32, 64, 64, 64,
        6, 112, 136, 136, 112, 136, 136, 112,
        6, 112, 136, 136, 120, 8, 8, 112,
        6, 0, 48, 48, 0, 48, 48, 0,
        6, 0, 48, 48, 0, 48, 32, 64,
        6, 16, 32, 64, 128, 64, 32, 16,
        6, 0, 0, 248, 0, 248, 0, 0,
        6, 64, 32, 16, 8, 16, 32, 64,
        6, 112, 136, 8, 16, 32, 0, 32,
        6, 112, 136, 184, 168, 184, 128, 120,
        6, 112, 136, 136, 248, 136, 136, 136,
        6, 240, 136, 136, 240, 136, 136, 240,
        6, 120, 128, 128, 128, 128, 128, 120,
        6, 240, 136, 136, 136, 136, 136, 240,
        6, 248, 128, 128, 240, 128, 128, 248,
        6, 248, 128, 128, 240, 128, 128, 128,
        6, 120, 128, 128, 184, 136, 136, 120,
        6, 136, 136, 136, 248, 136, 136, 136,
        6, 112, 32, 32, 32, 32, 32, 112,
        6, 56, 16, 16, 16, 144, 144, 96,
        6, 136, 144, 160, 192, 160, 144, 136,
        6, 128, 128, 128, 128, 128, 128, 248,
        6, 136, 216, 168, 168, 136, 136, 136,
        6, 136, 200, 200, 168, 152, 152, 136,
        6, 112, 136, 136, 136, 136, 136, 112,
        6, 240, 136, 136, 240, 128, 128, 128,
        6, 112, 136, 136, 136, 168, 144, 104,
        6, 240, 136, 136, 240, 160, 144, 136,
        6, 120, 128, 128, 112, 8, 8, 240,
        6, 248, 32, 32, 32, 32, 32, 32,
        6, 136, 136, 136, 136, 136, 136, 112,
        6, 136, 136, 136, 136, 136, 80, 32,
        6, 136, 136, 136, 168, 168, 216, 136,
        6, 136, 136, 80, 32, 80, 136, 136,
        6, 136, 136, 80, 32, 32, 32, 32,
        6, 248, 8, 16, 32, 64, 128, 248,
        6, 112, 64, 64, 64, 64, 64, 112,
        6, 128, 128, 64, 32, 16, 8, 8,
        6, 112, 16, 16, 16, 16, 16, 112,
        6, 32, 80, 136, 0, 0, 0, 0,
        6, 0, 0, 0, 0, 0, 0, 248,
        6, 64, 32, 16, 0, 0, 0, 0,
        6, 0, 0, 112, 8, 120, 136, 120,
        6, 128, 128, 176, 200, 136, 136, 240,
        6, 0, 0, 120, 128, 128, 128, 120,
        6, 8, 8, 104, 152, 136, 136, 120,
        6, 0, 0, 112, 136, 248, 128, 120,
        6, 48, 72, 64, 224, 64, 64, 64,
        6, 0, 120, 136, 136, 120, 8, 112,
        6, 128, 128, 176, 200, 136, 136, 136,
        6, 32, 0, 96, 32, 32, 32, 112,
        6, 16, 0, 48, 16, 16, 144, 96,
        6, 128, 128, 136, 144, 224, 144, 136,
        6, 96, 32, 32, 32, 32, 32, 112,
        6, 0, 0, 208, 168, 168, 168, 168,
        6, 0, 0, 176, 200, 136, 136, 136,
        6, 0, 0, 112, 136, 136, 136, 112,
        6, 0, 240, 136, 136, 240, 128, 128,
        6, 0, 120, 136, 136, 120, 8, 8,
        6, 0, 0, 176, 200, 128, 128, 128,
        6, 0, 0, 120, 128, 112, 8, 240,
        6, 64, 64, 224, 64, 64, 72, 48,
        6, 0, 0, 136, 136, 136, 152, 104,
        6, 0, 0, 136, 136, 136, 80, 32,
        6, 0, 0, 136, 136, 168, 168, 80,
        6, 0, 0, 136, 80, 32, 80, 136,
        6, 0, 136, 136, 136, 120, 8, 112,
        6, 0, 0, 248, 16, 32, 64, 248,
        6, 24, 32, 32, 64, 32, 32, 24,
        6, 32, 32, 32, 32, 32, 32, 32,
        6, 192, 32, 32, 16, 32, 32, 192,
        6, 0, 0, 72, 176, 0, 0, 0,
        6, 112, 136, 8, 16, 32, 0, 32,
	};
	// clang-format off

	static int GetCharNumber(char ch)
	{
		if(ch < 32) {
			return 0;
		}

		ch -= 32;
		return (ch < 0 || ch > 94) ? 95 : ch;
	}

	static int GetCharWidth(char ch)
	{
		return _font[GetCharNumber(ch) * 8];
	}

protected:
	void InternalDraw()
	{
		int startX = (int)(_x * _xScale / std::floor(_xScale));
		int lineWidth = 0;
		int x = startX;
		int y = _y;
		int lineHeight = 9;
		
		auto newLine = [&lineWidth, &x, &y, &lineHeight, startX]() {
			lineWidth = 0;
			x = startX;
			y += lineHeight;
			lineHeight = 9;
		};

		for(int i = 0; i < _text.size(); i++) {
			unsigned char c = _text[i];
			if(c == '\n') {
				newLine();
			} else if(c == '\t') {
				int tabWidth = (_tabSpace - (((x - startX) / 8) % _tabSpace)) * 8;
				x += tabWidth;
				lineWidth += tabWidth;
				if(_maxWidth > 0 && lineWidth > _maxWidth) {
					newLine();
				}
			} else if(c == 0x20) {
				//Space (ignore spaces at the start of a new line, when text wrapping is enabled)
				if(lineWidth > 0 || _maxWidth == 0) {
					if(_backColor & 0xFF000000) {
						//Draw bg color for spaces (when bg color is set)
						for(int row = 0; row < lineHeight; row++) {
							for(int column = 0; column < 6; column++) {
								DrawPixel(x + column, y + row - 1, _backColor);
							}
						}
					}

					lineWidth += 6;
					x += 6;
				}
			} else if(c >= 0x80) {
				//8x12 UTF-8 font for Japanese
				int code = (uint8_t)c;
				if(i + 2 < _text.size()) {
					code |= ((uint8_t)_text[i + 1]) << 8;
					code |= ((uint8_t)_text[i + 2]) << 16;

					auto res = _jpFont.find(code);
					if(res != _jpFont.end()) {
						lineWidth += 8;
						if(_maxWidth > 0 && lineWidth > _maxWidth) {
							newLine();
							lineWidth += 8;
						}

						uint8_t* charDef = (uint8_t*)res->second;

						for(int row = 0; row < 12; row++) {
							uint8_t rowData = charDef[row];
							for(int column = 0; column < 8; column++) {
								int drawFg = (rowData >> (7 - column)) & 0x01;
								DrawPixel(x + column, y + row - 2, drawFg ? _color : _backColor);
							}
						}
						i += 2;
						x += 8;
						lineHeight = 12;
					}
				}
			} else {
				//Variable size font for standard ASCII
				int ch = GetCharNumber(c);
				int width = GetCharWidth(c);
				
				lineWidth += width;
				if(_maxWidth > 0 && lineWidth > _maxWidth) {
					newLine();
					lineWidth += width;
				}

				int rowOffset = 0; // Raster glyphs contain their complete seven-row design.
				for(int row = 0; row < 8; row++) {
					uint8_t rowData = ((row == 7 && rowOffset == 0) || (row == 0 && rowOffset == 1)) ? 0 : _font[ch * 8 + 1 + row - rowOffset];
					for(int col = 0; col < width; col++) {
						int drawFg = (rowData >> (7 - col)) & 0x01;
						DrawPixel(x + col, y + row, drawFg ? _color : _backColor);
					}
				}
				for(int col = 0; col < width; col++) {
					DrawPixel(x + col, y - 1, _backColor);
				}
				x += width;
			}
		}
	}

public:
	DrawStringCommand(int x, int y, string text, int color, int backColor, int frameCount, int startFrame, int maxWidth = 0, bool overwritePixels = false) :
		DrawCommand(startFrame, frameCount, true), _x(x), _y(y), _color(color), _backColor(backColor), _maxWidth(maxWidth), _text(text)
	{
		//Invert alpha byte - 0 = opaque, 255 = transparent (this way, no need to specifiy alpha channel all the time)
		_overwritePixels = overwritePixels;
		_color = (~color & 0xFF000000) | (color & 0xFFFFFF);
		_backColor = (~backColor & 0xFF000000) | (backColor & 0xFFFFFF);
	}

	static TextSize MeasureString(string& text, uint32_t maxWidth = 0)
	{
		uint32_t maxX = 0;
		uint32_t x = 0;
		uint32_t y = 0;
		uint32_t lineHeight = 9;

		auto newLine = [&]() {
			maxX = std::max(x, maxX);
			x = 0;
			y += lineHeight;
			lineHeight = 9;
		};

		for(int i = 0; i < text.size(); i++) {
			unsigned char c = text[i];
			if(c == '\n') {
				maxX = std::max(x, maxX);
				x = 0;
				y += 9;
			} else if(c == '\t') {
				x += _tabSpace - (((x / 8) % _tabSpace)) * 8;
			} else if(c == 0x20) {
				//Space (ignore spaces at the start of a new line, when text wrapping is enabled)
				if(x > 0 || maxWidth == 0) {
					if(maxWidth > 0 && x + 6 > maxWidth) {
						newLine();
					}
					x += 6;
				}
			} else if(c >= 0x80) {
				//8x12 UTF-8 font for Japanese
				int code = (uint8_t)c;
				if(i + 2 < text.size()) {
					code |= ((uint8_t)text[i + 1]) << 8;
					code |= ((uint8_t)text[i + 2]) << 16;
					auto res = _jpFont.find(code);
					if(res != _jpFont.end()) {
						if(maxWidth > 0 && x + 8 > maxWidth) {
							newLine();
						}

						i += 2;
						x += 8;
						lineHeight = 12;
					}
				}
			} else {
				//Variable size font for standard ASCII
				int charWidth = GetCharWidth(c);
				if(maxWidth > 0 && x + charWidth > maxWidth) {
					newLine();
				}
				x += charWidth;
			}
		}

		TextSize size;
		size.X = std::max(x, maxX);
		size.Y = y + lineHeight;
		return size;
	}
};
