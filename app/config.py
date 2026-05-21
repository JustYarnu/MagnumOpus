import yaml
from pathlib import Path
from dataclasses import dataclass

@dataclass
class RepoConfig:
    path: str
    branch: str

@dataclass
class FileConfig:
    input_path: str

@dataclass
class CommitConfig:
    limit: int
    push_interval: int
    delay_seconds: int

@dataclass
class AppConfig:
    repo: RepoConfig
    file: FileConfig
    commit: CommitConfig


def load_config():

    project_root = Path(__file__).resolve().parent.parent
    config_path = project_root / "config.yaml"

    with open(config_path, "r") as f:
        raw = yaml.safe_load(f)

    return AppConfig(
        repo=RepoConfig(**raw["repo"]),
        file=FileConfig(**raw["file"]),
        commit=CommitConfig(**raw["commit"])
    )