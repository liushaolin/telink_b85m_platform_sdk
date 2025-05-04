TEL_PATH := @@@TEMPLATE@@@
TEL_CHIP := B85
PROJECT_NAME := @@@TEMPLATE@@@
PROJECT_PATH := .

# OUT
OUT_PATH := $(TEL_PATH)/build/$(PROJECT_NAME)

# Directoris
DIRS := \
    $(TEL_PATH)/chip/$(TEL_CHIP)/boot \
    $(TEL_PATH)/common \
    $(TEL_PATH)/chip/$(TEL_CHIP)/drivers \
    $(TEL_PATH)/demo/vendor/common/$(TEL_CHIP) \
    $(PROJECT_PATH)

SRCS :=
OBJS :=
LIBS :=  -ldriver

boot_dir := $(TEL_PATH)/chip/$(TEL_CHIP)/boot
boot_srcs := $(wildcard $(boot_dir)/*.S)
boot_objs := $(patsubst $(boot_dir)/%.S,$(OUT_PATH)/boot/%.o,$(boot_srcs))
SRCS += $(boot_srcs)
OBJS += $(boot_objs)

common_dir := $(TEL_PATH)/common
common_srcs := $(wildcard $(common_dir)/*.c) $(wildcard $(common_dir)/*.S)
common_objs := $(patsubst $(common_dir)/%.c,$(OUT_PATH)/common/%.o,$(filter %.c,$(common_srcs))) \
               $(patsubst $(common_dir)/%.S,$(OUT_PATH)/common/%.o,$(filter %.S,$(common_srcs)))
SRCS += $(common_srcs)
OBJS += $(common_objs)

drivers_dir := $(TEL_PATH)/chip/$(TEL_CHIP)/drivers
drivers_srcs := $(wildcard $(drivers_dir)/*.c) $(wildcard $(drivers_dir)/*/*.c)
drivers_objs := $(patsubst $(drivers_dir)/%.c,$(OUT_PATH)/drivers/%.o,$(drivers_srcs))
SRCS += $(drivers_srcs)
OBJS += $(drivers_objs)

vendor_dir := $(TEL_PATH)/demo/vendor/common/$(TEL_CHIP)
vendor_srcs := $(wildcard $(vendor_dir)/*.c) $(wildcard $(vendor_dir)/*/*.c)
vendor_objs := $(patsubst $(vendor_dir)/%.c,$(OUT_PATH)/vendor/%.o,$(vendor_srcs))
SRCS += $(vendor_srcs)
OBJS += $(vendor_objs)

proj_srcs := $(wildcard $(PROJECT_PATH)/*.c)
proj_objs := $(patsubst $(PROJECT_PATH)/%.c,$(OUT_PATH)/project/%.o,$(proj_srcs))
SRCS += $(proj_srcs)
OBJS += $(proj_objs)

# COMPILE OPTIONS
TC32PATH = tc32
AS      = $(TC32PATH)-elf-as
CC      = $(TC32PATH)-elf-gcc
LD      = $(TC32PATH)-elf-ld
NM      = $(TC32PATH)-elf-nm
OBJCOPY = $(TC32PATH)-elf-objcopy
OBJDUMP = $(TC32PATH)-elf-objdump
ARCH    = $(TC32PATH)-elf-ar
SIZE    = $(TC32PATH)-elf-size

GCC_FLAGS := \
-ffunction-sections \
-fdata-sections \
-Wall \
-O2 \
-fpack-struct \
-fshort-enums \
-finline-small-functions \
-std=gnu99 \
-fshort-wchar \
-fms-extensions 

ifeq ($(RETENTION_RAM_SIZE), 32KB)
	BOOT_FLAG := -DMCU_STARTUP_FLASH
else
	BOOT_FLAG := -DMCU_STARTUP_FLASH
endif

ifeq ($(RETENTION_RAM_SIZE), 32KB)
	LS_FLAGS := $(TEL_PATH)/project/tlsr_tc32/$(TEL_CHIP)/boot.link
else
	LS_FLAGS := $(TEL_PATH)/project/tlsr_tc32/$(TEL_CHIP)/link/boot_normal.link
endif

GCC_FLAGS += -DMCU_CORE_B85

INCLUDE_PATHS := -I$(PROJECT_PATH) -I$(TEL_PATH)/common -I$(TEL_PATH)/chip/$(TEL_CHIP)/drivers \
				-I$(TEL_PATH)/demo/vendor/common/$(TEL_CHIP)/calibration \
				-I$(TEL_PATH)/demo/vendor/common/$(TEL_CHIP)/flash

# TARGET
ELF_FILE := $(OUT_PATH)/$(PROJECT_NAME).elf
LST_FILE := $(OUT_PATH)/$(PROJECT_NAME).lst
BIN_FILE := $(OUT_PATH)/$(PROJECT_NAME).bin

# CREATE DIRS
$(shell mkdir -p $(sort $(dir $(OBJS))))

# RULES
$(OUT_PATH)/boot/%.o: $(TEL_PATH)/chip/$(TEL_CHIP)/boot/%.S
	@echo "Assembling $< -> $@"
	$(CC) $(BOOT_FLAG) -c -o"$@" "$<"

$(OUT_PATH)/common/%.o: $(TEL_PATH)/common/%.c
	@echo "Compiling $< -> $@"
	@$(CC) $(GCC_FLAGS) $(INCLUDE_PATHS) -c $< -o $@

$(OUT_PATH)/common/%.o: $(TEL_PATH)/common/%.S
	@echo "Assembling $< -> $@"
	$(CC) $(BOOT_FLAG) -c -o"$@" "$<"	

$(OUT_PATH)/drivers/%.o: $(TEL_PATH)/chip/$(TEL_CHIP)/drivers/%.c
	@echo "Compiling $< -> $@"
	@$(CC) $(GCC_FLAGS) $(INCLUDE_PATHS) -c $< -o $@

$(OUT_PATH)/vendor/%.o: $(TEL_PATH)/demo/vendor/common/$(TEL_CHIP)/%.c
	@echo "Compiling $< -> $@"
	@$(CC) $(GCC_FLAGS) $(INCLUDE_PATHS) -c $< -o $@

$(OUT_PATH)/project/%.o: $(PROJECT_PATH)/%.c
	@echo "Compiling $< -> $@"
	@$(CC) $(GCC_FLAGS) $(INCLUDE_PATHS) -c $< -o $@

# LINK RULES
$(ELF_FILE): $(OBJS)
	@echo 'Building target: $@'
	$(LD) --gc-sections -L $(TEL_PATH)/chip/$(TEL_CHIP)/drivers/lib -T $(LS_FLAGS) -o $(ELF_FILE) $(OBJS) $(USER_OBJS) $(LIBS)
	@echo 'Finished building target: $@'
	@echo ' '

$(LST_FILE): $(ELF_FILE)
	@echo 'Invoking: TC32 Create Extended Listing'
	$(OBJDUMP) -x -D -l -S  $(ELF_FILE)  > $(LST_FILE)
	@echo 'Finished building: $@'
	@echo ' '

$(BIN_FILE): $(ELF_FILE)
	@echo 'Create Flash image (binary format)'
	$(OBJCOPY) -v -O binary $(ELF_FILE)  $(BIN_FILE)
	python $(TEL_PATH)/tools/tl_firmware_tools.py add_crc $(BIN_FILE)
	@echo 'Finished building: $@'
	@echo ' '

sizedummy: $(ELF_FILE)
	@echo 'Invoking: Print Size'
	$(SIZE) -t $(ELF_FILE)
	@echo 'Finished building: $@'

clean:
	rm -rf $(OUT_PATH)

info:
	@echo "Directories:"
	@echo $(DIRS)
	@echo "Source files:"
	@echo $(SRCS)
	@echo "Object files:"
	@echo $(OBJS)

all: $(ELF_FILE) $(LST_FILE) $(BIN_FILE) sizedummy

b: bfr

# build -> flash -> reset
bfr: all
	Cmd_download_tool 1 B85 wf 0 -i $(BIN_FILE)
	Cmd_download_tool 1 B85 rst

.PHONY: all clean info