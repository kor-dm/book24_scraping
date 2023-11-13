from src import parse_configs, parse_site

def main():
    configs = parse_configs(input("Configuration name: "))
    parse_site(configs)


if (__name__ == "__main__"):
    main()
