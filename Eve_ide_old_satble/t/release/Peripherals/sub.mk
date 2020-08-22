C_SRCS += \
./Peripherals/system_gd32vf103.c 

OBJS += \
./Peripherals/system_gd32vf103.o 


C_DEPS += \
./Peripherals/system_gd32vf103.d


Peripherals/%.o: ../Peripherals/%.c
	riscv-nuclei-elf-gcc -march=rv32i -mabi=ilp32 -mcmodel=medlow -msmall-data-limit=8 -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections -fno-common  -g -I"D:/codes/python/Eve_ide/t/Application" -I"D:/codes/python/Eve_ide/t/Peripherals" -I"D:/codes/python/Eve_ide/t/Peripherals/Include" -I"D:/codes/python/Eve_ide/t/Peripherals/Source" -I"D:/codes/python/Eve_ide/t/RISCV/stubs" -I"D:/codes/python/Eve_ide/t/RISCV/drivers" -I"D:/codes/python/Eve_ide/t/RISCV/env_Eclipse" -std=gnu11 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -c -o "$@" "$<"
