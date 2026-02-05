INSTALL_DIR=/usr/local/bin

all:
	make all -C ./textwal
	make all -C ./py

install:
	sudo cp ./lyrwal.sh $(INSTALL_DIR)/lyrwal 
	sudo chmod +x $(INSTALL_DIR)/lyrwal
	make install -C ./textwal INSTALL_DIR=$(INSTALL_DIR)
	make install -C ./py

uninstall:
	rm -rf ~/.lyrwal
	rm -rf ~/.cache/lyrwal
	rm -rf ~/Pictures/lyrwal
	sudo rm -rf /usr/local/bin/lyrwal
