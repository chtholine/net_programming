import ipaddress


def largest_square_in_rectangle():
    n = int(input("Enter the length of the rectangle (n): "))
    m = int(input("Enter the width of the rectangle (m): "))

    min_side = min(n, m)
    largest_square_side = min_side // 2 * 2  # Ensure even side length
    largest_square_area = largest_square_side ** 2

    print(
        f"The largest square with even side length in the rectangle is {largest_square_side}x{largest_square_side} = {largest_square_area}.\n")


def create_city_distance_dictionary():
    city_distances = {}

    for i in range(2):
        city_name = input(f"Enter city {i + 1} name: ")
        distance = float(input("Enter distance from the city to another: "))

        if city_name not in city_distances:
            city_distances[city_name] = {}

        other_city_name = input(f"Enter the name of the other city: ")
        city_distances[city_name][other_city_name] = distance

    return city_distances


def check_ip_in_network(ip_address):
    networks = [
        ("193.10.10.1", "193.10.10.0/29"),
        ("193.10.10.9", "193.10.10.0/29"),
        ("194.20.20.5", "194.20.20.0/29"),
        ("194.20.20.5", "194.20.20.0/30")
    ]

    ip = ipaddress.IPv4Address(ip_address)

    for network_ip, network_cidr in networks:
        network = ipaddress.IPv4Network(network_cidr, strict=False)
        if ip in network:
            print(
                f"The IP address {ip} belongs to the network {network_cidr}.")
            return

    print(f"The IP address {ip} does not belong to any of the specified networks.")


def ip_in_network(ip, network_ip, network_mask):
    import ipaddress
    return ipaddress.ip_address(ip) in ipaddress.ip_network(f"{network_ip}/{network_mask}", strict=False)


def mixed_cipher(filename):
    keyword = input("Please enter a keyword for the mixed cipher: ").upper()
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    mixed_alphabet = "".join(
        sorted(set(keyword), key=keyword.index) + [char for char in alphabet if char not in keyword])

    with open(filename, 'r') as file:
        plaintext = file.read().upper()

    ciphertext = "".join([mixed_alphabet[alphabet.index(char)] if char in alphabet else char for char in plaintext])

    print("Plaintext:", alphabet)
    print("Ciphertext:", mixed_alphabet)
    print("\nEncrypted Text:")
    print(ciphertext)


if __name__ == "__main__":
    largest_square_in_rectangle()
    city_distance_data = create_city_distance_dictionary()
    print(f"City Distance Dictionary:\n{city_distance_data}\n")
    test_ip_addresses = ["193.10.10.5", "194.20.20.5", "192.168.1.1"]
    for ip_address in test_ip_addresses:
        check_ip_in_network(ip_address)
    filename = input(f"\nEnter the filename: ")  # name of the txt file in the directory
    mixed_cipher(filename)
