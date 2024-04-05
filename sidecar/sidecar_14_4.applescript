beep 1
beep 1
tell application "System Settings"
	activate
	delay 1
	tell application "System Events"
		tell process "System Settings"
			click menu item "显示器" of menu "显示" of menu bar item "显示" of menu bar 1
			delay 0.3
			tell group 1 of group 2 of splitter group 1 of group 1 of window "显示器"
				try
					click pop up button "添加"
					delay 0.3
					if (menu item "连接键盘和鼠标至" of menu "添加" of pop up button "添加") exists then
						click menu item 7 of menu "添加" of pop up button "添加"
					else
						click menu item 3 of menu "添加" of pop up button "添加"
					end if
				on error
					delay 0.5
				end try
			end tell
		end tell
	end tell
end tell
delay 1
beep 1
tell application "System Settings" to quit