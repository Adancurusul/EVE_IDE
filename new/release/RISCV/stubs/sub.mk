C_SRCS += \
./RISCV/stubs/close.c \
./RISCV/stubs/fstat.c \
./RISCV/stubs/isatty.c \
./RISCV/stubs/lseek.c \
./RISCV/stubs/read.c \
./RISCV/stubs/sbrk.c \
./RISCV/stubs/write.c \
./RISCV/stubs/write_hex.c \
./RISCV/stubs/_exit.c 

OBJS += \
./RISCV/stubs/close.o \
./RISCV/stubs/fstat.o \
./RISCV/stubs/isatty.o \
./RISCV/stubs/lseek.o \
./RISCV/stubs/read.o \
./RISCV/stubs/sbrk.o \
./RISCV/stubs/write.o \
./RISCV/stubs/write_hex.o \
./RISCV/stubs/_exit.o 


C_DEPS += \
./RISCV/stubs/close.d \
./RISCV/stubs/fstat.d \
./RISCV/stubs/isatty.d \
./RISCV/stubs/lseek.d \
./RISCV/stubs/read.d \
./RISCV/stubs/sbrk.d \
./RISCV/stubs/write.d \
./RISCV/stubs/write_hex.d \
./RISCV/stubs/_exit.d


RISCV/stubs/%.o: ../RISCV/stubs/%.c
	riscv-nuclei-elf-gcc -march=rv32i -mabi=ilp32 -mcmodel=medlow -msmall-data-limit=8 -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections -fno-common  -g -I"C:/Users/user/code/eve_idev0.0.2/new/Application" -I"C:/Users/user/code/eve_idev0.0.2/new/Peripherals" -I"C:/Users/user/code/eve_idev0.0.2/new/Peripherals/Include" -I"C:/Users/user/code/eve_idev0.0.2/new/Peripherals/Source" -I"C:/Users/user/code/eve_idev0.0.2/new/RISCV/stubs" -I"C:/Users/user/code/eve_idev0.0.2/new/RISCV/drivers" -I"C:/Users/user/code/eve_idev0.0.2/new/RISCV/env_Eclipse" -std=gnu11 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -c -o "$@" "$<"
