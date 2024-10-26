{"mode":"Text","hardwareTarget":"brain","textContent":"#region VEXcode Generated Robot Configuration\nfrom vex import *\nimport urandom\n\n# Brain should be defined by default\nbrain=Brain()\n\n# Robot configuration code\n\n\n# wait for rotation sensor to fully initialize\nwait(30, MSEC)\n\n\n# Make random actually random\ndef initializeRandomSeed():\n    wait(100, MSEC)\n    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()\n    urandom.seed(int(random))\n      \n# Set random seed \ninitializeRandomSeed()\n\n\ndef play_vexcode_sound(sound_name):\n    # Helper to make playing sounds from the V5 in VEXcode easier and\n    # keeps the code cleaner by making it clear what is happening.\n    print(\"VEXPlaySound:\" + sound_name)\n    wait(5, MSEC)\n\n# add a small delay to make sure we don't print in the middle of the REPL header\nwait(200, MSEC)\n# clear the console to make sure we don't have the REPL in the console\nprint(\"\\033[2J\")\n\n#endregion VEXcode Generated Robot Configuration\n\n\nmyVariable = 0\n\ndef when_started1():\n    global myVariable\n    pass\n\nwhen_started1()\n","textLanguage":"python","robotConfig":[],"slot":0,"platform":"V5","sdkVersion":"20240802.15.00.00","appVersion":"4.0.5","minVersion":"3.1.0","fileFormat":"2.0.0","targetBrainGen":"First","v5Sounds":[{"name":"game over","url":"static/sounds/mixkit-arcade-retro-game-over-213.wav"}],"v5SoundsEnabled":false,"target":"Physical"}