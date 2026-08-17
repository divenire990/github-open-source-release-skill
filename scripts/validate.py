#!/usr/bin/env python3
"""
Structural and Security Validation Script for github-open-source-release-skill.
Validates:
1. SKILL.md YAML front matter and required sections.
2. README language switcher interlinking (README.md <-> README.en.md).
3. Relative media file existence and validity (assets/workflow-demo.gif).
4. Genuine multi-frame GIF check (> 1 frame).
5. Deep scan for sensitive credentials and developer local machine paths.
6. Core documentation presence (LICENSE, CONTRIBUTING.md, SECURITY.md, .gitignore, CI workflow).
"""

import os
import re
import sys
from pathlib import Path
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent

def check_file_exists(rel_path: str) -> Path:
    p = REPO_ROOT / rel_path
    if not p.exists():
        raise AssertionError(f"Required file missing: {rel_path}")
    return p

def validate_skill_markdown():
    print("[1/6] Validating SKILL.md front matter & sections...")
    skill_path = check_file_exists("SKILL.md")
    content = skill_path.read_text(encoding="utf-8")

    # 1. Front matter
    front_matter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not front_matter_match:
        raise AssertionError("SKILL.md must start with YAML front matter (--- ... ---)")
    
    fm_text = front_matter_match.group(1)
    if "name: github-open-source-release" not in fm_text:
        raise AssertionError("SKILL.md front matter must specify 'name: github-open-source-release'")
    if "description:" not in fm_text:
        raise AssertionError("SKILL.md front matter must specify 'description'")

    # 2. Required sections
    required_sections = [
        "## 概述",
        "## 适用场景",
        "## 核心工作流与规范",
        "### 1. 发布前只读审计与最小公开文件集",
        "### 2. 预提交门禁（Pre-Commit Gates）",
        "### 3. Git 状态、作者隐私审计与规范发布提交",
        "### 4. 许可证决策与外部依赖边界",
        "### 5. README 体验与多媒体资产规范",
        "### 6. GitHub 仓库创建、双语元数据与推送",
        "### 7. 公开 Fork 仓库的清理与私有化重建",
        "### 8. GITHUB_TOKEN 覆盖与 Keyring 权限安全处理",
        "### 9. 发布后动作约束",
        "## 分层验收清单 (Layered Verification Checklist)"
    ]

    for sec in required_sections:
        if sec not in content:
            raise AssertionError(f"SKILL.md missing required section: '{sec}'")
    print("  -> SKILL.md front matter and all 13 required sections verified.")

def validate_bilingual_readmes():
    print("[2/6] Validating bilingual READMEs and interlinking...")
    zh_path = check_file_exists("README.md")
    en_path = check_file_exists("README.en.md")

    zh_text = zh_path.read_text(encoding="utf-8")
    en_text = en_path.read_text(encoding="utf-8")

    # Check top-level link
    expected_top_link = "[English](README.en.md) | [中文](README.md)"
    if not zh_text.startswith(expected_top_link):
        raise AssertionError("README.md must start with '[English](README.en.md) | [中文](README.md)'")
    if not en_text.startswith(expected_top_link):
        raise AssertionError("README.en.md must start with '[English](README.en.md) | [中文](README.md)'")

    # Check doc-only declaration in both
    if "Documentation-Only Skill" not in zh_text or "Documentation-Only Skill" not in en_text:
        raise AssertionError("Both READMEs must explicitly declare Documentation-Only Skill nature.")
    
    print("  -> Bilingual READMEs and language interlinking verified.")

def validate_media_assets():
    print("[3/6] Validating relative media assets and GIF frames...")
    gif_path = check_file_exists("assets/workflow-demo.gif")

    with Image.open(gif_path) as img:
        frame_count = getattr(img, "n_frames", 1)
        if frame_count <= 1:
            raise AssertionError(f"assets/workflow-demo.gif must be a genuine multi-frame GIF (found {frame_count} frames)")
        width, height = img.size
        print(f"  -> Workflow demo GIF verified: {frame_count} frames, {width}x{height}px, size={gif_path.stat().st_size} bytes.")

    # Check media references in markdown files
    for md_file in [REPO_ROOT / "README.md", REPO_ROOT / "README.en.md"]:
        text = md_file.read_text(encoding="utf-8")
        media_refs = re.findall(r'!\[.*?\]\((.*?)\)', text)
        for ref in media_refs:
            if ref.startswith("http://") or ref.startswith("https://"):
                continue  # badges
            clean_ref = ref.split("?")[0].split("#")[0]
            target = (md_file.parent / clean_ref).resolve()
            if not target.exists():
                raise AssertionError(f"Broken relative media reference in {md_file.name}: {ref}")
    print("  -> All relative media references resolve to existing local assets.")

def validate_required_repo_files():
    print("[4/6] Validating core repository metadata files...")
    check_file_exists("LICENSE")
    check_file_exists(".gitignore")
    check_file_exists("CONTRIBUTING.md")
    check_file_exists("SECURITY.md")
    check_file_exists(".github/workflows/ci.yml")

    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    if "2026 divenire990" not in license_text or "MIT License" not in license_text:
        raise AssertionError("LICENSE must be MIT License for 2026 divenire990")

    print("  -> LICENSE, .gitignore, CONTRIBUTING, SECURITY, CI workflow verified.")

def scan_sensitive_patterns():
    print("[5/6] Scanning repository for sensitive credentials and private paths...")

    # Sensitive patterns to block
    token_patterns = [
        re.compile(r"ghp_[A-Za-z0-9_]{30,}"),
        re.compile(r"github_pat_[A-Za-z0-9_]{30,}"),
        re.compile(r"gho_[A-Za-z0-9_]{30,}"),
        re.compile(r"AKIA[0-9A-Z]{16}"),
        re.compile(r"Bearer\s+ey[A-Za-z0-9_-]{30,}"),
    ]

    # Specific private developer paths that should NOT be in public repository files
    private_path_patterns = [
        re.compile(r"C:[\\/]Users[\\/]Divenire", re.IGNORECASE),
        re.compile(r"E:[\\/]cloak\s*browse", re.IGNORECASE),
    ]

    violations = []
    for root, dirs, files in os.walk(REPO_ROOT):
        # Ignore .git and temp dirs
        if ".git" in dirs:
            dirs.remove(".git")
        if "__pycache__" in dirs:
            dirs.remove("__pycache__")

        for file in files:
            file_path = Path(root) / file
            rel = file_path.relative_to(REPO_ROOT)
            
            # Skip binary files from text scanning
            if file_path.suffix.lower() in [".gif", ".png", ".jpg", ".ico"]:
                continue

            try:
                text = file_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue

            for pat in token_patterns:
                if pat.search(text):
                    violations.append(f"Hardcoded credential pattern matched in {rel}")

            for pat in private_path_patterns:
                if pat.search(text):
                    violations.append(f"Private local machine path matched in {rel}")

    if violations:
        raise AssertionError("Security scan failed:\n" + "\n".join(f"  - {v}" for v in violations))
    
    print("  -> Zero sensitive credentials or private machine paths detected.")

def validate_ci_workflow():
    print("[6/6] Validating CI configuration...")
    ci_path = check_file_exists(".github/workflows/ci.yml")
    ci_text = ci_path.read_text(encoding="utf-8")
    
    if "python scripts/validate.py" not in ci_text:
        raise AssertionError("CI workflow must execute 'python scripts/validate.py'")
    if "build" in ci_text and "python -m build" in ci_text:
        raise AssertionError("CI workflow should not contain fake python -m build packaging step")
    
    print("  -> GitHub Actions CI workflow verified.")

def main():
    print("=== Starting Structural & Security Validation ===")
    try:
        validate_skill_markdown()
        validate_bilingual_readmes()
        validate_media_assets()
        validate_required_repo_files()
        scan_sensitive_patterns()
        validate_ci_workflow()
        print("=== Validation PASSED: Repository is Release-Ready ===")
        return 0
    except AssertionError as err:
        print(f"\n[VALIDATION FAILED] {err}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"\n[UNEXPECTED ERROR] {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
