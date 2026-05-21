from pathlib import Path
from sumd.validator import validate_project_architecture

proj_dir = Path("/tmp/pytest-of-tom/pytest-195/test_architectural_validation_0")
errors = validate_project_architecture(proj_dir)
print("Returned errors:", errors)
