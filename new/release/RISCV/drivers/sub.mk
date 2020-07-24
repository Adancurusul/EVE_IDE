C_SRCS += \
./RISCV/drivers/n200_func.c 

OBJS += \
./RISCV/drivers/n200_func.o 


C_DEPS += \
./RISCV/drivers/n200_func.d


RISCV/drivers/%.o: ../RISCV/drivers/%.c
	riscv-nuclei-elf-gcc -march=rv32i -mabi=ilp32 -mcmodel=medlow -msmall-data-limit=8 -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections -fno-common  -g -I"C:/Users/user/code/eve_idev0.0.2/new/Application" -I"C:/Users/user/code/eve_idev0.0.2/new/Peripherals" -I"C:/Users/user/code/eve_idev0.0.2/new/Peripherals/Include" -I"C:/Users/user/code/eve_idev0.0.2/new/Peripherals/Source" -I"C:/Users/user/code/eve_idev0.0.2/new/RISCV/stubs" -I"C:/Users/user/code/eve_idev0.0.2/new/RISCV/drivers" -I"C:/Users/user/code/eve_idev0.0.2/new/RISCV/env_Eclipse" -std=gnu11 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -c -o "$@" "$<"
