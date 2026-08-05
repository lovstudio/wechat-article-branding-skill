#!/usr/bin/env python3
"""Validate a portable WeChat article branding profile."""

from __future__ import annotations

import argparse
import json
import re
import tempfile
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


HEX_COLOR = re.compile(r"^#[0-9A-Fa-f]{6}$")


def load_profile(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("profile root must be an object")
    return data


def valid_url(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(profile: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    publication = profile.get("publication")
    if not isinstance(publication, dict):
        errors.append("publication must be an object")
        publication = {}
    if not nonempty(publication.get("name")):
        errors.append("publication.name is required")
    if not nonempty(publication.get("logo")):
        errors.append("publication.logo is required")
    if publication.get("logo_policy") != "publisher_only":
        errors.append("publication.logo_policy must be publisher_only")

    brand = profile.get("brand")
    if not isinstance(brand, dict):
        errors.append("brand must be an object")
        brand = {}
    if not nonempty(brand.get("name")):
        errors.append("brand.name is required")
    if not valid_url(brand.get("site")):
        errors.append("brand.site must be an HTTP(S) URL")
    public_facts = brand.get("public_facts", [])
    if not isinstance(public_facts, list) or not all(nonempty(item) for item in public_facts):
        errors.append("brand.public_facts must be a list of non-empty strings")
    forbidden = brand.get("forbidden_context", [])
    if not isinstance(forbidden, list) or not all(nonempty(item) for item in forbidden):
        errors.append("brand.forbidden_context must be a list of non-empty strings")

    visual = profile.get("visual", {})
    if not isinstance(visual, dict):
        errors.append("visual must be an object")
        visual = {}
    color = visual.get("primary_color")
    if color is not None and (not isinstance(color, str) or not HEX_COLOR.fullmatch(color)):
        errors.append("visual.primary_color must use #RRGGBB")
    ratios = visual.get("cover_ratios", [])
    if not isinstance(ratios, list) or not all(nonempty(item) for item in ratios):
        errors.append("visual.cover_ratios must be a list of ratio strings")
    if "logo" in visual:
        errors.append("visual.logo is ambiguous; use publication.logo")

    products = profile.get("products", [])
    product_urls: set[str] = set()
    if not isinstance(products, list):
        errors.append("products must be a list")
    else:
        for index, product in enumerate(products):
            if not isinstance(product, dict):
                errors.append(f"products[{index}] must be an object")
                continue
            if not nonempty(product.get("name")):
                errors.append(f"products[{index}].name is required")
            if not nonempty(product.get("promise")):
                errors.append(f"products[{index}].promise is required")
            if not valid_url(product.get("url")):
                errors.append(f"products[{index}].url must be an HTTP(S) URL")
            else:
                product_urls.add(product["url"])

    blocks = profile.get("blocks", {})
    if not isinstance(blocks, dict):
        errors.append("blocks must be an object")
    else:
        endcap = blocks.get("endcap")
        if endcap is not None and not isinstance(endcap, (bool, dict)):
            errors.append("blocks.endcap must be a boolean or object")
        if isinstance(endcap, dict):
            enabled = endcap.get("enabled", True)
            if not isinstance(enabled, bool):
                errors.append("blocks.endcap.enabled must be a boolean")
            if endcap.get("mode", "stable") != "stable":
                errors.append("blocks.endcap.mode must be stable")
            if endcap.get("product_link_policy", "primary_only") != "primary_only":
                errors.append("blocks.endcap.product_link_policy must be primary_only")
            if enabled and not nonempty(endcap.get("title")):
                errors.append("blocks.endcap.title is required when enabled")
            paragraphs = endcap.get("paragraphs", [])
            if not isinstance(paragraphs, list) or not all(nonempty(item) for item in paragraphs):
                errors.append("blocks.endcap.paragraphs must be a list of non-empty strings")
            links = endcap.get("links", [])
            if not isinstance(links, list):
                errors.append("blocks.endcap.links must be a list")
            else:
                for index, link in enumerate(links):
                    if not isinstance(link, dict):
                        errors.append(f"blocks.endcap.links[{index}] must be an object")
                        continue
                    if not nonempty(link.get("label")):
                        errors.append(f"blocks.endcap.links[{index}].label is required")
                    if not valid_url(link.get("url")):
                        errors.append(f"blocks.endcap.links[{index}].url must be an HTTP(S) URL")
                    elif link["url"] in product_urls:
                        errors.append(
                            f"blocks.endcap.links[{index}].url duplicates a products[].url; "
                            "product links are resolved from products[].url"
                        )
    return errors


def self_test() -> int:
    profile = {
        "publication": {
            "name": "Example Publisher",
            "logo": "./assets/example-publisher-logo.svg",
            "logo_policy": "publisher_only",
        },
        "brand": {
            "name": "Example Studio",
            "site": "https://example.com",
            "public_facts": ["Builds useful software"],
            "forbidden_context": ["private note"],
        },
        "visual": {"primary_color": "#00B38A", "cover_ratios": ["2.35:1", "1:1"]},
        "products": [
            {"name": "Example Product", "promise": "A clear user result", "url": "https://example.com/product"}
        ],
        "blocks": {
            "endcap": {
                "enabled": True,
                "mode": "stable",
                "product_link_policy": "primary_only",
                "title": "Create useful things",
                "paragraphs": ["Approved reusable endcap copy"],
                "links": [{"label": "Example Studio", "url": "https://example.com"}],
            }
        },
    }
    errors = validate(profile)
    if errors:
        print("SELF-TEST FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    invalid = dict(profile)
    invalid["brand"] = {"name": "", "site": "not-a-url"}
    if not validate(invalid):
        print("SELF-TEST FAILED: invalid brand profile was accepted")
        return 1
    invalid_endcap = json.loads(json.dumps(profile))
    invalid_endcap["blocks"]["endcap"]["mode"] = "article-adaptive"
    if not validate(invalid_endcap):
        print("SELF-TEST FAILED: article-adaptive endcap was accepted")
        return 1
    missing_publication = json.loads(json.dumps(profile))
    del missing_publication["publication"]
    if not validate(missing_publication):
        print("SELF-TEST FAILED: profile without publisher identity was accepted")
        return 1
    ambiguous_logo = json.loads(json.dumps(profile))
    ambiguous_logo["visual"]["logo"] = "./assets/studio-logo.svg"
    if not validate(ambiguous_logo):
        print("SELF-TEST FAILED: ambiguous visual.logo was accepted")
        return 1
    duplicate_product_link = json.loads(json.dumps(profile))
    duplicate_product_link["blocks"]["endcap"]["links"].append(
        {"label": "Example Product", "url": "https://example.com/product"}
    )
    if not validate(duplicate_product_link):
        print("SELF-TEST FAILED: duplicated product endcap link was accepted")
        return 1
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "brand.json"
        path.write_text(json.dumps(profile, ensure_ascii=False), encoding="utf-8")
        if validate(load_profile(path)):
            print("SELF-TEST FAILED: JSON round trip")
            return 1
    print("SELF-TEST PASSED")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if args.profile is None:
        parser.error("profile JSON is required")
    try:
        errors = validate(load_profile(args.profile))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAILED: {exc}")
        return 1
    if errors:
        print(f"FAILED: {len(errors)} issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASSED: brand profile is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
