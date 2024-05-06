on findLastTargetIndex(targetItem, itemList)
	set lastIndex to 0
	repeat with i from (count of itemList) to 1 by -1
		if item i of itemList is targetItem then
			set lastIndex to i
			exit repeat
		end if
	end repeat
	return lastIndex
end findLastTargetIndex

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
					-- 获取所有菜单项的名称
					set menuItems to name of menu items of menu "添加" of pop up button "添加"
					-- 通过名字查找要准确一些，这里去找最后一个名字的索引，因为如果 ipadpro 有妙控键盘，就会出现两个名字，我们需要最后一个名字，第一个名字是连接键鼠的
					set targetIndex to (my findLastTargetIndex("XXX‘s iPad", menuItems))
					
					-- 点击目标菜单项
					click menu item targetIndex of menu "添加" of pop up button "添加"
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
