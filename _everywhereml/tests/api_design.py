"""
from everywhereml.project import Project
from everywhereml.project.toolchain import ArduinoCli


project = Project(name='HelloWorld', toolchain=ArduinoCli())

project.config.set_board(query='Nano 33', opt_optimizer='o3s')
project.config.set_port('/dev/cu.usb*')

exit()
project.files.add('main', contents='void setup() {} void loop() {}')

project.toolchain.compile()
project.toolchain.upload(port='auto')

project.serial.write('AT?')
project.serial.read(2) == 'OK'
"""