set counter to 0
set x to 0
beep 1

repeat while counter = 0 and x < 5
	tell application "System Settings"
		activate
		delay 1
		tell application "System Events"
			tell process "System Settings"
				click menu item "显示器" of menu "显示" of menu bar item "显示" of menu bar 1
				delay 0.5
				tell group 1 of group 2 of splitter group 1 of group 1 of window "显示器"
					try
						click pop up button 1
						delay 0.6
						if (menu item "连接键盘和鼠标至" of menu 1 of pop up button 1) exists then
							click menu item 5 of menu 1 of pop up button 1
						else
							click menu item 2 of menu 1 of pop up button 1
						end if
						set counter to 1
					on error
						if x = 0 then say "Sorry,Try again"
						set x to x + 1
						delay 2
					end try
				end tell
			end tell
		end tell
	end tell
end repeat
tell application "System Settings" to quit
if x = 5 then
	say "there are some errors"
end if