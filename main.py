from Client import Client


if __name__ == "__main__":
    client = Client()
    client.configure("", 5555)  # put server's ip here
    client.run_game()
