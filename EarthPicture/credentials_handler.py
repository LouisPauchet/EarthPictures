import json
import os


class CredentialsHandler:
    def __init__(self, config_file='credentials_config.json'):
        """
        Initializes the CredentialsHandler with a specified configuration file.

        If the configuration file does not exist, it will be created as an empty JSON file.

        Args:
            config_file (str): The path to the configuration file where credentials are stored. 
                               Defaults to 'credentials_config.json'.
        """
        self.config_file = config_file
        # Create the config file if it does not exist
        if not os.path.exists(self.config_file):
            with open(self.config_file, 'w') as f:
                json.dump({}, f)

    def get_credentials(self, provider):
        """
        Retrieves credentials for a specified provider from the configuration file.

        Args:
            provider (str): The name of the data provider (e.g., 'Copernicus', 'Planet').

        Returns:
            dict: A dictionary containing the credentials for the specified provider.

        Raises:
            ValueError: If credentials for the specified provider are not found in the configuration.
            FileNotFoundError: If the configuration file is missing.
            ValueError: If the configuration file is not valid JSON.
        """
        try:
            # Load current configuration
            config = self._load_config()

            # Check if provider credentials are in config
            if provider not in config:
                raise ValueError(
                    f"Credentials for '{provider}' not found. Please set them using the set_credentials method.")

            # Return the credentials for the provider
            return config[provider]

        except FileNotFoundError:
            raise FileNotFoundError(
                f"Configuration file '{self.config_file}' not found. Please ensure the file exists or create it using set_credentials.")

        except json.JSONDecodeError:
            raise ValueError(
                f"The configuration file '{self.config_file}' is not valid JSON. Please check the file format.")

    def set_credentials(self, provider, credentials):
        """
        Sets credentials for a specified provider in the configuration file.

        This method updates the credentials for the provider, or adds them if they do not exist.

        Args:
            provider (str): The name of the data provider (e.g., 'Copernicus', 'Planet').
            credentials (dict): A dictionary of credentials, e.g., {"username": "your_username", "password": "your_password"}.

        Example:
            To set credentials for a provider:

            ```
            handler = CredentialsHandler()
            handler.set_credentials("Copernicus", {"username": "my_user", "password": "my_pass"})
            ```
        """
        # Load current configuration
        config = self._load_config()

        # Update credentials for the specified provider
        config[provider] = credentials

        # Write updated configuration back to file
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)

    def _load_config(self):
        """
        Loads the configuration file as a dictionary.

        Returns:
            dict: Configuration data as a dictionary.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            json.JSONDecodeError: If the configuration file is not a valid JSON file.
        """
        with open(self.config_file, 'r') as f:
            return json.load(f)
