# Compatibility shim for distutils on Python 3.12+
import sys

# Try to import version handling, fallback to simple implementation
try:
    from packaging import version
    Version = version.Version
except ImportError:
    try:
        from distutils.version import StrictVersion as DistutilsStrictVersion
        class Version:
            def __init__(self, vstring):
                self._version = DistutilsStrictVersion(vstring)
            
            def __str__(self):
                return str(self._version)
            
            def __eq__(self, other):
                return self._version == DistutilsStrictVersion(str(other))
            
            def __lt__(self, other):
                return self._version < DistutilsStrictVersion(str(other))
            
            def __le__(self, other):
                return self._version <= DistutilsStrictVersion(str(other))
            
            def __gt__(self, other):
                return self._version > DistutilsStrictVersion(str(other))
            
            def __ge__(self, other):
                return self._version >= DistutilsStrictVersion(str(other))
    except ImportError:
        # Simple fallback for basic version comparison
        class Version:
            def __init__(self, vstring):
                self.vstring = str(vstring)
                self.parts = [int(x) for x in vstring.split('.') if x.isdigit()]
            
            def __str__(self):
                return self.vstring
            
            def _compare(self, other):
                other_parts = [int(x) for x in str(other).split('.') if x.isdigit()]
                for i in range(max(len(self.parts), len(other_parts))):
                    a = self.parts[i] if i < len(self.parts) else 0
                    b = other_parts[i] if i < len(other_parts) else 0
                    if a < b:
                        return -1
                    elif a > b:
                        return 1
                return 0
            
            def __eq__(self, other):
                return self._compare(other) == 0
            
            def __lt__(self, other):
                return self._compare(other) < 0
            
            def __le__(self, other):
                return self._compare(other) <= 0
            
            def __gt__(self, other):
                return self._compare(other) > 0
            
            def __ge__(self, other):
                return self._compare(other) >= 0

class StrictVersion:
    def __init__(self, vstring):
        self.version = Version(vstring)
    
    def __str__(self):
        return str(self.version)
    
    def __eq__(self, other):
        return self.version == Version(str(other))
    
    def __lt__(self, other):
        return self.version < Version(str(other))
    
    def __le__(self, other):
        return self.version <= Version(str(other))
    
    def __gt__(self, other):
        return self.version > Version(str(other))
    
    def __ge__(self, other):
        return self.version >= Version(str(other))

# Create a mock distutils module
class MockDistutils:
    class version:
        StrictVersion = StrictVersion

# Add to sys.modules before importing gradio
sys.modules['distutils'] = MockDistutils()
sys.modules['distutils.version'] = MockDistutils.version