



~sndbuf = Buffer.read(s, "/Users/abe/Desktop/THESIS_WORK/audio/audOnly.wav"); // 19.02


~sndbuf.play;
1/30

(




SynthDef.new(\grain, {
	arg amp=1, grainFreq = 24, grainPeriod = 0.1, myRate = 1,  position=0.5,  sndbuf, pan = 0, out = 0, gate = 0, envTime = 19.02;
	var env, trig, duration, sig, posEnv, saw;

	env = EnvGen.kr(Env.adsr(0.05, 0.1, 0.5, 3), gate);
	trig = Impulse.ar(grainFreq);
	posEnv = EnvGen.kr(Env.circle([0,1], [envTime, 1], 'lin', 1));

 	duration = 429.06.reciprocal;
	sig = GrainBuf.ar(1, trig, grainPeriod, ~sndbuf, myRate, posEnv, 2);
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
x = Synth.new(\grain, [\gate, 1]);
)

x.set(\grainFreq, 120);
x.set(\amp, 12.dbamp);
x.set(\envTime, 19*10);


NetAddr.langPort;