all:
	make all -C ./textwal
	make all -C ./py

install:
	sudo cp ./lyrwal.sh /usr/local/bin/lyrwal
	sudo chmod +x /usr/local/bin/lyrwal
	make install -C ./textwal
	make install -C ./py

uninstall:
	rm -rf ~/.lyrwal
	rm -rf ~/.cache/lyrwal
	rm -rf ~/Pictures/lyrwal
	sudo rm -rf /usr/local/bin/lyrwal
