from dataclasses import dataclass
from copy import deepcopy
import json
import yaml

# ========================================================================
# spaces config
# ========================================================================


def spaces_config():
    return deepcopy(
        {
            "spaces": [
                {
                    "name": "TanglerTest",
                    "directory": "./test.space.copy/",
                }
            ]
        }
    )


# ========================================================================
# ========================================================================
# ========================================================================


class FilesystemSpaceViewer:
    def __init__(self, path):
        self.path = path

    def config_file(self):
        with open(f"{self.path}/_config.yaml", "r") as f:
            return yaml.safe_load(f)


initial_fsspace = FilesystemSpaceViewer("tests/assets/test.space")
current_fsspace = FilesystemSpaceViewer("tests/assets/test.space.copy")


@dataclass
class Values:
    config_section_name: str
    type_name: str
    type_name_second: str
    field_name: str
    field_name_second: str


# NOTE:              : is moveable?
# field_name         : yes
# field_name_second  : no (it's not moveable because "title" field is special and required)
# TODO: write tests that check above

exising = Values(
    config_section_name="formatters",
    type_name="task",
    type_name_second="note",
    field_name="category",
    field_name_second="title",
)

not_exising = Values(
    config_section_name="not_existing_section_name",
    type_name="not_existing_type_name",
    type_name_second="not_existing_type_name_second",
    field_name="not_existing_field_name",
    field_name_second="not_existing_field_name_second",
)

# TODO: assert above actually exist?
# TODO: assert above actually do not exist?

# ========================================================================
# type - definitions
# ========================================================================

definition_new_type_correct = {
    "emoji": "x",
    "template": "smth",
    "fields": [
        {
            "name": "title",
            "required": True,
            "values": "text",
            "width": 150,
        }
    ],
}
definition_new_type_invalid_key = {
    **definition_new_type_correct,
    "invalid_key": ["invalid_key_value"],
}
definition_new_type_invalid_key_value = {
    **definition_new_type_correct,
    "fields": ["invalid_key_value"],
}

# ========================================================================
# type - patches
# ========================================================================

patch_type_correct = {"template": "new value"}
patch_type_invalid_key = {
    **patch_type_correct,
    "invalid_key": "invalid_key_value",
}
patch_type_invalid_key_value = {
    **patch_type_correct,
    "emoji": 10,
}

# ========================================================================
# field - definitions
# ========================================================================


definition_new_field_correct = {
    "required": False,
    "values": "text",
    "width": 200,
}
definition_new_field_invalid_key = {
    **definition_new_field_correct,
    "invalid_key": True,
}
definition_new_field_invalid_key_value = {
    **definition_new_field_correct,
    "values": False,
}

# ========================================================================
# field - patches
# ========================================================================


patch_field_correct = {"width": 400}
patch_field_invalid_key = {
    **patch_field_correct,
    "invalid_key": "invalid_key_value",
}
patch_field_invalid_key_value = {
    **patch_field_correct,
    "emoji": False,
}

# ==============================================================
# ==============================================================
# ==============================================================

# TODO: check definition missing required key
# TODO: check definition missing optional key that default value was used
# TODO: check key and value case-sensitivity

# ==============================================================
# ==============================================================
# ==============================================================


# original_types = asserted_rq.get(prod_client, "/config/types")
# existing_type_name = list(original_types.keys())[0]

# assert existing_type_name is not None and existing_type_name != ""
# assert bool(existing_type_name)
