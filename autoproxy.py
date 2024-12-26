import os
import yaml
import subprocess

def load_config(config_path):
    """Load configuration from the YAML file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def configure_git(proxy, no_proxy, git_config_location):
    """Configure Git with the given proxy settings."""
    try:
        subprocess.run(
            ["git", "config", "--global", "http.proxy", proxy['http']],
            check=True
        )
        subprocess.run(
            ["git", "config", "--global", "https.proxy", proxy['https']],
            check=True
        )
        subprocess.run(
            ["git", "config", "--global", "http.noProxy", no_proxy],
            check=True
        )

        print(f"Git proxy settings applied successfully in {git_config_location}")
    except subprocess.CalledProcessError as e:
        print(f"Error configuring Git: {e}")

def main():
    config_path = "autoproxy.yml"

    if not os.path.exists(config_path):
        print(f"Config file {config_path} does not exist.")
        return

    config = load_config(config_path)

    proxy = config.get("proxy", {})
    no_proxy = proxy.get("no_proxy", "")

    applications = config.get("applications", {})

    git_settings = applications.get("git", {})
    if git_settings:
        git_config_location = os.path.expanduser(git_settings['config']['location'])
        configure_git(proxy, no_proxy, git_config_location)
    else:
        print("No Git configuration found in the config file.")

if __name__ == "__main__":
    main()
