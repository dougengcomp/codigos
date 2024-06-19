import netifaces

def print_interfaces():
    interfaces = netifaces.interfaces()
    if interfaces:
        print("Available interfaces:")
        for interface in interfaces:
            print(interface)
    else:
        print("No interfaces found.")

if __name__ == "__main__":
    print_interfaces()
