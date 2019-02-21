

(

)
429.06*30 =12872

~sndbuf = Buffer.read(s, "/Users/abe/Desktop/THESIS_WORK/audio/audOnly.wav"); // 19.02

)
~sndbuf.play;
1/30

(




SynthDef.new(\grain, {
	arg amp=1, grainFreq = 30, grainPeriod = 0.1, myRate = 1,  position=0.5,  sndbuf, pan = 0, out = 0, gate = 0, envTime = 429.1;
	var env, trig, duration, sig, posEnv, saw;

	env = EnvGen.kr(Env.adsr(0.05, 0.1, 0.5, 3), gate);
	trig = Impulse.ar(grainFreq);
	posEnv = EnvGen.kr(Env([0,1], [envTime], 'lin', 1));

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
b.openRead("/Users/abe/Desktop/THESIS_WORK/audio/audOnly.wav"); //19.02
b.duration;
b.numChannels;
b.free;

(
x = Synth.new(\grain);

OSCdef.new(
	\toggle,
	{
		arg msg, time, addr, port;
		x.set(\gate, msg[1]);
		msg[1].postln;
	},
	'/toggler' //remember different "/" direction for python osc
);


OSCdef.new(
	\python,
	{
		arg msg, time, addr, port;
		var duration, frameRate = 24;
		duration = 19.02; // seconds of buffer
		duration = duration * frameRate; // frameRate = grainFreq
//		msg[1].postln;
		~pointer = (msg[1]/duration);
		x.set(\position, ~pointer);
	},
	'/filter' //remember different "/" direction for python osc
);

)

x.set(\gate, 0);


NetAddr.langPort;