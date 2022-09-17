# Update production EXEs
update: source/main.py source/terminal.py
	pyinstaller --noconfirm --onefile --console --distpath "exes" -n pdg.exe  "source/terminal.py"
	pyinstaller --noconfirm --onefile --windowed --distpath "exes" -n editor.exe  "source/main.py"
	del *.spec