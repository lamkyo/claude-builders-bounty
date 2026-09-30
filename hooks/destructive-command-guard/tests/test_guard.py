import sys
import os
import importlib.util

# Load module from file with hyphens
module_name = "pre_tool_use"
file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "pre-tool-use")

spec = importlib.util.spec_from_file_location(module_name, file_path)
pre_tool_use = importlib.util.module_from_spec(spec)
sys.modules[module_name] = pre_tool_use
spec.loader.exec_module(pre_tool_use)

check_destructive = pre_tool_use.check_destructive

def test_guard():
    # Should block
    blocked, _ = check_destructive("rm -rf /tmp/x")
    assert blocked
    
    blocked, _ = check_destructive("bash -c 'rm -rf /tmp/x'")
    assert blocked
    
    blocked, _ = check_destructive("cmd1 && rm -rf /tmp/x")
    assert blocked

    # Should allow
    blocked, _ = check_destructive("echo 'rm -rf /tmp/x'")
    assert not blocked
    
    blocked, _ = check_destructive("printf 'DROP TABLE x'")
    assert not blocked
    
    blocked, _ = check_destructive("echo 'hello; DROP TABLE x'")
    assert not blocked
    
    blocked, _ = check_destructive("echo \"hello | DROP TABLE x\"")
    assert not blocked
    
    blocked, _ = check_destructive("echo 'a;b|c&&d'")
    assert not blocked
    
    blocked, _ = check_destructive("echo \\\"rm -rf /tmp\\\"")
    assert not blocked

    print("✅ All guard tests passed!")

if __name__ == "__main__":
    test_guard()
