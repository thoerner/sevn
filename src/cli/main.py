#!/usr/bin/env python3
"""
CLI entry point for the environment variable manager.
"""

import sys
from .commands import CommandHandler, create_parser

def main() -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    handler = CommandHandler()
    
    # Dispatch to appropriate command handler
    if args.command == 'load':
        return handler.load(args)
    elif args.command == 'set':
        return handler.set(args)
    elif args.command == 'list':
        return handler.list(args)
    elif args.command == 'delete':
        return handler.delete(args)
    else:
        parser.print_help()
        return 1

if __name__ == '__main__':
    sys.exit(main()) 