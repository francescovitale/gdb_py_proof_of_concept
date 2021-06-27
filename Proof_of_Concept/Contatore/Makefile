# The folder has the following structure:
# inc
# src
# obj
# elf
# bin

# A rule creates the folders obj, elf and bin

# A rule creates the object files from the .c files and places them in the obj folder

# A rule creates the object files from the .s files and places them in the obj folder

# A rule creates the elf files from the .o files and places them in the elf folder
 
# A rule creates the bin files from the .elf files and places them in the bin folder

TARGET     = demo

MCU_MC     = STM32F303xC
MCU_LC     = stm32f303xc

DEFS       = -D$(MCU_MC)
DEFS       += -DUSE_DBPRINTF

INCS       = -Iinc
INCS      += -I../../../Materiale_STM_per_STM32F303/Drivers/CMSIS/Include
INCS      += -I../../../Materiale_STM_per_STM32F303/Drivers/CMSIS/Device/ST/STM32F3xx/Include
INCS	  += -I../../../Materiale_STM_per_STM32F303/Drivers/STM32F3xx_HAL_Driver/Inc
INCS	  += -I../../../Materiale_STM_per_STM32F303/Drivers/BSP/STM32F3-Discovery

PREFIX     = arm-none-eabi
CC         = $(PREFIX)-gcc
AR         = $(PREFIX)-ar
OBJCOPY    = $(PREFIX)-objcopy
OBJDUMP    = $(PREFIX)-objdump
SIZE       = $(PREFIX)-size
GDB        = $(PREFIX)-gdb-py

CFLAGS	   = -Wall -g -std=c99 -Os
CFLAGS    += -mlittle-endian -mcpu=cortex-m4 -march=armv7e-m -mthumb
CFLAGS    += -mfpu=fpv4-sp-d16 -mfloat-abi=hard
CFLAGS    += -ffunction-sections -fdata-sections
CFLAGS    += $(INCS) $(DEFS)

LIBS       = -LCMSIS/Lib

LDFLAGS    = -Wl,--gc-sections -Wl,-Map=$(TARGET).map $(LIBS) -Tls/STM32F303VCTx_FLASH.ld

LDFLAGS   += --specs=rdimon.specs -lc -lrdimon

SRCS = \
src/main.c \
src/system_stm32f3xx.c \
src/stm32f3xx_hal_msp.c \
src/stm32f3xx_it.c \
src/stm32f3xx_hal_tim.c \
src/stm32f3xx_hal.c \
src/stm32f3xx_hal_gpio.c \
src/stm32f3xx_hal_rcc.c \
src/stm32f3xx_hal_cortex.c \
src/stm32f3xx_hal_tim_ex.c \
src/stm32f3_discovery.c

SRCS_FN = $(notdir $(SRCS))

OBJS       = $(addprefix obj/,$(SRCS_FN:.c=.o))
DEPS       = $(addprefix dep/,$(SRCS_FN:.c=.d))

.PHONY: all dirs debug prepare clean

all: $(TARGET).bin

-include $(DEPS)

dirs: dep obj

dep obj:

	@echo "[MKDIR]   $@"
	mkdir -p $@

obj/%.o : src/%.c 
	@echo "generating \"$@\" from \"$<\""
	$(CC) $(CFLAGS) -c -o $@ $< -MMD -MF dep/$(*F).d

$(TARGET).elf: $(OBJS)
	@echo "[LD]      $(TARGET).elf"
	$(CC) $(CFLAGS) $(LDFLAGS) src/startup_$(MCU_LC).s $^ -o $@
	@echo "[OBJDUMP] $(TARGET).lst"
	$(OBJDUMP) -St $(TARGET).elf >$(TARGET).lst
	@echo "[SIZE]    $(TARGET).elf"
	$(SIZE) $(TARGET).elf
	
$(TARGET).bin: $(TARGET).elf
	@echo "[OBJCOPY] $(TARGET).bin"
	$(OBJCOPY) -O binary $< $@	
	
debug:
	#@if ! nc -z localhost 3333; then \
	#	@echo "\n\t[Error] OpenOCD is not running!\n"; exit 1; \
	#else \
	$(GDB)  -ex "target extended localhost:3333" \
			-ex "monitor arm semihosting enable" \
			-ex "monitor reset halt" \
			-ex "load" \
			-ex "monitor reset init" \
			$(GDBFLAGS) $(TARGET).elf; \
	#Efi	

clean:
	@echo "[RM]      $(TARGET).bin"; rm -f $(TARGET).bin
	@echo "[RM]      $(TARGET).elf"; rm -f $(TARGET).elf
	@echo "[RM]      $(TARGET).map"; rm -f $(TARGET).map
	@echo "[RM]      $(TARGET).lst"; rm -f $(TARGET).lst
	#@echo "[RM]      src files"; rm -f src/*
	#@echo "[RM]      ld script"; rm -f src/linkerScript.ld
	@echo "[RMDIR]   dep"          ; rm -fr dep
	@echo "[RMDIR]   obj"          ; rm -fr obj
	#@echo "[RMDIR]   src"          ; rm -fr src