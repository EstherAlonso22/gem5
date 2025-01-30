cd util/m5 && scons build/x86/out/m5;

scons arm64.CROSS_COMPILE=aarch64-linux-gnu- build/arm64/out/m5;
