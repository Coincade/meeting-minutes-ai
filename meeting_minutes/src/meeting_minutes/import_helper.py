"""
Import helper for robust module loading in deployment environments.
"""
import sys
import os
from pathlib import Path
import importlib.util

def import_module_from_path(module_name: str, file_path: str):
    """Import a module from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec for {module_name} from {file_path}")
    
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def setup_paths():
    """Setup Python paths for the meeting minutes package."""
    # Get the current directory (where this file is located)
    current_dir = Path(__file__).parent
    
    # Add the current directory to sys.path if not already there
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    
    return current_dir

def import_crews():
    """Import crew modules with fallback mechanisms."""
    current_dir = setup_paths()
    
    # Try standard imports first
    try:
        from crews.meeting_minutes_crew.meeting_minutes_crew import MeetingMinutesCrew
        from crews.gmailcrew.gmailcrew import GmailCrew
        return MeetingMinutesCrew, GmailCrew
    except ImportError as e:
        print(f"Standard import failed: {e}")
        
        # Try alternative import method
        try:
            # Import meeting minutes crew
            meeting_minutes_path = current_dir / "crews" / "meeting_minutes_crew" / "meeting_minutes_crew.py"
            meeting_minutes_module = import_module_from_path("meeting_minutes_crew", str(meeting_minutes_path))
            MeetingMinutesCrew = meeting_minutes_module.MeetingMinutesCrew
            
            # Import gmail crew
            gmail_path = current_dir / "crews" / "gmailcrew" / "gmailcrew.py"
            gmail_module = import_module_from_path("gmailcrew", str(gmail_path))
            GmailCrew = gmail_module.GmailCrew
            
            return MeetingMinutesCrew, GmailCrew
        except Exception as e2:
            print(f"Alternative import also failed: {e2}")
            
            # Try one more approach - import each file individually
            try:
                # Import gmail tool first
                gmail_tool_path = current_dir / "crews" / "gmailcrew" / "tools" / "gmail_tool.py"
                gmail_tool_module = import_module_from_path("gmail_tool", str(gmail_tool_path))
                
                # Import gmail utility
                gmail_utility_path = current_dir / "crews" / "gmailcrew" / "tools" / "gmail_utility.py"
                gmail_utility_module = import_module_from_path("gmail_utility", str(gmail_utility_path))
                
                # Now import the crews
                meeting_minutes_module = import_module_from_path("meeting_minutes_crew", str(meeting_minutes_path))
                gmail_module = import_module_from_path("gmailcrew", str(gmail_path))
                
                MeetingMinutesCrew = meeting_minutes_module.MeetingMinutesCrew
                GmailCrew = gmail_module.GmailCrew
                
                return MeetingMinutesCrew, GmailCrew
            except Exception as e3:
                print(f"All import methods failed: {e3}")
                raise ImportError(f"Could not import crew modules after trying all methods: {e3}") 