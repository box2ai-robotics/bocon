# Makefile
# code by LinCC111 2025.1.13 Box2AI-Robotics copyright
RULES_DIR := /etc/udev/rules.d
UDEV_RULES := bocon/bocon-udev/99-bocon.rules
BOCON_REPO_DIR := bocon/dkms-hid-bocon
BOCOND_REPO := bocon/bocond

# DKMS INSTALL VERSION
DKMS_VERSION := 3.2

# INSTALL NINTENDO DKMS MODULES
install_nintendo:
	@echo "Install dkms libevdev-dev libudev-dev for linux..."
	@sudo apt-get install -y dkms libevdev-dev libudev-dev
	@echo "Removing any previous instances of the nintendo module..."
	@cd $(BOCON_REPO_DIR) && sudo dkms remove nintendo -v $(DKMS_VERSION) --all || true
	@echo "Checking for any existing nintendo modules..."
	@sudo dkms status | grep -i nintendo && sudo dkms remove nintendo -v $(DKMS_VERSION) --all || true
	@cd $(BOCON_REPO_DIR) && sudo dkms add .
	@cd $(BOCON_REPO_DIR) && sudo dkms build nintendo -v $(DKMS_VERSION)
	@cd $(BOCON_REPO_DIR) && sudo dkms install nintendo -v $(DKMS_VERSION)
	@echo "nintendo dkms module installed successfully."

# INSTALL JOYCOND
install_joycond:
	@cd $(BOCOND_REPO) && cmake .
	@cd $(BOCOND_REPO) && sudo make install
	@cd $(BOCOND_REPO) && sudo systemctl enable --now joycond
	@echo "joycond installed and started successfully."

# INSTALL UBUNTU SYSTEM DEPENDENCIES
install-hid-deps:
	sudo apt-get install -y \
		libhidapi-dev \
		libhidapi-hidraw0 \
		libhidapi-libusb0 \
		
# INSTALL JOYCON UDEV RULES
install-udev-rules:
	@echo "Installing udev rules..."
	@sudo cp $(UDEV_RULES) $(RULES_DIR)
	sudo udevadm control --reload-rules && sudo udevadm trigger
	@echo "Udev rules installed successfully."

# DELETE TEMPORARY FILES
clean:
	@echo "No need clean."

# INSTALL ALL TARGET
install: install_nintendo install_joycond clean install-hid-deps install-udev-rules
	@echo "All dependencies installed successfully."

