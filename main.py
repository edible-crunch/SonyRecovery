from repair.recovery_engine import RecoveryEngine

engine = RecoveryEngine()

mov = input("Recovered MOV:\n").strip().strip('"')
mp4 = input("Recovered MP4:\n").strip().strip('"')
hvcc = input("HVCC BIN:\n").strip().strip('"')

engine.load_mov(mov)
engine.load_mp4(mp4)
engine.load_hvcc(hvcc)

engine.summary()

while True:

    print()
    choice = input(
        "Frame to inspect (0 to quit): "
    )

    frame = int(choice)

    if frame == 0:
        break

    engine.analyze_sample(frame)