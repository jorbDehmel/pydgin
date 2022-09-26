# Update production EXEs
update: exes/editor.exe exes/pdg.exe
	echo Updated
	

exes/editor.exe:	source/main.py source/main.py
	pyinstaller --noconfirm --onefile --windowed --distpath "exes" -n editor.exe  "source/main.py"
	del *.spec
exes/pdg.exe:	source/terminal.py source/main.py
	pyinstaller --noconfirm --onefile --console --distpath "exes" -n pdg.exe  "source/terminal.py"
	del *.spec