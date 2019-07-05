while true do
	emu.speedmode("normal") -- Set the speed of the emulator

	-- Declare and set variables or functions if needed

	frame = 1

	while true do
		
		-- Execute instructions for FCEUX
		if (frame < 150 and frame > 50) then	
			joypad.write(1, {start=1})
		else
			joypad.write(1, {right=1})
		end;
		
		black = frame > 200
		if frame > 200 then
			for x = 0, 255 do
				r,g,b,palette = emu.getscreenpixel(x, 100, true)
				if (r ~= 0 or g ~= 0 or b ~= 0) then
					black = false
				end;
			end;
		end;
		if (black) then
			print("RESTART");
			break;
		end;
		
		gui.text(20, 20, frame)
	  	emu.frameadvance() -- This essentially tells FCEUX to keep running
		frame = frame + 1

	end;
	emu.softreset()
end;
