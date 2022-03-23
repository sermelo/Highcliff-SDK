import rpyc

connection = rpyc.connect("localhost", 18861)
print(connection.root)
print(connection.root.get_ai())
