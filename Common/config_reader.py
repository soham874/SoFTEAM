import os

class ConfigReader:
    def __init__(self, filepath = None):
        self.config = {}
        self.filepath = filepath
        self.parse_config()
    
    def parse_config(self):
        if self.filepath is not None and os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                config_lines = f.readlines()
                for aline in config_lines:
                    k,v = aline.strip().split("=")
                    self.config[k] = v
    
    def get_config_from_env_or_file(self, varname_os_env, secret_path = None):
        
        if (varname_os_env in os.environ):
            return os.environ[varname_os_env]

        config = ""
        if secret_path is not None and os.path.exists(secret_path):
            with open(secret_path, "r") as f:
                config = f.read()

        if config == "":
            raise Exception(f"{varname_os_env} is not found in env, also {secret_path} does not exist")
        
        for line in config:

            # Split the line on the equals sign
            parts = line.strip().split('=')
            
            # Check if the key part matches the key
            if parts[0] == varname_os_env:
                # Return the value part
                return parts[1]

        # If the key was not found in the file, raise Exception
        raise Exception(f"{varname_os_env} does not exist in file {secret_path}")