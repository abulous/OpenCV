(

OSCdef.new(
	\python,
	{
		arg msg, time, addr, port;
//		msg[1].postln;
		~pointer = (msg[1]/18921546);
//		~pointer = (msg[1]/430);

//		~pointer.postln;
		x.set(\position, ~pointer);
	},
	'/filter'
);
)

 ~sndbuf = Buffer.read(s, "/Users/abe/Desktop/THESIS_WORK/Audio/rvv19Mono.wav"); // 429.06

~sndbuf.play;


(
OSCdef.new(
	\toggle,
	{
		arg msg, time, addr, port;
		x.set(\gate, msg[1]);
	},
	'/1/toggle'
);

OSCdef.new(
	\fader1,
	{
		arg msg, time, addr, port;
		x.set(\envTime, msg[1].linlin(0, 1, 1, 430));
		msg[1].postln;
	//	x.set(\position, msg[1]);
	},
	'/1/fader1'
);
)
1/18921546

(
SynthDef.new(\grain, {
	arg amp=1, grainFreq = 100, grainPeriod = 0.1, myRate = 1,  position=0.5,  sndbuf, pan = 0, out = 0, gate = 0, envTime = 1;
	var env, trig, duration, sig, posEnv, saw;

	env = EnvGen.kr(Env.adsr(0.05, 0.1, 0.5, 3), gate);
	trig = Impulse.ar(grainFreq);
	posEnv = EnvGen.kr(Env.circle([0,1], [envTime, 1], 'lin', 1));
	//saw = Saw.kr(

 	duration = 429.06.reciprocal;

	sig = GrainBuf.ar(1, trig, grainPeriod, ~sndbuf, myRate, position, 2);
 	/*sig = GrainBuf.ar(
 		\numChannels, 1,
 		\trigger, trig,
 		\dur, grainPeriod,
 		\sndbuf, ~sndbuf,
 		\rate, myRate,
 		\pos, position,
 		\interp, 2,
 	) ;*/
	sig = Pan2.ar(sig, pan);
	sig = sig * env * amp;
	Out.ar(out, sig);
}).add


)

b = SoundFile.new;
b.openRead("/Users/abe/Desktop/THESIS_WORK/Audio/rvv19Mono.wav"); // 429.06
b.duration;
b.numChannels;
b.free;


x.set(\envTime, 10);

x = Synth.new(\grain);
x = Synth.new(\grain, [\gate, 1]);
x.set(\freq, 70)
x.set(\gate, 0)






NetAddr.langPort;