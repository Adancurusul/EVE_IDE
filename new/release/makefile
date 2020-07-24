
-include ../makefile.init



RM := rm -rf

-include object.mk
-include source.mk
-include RISCV/drivers/sub.mk
-include RISCV/stubs/sub.mk
-include RISCV/env_Eclipse/sub.mk
-include Peripherals/sub.mk
-include Peripherals/Source/sub.mk
-include App/sub.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(CC_DEPS)),)
-include $(CC_DEPS)
endif
ifneq ($(strip $(C++_DEPS)),)
-include $(C++_DEPS)
endif
ifneq ($(strip $(C_UPPER_DEPS)),)
-include $(C_UPPER_DEPS)
endif
ifneq ($(strip $(CXX_DEPS)),)
-include $(CXX_DEPS)
endif
ifneq ($(strip $(ASM_DEPS)),)
-include $(ASM_DEPS)
endif
ifneq ($(strip $(S_UPPER_DEPS)),)
-include $(S_UPPER_DEPS)
endif
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
ifneq ($(strip $(CPP_DEPS)),)
-include $(CPP_DEPS)
endif
endif
-include ../makefile.defs
SECONDARY_FLASH +=  \
new.hex \

SECONDARY_LIST += \
new.lst \

SECONDARY_SIZE += \
new.siz \

all: new.elf secondary-outputs
new.elf: $(OBJS) $(USER_OBJS)
	@echo 'Building target: $@'
	@echo 'Invoking: GNU RISC-V Cross C++ Linker'
	riscv-nuclei-elf-g++ -march=rv32i -mabi=ilp32 -mcmodel=medlow -msmall-data-limit=8 -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections -fno-common  -g -T "C:/Users/user/code/eve_idev0.0.2/new/RISCV/env_Eclipse/GD32VF103xB.lds" -nostartfiles -Xlinker --gc-sections -Wl,-Map,"new.map" --specs=nano.specs -o "new.elf" $(OBJS) $(USER_OBJS) $(LIBS)
	@echo 'Finished building target: $@'
	@echo ' '
new.bin: new.elf 
	riscv-nuclei-elf-objcopy -O binary "new.elf"  "new.bin"

new.hex: new.elf
	riscv-nuclei-elf-objcopy -O ihex "new.elf"  "new.hex"

new.lst: new.elf
	riscv-nuclei-elf-objdump --source --all-headers --demangle --line-numbers --wide "new.elf" > "new.lst"

new.siz: new.elf
	riscv-nuclei-elf-size --format=berkeley "new.elf"

clean:
	-$(RM) $(CC_DEPS)$(C++_DEPS)$(OBJS)$(C_UPPER_DEPS)$(CXX_DEPS)$(SECONDARY_FLASH)$(SECONDARY_LIST)$(SECONDARY_SIZE)$(ASM_DEPS)$(S_UPPER_DEPS)$(C_DEPS)$(CPP_DEPS) new.elf

secondary-outputs: $(SECONDARY_FLASH) $(SECONDARY_LIST) $(SECONDARY_SIZE)

.PHONY: all clean dependents

-include ../makefile.targets