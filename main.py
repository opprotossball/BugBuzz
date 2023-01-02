from Client import Client


if __name__ == "__main__":
    client = Client()
    client.configure("10.0.20.100", 5555)
    client.run_game()
