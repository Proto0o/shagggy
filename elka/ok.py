import sounddevice as sd
  # seconds

def callback(indata, outdata, frames, time, status):
	if status:
		print(status)
	outdata[:] = indata

while True:
	x=sd.Stream.read(frames=1)
	print(x)