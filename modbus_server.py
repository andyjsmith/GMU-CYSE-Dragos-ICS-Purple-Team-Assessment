from pyModbusTCP.server import ModbusServer, DataBank


server = ModbusServer(host="0.0.0.0", port=502)
DataBank.set_bits(0, [1, 1, 1, 1, 1, 1, 1, 1, 1])
DataBank.set_words(0, [2**15-1, 2**15-1, 2**15-1, 2**15-1,
                       2**15-1, 2**15-1, 2**15-1, 2**15-1, 2**15-1, 2**15-1])
print("Press Ctrl+C to safely stop server")
server.start()
