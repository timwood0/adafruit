-- D1 is connected to green led
-- D2 is connected to blue led
-- D3 is connected to red led
require("pwm")
HZ = 200
DC = 255
pwm.setup(1, 500, 512)
pwm.setup(2, 500, 512)
pwm.setup(3, 500, 512)
pwm.start(1)
pwm.start(2)
pwm.start(3)

function led(r, g, b)
	pwm.setduty(1, g)
	pwm.setduty(2, b)
	pwm.setduty(3, r)
end

function al1()
	if lighton==0 then
		lighton=1
		led(DC, DC, DC)
		-- 512/1024, 50% duty cycle
	else
		lighton=0
		led(0, 0, 0)
	end
end

function l1()
	light(1)
end

function l2()
	light(2)
end

function l3()
	light(3)
end


function light(l)
	if lon[l] == 0 then
		lon[l] = 1
		pwm.setduty(l, DC)
	else
		lon[l] = 0
		pwm.setduty(l, 0)
	end
end

--led(512, 0, 0)
--led(0, 0, 512)

lon = { 0, 0, 0 }
lighton=0

tmr.alarm(0, HZ, 1, l1)
tmr.alarm(1, HZ - 63, 1, l2)
tmr.alarm(2, HZ + 63, 1, l3)
