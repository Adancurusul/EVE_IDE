C_SRCS += \
./RISCV/env_Eclipse/handlers.c \
./RISCV/env_Eclipse/init.c \
./RISCV/env_Eclipse/your_printf.c 

OBJS += \
./RISCV/env_Eclipse/entry.o \
./RISCV/env_Eclipse/handlers.o \
./RISCV/env_Eclipse/init.o \
./RISCV/env_Eclipse/start.o \
./RISCV/env_Eclipse/your_printf.o 


C_DEPS += \
./RISCV/env_Eclipse/handlers.d \
./RISCV/env_Eclipse/init.d \
./RISCV/env_Eclipse/your_printf.d


S_UPPER_SRCS += \
./RISCV/env_Eclipse/entry.S \
./RISCV/env_Eclipse/start.S 

S_UPPER_DEPS += \
./RISCV/env_Eclipse/entry.d \
./RISCV/env_Eclipse/start.d

RISCV/env_Eclipse/%.o: ../RISCV/env_Eclipse/%.S
	riscv-nuclei-elf-gcc -march=rv32i -mabi=ilp32 -mcmodel=medlow -msmall-data-limit=8 -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections -fno-common  -g -I"C:/Users/user/code/eve_idev0.0.2/new/Application" -I"C:/Users/user/code/eve_idev0.0.2/new/Peripherals" -I"C:/Users/user/code/eve_idev0.0.2/new/Peripherals/Include" -I"C:/Users/user/code/eve_idev0.0.2/new/Peripherals/Source" -I"C:/Users/user/code/eve_idev0.0.2/new/RISCV/stubs" -I"C:/Users/user/code/eve_idev0.0.2/new/RISCV/drivers" -I"C:/Users/user/code/eve_idev0.0.2/new/RISCV/env_Eclipse" -std=gnu11 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -c -o "$@" "$<"
RISCV/env_Eclipse/%.o: ../RISCV/env_Eclipse/%.c
	riscv-nuclei-elf-gcc -march=rv32i -mabi=ilp32 -mcmodel=medlow -msmall-data-limit=8 -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections -fno-common  -g -I"C:/Users/user/code/eve_idev0.0.2/new/Application" -I"C:/Users/user/code/eve_idev0.0.2/new/Peripherals" -I"C:/Users/user/code/eve_idev0.0.2/new/Peripherals/Include" -I"C:/Users/user/code/eve_idev0.0.2/new/Peripherals/Source" -I"C:/Users/user/code/eve_idev0.0.2/new/RISCV/stubs" -I"C:/Users/user/code/eve_idev0.0.2/new/RISCV/drivers" -I"C:/Users/user/code/eve_idev0.0.2/new/RISCV/env_Eclipse" -std=gnu11 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -c -o "$@" "$<"
