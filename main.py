from src import parse_configs, parse_site, setup_dir, write_data, log_cli


def main():
    configs = parse_configs(input("Configuration name: "))
    dir = setup_dir()
    for item in parse_site(configs, logging = log_cli):
        if (write_data(item, dir)): 
            print("[ERROR] Program cannot write data to file")


if (__name__ == "__main__"):
    main()
