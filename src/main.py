from dotenv import find_dotenv, load_dotenv


def load_environment() -> None:
    """Load environment variables, prioritizing environment-specific settings."""
    general_env_path = find_dotenv(".env")
    if general_env_path:
        load_dotenv(dotenv_path=general_env_path)
        print(f"Loaded general environment variables from: {general_env_path}")
    else:
        print(f"General .env file not found.")


def run_app() -> None:
    """Main application entry point."""
    from db.base import Base
    from db.session import engine
    from db.initialize import mesid_initialize
    from pages.ContainerScan import ContainerScan
    from components.splash import Splash

    Base.metadata.create_all(engine)
    mesid_initialize()
    root = Splash(ContainerScan)
    root.mainloop()


if __name__ == "__main__":
    load_environment()
    run_app()
