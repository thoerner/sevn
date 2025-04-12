"""
CLI commands implementation for the environment variable manager.
"""

import os
import sys
import argparse
import signal
import tempfile
import subprocess
from typing import List, Optional
from core.profiles import ProfileManager

EXAMPLES = """
Examples:
  # Set a secret in a profile
  envault set STRIPE_KEY=sk_test_123 --profile myproject
  
  # List all profiles
  envault list
  
  # Load secrets into current shell
  eval "$(envault load myproject)"
  
  # Spawn a new shell with loaded secrets
  envault load myproject --shell
  
  # Delete a secret from a profile
  envault delete myproject --key STRIPE_KEY
  
  # Delete an entire profile
  envault delete myproject

Shell Integration:
  For easier usage, add this function to your .bashrc or .zshrc:
  
  load_env() {
      eval "$(envault load ${1:-default})"
  }
  
  Then you can simply use: load_env myproject
"""

class CommandHandler:
    def __init__(self):
        self.profile_manager = ProfileManager()

    def load(self, args: argparse.Namespace) -> int:
        """
        Load environment variables from a profile.
        
        If --shell is specified, spawns a new shell with the variables.
        Otherwise, prints the export commands to stdout.
        """
        profile_name = args.profile
        
        # Get the decrypted content
        content = self.profile_manager.load_profile(profile_name)
        if content is None:
            print(f"Error: Profile '{profile_name}' not found or cannot be decrypted",
                  file=sys.stderr)
            return 1
        
        if args.shell:
            # Create a secure temporary file for the shell
            with tempfile.NamedTemporaryFile(mode='w', prefix='env_', suffix='.sh', delete=False) as temp_file:
                temp_path = temp_file.name
                temp_file.write(content)
            
            try:
                # Secure the temporary file
                os.chmod(temp_path, 0o600)
                
                # Spawn a new shell with the profile
                shell = os.environ.get('SHELL', '/bin/bash')
                process = subprocess.Popen([
                    shell,
                    '--rcfile', temp_path
                ])
                
                # Handle Ctrl+C gracefully
                def signal_handler(sig, frame):
                    process.terminate()
                    sys.exit(0)
                    
                signal.signal(signal.SIGINT, signal_handler)
                
                # Wait for the shell to exit
                process.wait()
                return process.returncode
            finally:
                # Always clean up the temporary file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
        else:
            # Print directly to stdout for eval
            print(content.rstrip())  # Remove trailing newlines
            return 0

    def set(self, args: argparse.Namespace) -> int:
        """Set an environment variable in a profile."""
        profile_name = args.profile
        key, value = args.key_value.split('=', 1)
        
        if self.profile_manager.set_variable(profile_name, key, value):
            print(f"✔️ Key saved to profile \"{profile_name}\"")
            return 0
        else:
            print(f"Error: Failed to set variable in profile '{profile_name}'",
                  file=sys.stderr)
            return 1

    def list(self, args: argparse.Namespace) -> int:
        """List all available profiles."""
        profiles = self.profile_manager.list_profiles()
        if not profiles:
            print("No profiles found.")
            return 0
            
        print("Available profiles:")
        for profile in profiles:
            print(f"  - {profile}")
        return 0

    def delete(self, args: argparse.Namespace) -> int:
        """Delete a profile or a variable from a profile."""
        profile_name = args.profile
        
        if args.key:
            # Delete a specific variable
            if self.profile_manager.delete_variable(profile_name, args.key):
                print(f"✔️ Variable '{args.key}' deleted from profile \"{profile_name}\"")
                return 0
            else:
                print(f"Error: Failed to delete variable from profile '{profile_name}'",
                      file=sys.stderr)
                return 1
        else:
            # Delete entire profile
            if self.profile_manager.delete_profile(profile_name):
                print(f"✔️ Profile \"{profile_name}\" deleted")
                return 0
            else:
                print(f"Error: Failed to delete profile '{profile_name}'",
                      file=sys.stderr)
                return 1

def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="Secure environment variable manager",
        epilog=EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # load command
    load_parser = subparsers.add_parser('load',
        help="Load environment variables from a profile",
        description="Load environment variables from a profile. Use with eval or --shell.",
        epilog="""
Examples:
  # Load into current shell
  eval "$(envault load myproject)"
  
  # Start new shell with variables
  envault load myproject --shell""",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    load_parser.add_argument('profile', help="Profile name")
    load_parser.add_argument('--shell', action='store_true',
        help="Spawn a new shell with the profile's environment variables")
    
    # set command
    set_parser = subparsers.add_parser('set',
        help="Set an environment variable in a profile",
        description="Set an environment variable in a profile.",
        epilog="""
Example:
  envault set STRIPE_KEY=sk_test_123 --profile myproject""",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    set_parser.add_argument('key_value',
        help="Environment variable in KEY=VALUE format")
    set_parser.add_argument('--profile', '-p', required=True,
        help="Profile name")
    
    # list command
    list_parser = subparsers.add_parser('list',
        help="List all available profiles",
        description="List all available profiles.",
        epilog="""
Example:
  envault list""",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    # delete command
    delete_parser = subparsers.add_parser('delete',
        help="Delete a profile or a variable from a profile",
        description="Delete a profile or a specific variable from a profile.",
        epilog="""
Examples:
  # Delete a specific variable
  envault delete myproject --key STRIPE_KEY
  
  # Delete entire profile
  envault delete myproject""",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    delete_parser.add_argument('profile', help="Profile name")
    delete_parser.add_argument('--key', '-k',
        help="Key to delete (if not specified, deletes entire profile)")
    
    return parser 